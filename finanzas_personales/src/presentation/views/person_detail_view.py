"""
Vista Detallada de Persona - Interfaz de Usuario

Este panel muestra la información detallada de una persona seleccionada,
organizada en pestañas (tabs) como un navegador web o un explorador de archivos.

Pestañas:
1. General - Datos personales básicos
2. Foto - Imagen de perfil
3. Movimientos - Historial de ingresos y gastos
4. Categorías - Gestión de categorías
5. Resumen - Gráficos y estadísticas
6. Observaciones - Notas libres

Esta organización por pestañas es típica de software de escritorio
de los años 2005-2010, permitiendo mucha información organizada.
"""
import wx
import wx.lib.scrolledpanel as scrolled
import os
from pathlib import Path

from ...domain.persona import Persona
from ...application.services.persona_service import PersonaService
from ...application.services.movimiento_service import MovimientoService
from ...shared.design_tokens import COLORS, DIMENSIONS, ICONS

# Imports para gráficos
try:
    import matplotlib
    matplotlib.use('WXAgg')  # Backend para wxPython
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


PAGE_MARGIN = 14
SECTION_MARGIN = 10
FIELD_GAP = 12
BUTTON_HEIGHT = 34
SUMMARY_TEXT_HEIGHT = 96
BUTTON_MIN_WIDTH = 128


