"""
Ventana Principal - Interfaz Profesional Mejorada

Implementa el diseño UX clásico de oficina con:
- Layout Master-Detail (Sidebar + Main Area)
- Toolbar profesional con iconos
- Colores y estilos según design tokens
- Accesibilidad WCAG 2.1 AA

Layout:
┌─────────────────────────────────────────────────────────┐
│  Menú  |  Toolbar                                       │
├───────────────┬─────────────────────────────────────────┤
│               │                                         │
│  Panel        │   Área Principal - Pestañas             │
│  Lateral      │                                         │
│  (280px)      │   General | Movimientos | Resumen      │
│               │                                         │
├───────────────┴─────────────────────────────────────────┤
│  Barra de Estado                                        │
└─────────────────────────────────────────────────────────┘
"""
import wx

from ...infrastructure.db.database import Database
from ...infrastructure.repositories.persona_repository import PersonaRepository
from ...application.services.persona_service import PersonaService
from ...application.services.movimiento_service import MovimientoService
from ..presenters.main_presenter import MainPresenter
from .person_list_panel import PersonListPanel
from .person_detail_view import PersonDetailView
from ...shared.design_tokens import COLORS, DIMENSIONS, ICONS


class MainWindow(wx.Frame):
    """
    Ventana principal con diseño profesional Master-Detail.
    """
    
    def __init__(self, parent, title="Finanzas Personales"):
        """Inicializa la ventana principal con diseño profesional."""
        super().__init__(
            parent, 
            title=title,
            size=(DIMENSIONS['window_default_width'], DIMENSIONS['window_default_height'])
        )
        
        # Configurar ventana
        self.SetMinSize((DIMENSIONS['window_min_width'], DIMENSIONS['window_min_height']))
        self.SetBackgroundColour(COLORS['window_bg'])
        
        # Inicializar servicios
        self._init_services()
        
        # Configurar UI
        self._setup_menu()
        self._setup_main_layout()  # Crea main_panel primero
        self._setup_status_bar()
        
        # Centrar ventana
        self.Center()
        
        # Cargar datos iniciales
        self._load_initial_data()
    
    def _init_services(self):
        """Inicializa servicios y presentador."""
        from ...infrastructure.config.settings import Config
        
        self.db = Database(str(Config.DB_PATH))
        conn = self.db.get_connection()
        
        # Esta ventana sigue actuando como composition root de la capa de
        # presentacion: arma repositorios, servicios y presenter en un solo lugar.
        persona_repo = PersonaRepository(conn)
        from ...infrastructure.repositories.movimiento_repository import MovimientoRepository
        from ...infrastructure.repositories.categoria_repository import CategoriaRepository
        movimiento_repo = MovimientoRepository(conn)
        categoria_repo = CategoriaRepository(conn)
        
        # Los servicios encapsulan reglas de aplicacion y dejan la vista solo
        # con coordinacion de eventos y renderizado.
        self.persona_service = PersonaService(persona_repo)
        self.movimiento_service = MovimientoService(movimiento_repo)
        self.categoria_repo = categoria_repo
        
        # El presenter es el intermediario entre widgets wx y casos de uso.
        self.presenter = MainPresenter(
            self,
            self.persona_service,
            self.movimiento_service
        )
    
    def _setup_menu(self):
        """Configura menú superior clásico."""
        menubar = wx.MenuBar()
        
        # Menú Archivo
        file_menu = wx.Menu()
        
        new_item = file_menu.Append(
            wx.ID_NEW,
            f"{ICONS['add']} &Nueva Persona\tCtrl+N",
            "Crear una nueva persona"
        )
        self.Bind(wx.EVT_MENU, self._on_new_person, new_item)
        
        file_menu.AppendSeparator()
        
        save_item = file_menu.Append(
            wx.ID_SAVE,
            f"{ICONS['save']} &Guardar\tCtrl+S",
            "Guardar cambios"
        )
        self.Bind(wx.EVT_MENU, self._on_save, save_item)
        
        file_menu.AppendSeparator()
        
        export_item = file_menu.Append(
            wx.ID_ANY,
            f"{ICONS['receipt']} &Exportar...",
            "Exportar datos"
        )
        self.Bind(wx.EVT_MENU, self._on_export, export_item)
        
        file_menu.AppendSeparator()
        
        exit_item = file_menu.Append(
            wx.ID_EXIT,
            f"{ICONS['close']} &Salir\tAlt+F4",
            "Cerrar la aplicación"
        )
        self.Bind(wx.EVT_MENU, self._on_exit, exit_item)
        
        menubar.Append(file_menu, "&Archivo")
        
        # Menú Editar
        edit_menu = wx.Menu()
        undo_item = edit_menu.Append(
            wx.ID_UNDO,
            f"{ICONS['undo']} &Deshacer\tCtrl+Z",
            "Deshacer en el contexto activo"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_undo, undo_item)
        redo_item = edit_menu.Append(
            wx.ID_ANY,
            f"&Rehacer\tCtrl+Y",
            "Rehacer en el contexto activo"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_redo, redo_item)
        edit_menu.AppendSeparator()
        cut_item = edit_menu.Append(
            wx.ID_CUT,
            f"Cor&tar\tCtrl+X",
            "Cortar selecciÃ³n en el campo activo"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_cut, cut_item)
        copy_item = edit_menu.Append(
            wx.ID_COPY,
            f"&Copiar\tCtrl+C",
            "Copiar selecciÃ³n en el campo activo"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_copy, copy_item)
        paste_item = edit_menu.Append(
            wx.ID_PASTE,
            f"&Pegar\tCtrl+V",
            "Pegar en el campo activo"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_paste, paste_item)
        edit_menu.AppendSeparator()
        delete_item = edit_menu.Append(
            wx.ID_DELETE,
            f"{ICONS['delete']} &Eliminar\tDel",
            "Eliminar la selecciÃ³n o la entidad actual"
        )
        self.Bind(wx.EVT_MENU, self._on_delete, delete_item)
        menubar.Append(edit_menu, "&Editar")
        
        # Menú Ver
        view_menu = wx.Menu()
        refresh_item = view_menu.Append(
            wx.ID_ANY,
            f"{ICONS['refresh']} &Actualizar\tF5",
            "Recargar datos de la aplicaciÃ³n"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_refresh, refresh_item)
        view_menu.AppendSeparator()
        summary_item = view_menu.Append(
            wx.ID_ANY,
            "&Resumen Financiero\tF2",
            "Abrir la pestaÃ±a de resumen financiero"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_summary, summary_item)
        graphs_item = view_menu.Append(
            wx.ID_ANY,
            "&Gráficos\tF3",
            "Ir a la sección de gráficos"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_graphs, graphs_item)
        menubar.Append(view_menu, "&Ver")
        
        # Menú Herramientas
        tools_menu = wx.Menu()
        settings_item = tools_menu.Append(
            wx.ID_ANY,
            f"{ICONS['settings']} &Configuración...",
            "Opciones de configuración del producto"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_settings, settings_item)
        tools_menu.AppendSeparator()
        search_item = tools_menu.Append(
            wx.ID_ANY,
            f"{ICONS['search']} &Buscar\tCtrl+F",
            "Llevar el foco al buscador principal"
        )
        self.Bind(wx.EVT_MENU, self._on_menu_search, search_item)
        menubar.Append(tools_menu, "&Herramientas")
        
        # Menú Ayuda
        help_menu = wx.Menu()
        help_item = help_menu.Append(
            wx.ID_HELP,
            f"{ICONS['help']} &Ayuda\tF1",
            "Mostrar ayuda"
        )
        self.Bind(wx.EVT_MENU, self._on_help, help_item)
        
        help_menu.AppendSeparator()
        
        about_item = help_menu.Append(
            wx.ID_ABOUT,
            f"{ICONS['info']} &Acerca de...",
            "Información sobre la aplicación"
        )
        self.Bind(wx.EVT_MENU, self._on_about, about_item)
        
        menubar.Append(help_menu, "A&yuda")
        
        self.SetMenuBar(menubar)
    
    def _setup_toolbar(self, parent):
        """Configura toolbar profesional con iconos."""
        toolbar_panel = wx.Panel(parent, size=(-1, DIMENSIONS['toolbar_height'] + 8))
        toolbar_panel.SetBackgroundColour(COLORS['toolbar_bg'])
        
        toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_height = DIMENSIONS['button_height']
        primary_button_width = DIMENSIONS['button_min_width'] + 22
        search_height = DIMENSIONS['input_height'] + 4
        
        # Botón Nuevo
        btn_new = wx.Button(
            toolbar_panel,
            label=f"{ICONS['add']} Nuevo",
            size=(primary_button_width, button_height)
        )
        btn_new.SetBackgroundColour(COLORS['primary'])
        btn_new.SetForegroundColour(COLORS['text_inverse'])
        btn_new.SetToolTip("Crear nueva persona (Ctrl+N)")
        btn_new.Bind(wx.EVT_BUTTON, self._on_new_person)
        toolbar_sizer.Add(btn_new, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)
        
        # Botón Guardar
        btn_save = wx.Button(
            toolbar_panel,
            label=f"{ICONS['save']} Guardar",
            size=(primary_button_width, button_height)
        )
        btn_save.SetBackgroundColour(COLORS['secondary'])
        btn_save.SetToolTip("Guardar cambios (Ctrl+S)")
        btn_save.Bind(wx.EVT_BUTTON, self._on_save)
        toolbar_sizer.Add(btn_save, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)
        
        # Botón Eliminar
        btn_delete = wx.Button(
            toolbar_panel,
            label=f"{ICONS['delete']} Eliminar",
            size=(primary_button_width, button_height)
        )
        btn_delete.SetBackgroundColour(COLORS['error'])
        btn_delete.SetForegroundColour(COLORS['text_inverse'])
        btn_delete.SetToolTip("Eliminar selección")
        btn_delete.Bind(wx.EVT_BUTTON, self._on_delete)
        toolbar_sizer.Add(btn_delete, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)
        
        # Separador vertical
        line = wx.StaticLine(toolbar_panel, style=wx.LI_VERTICAL)
        toolbar_sizer.Add(line, 0, wx.EXPAND | wx.ALL, 6)
        
        # Campo de búsqueda
        lbl_search = wx.StaticText(toolbar_panel, label="Buscar:")
        toolbar_sizer.Add(lbl_search, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        
        self.search_ctrl = wx.SearchCtrl(
            toolbar_panel,
            size=(240, search_height),
            style=wx.TE_PROCESS_ENTER
        )
        self.search_ctrl.SetDescriptiveText("Nombre o apellido...")
        self.search_ctrl.ShowCancelButton(True)
        self.search_ctrl.SetToolTip("Buscar personas")
        self.search_ctrl.Bind(wx.EVT_TEXT, self._on_search)
        self.search_ctrl.Bind(wx.EVT_SEARCH_CANCEL, self._on_search_cancel)
        toolbar_sizer.Add(self.search_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)
        
        # Separador expansible
        toolbar_sizer.AddStretchSpacer()
        
        # Botón Ayuda
        btn_help = wx.Button(
            toolbar_panel,
            label=f"{ICONS['help']} Ayuda",
            size=(DIMENSIONS['button_min_width'], button_height)
        )
        btn_help.SetToolTip("Mostrar ayuda (F1)")
        btn_help.Bind(wx.EVT_BUTTON, self._on_help)
        toolbar_sizer.Add(btn_help, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 6)
        
        toolbar_panel.SetSizer(toolbar_sizer)
        self.toolbar_panel = toolbar_panel
    
    def _setup_main_layout(self):
        """Configura layout principal Master-Detail."""
        # Panel contenedor principal
        self.main_panel = wx.Panel(self)
        self.main_panel.SetBackgroundColour(COLORS['window_bg'])
        
        # Crear toolbar como hijo de main_panel
        self._setup_toolbar(self.main_panel)
        
        # Layout vertical principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Agregar toolbar
        main_sizer.Add(self.toolbar_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        
        # Separador
        main_sizer.AddSpacer(10)
        
        # Splitter para panel lateral y área principal
        self.splitter = wx.SplitterWindow(
            self.main_panel,
            style=wx.SP_LIVE_UPDATE | wx.SP_3DBORDER
        )
        self.splitter.SetBackgroundColour(COLORS['border'])
        
        # Panel lateral (Lista de personas)
        self.person_list = PersonListPanel(self.splitter, self.presenter)
        self.person_list.SetBackgroundColour(COLORS['panel_bg'])
        
        # Área principal (Pestañas)
        self.person_detail = PersonDetailView(
            self.splitter,
            self.presenter,
            self.persona_service,
            self.movimiento_service,
            self.categoria_repo
        )
        self.person_detail.SetBackgroundColour(COLORS['panel_bg'])
        
        # Dividir ventana
        self.splitter.SplitVertically(
            self.person_list,
            self.person_detail,
            DIMENSIONS['sidebar_width']
        )
        self.splitter.SetMinimumPaneSize(DIMENSIONS['sidebar_min_width'])
        self.splitter.SetSashGravity(0.0)
        
        main_sizer.Add(self.splitter, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        self.main_panel.SetSizer(main_sizer)
    
    def _setup_status_bar(self):
        """Configura barra de estado profesional."""
        self.statusbar = self.CreateStatusBar(3)
        self.statusbar.SetBackgroundColour(COLORS['statusbar_bg'])
        
        # Configurar anchos de secciones
        self.statusbar.SetStatusWidths([-2, -3, -1])
        
        # Textos iniciales
        self.statusbar.SetStatusText("Listo", 0)
        self.statusbar.SetStatusText("Sin persona seleccionada", 1)
        self.statusbar.SetStatusText("v0.2.0", 2)
    
    def _load_initial_data(self):
        """Carga datos iniciales."""
        self.presenter.load_personas()
    
    # ===== EVENT HANDLERS =====
    
    def _on_new_person(self, event):
        """Maneja creación de nueva persona."""
        self.presenter.create_new_persona()
    
    def _on_save(self, event):
        """Maneja guardar cambios."""
        if self.person_detail.notebook.IsShown():
            if self.person_detail.save_current_person():
                self.statusbar.SetStatusText("Cambios guardados", 0)
            return

        self._show_menu_context(
            "Guardar",
            "Abra o cree una persona para disponer de un contexto de guardado."
        )
    
    def _on_delete(self, event):
        """Maneja eliminación."""
        persona = self.presenter.current_persona
        if not persona:
            self._show_menu_context(
                "Eliminar",
                "Seleccione una persona para poder eliminarla desde la barra principal."
            )
            return

        respuesta = wx.MessageBox(
            f"¿Desea eliminar a {persona.nombre_completo}?\n\nSe borrarán también sus movimientos asociados.",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_WARNING,
        )
        if respuesta == wx.YES:
            self.presenter.delete_persona(persona.id)
    
    def _on_search(self, event):
        """Maneja búsqueda en tiempo real."""
        search_term = self.search_ctrl.GetValue()
        self.presenter.search_personas(search_term)
    
    def _on_search_cancel(self, event):
        """Maneja cancelación de búsqueda."""
        self.search_ctrl.SetValue("")
        self.presenter.load_personas()

    def _show_menu_context(self, title: str, message: str) -> None:
        """Muestra contexto útil cuando una acción aún no tiene flujo completo."""
        wx.MessageBox(message, title, wx.OK | wx.ICON_INFORMATION)
        self.statusbar.SetStatusText(title, 0)

    def _apply_text_action(self, action_name: str, title: str, fallback_message: str) -> None:
        """Intenta aplicar una acción sobre el control de texto con foco."""
        focused = wx.Window.FindFocus()
        action = getattr(focused, action_name, None) if focused else None

        if callable(action):
            try:
                action()
                self.statusbar.SetStatusText(f"{title} aplicado", 0)
                return
            except Exception:
                pass

        self._show_menu_context(title, fallback_message)

    def _on_menu_undo(self, event):
        self._apply_text_action(
            "Undo",
            "Deshacer",
            "No hay una acción deshacible en el control activo."
        )

    def _on_menu_redo(self, event):
        self._apply_text_action(
            "Redo",
            "Rehacer",
            "No hay una acción rehacible en el control activo."
        )

    def _on_menu_cut(self, event):
        self._apply_text_action(
            "Cut",
            "Cortar",
            "Seleccione texto editable para usar Cortar."
        )

    def _on_menu_copy(self, event):
        self._apply_text_action(
            "Copy",
            "Copiar",
            "Seleccione texto o contenido copiable para usar Copiar."
        )

    def _on_menu_paste(self, event):
        self._apply_text_action(
            "Paste",
            "Pegar",
            "Sitúe el foco en un campo editable para usar Pegar."
        )

    def _on_menu_refresh(self, event):
        self.refresh_data()
        self.statusbar.SetStatusText("Datos actualizados", 0)

    def _on_menu_summary(self, event):
        if self.presenter.current_persona and self.person_detail.notebook.IsShown():
            self.person_detail.notebook.SetSelection(4)
            self.statusbar.SetStatusText("Pestaña de resumen abierta", 0)
            return

        self._show_menu_context(
            "Resumen Financiero",
            "Seleccione primero una persona para abrir su resumen financiero."
        )

    def _on_menu_graphs(self, event):
        if self.presenter.current_persona and self.person_detail.notebook.IsShown():
            self.person_detail.notebook.SetSelection(4)
            self._show_menu_context(
                "Gráficos",
                "Los gráficos están dentro de la pestaña 'Resumen' de la persona seleccionada."
            )
            return

        self._show_menu_context(
            "Gráficos",
            "Seleccione una persona para visualizar los gráficos financieros."
        )

    def _on_menu_settings(self, event):
        self._show_menu_context(
            "Configuración",
            "La pantalla de configuración aún no está implementada. "
            "Aquí deberían ir rutas, preferencias visuales y opciones de exportación."
        )

    def _on_menu_search(self, event):
        self.search_ctrl.SetFocus()
        self.search_ctrl.SelectAll()
        self.statusbar.SetStatusText("Buscador principal enfocado", 0)
    
    def _on_export(self, event):
        """Maneja exportación a Excel."""
        from ...infrastructure.export.data_exporter import DataExporter
        
        dialog = wx.FileDialog(
            self,
            "Exportar a Excel",
            wildcard="Excel files (*.xlsx)|*.xlsx",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            filepath = dialog.GetPath()
            try:
                exporter = DataExporter(str(self.db.db_path))
                exporter.export_to_excel(filepath)
                wx.MessageBox(
                    f"Datos exportados exitosamente a:\n{filepath}",
                    "Exportación Completa",
                    wx.OK | wx.ICON_INFORMATION
                )
                self.statusbar.SetStatusText(f"Exportado: {filepath}", 0)
            except Exception as e:
                wx.MessageBox(
                    f"Error al exportar:\n{str(e)}",
                    "Error",
                    wx.OK | wx.ICON_ERROR
                )
        dialog.Destroy()
    
    def _on_help(self, event):
        """Muestra ayuda."""
        wx.MessageBox(
            "Finanzas Personales - Ayuda\n\n"
            "Atajos de teclado:\n"
            "  Ctrl+N: Nueva persona\n"
            "  Ctrl+S: Guardar\n"
            "  Ctrl+F: Buscar\n"
            "  F1: Esta ayuda\n"
            "  F5: Actualizar\n\n"
            "Para más ayuda consulte la documentación.",
            "Ayuda",
            wx.OK | wx.ICON_INFORMATION
        )
    
    def _on_about(self, event):
        """Muestra diálogo Acerca de."""
        wx.MessageBox(
            f"{ICONS['money']} Finanzas Personales v0.2.0\n\n"
            "Aplicación de escritorio para gestionar finanzas personales.\n\n"
            "Diseño UX Profesional - Estilo clásico de oficina\n"
            "Con accesibilidad WCAG 2.1 AA\n\n"
            "© 2026 - Proyecto Didáctico",
            "Acerca de",
            wx.OK | wx.ICON_INFORMATION
        )
    
    def _on_exit(self, event):
        """Maneja salida de la aplicación."""
        self.Close()
    
    # ===== MÉTODOS PÚBLICOS =====
    
    def update_person_list(self, personas):
        """Actualiza lista de personas."""
        self.person_list.update_list(personas)
        count = len(personas)
        self.statusbar.SetStatusText(f"Total de personas: {count}", 1)
    
    def show_person_detail(self, persona):
        """Muestra detalle de persona."""
        self.person_detail.load_person(persona)
        self.statusbar.SetStatusText(f"Viendo: {persona.nombre_completo}", 1)
    
    def refresh_data(self):
        """Refresca todos los datos."""
        self._load_initial_data()

        if self.presenter.current_persona:
            self.presenter.select_persona(self.presenter.current_persona.id)

    def show_status(self, message: str, field: int = 0):
        """Publica un mensaje corto en la barra de estado."""
        self.statusbar.SetStatusText(message, field)

    def show_error(self, message: str):
        """Muestra errores del presenter con feedback visual."""
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)
        self.statusbar.SetStatusText("Se produjo un error", 0)

    def show_new_person_form(self):
        """Abre la ficha vacía para crear una nueva persona."""
        self.person_list.clear_selection()
        self.person_detail.create_new_person()
        self.statusbar.SetStatusText("Nueva ficha preparada", 0)
        self.statusbar.SetStatusText("Nueva persona sin guardar", 1)

    def clear_person_detail(self):
        """Limpia el área principal cuando ya no hay persona activa."""
        self.person_detail.show_empty_state()
        self.statusbar.SetStatusText("Sin persona seleccionada", 1)

    def select_person(self, persona_id: int):
        """Selecciona una persona en la lista lateral."""
        self.person_list.select_person(persona_id)
