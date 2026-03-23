"""
Diálogos para gestión de Personas y Movimientos
"""
import wx
from datetime import date
from typing import Optional, Callable
from ...domain.persona import Persona
from ...domain.movimiento import Movimiento, TipoMovimiento


class PersonaDialog(wx.Dialog):
    """Diálogo para crear/editar persona."""
    
    def __init__(self, parent, title="Nueva Persona", persona: Optional[Persona] = None):
        super().__init__(parent, title=title, size=(450, 350))
        
        self.persona = persona
        self.result = None
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Campos
        grid = wx.FlexGridSizer(5, 2, 10, 10)
        grid.AddGrowableCol(1, 1)
        
        # Nombres
        grid.Add(wx.StaticText(panel, label="Nombres:*"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.txt_nombres = wx.TextCtrl(panel)
        grid.Add(self.txt_nombres, 0, wx.EXPAND)
        
        # Apellidos
        grid.Add(wx.StaticText(panel, label="Apellidos:*"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.txt_apellidos = wx.TextCtrl(panel)
        grid.Add(self.txt_apellidos, 0, wx.EXPAND)
        
        # Identificación
        grid.Add(wx.StaticText(panel, label="Identificación:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.txt_identificacion = wx.TextCtrl(panel)
        grid.Add(self.txt_identificacion, 0, wx.EXPAND)
        
        # Teléfono
        grid.Add(wx.StaticText(panel, label="Teléfono:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.txt_telefono = wx.TextCtrl(panel)
        grid.Add(self.txt_telefono, 0, wx.EXPAND)
        
        # Correo
        grid.Add(wx.StaticText(panel, label="Correo:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.txt_correo = wx.TextCtrl(panel)
        grid.Add(self.txt_correo, 0, wx.EXPAND)
        
        sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 15)
        
        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.AddStretchSpacer()
        
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_sizer.Add(btn_cancel, 0, wx.RIGHT, 5)
        
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_ok.SetDefault()
        btn_sizer.Add(btn_ok, 0)
        
        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 15)
        
        panel.SetSizer(sizer)
        
        # Cargar datos si es edición
        if persona:
            self.txt_nombres.SetValue(persona.nombres)
            self.txt_apellidos.SetValue(persona.apellidos)
            self.txt_identificacion.SetValue(persona.identificacion or "")
            self.txt_telefono.SetValue(persona.telefono or "")
            self.txt_correo.SetValue(persona.correo or "")
        
        # Bind
        btn_ok.Bind(wx.EVT_BUTTON, self._on_ok)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
    
    def _on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()
    
    def _on_ok(self, event):
        nombres = self.txt_nombres.GetValue().strip()
        apellidos = self.txt_apellidos.GetValue().strip()
        
        if not nombres or not apellidos:
            wx.MessageBox("Nombres y apellidos son obligatorios", "Validación", 
                         wx.OK | wx.ICON_WARNING, self)
            return
        
        self.result = {
            'nombres': nombres,
            'apellidos': apellidos,
            'identificacion': self.txt_identificacion.GetValue().strip() or None,
            'telefono': self.txt_telefono.GetValue().strip() or None,
            'correo': self.txt_correo.GetValue().strip() or None
        }
        
        self.EndModal(wx.ID_OK)
    
    def get_data(self):
        return self.result


class MovimientoDialog(wx.Dialog):
    """Diálogo para crear/editar movimiento."""
    
    def __init__(self, parent, title="Nuevo Movimiento", movimiento: Optional[Movimiento] = None, 
                 categorias=None, readonly=False):
        super().__init__(parent, title=title, size=(500, 400))
        
        self.movimiento = movimiento
        self.categorias = categorias or []
        self.result = None
        self.readonly = readonly
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Campos
        grid = wx.FlexGridSizer(6, 2, 10, 10)
        grid.AddGrowableCol(1, 1)
        
        # Fecha
        grid.Add(wx.StaticText(panel, label="Fecha:*"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.date_picker = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN)
        grid.Add(self.date_picker, 0, wx.EXPAND)
        
        # Tipo
        grid.Add(wx.StaticText(panel, label="Tipo:*"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.choice_tipo = wx.Choice(panel, choices=["INGRESO", "GASTO"])
        self.choice_tipo.SetSelection(0)
        self.choice_tipo.Bind(wx.EVT_CHOICE, self._on_tipo_change)
        grid.Add(self.choice_tipo, 0, wx.EXPAND)
        
        # Categoría
        grid.Add(wx.StaticText(panel, label="Categoría:*"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.choice_categoria = wx.Choice(panel)
        grid.Add(self.choice_categoria, 0, wx.EXPAND)
        
        # Monto
        grid.Add(wx.StaticText(panel, label="Monto:*"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.txt_monto = wx.TextCtrl(panel)
        grid.Add(self.txt_monto, 0, wx.EXPAND)
        
        # Descripción
        grid.Add(wx.StaticText(panel, label="Descripción:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.txt_descripcion = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(-1, 60))
        grid.Add(self.txt_descripcion, 0, wx.EXPAND)
        
        # Es recurrente
        grid.Add(wx.StaticText(panel, label="Recurrente:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.chk_recurrente = wx.CheckBox(panel, label="Repetir mensualmente")
        self.chk_recurrente.Disable()
        self.chk_recurrente.SetToolTip("Funcionalidad pendiente de implementaciÃ³n")
        grid.Add(self.chk_recurrente, 0, wx.EXPAND)
        
        sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 15)
        
        # Botones
        if not readonly:
            btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
            btn_sizer.AddStretchSpacer()
            
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            btn_sizer.Add(btn_cancel, 0, wx.RIGHT, 5)
            
            btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
            btn_ok.SetDefault()
            btn_sizer.Add(btn_ok, 0)
            
            sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 15)
            
            btn_ok.Bind(wx.EVT_BUTTON, self._on_ok)
        else:
            # Solo modo lectura - botón cerrar
            btn_cerrar = wx.Button(panel, wx.ID_OK, "Cerrar")
            sizer.Add(btn_cerrar, 0, wx.ALIGN_CENTER | wx.ALL, 15)
        
        panel.SetSizer(sizer)
        
        # Cargar categorías
        self._actualizar_categorias()
        
        # Cargar datos si es edición
        if movimiento:
            # Fecha
            wx_date = wx.DateTime()
            wx_date.Set(movimiento.fecha.day, movimiento.fecha.month - 1, movimiento.fecha.year)
            self.date_picker.SetValue(wx_date)
            
            # Tipo
            tipo_idx = 0 if movimiento.tipo == TipoMovimiento.INGRESO else 1
            self.choice_tipo.SetSelection(tipo_idx)
            
            # Categoría
            self._actualizar_categorias()
            for i, cat in enumerate(self.categorias_filtradas):
                if cat.id == movimiento.categoria_id:
                    self.choice_categoria.SetSelection(i)
                    break
            
            # Monto y descripción
            self.txt_monto.SetValue(str(movimiento.monto))
            self.txt_descripcion.SetValue(movimiento.descripcion or "")
            
            if readonly:
                # Deshabilitar todo
                self.date_picker.Disable()
                self.choice_tipo.Disable()
                self.choice_categoria.Disable()
                self.txt_monto.Disable()
                self.txt_descripcion.Disable()
                self.chk_recurrente.Disable()
        else:
            # Fecha actual por defecto
            self.date_picker.SetValue(wx.DateTime.Now())
        
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
    
    def _on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()
    
    def _on_tipo_change(self, event):
        self._actualizar_categorias()
    
    def _actualizar_categorias(self):
        """Actualiza las categorías según el tipo seleccionado."""
        self.choice_categoria.Clear()
        tipo = self.choice_tipo.GetStringSelection()
        
        self.categorias_filtradas = []
        for cat in self.categorias:
            if cat.activa and (cat.tipo.value == tipo or cat.tipo.value == "AMBOS"):
                self.categorias_filtradas.append(cat)
                self.choice_categoria.Append(cat.nombre)
        
        if self.categorias_filtradas:
            self.choice_categoria.SetSelection(0)
    
    def _on_ok(self, event):
        # Validaciones
        if self.choice_categoria.GetSelection() == wx.NOT_FOUND:
            wx.MessageBox("Debe seleccionar una categoría", "Validación", 
                         wx.OK | wx.ICON_WARNING, self)
            return
        
        monto_str = self.txt_monto.GetValue().strip()
        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError()
        except ValueError:
            wx.MessageBox("El monto debe ser un número positivo", "Validación", 
                         wx.OK | wx.ICON_WARNING, self)
            return
        
        # Obtener fecha
        wx_date = self.date_picker.GetValue()
        fecha = date(wx_date.GetYear(), wx_date.GetMonth() + 1, wx_date.GetDay())
        
        # Obtener categoría seleccionada
        categoria = self.categorias_filtradas[self.choice_categoria.GetSelection()]
        
        self.result = {
            'fecha': fecha,
            'tipo': TipoMovimiento.INGRESO if self.choice_tipo.GetSelection() == 0 else TipoMovimiento.GASTO,
            'categoria_id': categoria.id,
            'monto': monto,
            'descripcion': self.txt_descripcion.GetValue().strip() or None,
        }
        
        self.EndModal(wx.ID_OK)
    
    def get_data(self):
        return self.result


class FiltrosMovimientoDialog(wx.Dialog):
    """Diálogo para filtros avanzados de movimientos."""
    
    def __init__(self, parent, filtros_actuales=None, categorias=None):
        super().__init__(parent, title="Filtrar Movimientos", size=(450, 400))
        
        self.result = filtros_actuales or {}
        self.categorias = categorias or []
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Grupo Fecha
        fecha_box = wx.StaticBox(panel, label="Rango de Fechas")
        fecha_sizer = wx.StaticBoxSizer(fecha_box, wx.VERTICAL)
        
        # Desde
        desde_sizer = wx.BoxSizer(wx.HORIZONTAL)
        desde_sizer.Add(wx.StaticText(fecha_box, label="Desde:"), 0, wx.CENTER | wx.RIGHT, 5)
        self.date_desde = wx.adv.DatePickerCtrl(fecha_box, style=wx.adv.DP_DROPDOWN)
        desde_sizer.Add(self.date_desde, 1)
        fecha_sizer.Add(desde_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Hasta
        hasta_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hasta_sizer.Add(wx.StaticText(fecha_box, label="Hasta:  "), 0, wx.CENTER | wx.RIGHT, 5)
        self.date_hasta = wx.adv.DatePickerCtrl(fecha_box, style=wx.adv.DP_DROPDOWN)
        hasta_sizer.Add(self.date_hasta, 1)
        fecha_sizer.Add(hasta_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        sizer.Add(fecha_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Grupo Tipo y Categoría
        tipo_box = wx.StaticBox(panel, label="Tipo y Categoría")
        tipo_sizer = wx.StaticBoxSizer(tipo_box, wx.VERTICAL)
        
        # Tipo
        tipo_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        tipo_sizer2.Add(wx.StaticText(tipo_box, label="Tipo:"), 0, wx.CENTER | wx.RIGHT, 5)
        self.choice_tipo = wx.Choice(tipo_box, choices=["Todos", "Ingresos", "Gastos"])
        self.choice_tipo.SetSelection(0)
        tipo_sizer2.Add(self.choice_tipo, 1)
        tipo_sizer.Add(tipo_sizer2, 0, wx.EXPAND | wx.ALL, 5)
        
        # Categoría
        cat_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cat_sizer.Add(wx.StaticText(tipo_box, label="Categoría:"), 0, wx.CENTER | wx.RIGHT, 5)
        self.choice_categoria = wx.Choice(tipo_box, choices=["Todas"] + [c.nombre for c in self.categorias if c.activa])
        self.choice_categoria.SetSelection(0)
        cat_sizer.Add(self.choice_categoria, 1)
        tipo_sizer.Add(cat_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        sizer.Add(tipo_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Grupo Monto
        monto_box = wx.StaticBox(panel, label="Rango de Monto")
        monto_sizer = wx.StaticBoxSizer(monto_box, wx.VERTICAL)
        
        min_sizer = wx.BoxSizer(wx.HORIZONTAL)
        min_sizer.Add(wx.StaticText(monto_box, label="Mínimo: $"), 0, wx.CENTER)
        self.txt_monto_min = wx.TextCtrl(monto_box)
        min_sizer.Add(self.txt_monto_min, 1)
        monto_sizer.Add(min_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        max_sizer = wx.BoxSizer(wx.HORIZONTAL)
        max_sizer.Add(wx.StaticText(monto_box, label="Máximo: $"), 0, wx.CENTER)
        self.txt_monto_max = wx.TextCtrl(monto_box)
        max_sizer.Add(self.txt_monto_max, 1)
        monto_sizer.Add(max_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        sizer.Add(monto_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.AddStretchSpacer()
        
        btn_limpiar = wx.Button(panel, label="Limpiar Filtros")
        btn_limpiar.Bind(wx.EVT_BUTTON, self._on_limpiar)
        btn_sizer.Add(btn_limpiar, 0, wx.RIGHT, 5)
        
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_sizer.Add(btn_cancel, 0, wx.RIGHT, 5)
        
        btn_ok = wx.Button(panel, wx.ID_OK, "Aplicar")
        btn_ok.SetDefault()
        btn_sizer.Add(btn_ok, 0)
        
        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 15)
        
        panel.SetSizer(sizer)
        
        # Cargar filtros actuales
        self._cargar_filtros()
        
        btn_ok.Bind(wx.EVT_BUTTON, self._on_ok)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
    
    def _on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()
    
    def _cargar_filtros(self):
        """Carga los filtros actuales en los controles."""
        if 'fecha_desde' in self.result:
            wx_date = wx.DateTime()
            wx_date.Set(self.result['fecha_desde'].day, 
                       self.result['fecha_desde'].month - 1, 
                       self.result['fecha_desde'].year)
            self.date_desde.SetValue(wx_date)
        
        if 'fecha_hasta' in self.result:
            wx_date = wx.DateTime()
            wx_date.Set(self.result['fecha_hasta'].day, 
                       self.result['fecha_hasta'].month - 1, 
                       self.result['fecha_hasta'].year)
            self.date_hasta.SetValue(wx_date)
        
        if 'tipo' in self.result:
            idx = {"INGRESO": 1, "GASTO": 2}.get(self.result['tipo'], 0)
            self.choice_tipo.SetSelection(idx)
        
        if 'categoria_id' in self.result:
            for i, cat in enumerate(self.categorias):
                if cat.id == self.result['categoria_id']:
                    self.choice_categoria.SetSelection(i + 1)  # +1 porque "Todas" es 0
                    break
        
        if 'monto_min' in self.result:
            self.txt_monto_min.SetValue(str(self.result['monto_min']))
        
        if 'monto_max' in self.result:
            self.txt_monto_max.SetValue(str(self.result['monto_max']))
    
    def _on_limpiar(self, event):
        """Limpia todos los filtros."""
        self.date_desde.SetValue(wx.DateTime())
        self.date_hasta.SetValue(wx.DateTime())
        self.choice_tipo.SetSelection(0)
        self.choice_categoria.SetSelection(0)
        self.txt_monto_min.SetValue("")
        self.txt_monto_max.SetValue("")
    
    def _on_ok(self, event):
        self.result = {}
        
        # Fecha desde
        wx_date = self.date_desde.GetValue()
        if wx_date.IsValid():
            self.result['fecha_desde'] = date(
                wx_date.GetYear(),
                wx_date.GetMonth() + 1,
                wx_date.GetDay()
            )
        
        # Fecha hasta
        wx_date = self.date_hasta.GetValue()
        if wx_date.IsValid():
            self.result['fecha_hasta'] = date(
                wx_date.GetYear(),
                wx_date.GetMonth() + 1,
                wx_date.GetDay()
            )
        
        # Tipo
        tipo_idx = self.choice_tipo.GetSelection()
        if tipo_idx == 1:
            self.result['tipo'] = "INGRESO"
        elif tipo_idx == 2:
            self.result['tipo'] = "GASTO"
        
        # Categoría
        cat_idx = self.choice_categoria.GetSelection()
        if cat_idx > 0:
            self.result['categoria_id'] = self.categorias[cat_idx - 1].id
        
        # Monto mínimo
        monto_min = self.txt_monto_min.GetValue().strip()
        if monto_min:
            try:
                self.result['monto_min'] = float(monto_min)
            except ValueError:
                pass
        
        # Monto máximo
        monto_max = self.txt_monto_max.GetValue().strip()
        if monto_max:
            try:
                self.result['monto_max'] = float(monto_max)
            except ValueError:
                pass
        
        self.EndModal(wx.ID_OK)
    
    def get_filtros(self):
        return self.result