class PersonDetailView(wx.Panel):
    """
    Panel derecho que muestra los detalles de una persona.
    
    Usa un Notebook (cuaderno de pestañas) para organizar la información.
    """
    
    def __init__(self, parent, presenter, persona_service, movimiento_service, categoria_repo):
        super().__init__(parent)
        
        self.presenter = presenter
        self.persona_service = persona_service
        self.movimiento_service = movimiento_service
        self.categoria_repo = categoria_repo
        self.current_persona = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """
        Configura la interfaz con pestañas.
        
        Un Notebook es el widget típico de pestañas en wxPython.
        """
        # Sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Mensaje inicial cuando no hay persona seleccionada
        self.empty_message = wx.StaticText(
            self, 
            label="Seleccione una persona de la lista\no cree una nueva",
            style=wx.ALIGN_CENTER
        )
        font = self.empty_message.GetFont()
        font.SetPointSize(14)
        self.empty_message.SetFont(font)
        main_sizer.Add(self.empty_message, 1, wx.ALIGN_CENTER)
        
        # Notebook (pestañas) - inicialmente oculto
        self.notebook = wx.Notebook(self)
        self.notebook.Hide()
        
        # Crear pestañas
        self.tab_general = self._create_general_tab()
        self.tab_foto = self._create_foto_tab()
        self.tab_movimientos = self._create_movimientos_tab()
        self.tab_categorias = self._create_categorias_tab()
        self.tab_resumen = self._create_resumen_tab()
        self.tab_observaciones = self._create_observaciones_tab()
        
        # Agregar pestañas al notebook
        self.notebook.AddPage(self.tab_general, "General")
        self.notebook.AddPage(self.tab_foto, "Foto")
        self.notebook.AddPage(self.tab_movimientos, "Movimientos")
        self.notebook.AddPage(self.tab_categorias, "Categorías")
        self.notebook.AddPage(self.tab_resumen, "Resumen")
        self.notebook.AddPage(self.tab_observaciones, "Observaciones")
        
        main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)

    def _create_scrolled_tab(self):
        """Crea una pestaña con scroll vertical listo para contenido variable."""
        panel = scrolled.ScrolledPanel(
            self.notebook,
            style=wx.TAB_TRAVERSAL | wx.VSCROLL,
        )
        panel.SetBackgroundColour(COLORS['panel_bg'])
        panel.SetAutoLayout(True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetupScrolling(scroll_x=False, scrollToTop=False, rate_y=16)
        return panel, sizer

    def _refresh_tab_layout(self, tab) -> None:
        """Recalcula layout y rango de scroll cuando cambia el contenido."""
        tab.Layout()
        if hasattr(tab, "FitInside"):
            tab.FitInside()
        if hasattr(tab, "SetupScrolling"):
            tab.SetupScrolling(scroll_x=False, scrollToTop=False, rate_y=16)

    def _get_general_control(self, name: str):
        """Obtiene un control de la pestaña General por nombre."""
        return wx.FindWindowByName(name, self.tab_general)

    def _collect_persona_form_data(self) -> dict:
        """Lee el formulario actual y normaliza campos opcionales."""
        def cleaned(control_name: str):
            value = self._get_general_control(control_name).GetValue().strip()
            return value or None

        return {
            "nombres": self._get_general_control("txt_nombres").GetValue().strip(),
            "apellidos": self._get_general_control("txt_apellidos").GetValue().strip(),
            "identificacion": cleaned("txt_identificacion"),
            "telefono": cleaned("txt_telefono"),
            "correo": cleaned("txt_correo"),
            "observaciones": self.txt_observaciones.GetValue().strip() or None,
        }

    def _reset_resumen(self) -> None:
        """Restablece la pestaña de resumen cuando no hay persona activa."""
        self.lbl_saldo.SetLabel("$0.00")
        self.lbl_saldo.SetForegroundColour(wx.Colour(0, 100, 0))
        self.lbl_kpi_ingresos.SetLabel("$0.00")
        self.lbl_kpi_gastos.SetLabel("$0.00")
        self.lbl_kpi_ahorro.SetLabel("0.0%")
        self.lbl_kpi_ratio.SetLabel("0.00")

        self.lbl_num_trans.SetLabel("Total transacciones: 0")
        self.lbl_prom_ingreso.SetLabel("Promedio por ingreso: $0.00")
        self.lbl_prom_gasto.SetLabel("Promedio por gasto: $0.00")
        self.lbl_prom_diario.SetLabel("Promedio diario: $0.00")
        self.lbl_mejor_dia.SetLabel("Mejor dÃ­a: -")
        self.lbl_peor_dia.SetLabel("Peor dÃ­a: -")
        self.lbl_dias_neg.SetLabel("DÃ­as negativos seguidos: 0")
        self.lbl_variabilidad.SetLabel("Variabilidad: 0%")

        self.list_top_gastos.DeleteAllItems()
        self.lbl_cambio_ingresos.SetLabel("Ingresos: 0%")
        self.lbl_cambio_gastos.SetLabel("Gastos: 0%")
        self.lbl_cambio_balance.SetLabel("Balance: 0%")
        self.lbl_proy_ingresos.SetLabel("Ingresos: $0.00")
        self.lbl_proy_gastos.SetLabel("Gastos: $0.00")
        self.lbl_proy_balance.SetLabel("Balance: $0.00")
        self.txt_alertas_resumen.SetValue("Sin alertas.")
        self.txt_recomendaciones_resumen.SetValue("Sin recomendaciones.")

        if MATPLOTLIB_AVAILABLE and hasattr(self, "canvas"):
            for ax in (self.ax1, self.ax2, self.ax3, self.ax4):
                ax.clear()
                ax.text(0.5, 0.5, "Sin datos", ha="center", va="center", fontsize=9)
                ax.axis("off")
            self.canvas.draw()

        self._refresh_tab_layout(self.tab_resumen)

    def _build_readonly_text_area(self, parent, min_height: int) -> wx.TextCtrl:
        """Crea un cuadro de texto de solo lectura con scroll vertical."""
        control = wx.TextCtrl(
            parent,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP | wx.BORDER_SUNKEN | wx.VSCROLL,
        )
        control.SetMinSize((-1, min_height))
        control.SetBackgroundColour(COLORS["panel_bg"])
        return control

    def _format_multiline_content(self, items, empty_message: str) -> str:
        """Normaliza contenido multilinea para etiquetas y cuadros de texto."""
        if not items:
            return empty_message
        if isinstance(items, str):
            cleaned = items.strip()
            return cleaned or empty_message
        return "\n".join(str(item) for item in items if str(item).strip()) or empty_message

    def _update_general_context(self, movimientos_count: int = 0) -> None:
        """Actualiza el bloque informativo de la ficha general."""
        nombres = self._get_general_control("txt_nombres").GetValue().strip()
        apellidos = self._get_general_control("txt_apellidos").GetValue().strip()
        telefono = self._get_general_control("txt_telefono").GetValue().strip()
        correo = self._get_general_control("txt_correo").GetValue().strip()
        identificacion = self._get_general_control("txt_identificacion").GetValue().strip()
        observaciones = self.txt_observaciones.GetValue().strip()

        nombre_visible = " ".join(part for part in (nombres, apellidos) if part).strip() or "Sin nombre definido"
        fecha_registro = self._get_general_control("lbl_fecha_registro").GetLabel()

        if self.current_persona:
            self.lbl_general_estado.SetLabel(f"Ficha activa: {nombre_visible}")
            self.lbl_general_registro.SetLabel(f"Registro creado el {fecha_registro}")
        else:
            self.lbl_general_estado.SetLabel("Nueva persona en edición")
            self.lbl_general_registro.SetLabel("La fecha de registro se asignará al guardar")

        canales = []
        if telefono:
            canales.append("teléfono")
        if correo:
            canales.append("correo")
        if identificacion:
            canales.append("identificación")

        if canales:
            self.lbl_general_contacto.SetLabel(
                f"Canales disponibles: {len(canales)}/3 ({', '.join(canales)})"
            )
        else:
            self.lbl_general_contacto.SetLabel("Canales disponibles: 0/3. Conviene registrar al menos uno.")

        foto_estado = "con foto" if self.current_persona and self.current_persona.foto_path else "sin foto"
        observaciones_estado = "con observaciones" if observaciones else "sin observaciones"
        self.lbl_general_actividad.SetLabel(
            f"Movimientos registrados: {movimientos_count}. Perfil {foto_estado} y {observaciones_estado}."
        )

    def _update_observaciones_status(self, event=None) -> None:
        """Actualiza el estado contextual de la pestaña de observaciones."""
        contenido = self.txt_observaciones.GetValue().strip()
        caracteres = len(contenido)

        if not contenido:
            mensaje = "Sin observaciones registradas. Use este espacio para acuerdos, recordatorios y contexto."
        elif caracteres < 120:
            mensaje = f"{caracteres} caracteres. Puede ampliar contexto si necesita más trazabilidad."
        else:
            mensaje = f"{caracteres} caracteres registrados. El cuadro tiene scroll si el texto crece."

        self.lbl_obs_estado.SetLabel(mensaje)
        self._refresh_tab_layout(self.tab_observaciones)

        if event is not None:
            event.Skip()

    def show_empty_state(self) -> None:
        """Restaura el estado vacío cuando no hay persona seleccionada."""
        self.current_persona = None
        self.empty_message.Show()
        self.notebook.Hide()
        self.Layout()

    def save_current_person(self) -> bool:
        """Guarda la persona visible usando el flujo del presenter."""
        return self._save_persona()

    def _save_persona(self) -> bool:
        """Centraliza el guardado desde la pestaña general y observaciones."""
        datos = self._collect_persona_form_data()
        guardado = self.presenter.save_persona(datos)
        if guardado:
            self._update_observaciones_status()
        return guardado
    
    def _create_general_tab(self) -> wx.Panel:
        """Crea la pestaña de información general."""
        panel, root_sizer = self._create_scrolled_tab()

        intro = wx.StaticText(
            panel,
            label="Complete la ficha principal y use las pestañas siguientes para foto, movimientos y análisis.",
        )
        intro.SetForegroundColour(COLORS["text_secondary"])
        root_sizer.Add(intro, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        form_box = wx.StaticBox(panel, label="Ficha principal")
        form_sizer = wx.StaticBoxSizer(form_box, wx.VERTICAL)

        grid = wx.FlexGridSizer(6, 2, FIELD_GAP, FIELD_GAP)
        grid.AddGrowableCol(1, 1)

        fields = [
            ("Nombres:", "txt_nombres"),
            ("Apellidos:", "txt_apellidos"),
            ("Identificación:", "txt_identificacion"),
            ("Teléfono:", "txt_telefono"),
            ("Correo:", "txt_correo"),
            ("Fecha Registro:", "lbl_fecha_registro"),
        ]

        for label_text, control_name in fields:
            label = wx.StaticText(form_box, label=label_text)
            grid.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP, 2)

            if control_name.startswith("txt_"):
                control = wx.TextCtrl(form_box, name=control_name)
                control.SetMinSize((-1, DIMENSIONS["input_height"] + 6))
                if control_name in {"txt_nombres", "txt_apellidos"}:
                    control.SetToolTip("Campo obligatorio")
            else:
                control = wx.StaticText(form_box, label="-", name=control_name)

            grid.Add(control, 1, wx.EXPAND)

        form_sizer.Add(grid, 0, wx.EXPAND | wx.ALL, PAGE_MARGIN)
        root_sizer.Add(form_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        context_box = wx.StaticBox(panel, label="Contexto del registro")
        context_sizer = wx.StaticBoxSizer(context_box, wx.VERTICAL)

        self.lbl_general_estado = wx.StaticText(context_box, label="Nueva persona en edición")
        self.lbl_general_registro = wx.StaticText(
            context_box,
            label="La fecha de registro se asignará al guardar",
        )
        self.lbl_general_contacto = wx.StaticText(
            context_box,
            label="Canales disponibles: 0/3. Conviene registrar al menos uno.",
        )
        self.lbl_general_actividad = wx.StaticText(
            context_box,
            label="Movimientos registrados: 0. Perfil sin foto y sin observaciones.",
        )

        for label in (
            self.lbl_general_estado,
            self.lbl_general_registro,
            self.lbl_general_contacto,
            self.lbl_general_actividad,
        ):
            context_sizer.Add(label, 0, wx.EXPAND | wx.BOTTOM, 6)

        root_sizer.Add(context_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_guardar = wx.Button(panel, label="Guardar ficha", size=(BUTTON_MIN_WIDTH + 26, BUTTON_HEIGHT))
        self.btn_cancelar = wx.Button(panel, label="Cancelar cambios", size=(BUTTON_MIN_WIDTH + 34, BUTTON_HEIGHT))
        self.btn_guardar.SetBackgroundColour(COLORS["primary"])
        self.btn_guardar.SetForegroundColour(COLORS["text_inverse"])
        self.btn_cancelar.SetToolTip("Restaurar los datos visibles en pantalla")
        self.btn_guardar.Bind(wx.EVT_BUTTON, self._on_guardar_persona)
        self.btn_cancelar.Bind(wx.EVT_BUTTON, self._on_cancelar_persona)
        btn_sizer.Add(self.btn_guardar, 0, wx.RIGHT, SECTION_MARGIN)
        btn_sizer.Add(self.btn_cancelar, 0)

        root_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, PAGE_MARGIN)

        return panel
    
    def _create_foto_tab(self) -> wx.Panel:
        """Crea la pestaña de foto de perfil con funcionalidad de cámara."""
        panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Área de visualización de foto con borde
        foto_container = wx.Panel(panel, size=(220, 220))
        foto_container.SetBackgroundColour(COLORS['panel_bg'])
        
        # Área para mostrar la foto
        self.foto_bitmap = wx.StaticBitmap(
            foto_container, 
            bitmap=wx.Bitmap(200, 200)
        )
        self.foto_bitmap.SetBackgroundColour(COLORS['input_bg'])
        self.foto_bitmap.Center()
        
        sizer.Add(foto_container, 1, wx.ALIGN_CENTER | wx.ALL, 20)
        
        # Información de la foto
        self.lbl_foto_info = wx.StaticText(
            panel, 
            label="Sin foto de perfil",
            style=wx.ALIGN_CENTER
        )
        self.lbl_foto_info.SetForegroundColour(COLORS['text_muted'])
        sizer.Add(self.lbl_foto_info, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_cargar_foto = wx.Button(
            panel, 
            label=f"{ICONS['photo']} Cargar Foto",
            size=(BUTTON_MIN_WIDTH + 18, BUTTON_HEIGHT)
        )
        self.btn_cargar_foto.SetToolTip("Seleccionar foto desde archivo")
        self.btn_cargar_foto.Bind(wx.EVT_BUTTON, self._on_cargar_foto)
        
        self.btn_capturar = wx.Button(
            panel, 
            label=f"{ICONS['camera']} Usar Webcam",
            size=(BUTTON_MIN_WIDTH + 26, BUTTON_HEIGHT)
        )
        self.btn_capturar.SetBackgroundColour(COLORS['primary'])
        self.btn_capturar.SetForegroundColour(COLORS['text_inverse'])
        self.btn_capturar.SetToolTip("Capturar foto con la cámara web")
        self.btn_capturar.Bind(wx.EVT_BUTTON, self._on_capturar_foto)
        
        self.btn_eliminar_foto = wx.Button(
            panel, 
            label=f"{ICONS['delete']} Eliminar",
            size=(BUTTON_MIN_WIDTH, BUTTON_HEIGHT)
        )
        self.btn_eliminar_foto.SetBackgroundColour(COLORS['error'])
        self.btn_eliminar_foto.SetForegroundColour(COLORS['text_inverse'])
        self.btn_eliminar_foto.SetToolTip("Eliminar foto actual")
        self.btn_eliminar_foto.Bind(wx.EVT_BUTTON, self._on_eliminar_foto)
        
        btn_sizer.Add(self.btn_cargar_foto, 0, wx.RIGHT, 8)
        btn_sizer.Add(self.btn_capturar, 0, wx.RIGHT, 8)
        btn_sizer.Add(self.btn_eliminar_foto, 0)
        
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        # Instrucciones
        instrucciones = wx.StaticText(
            panel,
            label="Tamaño recomendado: 400x400px\n"
                  "Formatos: JPG, PNG",
            style=wx.ALIGN_CENTER
        )
        instrucciones.SetForegroundColour(COLORS['text_muted'])
        instrucciones.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer.Add(instrucciones, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        
        panel.SetSizer(sizer)
        return panel
    
    def _create_movimientos_tab(self) -> wx.Panel:
        """Crea la pestaña de movimientos financieros."""
        panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)

        info = wx.StaticText(
            panel,
            label="El historial usa scroll propio y cualquier cambio aquí actualiza el resumen financiero.",
        )
        info.SetForegroundColour(COLORS["text_secondary"])
        sizer.Add(info, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)
        
        # Toolbar de movimientos
        toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_nuevo_mov = wx.Button(panel, label="+ Nuevo", size=(BUTTON_MIN_WIDTH, BUTTON_HEIGHT))
        self.btn_nuevo_mov.SetToolTip("Ctrl+M - Nuevo movimiento")
        toolbar_sizer.Add(self.btn_nuevo_mov, 0, wx.RIGHT, SECTION_MARGIN)
        
        self.btn_editar_mov = wx.Button(panel, label="✏️ Editar", size=(BUTTON_MIN_WIDTH, BUTTON_HEIGHT))
        self.btn_editar_mov.Enable(False)
        toolbar_sizer.Add(self.btn_editar_mov, 0, wx.RIGHT, SECTION_MARGIN)
        
        self.btn_eliminar_mov = wx.Button(panel, label="🗑️ Eliminar", size=(BUTTON_MIN_WIDTH, BUTTON_HEIGHT))
        self.btn_eliminar_mov.Enable(False)
        toolbar_sizer.Add(self.btn_eliminar_mov, 0, wx.RIGHT, SECTION_MARGIN + 4)
        
        toolbar_sizer.AddStretchSpacer()
        
        # Filtros
        toolbar_sizer.Add(wx.StaticText(panel, label="Filtros:"), 0, wx.CENTER | wx.RIGHT, 6)
        
        self.choice_tipo = wx.Choice(panel, choices=["Todos", "Ingresos", "Gastos"])
        self.choice_tipo.SetSelection(0)
        self.choice_tipo.Bind(wx.EVT_CHOICE, self._on_filtro_change)
        self.choice_tipo.SetMinSize((136, BUTTON_HEIGHT))
        toolbar_sizer.Add(self.choice_tipo, 0, wx.RIGHT, SECTION_MARGIN)
        
        self.btn_filtros_avanzados = wx.Button(
            panel,
            label="🔍 Avanzados...",
            size=(BUTTON_MIN_WIDTH + 18, BUTTON_HEIGHT),
        )
        toolbar_sizer.Add(self.btn_filtros_avanzados, 0, wx.RIGHT, SECTION_MARGIN)
        
        self.btn_limpiar_filtros = wx.Button(panel, label="Limpiar", size=(BUTTON_MIN_WIDTH - 16, BUTTON_HEIGHT))
        toolbar_sizer.Add(self.btn_limpiar_filtros, 0)
        
        sizer.Add(toolbar_sizer, 0, wx.EXPAND | wx.ALL, PAGE_MARGIN)
        
        # Tabla de movimientos (usamos ListCtrl para estilo clásico)
        self.list_movimientos = wx.ListCtrl(
            panel, 
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN
        )
        
        # Configurar columnas
        self.list_movimientos.InsertColumn(0, "Fecha", width=100)
        self.list_movimientos.InsertColumn(1, "Tipo", width=80)
        self.list_movimientos.InsertColumn(2, "Categoría", width=120)
        self.list_movimientos.InsertColumn(3, "Descripción", width=200)
        self.list_movimientos.InsertColumn(4, "Monto", width=100, format=wx.LIST_FORMAT_RIGHT)
        
        # Estilo clásico de tabla
        self.list_movimientos.SetBackgroundColour(wx.WHITE)
        
        # Bind para selección
        self.list_movimientos.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_movimiento_selected)
        self.list_movimientos.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_movimiento_deselected)
        self.list_movimientos.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_movimiento_doble_click)
        
        sizer.Add(self.list_movimientos, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, PAGE_MARGIN)
        
        # Total
        self.lbl_total_movimientos = wx.StaticText(
            panel, 
            label="Total: 0 movimientos"
        )
        font = self.lbl_total_movimientos.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.lbl_total_movimientos.SetFont(font)
        sizer.Add(self.lbl_total_movimientos, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, PAGE_MARGIN)
        
        # Bindings de botones
        self.btn_nuevo_mov.Bind(wx.EVT_BUTTON, self._on_nuevo_movimiento)
        self.btn_editar_mov.Bind(wx.EVT_BUTTON, self._on_editar_movimiento)
        self.btn_eliminar_mov.Bind(wx.EVT_BUTTON, self._on_eliminar_movimiento)
        self.btn_filtros_avanzados.Bind(wx.EVT_BUTTON, self._on_filtros_avanzados)
        self.btn_limpiar_filtros.Bind(wx.EVT_BUTTON, self._on_limpiar_filtros)
        
        panel.SetSizer(sizer)
        return panel
    
    def _create_categorias_tab(self) -> wx.Panel:
        """Crea la pestaña de gestión de categorías."""
        panel = wx.Panel(self.notebook)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Explicación
        lbl_info = wx.StaticText(
            panel, 
            label="Las categorías se comparten entre todas las personas.\n"
                  "Puedes activar/desactivar categorías según tus necesidades."
        )
        sizer.Add(lbl_info, 0, wx.ALL, 10)
        
        # Lista de categorías
        self.list_categorias = wx.ListCtrl(
            panel,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN
        )
        self.list_categorias.InsertColumn(0, "Nombre", width=150)
        self.list_categorias.InsertColumn(1, "Tipo", width=100)
        self.list_categorias.InsertColumn(2, "Descripción", width=250)
        self.list_categorias.InsertColumn(3, "Estado", width=80)
        
        sizer.Add(self.list_categorias, 1, wx.EXPAND | wx.ALL, 10)
        
        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_nueva_cat = wx.Button(panel, label="Nueva Categoría", size=(BUTTON_MIN_WIDTH + 28, BUTTON_HEIGHT))
        self.btn_editar_cat = wx.Button(panel, label="Editar", size=(BUTTON_MIN_WIDTH - 8, BUTTON_HEIGHT))
        self.btn_activar_cat = wx.Button(panel, label="Activar/Desactivar", size=(BUTTON_MIN_WIDTH + 48, BUTTON_HEIGHT))
        
        btn_sizer.Add(self.btn_nueva_cat, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_editar_cat, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_activar_cat, 0)
        
        sizer.Add(btn_sizer, 0, wx.ALL, 10)
        
        panel.SetSizer(sizer)
        return panel
    
    def _create_resumen_tab(self) -> wx.Panel:
        """Crea la pestaña de resumen y gráficos avanzados."""
        panel, sizer = self._create_scrolled_tab()

        intro = wx.StaticText(
            panel,
            label="Esta vista concentra indicadores, gráficos y recomendaciones. Si el contenido crece, la pestaña completa y los cuadros inferiores tienen scroll.",
        )
        intro.SetForegroundColour(COLORS["text_secondary"])
        sizer.Add(intro, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        kpi_box = wx.StaticBox(panel, label="Indicadores Principales")
        kpi_sizer = wx.StaticBoxSizer(kpi_box, wx.VERTICAL)

        self.lbl_saldo = wx.StaticText(kpi_box, label="$0.00")
        font = self.lbl_saldo.GetFont()
        font.SetPointSize(24)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.lbl_saldo.SetFont(font)
        self.lbl_saldo.SetForegroundColour(wx.Colour(0, 100, 0))
        kpi_sizer.Add(self.lbl_saldo, 0, wx.ALIGN_CENTER | wx.TOP, PAGE_MARGIN)
        kpi_sizer.Add(
            wx.StaticText(kpi_box, label="Saldo total disponible", style=wx.ALIGN_CENTER),
            0,
            wx.ALIGN_CENTER | wx.BOTTOM,
            FIELD_GAP,
        )

        kpi_grid = wx.FlexGridSizer(2, 4, FIELD_GAP, 20)
        for column in range(4):
            kpi_grid.AddGrowableCol(column, 1)

        kpi_grid.Add(wx.StaticText(kpi_box, label="💰 INGRESOS"), 0, wx.ALIGN_CENTER)
        self.lbl_kpi_ingresos = wx.StaticText(kpi_box, label="$0.00")
        self.lbl_kpi_ingresos.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.lbl_kpi_ingresos.SetForegroundColour(wx.Colour(0, 128, 0))
        kpi_grid.Add(self.lbl_kpi_ingresos, 0, wx.ALIGN_CENTER)

        kpi_grid.Add(wx.StaticText(kpi_box, label="💸 GASTOS"), 0, wx.ALIGN_CENTER)
        self.lbl_kpi_gastos = wx.StaticText(kpi_box, label="$0.00")
        self.lbl_kpi_gastos.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.lbl_kpi_gastos.SetForegroundColour(wx.Colour(200, 0, 0))
        kpi_grid.Add(self.lbl_kpi_gastos, 0, wx.ALIGN_CENTER)

        kpi_grid.Add(wx.StaticText(kpi_box, label="📊 TASA AHORRO"), 0, wx.ALIGN_CENTER)
        self.lbl_kpi_ahorro = wx.StaticText(kpi_box, label="0%")
        self.lbl_kpi_ahorro.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        kpi_grid.Add(self.lbl_kpi_ahorro, 0, wx.ALIGN_CENTER)

        kpi_grid.Add(wx.StaticText(kpi_box, label="⚖️ RATIO G/I"), 0, wx.ALIGN_CENTER)
        self.lbl_kpi_ratio = wx.StaticText(kpi_box, label="0.00")
        self.lbl_kpi_ratio.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        kpi_grid.Add(self.lbl_kpi_ratio, 0, wx.ALIGN_CENTER)

        kpi_sizer.Add(kpi_grid, 0, wx.EXPAND | wx.ALL, PAGE_MARGIN)
        sizer.Add(kpi_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        if MATPLOTLIB_AVAILABLE:
            graphs_box = wx.StaticBox(panel, label="Análisis Visual")
            graphs_sizer = wx.StaticBoxSizer(graphs_box, wx.VERTICAL)
            self.figure = Figure(figsize=(9.5, 7.5), dpi=80)
            self.ax1 = self.figure.add_subplot(221)
            self.ax2 = self.figure.add_subplot(222)
            self.ax3 = self.figure.add_subplot(223)
            self.ax4 = self.figure.add_subplot(224)
            self.figure.subplots_adjust(left=0.08, right=0.97, top=0.92, bottom=0.09, wspace=0.28, hspace=0.42)
            self.canvas = FigureCanvas(graphs_box, -1, self.figure)
            self.canvas.SetMinSize((-1, 520))
            graphs_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, SECTION_MARGIN)
            sizer.Add(graphs_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        metrics_box = wx.StaticBox(panel, label="Métricas Detalladas")
        metrics_sizer = wx.StaticBoxSizer(metrics_box, wx.VERTICAL)
        metrics_grid = wx.FlexGridSizer(4, 2, 8, 30)
        metrics_grid.AddGrowableCol(0, 1)
        metrics_grid.AddGrowableCol(1, 1)

        self.lbl_num_trans = wx.StaticText(metrics_box, label="Total transacciones: 0")
        self.lbl_prom_ingreso = wx.StaticText(metrics_box, label="Promedio por ingreso: $0.00")
        self.lbl_prom_gasto = wx.StaticText(metrics_box, label="Promedio por gasto: $0.00")
        self.lbl_prom_diario = wx.StaticText(metrics_box, label="Promedio diario: $0.00")
        self.lbl_mejor_dia = wx.StaticText(metrics_box, label="Mejor día: -")
        self.lbl_peor_dia = wx.StaticText(metrics_box, label="Peor día: -")
        self.lbl_dias_neg = wx.StaticText(metrics_box, label="Días negativos seguidos: 0")
        self.lbl_variabilidad = wx.StaticText(metrics_box, label="Variabilidad: 0%")

        for label in (
            self.lbl_num_trans,
            self.lbl_prom_ingreso,
            self.lbl_prom_gasto,
            self.lbl_prom_diario,
            self.lbl_mejor_dia,
            self.lbl_peor_dia,
            self.lbl_dias_neg,
            self.lbl_variabilidad,
        ):
            metrics_grid.Add(label, 0, wx.EXPAND)

        metrics_sizer.Add(metrics_grid, 0, wx.EXPAND | wx.ALL, PAGE_MARGIN)
        sizer.Add(metrics_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        tops_box = wx.StaticBox(panel, label="Tops y Comparativas")
        tops_sizer = wx.StaticBoxSizer(tops_box, wx.HORIZONTAL)

        top_gastos_sizer = wx.BoxSizer(wx.VERTICAL)
        top_gastos_sizer.Add(wx.StaticText(tops_box, label="🔴 TOP 5 GASTOS"), 0, wx.BOTTOM, 6)
        self.list_top_gastos = wx.ListCtrl(tops_box, style=wx.LC_REPORT | wx.LC_NO_HEADER, size=(300, 140))
        self.list_top_gastos.InsertColumn(0, "Categoría", width=180)
        self.list_top_gastos.InsertColumn(1, "Monto", width=110)
        top_gastos_sizer.Add(self.list_top_gastos, 0, wx.EXPAND)
        tops_sizer.Add(top_gastos_sizer, 0, wx.ALL, SECTION_MARGIN)

        cambio_sizer = wx.BoxSizer(wx.VERTICAL)
        cambio_sizer.Add(wx.StaticText(tops_box, label="📈 VS MES ANTERIOR"), 0, wx.BOTTOM, 6)
        self.lbl_cambio_ingresos = wx.StaticText(tops_box, label="Ingresos: 0%")
        self.lbl_cambio_gastos = wx.StaticText(tops_box, label="Gastos: 0%")
        self.lbl_cambio_balance = wx.StaticText(tops_box, label="Balance: 0%")
        cambio_sizer.Add(self.lbl_cambio_ingresos, 0, wx.BOTTOM, 4)
        cambio_sizer.Add(self.lbl_cambio_gastos, 0, wx.BOTTOM, 4)
        cambio_sizer.Add(self.lbl_cambio_balance, 0, wx.BOTTOM, FIELD_GAP)
        cambio_sizer.Add(wx.StaticText(tops_box, label="🔮 PROYECCIÓN MES"), 0, wx.BOTTOM, 6)
        self.lbl_proy_ingresos = wx.StaticText(tops_box, label="Ingresos: $0.00")
        self.lbl_proy_gastos = wx.StaticText(tops_box, label="Gastos: $0.00")
        self.lbl_proy_balance = wx.StaticText(tops_box, label="Balance: $0.00")
        cambio_sizer.Add(self.lbl_proy_ingresos, 0, wx.BOTTOM, 4)
        cambio_sizer.Add(self.lbl_proy_gastos, 0, wx.BOTTOM, 4)
        cambio_sizer.Add(self.lbl_proy_balance, 0)
        tops_sizer.Add(cambio_sizer, 0, wx.ALL, SECTION_MARGIN)

        sizer.Add(tops_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        alerts_box = wx.StaticBox(panel, label="Alertas y Recomendaciones")
        alerts_sizer = wx.StaticBoxSizer(alerts_box, wx.VERTICAL)
        alerts_sizer.Add(
            wx.StaticText(
                alerts_box,
                label="Los cuadros inferiores tienen scroll independiente para evitar que el contenido se recorte.",
            ),
            0,
            wx.EXPAND | wx.BOTTOM,
            8,
        )
        alerts_sizer.Add(wx.StaticText(alerts_box, label="⚠️ ALERTAS"), 0, wx.BOTTOM, 4)
        self.txt_alertas_resumen = self._build_readonly_text_area(alerts_box, SUMMARY_TEXT_HEIGHT)
        alerts_sizer.Add(self.txt_alertas_resumen, 1, wx.EXPAND | wx.BOTTOM, FIELD_GAP)
        alerts_sizer.Add(wx.StaticText(alerts_box, label="💡 RECOMENDACIONES"), 0, wx.BOTTOM, 4)
        self.txt_recomendaciones_resumen = self._build_readonly_text_area(alerts_box, SUMMARY_TEXT_HEIGHT)
        alerts_sizer.Add(self.txt_recomendaciones_resumen, 1, wx.EXPAND)
        sizer.Add(alerts_sizer, 0, wx.EXPAND | wx.ALL, PAGE_MARGIN)

        return panel
    
    def _create_observaciones_tab(self) -> wx.Panel:
        """Crea la pestaña de observaciones/notas."""
        panel, sizer = self._create_scrolled_tab()

        lbl_info = wx.StaticText(
            panel,
            label="Use este espacio para acuerdos, contexto personal, recordatorios y observaciones de seguimiento.",
        )
        lbl_info.SetForegroundColour(COLORS["text_secondary"])
        sizer.Add(lbl_info, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        self.lbl_obs_estado = wx.StaticText(
            panel,
            label="Sin observaciones registradas. Use este espacio para acuerdos, recordatorios y contexto.",
        )
        self.lbl_obs_estado.SetForegroundColour(COLORS["text_muted"])
        sizer.Add(self.lbl_obs_estado, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, PAGE_MARGIN)

        self.txt_observaciones = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE | wx.TE_WORDWRAP | wx.BORDER_SUNKEN | wx.VSCROLL,
        )
        self.txt_observaciones.SetMinSize((-1, 240))
        self.txt_observaciones.Bind(wx.EVT_TEXT, self._update_observaciones_status)
        sizer.Add(self.txt_observaciones, 1, wx.EXPAND | wx.ALL, PAGE_MARGIN)

        self.btn_guardar_obs = wx.Button(
            panel,
            label="Guardar observaciones",
            size=(BUTTON_MIN_WIDTH + 46, BUTTON_HEIGHT),
        )
        self.btn_guardar_obs.Bind(wx.EVT_BUTTON, self._on_guardar_observaciones)
        sizer.Add(self.btn_guardar_obs, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM, PAGE_MARGIN)

        return panel
    
    def load_person(self, persona: Persona):
        """
        Carga los datos de una persona en la vista.
        
        Args:
            persona: Objeto Persona a mostrar
        """
        self.current_persona = persona
        
        # Ocultar mensaje vacío y mostrar notebook
        self.empty_message.Hide()
        self.notebook.Show()
        
        # Cargar datos en pestaña General
        self._load_general_tab(persona)
        
        # Cargar observaciones
        self.txt_observaciones.SetValue(persona.observaciones or "")
        self._update_observaciones_status()
        
        # Cargar foto
        self._actualizar_vista_foto()

        # Cargar datos de otras pestañas
        self._load_movimientos(persona.id)
        self._load_resumen(persona.id)
        self._load_categorias()
        self._update_general_context(self.list_movimientos.GetItemCount())

        # Actualizar layout
        self.Layout()
    
    def _load_general_tab(self, persona: Persona):
        """Carga los datos en la pestaña General."""
        self._get_general_control("txt_nombres").SetValue(persona.nombres)
        self._get_general_control("txt_apellidos").SetValue(persona.apellidos)
        self._get_general_control("txt_identificacion").SetValue(persona.identificacion or "")
        self._get_general_control("txt_telefono").SetValue(persona.telefono or "")
        self._get_general_control("txt_correo").SetValue(persona.correo or "")
        self._get_general_control("lbl_fecha_registro").SetLabel(
            persona.fecha_registro.strftime("%d/%m/%Y")
        )
        self._refresh_tab_layout(self.tab_general)
    
    def _load_movimientos(self, persona_id: int):
        """Carga los movimientos en la tabla."""
        movimientos = self.movimiento_service.listar_movimientos(persona_id)

        filtro_basico = self.choice_tipo.GetStringSelection()
        if filtro_basico == "Ingresos":
            movimientos = [mov for mov in movimientos if mov.es_ingreso]
        elif filtro_basico == "Gastos":
            movimientos = [mov for mov in movimientos if mov.es_gasto]

        self._actualizar_lista_movimientos(movimientos)
    
    def _load_resumen(self, persona_id: int):
        """Carga el resumen financiero completo con análisis avanzado."""
        # Obtener análisis completo
        from ...application.services.analisis_service import AnalisisFinancieroService
        
        analisis_service = AnalisisFinancieroService(self.movimiento_service, self.categoria_repo)
        analisis = analisis_service.analizar(persona_id)
        
        # ===== KPIs PRINCIPALES =====
        self.lbl_saldo.SetLabel(f"${analisis.saldo_total:,.2f}")
        color_saldo = wx.Colour(0, 128, 0) if analisis.saldo_total >= 0 else wx.Colour(200, 0, 0)
        self.lbl_saldo.SetForegroundColour(color_saldo)
        
        self.lbl_kpi_ingresos.SetLabel(f"${analisis.total_ingresos:,.2f}")
        self.lbl_kpi_gastos.SetLabel(f"${analisis.total_gastos:,.2f}")
        
        self.lbl_kpi_ahorro.SetLabel(f"{analisis.tasa_ahorro:.1f}%")
        color_ahorro = wx.Colour(0, 128, 0) if analisis.tasa_ahorro >= 20 else wx.Colour(200, 150, 0)
        self.lbl_kpi_ahorro.SetForegroundColour(color_ahorro)
        
        self.lbl_kpi_ratio.SetLabel(f"{analisis.ratio_gasto_ingreso:.2f}")
        
        # ===== MÉTRICAS DETALLADAS =====
        self.lbl_num_trans.SetLabel(f"Total transacciones: {analisis.num_transacciones} "
                                   f"({analisis.num_ingresos} ingresos, {analisis.num_gastos} gastos)")
        self.lbl_prom_ingreso.SetLabel(f"Promedio por ingreso: ${analisis.promedio_ingreso:,.2f}")
        self.lbl_prom_gasto.SetLabel(f"Promedio por gasto: ${analisis.promedio_gasto:,.2f}")
        self.lbl_prom_diario.SetLabel(f"Promedio diario: ${analisis.promedio_diario_gasto:,.2f}")
        self.lbl_mejor_dia.SetLabel(f"Mejor día: {analisis.mejor_dia_semana}")
        self.lbl_peor_dia.SetLabel(f"Peor día: {analisis.peor_dia_semana}")
        self.lbl_dias_neg.SetLabel(f"Días negativos seguidos: {analisis.dias_consecutivos_negativos}")
        self.lbl_variabilidad.SetLabel(f"Variabilidad: {analisis.variabilidad_ingresos:.1f}%")
        
        # ===== TOPS =====
        self.list_top_gastos.DeleteAllItems()
        for i, (cat, monto) in enumerate(analisis.top_5_gastos):
            idx = self.list_top_gastos.InsertItem(i, cat)
            self.list_top_gastos.SetItem(idx, 1, f"${monto:,.2f}")
        
        # ===== COMPARATIVA MES ANTERIOR =====
        def format_cambio(valor):
            color = "🟢" if valor > 0 else "🔴" if valor < 0 else "⚪"
            return f"{color} {valor:+.1f}%"
        
        self.lbl_cambio_ingresos.SetLabel(f"Ingresos: {format_cambio(analisis.cambio_mes_anterior.get('ingresos', 0))}")
        self.lbl_cambio_gastos.SetLabel(f"Gastos: {format_cambio(analisis.cambio_mes_anterior.get('gastos', 0))}")
        self.lbl_cambio_balance.SetLabel(f"Balance: {format_cambio(analisis.cambio_mes_anterior.get('balance', 0))}")
        
        # ===== PROYECCIONES =====
        proy = analisis.proyeccion_mes_siguiente
        self.lbl_proy_ingresos.SetLabel(f"Ingresos: ${proy.get('ingresos', 0):,.2f}")
        self.lbl_proy_gastos.SetLabel(f"Gastos: ${proy.get('gastos', 0):,.2f}")
        self.lbl_proy_balance.SetLabel(f"Balance: ${proy.get('balance', 0):,.2f}")
        
        # ===== ALERTAS Y RECOMENDACIONES =====
        self.txt_alertas_resumen.SetValue(
            self._format_multiline_content(analisis.alertas, "Sin alertas.")
        )
        self.txt_recomendaciones_resumen.SetValue(
            self._format_multiline_content(analisis.recomendaciones, "Sin recomendaciones.")
        )
        
        # ===== GRÁFICOS =====
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'canvas'):
            self._update_graficos_avanzados(analisis)

        self._refresh_tab_layout(self.tab_resumen)
    
    def _update_graficos(self, ingresos: float, gastos: float, movimientos: list):
        """Actualiza los gráficos de matplotlib."""
        # Limpiar ejes
        self.ax1.clear()
        self.ax2.clear()
        
        # Gráfico 1: Barras - Ingresos vs Gastos
        categorias = ['Ingresos', 'Gastos']
        valores = [ingresos, gastos]
        colores = ['#4CAF50', '#F44336']  # Verde y Rojo
        
        bars = self.ax1.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5)
        self.ax1.set_title('Ingresos vs Gastos', fontweight='bold', fontsize=9)
        self.ax1.set_ylabel('Monto ($)', fontweight='bold', fontsize=8)
        self.ax1.tick_params(axis='both', labelsize=8)
        self.ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Agregar valores sobre las barras
        for bar in bars:
            height = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2., height,
                         f'${height:,.0f}',
                         ha='center', va='bottom', fontsize=7)
        
        # Gráfico 2: Torta - Gastos por Categoría
        # Calcular gastos por categoría
        gastos_por_categoria = {}
        for mov in movimientos:
            if mov.tipo.value == 'Gasto':
                # Obtener nombre de categoría
                categoria = self.categoria_repo.find_by_id(mov.categoria_id)
                nombre_cat = categoria.nombre if categoria else f"Cat {mov.categoria_id}"
                
                if nombre_cat in gastos_por_categoria:
                    gastos_por_categoria[nombre_cat] += mov.monto
                else:
                    gastos_por_categoria[nombre_cat] = mov.monto
        
        if gastos_por_categoria:
            nombres = list(gastos_por_categoria.keys())
            montos = list(gastos_por_categoria.values())
            
            # Colores pastel
            colores_pastel = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', 
                              '#99CCFF', '#FFB366', '#B3FF66', '#66FFB3', '#B366FF']
            
            # Crear gráfico de torta - fuentes pequeñas para ajustarse al espacio
            wedges, texts, autotexts = self.ax2.pie(
                montos, 
                labels=nombres, 
                autopct='%1.1f%%',
                colors=colores_pastel[:len(nombres)],
                startangle=90,
                textprops={'fontsize': 7}
            )
            
            self.ax2.set_title('Gastos por Categoría', fontweight='bold', fontsize=9)
        else:
            self.ax2.text(0.5, 0.5, 'Sin datos de gastos',
                         ha='center', va='center', fontsize=12)
            self.ax2.set_xlim(0, 1)
            self.ax2.set_ylim(0, 1)
            self.ax2.axis('off')
        
        # Ajustar layout
        self.figure.tight_layout()
        
        # Redibujar canvas
        self.canvas.draw()
    
    def _update_graficos_avanzados(self, analisis):
        """Actualiza los 4 gráficos con análisis financiero avanzado."""
        import matplotlib.patches as mpatches
        
        # Limpiar todos los ejes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        
        # ===== GRÁFICO 1: EVOLUCIÓN MENSUAL (Línea) =====
        if analisis.tendencia_mensual:
            meses = [f"{m.mes}/{m.anio}" for m in analisis.tendencia_mensual]
            ingresos = [m.ingresos for m in analisis.tendencia_mensual]
            gastos = [m.gastos for m in analisis.tendencia_mensual]
            balances = [m.balance for m in analisis.tendencia_mensual]
            
            x = range(len(meses))
            
            # Líneas
            self.ax1.plot(x, ingresos, 'g-', marker='o', label='Ingresos', linewidth=2)
            self.ax1.plot(x, gastos, 'r-', marker='s', label='Gastos', linewidth=2)
            self.ax1.plot(x, balances, 'b-', marker='^', label='Balance', linewidth=2, linestyle='--')
            
            self.ax1.set_title('Evolución Mensual', fontweight='bold', fontsize=9)
            self.ax1.set_ylabel('Monto ($)', fontsize=8)
            self.ax1.set_xticks(x)
            self.ax1.set_xticklabels(meses, rotation=45, ha='right', fontsize=7)
            self.ax1.legend(fontsize=7)
            self.ax1.grid(True, alpha=0.3)
            self.ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        else:
            self.ax1.text(0.5, 0.5, 'Sin datos suficientes', ha='center', va='center', fontsize=9)
            self.ax1.axis('off')
        
        # ===== GRÁFICO 2: DISTRIBUCIÓN DE GASTOS (Torta) =====
        if analisis.gastos_por_categoria:
            # Tomar top 6 categorías, el resto agrupar en "Otros"
            items = sorted(analisis.gastos_por_categoria.items(), key=lambda x: x[1], reverse=True)
            if len(items) > 6:
                top_5 = items[:5]
                otros = sum(monto for _, monto in items[5:])
                items = top_5 + [('Otros', otros)]
            
            categorias = [item[0] for item in items]
            valores = [item[1] for item in items]
            
            colores = plt.cm.Set3(range(len(categorias)))
            
            wedges, texts, autotexts = self.ax2.pie(
                valores,
                labels=[c[:10] + '...' if len(c) > 10 else c for c in categorias],
                autopct='%1.1f%%',
                colors=colores,
                startangle=90,
                textprops={'fontsize': 7}
            )
            
            self.ax2.set_title('Distribución Gastos', fontweight='bold', fontsize=9)
        else:
            self.ax2.text(0.5, 0.5, 'Sin gastos', ha='center', va='center', fontsize=9)
            self.ax2.axis('off')
        
        # ===== GRÁFICO 3: COMPARACIÓN INGRESOS VS GASTOS (Barras) =====
        categorias = ['Total']
        valores_ingresos = [analisis.total_ingresos]
        valores_gastos = [analisis.total_gastos]
        
        x = range(len(categorias))
        width = 0.35
        
        bars1 = self.ax3.bar([i - width/2 for i in x], valores_ingresos, width, 
                            label='Ingresos', color='#2ecc71', edgecolor='black')
        bars2 = self.ax3.bar([i + width/2 for i in x], valores_gastos, width,
                            label='Gastos', color='#e74c3c', edgecolor='black')
        
        # Agregar valores sobre las barras
        for bar in bars1:
            height = bar.get_height()
            self.ax3.text(bar.get_x() + bar.get_width()/2., height,
                         f'${height:,.0f}',
                         ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        for bar in bars2:
            height = bar.get_height()
            self.ax3.text(bar.get_x() + bar.get_width()/2., height,
                         f'${height:,.0f}',
                         ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        self.ax3.set_title('Ingresos vs Gastos', fontweight='bold', fontsize=9)
        self.ax3.set_ylabel('Monto ($)', fontsize=8)
        self.ax3.set_xticks(x)
        self.ax3.set_xticklabels(categorias)
        self.ax3.legend(fontsize=8)
        self.ax3.grid(axis='y', alpha=0.3)
        
        # ===== GRÁFICO 4: TOP CATEGORÍAS (Barras horizontales) =====
        if analisis.top_5_gastos:
            cats = [cat[:15] + '...' if len(cat) > 15 else cat for cat, _ in analisis.top_5_gastos]
            montos = [monto for _, monto in analisis.top_5_gastos]
            
            y_pos = range(len(cats))
            
            bars = self.ax4.barh(y_pos, montos, color='#e74c3c', edgecolor='black', alpha=0.7)
            
            # Agregar valores
            for i, (bar, monto) in enumerate(zip(bars, montos)):
                self.ax4.text(monto + max(montos)*0.01, i,
                             f'${monto:,.0f}',
                             va='center', fontsize=7)
            
            self.ax4.set_yticks(y_pos)
            self.ax4.set_yticklabels(cats, fontsize=7)
            self.ax4.set_xlabel('Monto ($)', fontsize=8)
            self.ax4.set_title('Top 5 Gastos', fontweight='bold', fontsize=9)
            self.ax4.grid(axis='x', alpha=0.3)
        else:
            self.ax4.text(0.5, 0.5, 'Sin datos', ha='center', va='center', fontsize=9)
            self.ax4.axis('off')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def _load_categorias(self):
        """Carga todas las categorías en la tabla."""
        # Limpiar tabla
        self.list_categorias.DeleteAllItems()
        
        # Obtener todas las categorías
        categorias = self.categoria_repo.find_all()
        
        # Llenar tabla
        for i, cat in enumerate(categorias):
            index = self.list_categorias.InsertItem(i, cat.nombre)
            self.list_categorias.SetItem(index, 1, cat.tipo.value)
            self.list_categorias.SetItem(index, 2, cat.descripcion or "")
            estado = "Activo" if cat.activa else "Inactivo"
            self.list_categorias.SetItem(index, 3, estado)
            
            # Color según estado
            if not cat.activa:
                self.list_categorias.SetItemTextColour(index, wx.Colour(150, 150, 150))
    
    def create_new_person(self):
        """Prepara la vista para crear una nueva persona."""
        self.current_persona = None
        self.empty_message.Hide()
        self.notebook.Show()

        self._get_general_control("txt_nombres").SetValue("")
        self._get_general_control("txt_apellidos").SetValue("")
        self._get_general_control("txt_identificacion").SetValue("")
        self._get_general_control("txt_telefono").SetValue("")
        self._get_general_control("txt_correo").SetValue("")
        self._get_general_control("lbl_fecha_registro").SetLabel("-")
        self.txt_observaciones.SetValue("")
        self._update_observaciones_status()
        self._actualizar_lista_movimientos([])
        self._reset_resumen()
        self._actualizar_vista_foto()
        self._update_general_context()
        
        # Seleccionar primera pestaña
        self.notebook.SetSelection(0)

        self.Layout()

    def _on_guardar_persona(self, event):
        """Guarda la ficha visible desde la pestaña general."""
        self._save_persona()

    def _on_cancelar_persona(self, event):
        """Restaura los datos actuales o vuelve al estado vacío."""
        if self.current_persona:
            self.presenter.select_persona(self.current_persona.id)
        else:
            self.show_empty_state()
            if hasattr(self.presenter.view, "show_status"):
                self.presenter.view.show_status("Edición cancelada", 0)

    def _on_guardar_observaciones(self, event):
        """Guarda observaciones reutilizando el mismo flujo de ficha."""
        self._save_persona()
    
    # ===== MÉTODOS DE FOTO =====
    
    def _on_cargar_foto(self, event):
        """Maneja carga de foto desde archivo."""
        if not self.current_persona:
            wx.MessageBox(
                "Primero debe guardar la persona",
                "Aviso",
                wx.OK | wx.ICON_INFORMATION
            )
            return
        
        # Diálogo de selección de archivo
        wildcard = "Imágenes (*.jpg;*.png)|*.jpg;*.png|Todos los archivos (*.*)|*.*"
        dialog = wx.FileDialog(
            self,
            "Seleccionar foto de perfil",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            self._procesar_foto(filepath)
        
        dialog.Destroy()
    
    def _on_capturar_foto(self, event):
        """Maneja captura de foto con webcam usando diálogo integrado."""
        if not self.current_persona:
            wx.MessageBox(
                "Primero debe guardar la persona",
                "Aviso",
                wx.OK | wx.ICON_INFORMATION
            )
            return
        
        try:
            from .camera_dialog import capture_photo_dialog
            
            # Abrir diálogo de captura integrado
            photo_path = capture_photo_dialog(
                parent=self,
                persona_id=self.current_persona.id
            )
            
            if photo_path:
                self._procesar_foto(photo_path)
                wx.MessageBox(
                    "Foto capturada exitosamente",
                    "Éxito",
                    wx.OK | wx.ICON_INFORMATION
                )
            
        except Exception as e:
            wx.MessageBox(
                f"Error al capturar foto:\n{str(e)}",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
    
    def _on_eliminar_foto(self, event):
        """Maneja eliminación de foto."""
        if not self.current_persona or not self.current_persona.foto_path:
            wx.MessageBox(
                "No hay foto para eliminar",
                "Aviso",
                wx.OK | wx.ICON_INFORMATION
            )
            return
        
        # Confirmar eliminación
        respuesta = wx.MessageBox(
            "¿Está seguro de que desea eliminar la foto de perfil?",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_QUESTION
        )
        
        if respuesta == wx.YES:
            try:
                # Eliminar archivo
                if os.path.exists(self.current_persona.foto_path):
                    os.remove(self.current_persona.foto_path)
                
                # Actualizar persona
                self.persona_service.eliminar_foto(self.current_persona.id)
                self.current_persona.foto_path = None
                
                # Actualizar UI
                self._actualizar_vista_foto()
                
                wx.MessageBox(
                    "Foto eliminada exitosamente",
                    "Éxito",
                    wx.OK | wx.ICON_INFORMATION
                )
                
            except Exception as e:
                wx.MessageBox(
                    f"Error al eliminar foto:\n{str(e)}",
                    "Error",
                    wx.OK | wx.ICON_ERROR
                )
    
    def _procesar_foto(self, filepath: str):
        """
        Procesa y guarda la foto seleccionada.
        
        Args:
            filepath: Ruta al archivo de imagen
        """
        try:
            # Copiar a directorio de fotos
            from ...infrastructure.config.settings import Config
            import shutil
            
            ext = Path(filepath).suffix
            new_filename = f"persona_{self.current_persona.id}{ext}"
            new_path = Config.PHOTOS_DIR / new_filename
            
            shutil.copy2(filepath, new_path)
            
            # Actualizar persona
            self.persona_service.actualizar_foto(
                self.current_persona.id,
                str(new_path)
            )
            self.current_persona.foto_path = str(new_path)
            
            # Actualizar UI
            self._actualizar_vista_foto()
            
        except Exception as e:
            wx.MessageBox(
                f"Error al procesar foto:\n{str(e)}",
                "Error",
                wx.OK | wx.ICON_ERROR
            )
    
    def _actualizar_vista_foto(self):
        """Actualiza la vista de foto según el estado actual."""
        if self.current_persona and self.current_persona.foto_path:
            # Cargar y mostrar foto
            if os.path.exists(self.current_persona.foto_path):
                img = wx.Image(
                    self.current_persona.foto_path,
                    wx.BITMAP_TYPE_ANY
                )
                # Redimensionar manteniendo proporción
                img = img.Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
                self.foto_bitmap.SetBitmap(wx.Bitmap(img))
                self.lbl_foto_info.SetLabel(
                    f"Foto actualizada: {Path(self.current_persona.foto_path).name}"
                )
                self.lbl_foto_info.SetForegroundColour(COLORS['success'])
            else:
                self._mostrar_placeholder_foto()
        else:
            self._mostrar_placeholder_foto()
        
        self._update_general_context(self.list_movimientos.GetItemCount())
        self.Layout()
    
    def _mostrar_placeholder_foto(self):
        """Muestra imagen placeholder cuando no hay foto."""
        # Crear bitmap vacío
        bitmap = wx.Bitmap(200, 200)
        dc = wx.MemoryDC(bitmap)
        dc.SetBackground(wx.Brush(COLORS['input_bg']))
        dc.Clear()
        
        # Dibujar icono o texto
        dc.SetTextForeground(COLORS['text_muted'])
        font = wx.Font(48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        dc.DrawText(ICONS['user'], 75, 65)
        
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        dc.DrawText("Sin foto", 78, 130)
        
        dc.SelectObject(wx.NullBitmap)
        self.foto_bitmap.SetBitmap(bitmap)
        self.lbl_foto_info.SetLabel("Sin foto de perfil")
        self.lbl_foto_info.SetForegroundColour(COLORS['text_muted'])
    
    # ===== MÉTODOS DE MOVIMIENTOS =====
    
    def _on_nuevo_movimiento(self, event):
        """Abre diálogo para crear nuevo movimiento."""
        if not self.current_persona:
            wx.MessageBox("Primero seleccione una persona", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return
        
        from .dialogs import MovimientoDialog
        
        categorias = self.categoria_repo.find_all()
        dialog = MovimientoDialog(self, "Nuevo Movimiento", categorias=categorias)
        
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.get_data()
            try:
                self.movimiento_service.crear_movimiento(
                    persona_id=self.current_persona.id,
                    **data
                )
                self._load_movimientos(self.current_persona.id)
                self._load_resumen(self.current_persona.id)
                wx.MessageBox("Movimiento creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al crear movimiento:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
    
    def _on_editar_movimiento(self, event):
        """Abre diálogo para editar movimiento seleccionado."""
        if not self.current_persona:
            return
        
        selected = self.list_movimientos.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Seleccione un movimiento para editar", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return
        
        # Obtener ID del movimiento (lo guardamos en el item data)
        movimiento_id = self.list_movimientos.GetItemData(selected)
        
        from .dialogs import MovimientoDialog
        from ...domain.movimiento import Movimiento
        
        movimientos = self.movimiento_service.listar_movimientos(self.current_persona.id)
        movimiento = next((m for m in movimientos if m.id == movimiento_id), None)
        
        if not movimiento:
            wx.MessageBox("No se encontró el movimiento", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        categorias = self.categoria_repo.find_all()
        dialog = MovimientoDialog(self, "Editar Movimiento", movimiento=movimiento, categorias=categorias)
        
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.get_data()
            try:
                self.movimiento_service.actualizar_movimiento(movimiento_id, **data)
                self._load_movimientos(self.current_persona.id)
                self._load_resumen(self.current_persona.id)
                wx.MessageBox("Movimiento actualizado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al actualizar movimiento:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
    
    def _on_eliminar_movimiento(self, event):
        """Elimina movimiento seleccionado."""
        if not self.current_persona:
            return
        
        selected = self.list_movimientos.GetFirstSelected()
        if selected == -1:
            wx.MessageBox("Seleccione un movimiento para eliminar", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return
        
        movimiento_id = self.list_movimientos.GetItemData(selected)
        
        # Confirmar eliminación
        respuesta = wx.MessageBox(
            "¿Está seguro de que desea eliminar este movimiento?\n\nEsta acción no se puede deshacer.",
            "Confirmar Eliminación",
            wx.YES_NO | wx.ICON_WARNING
        )
        
        if respuesta == wx.YES:
            try:
                self.movimiento_service.eliminar_movimiento(movimiento_id)
                self._load_movimientos(self.current_persona.id)
                self._load_resumen(self.current_persona.id)
                wx.MessageBox("Movimiento eliminado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al eliminar movimiento:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)
    
    def _on_movimiento_selected(self, event):
        """Habilita botones de editar/eliminar cuando se selecciona un movimiento."""
        self.btn_editar_mov.Enable(True)
        self.btn_eliminar_mov.Enable(True)
        # Guardar el ID del movimiento en el item
        movimiento_id = event.GetData()
    
    def _on_movimiento_deselected(self, event):
        """Deshabilita botones cuando no hay selección."""
        self.btn_editar_mov.Enable(False)
        self.btn_eliminar_mov.Enable(False)
    
    def _on_movimiento_doble_click(self, event):
        """Abre diálogo de edición al hacer doble clic."""
        self._on_editar_movimiento(event)
    
    def _on_filtro_change(self, event):
        """Aplica filtro básico cuando cambia el tipo."""
        if self.current_persona:
            self._load_movimientos(self.current_persona.id)
    
    def _on_filtros_avanzados(self, event):
        """Abre diálogo de filtros avanzados."""
        from .dialogs import FiltrosMovimientoDialog
        
        categorias = self.categoria_repo.find_all()
        dialog = FiltrosMovimientoDialog(self, self.filtros_actuales if hasattr(self, 'filtros_actuales') else None, categorias)
        
        if dialog.ShowModal() == wx.ID_OK:
            self.filtros_actuales = dialog.get_filtros()
            self._aplicar_filtros()
        
        dialog.Destroy()
    
    def _on_limpiar_filtros(self, event):
        """Limpia todos los filtros."""
        self.choice_tipo.SetSelection(0)
        if hasattr(self, 'filtros_actuales'):
            delattr(self, 'filtros_actuales')
        if self.current_persona:
            self._load_movimientos(self.current_persona.id)
    
    def _aplicar_filtros(self):
        """Aplica filtros avanzados a la lista de movimientos."""
        if not self.current_persona:
            return
        
        # Obtener movimientos filtrados
        movimientos = self.movimiento_service.listar_movimientos(self.current_persona.id)
        
        if hasattr(self, 'filtros_actuales'):
            filtros = self.filtros_actuales
            
            # Filtrar por fecha
            if 'fecha_desde' in filtros:
                movimientos = [m for m in movimientos if m.fecha >= filtros['fecha_desde']]
            if 'fecha_hasta' in filtros:
                movimientos = [m for m in movimientos if m.fecha <= filtros['fecha_hasta']]
            
            # Filtrar por tipo
            if 'tipo' in filtros:
                from ...domain.movimiento import TipoMovimiento
                tipo_enum = TipoMovimiento.INGRESO if filtros['tipo'] == "INGRESO" else TipoMovimiento.GASTO
                movimientos = [m for m in movimientos if m.tipo == tipo_enum]
            
            # Filtrar por categoría
            if 'categoria_id' in filtros:
                movimientos = [m for m in movimientos if m.categoria_id == filtros['categoria_id']]
            
            # Filtrar por monto
            if 'monto_min' in filtros:
                movimientos = [m for m in movimientos if m.monto >= filtros['monto_min']]
            if 'monto_max' in filtros:
                movimientos = [m for m in movimientos if m.monto <= filtros['monto_max']]
        
        # Actualizar lista
        self._actualizar_lista_movimientos(movimientos)
    
    def _actualizar_lista_movimientos(self, movimientos):
        """Actualiza la lista de movimientos con los datos filtrados."""
        self.list_movimientos.DeleteAllItems()
        
        for i, mov in enumerate(movimientos):
            index = self.list_movimientos.InsertItem(i, mov.fecha.strftime("%d/%m/%Y"))
            self.list_movimientos.SetItem(index, 1, mov.tipo.value)
            
            # Obtener nombre de categoría
            categoria = self.categoria_repo.find_by_id(mov.categoria_id)
            cat_nombre = categoria.nombre if categoria else f"Cat #{mov.categoria_id}"
            self.list_movimientos.SetItem(index, 2, cat_nombre)
            
            self.list_movimientos.SetItem(index, 3, mov.descripcion or "")
            self.list_movimientos.SetItem(index, 4, f"${mov.monto:,.2f}")
            
            # Guardar ID en el item
            self.list_movimientos.SetItemData(index, mov.id)
            
            # Color según tipo
            if mov.tipo.value == "GASTO":
                self.list_movimientos.SetItemTextColour(index, wx.Colour(200, 50, 50))
            else:
                self.list_movimientos.SetItemTextColour(index, wx.Colour(50, 150, 50))
        
        self.lbl_total_movimientos.SetLabel(f"Total: {len(movimientos)} movimientos")
        self._update_general_context(len(movimientos))
