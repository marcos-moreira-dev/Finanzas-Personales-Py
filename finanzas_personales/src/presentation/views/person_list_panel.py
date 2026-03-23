"""
Panel de Lista de Personas - Interfaz Profesional

Panel lateral con diseño clásico de oficina:
- Header con título destacado
- Buscador integrado
- Lista con selección visual
- Contador de personas

Layout:
┌────────────────────┐
│ 👥 PERSONAS        │  ← Header
├────────────────────┤
│ 🔍 Buscar...       │  ← Buscador
├────────────────────┤
│ ▼ Juan Pérez      │
│   María López     │  ← Lista
│   Carlos Ruiz     │
│                   │
├────────────────────┤
│ [➕ Nueva Persona] │  ← Botón
├────────────────────┤
│ Total: 3 personas │  ← Contador
└────────────────────┘
"""
import wx
from typing import List

from ...domain.persona import Persona
from ...shared.design_tokens import COLORS, DIMENSIONS, ICONS


class PersonListPanel(wx.Panel):
    """
    Panel lateral con lista de personas estilo clásico.
    """
    
    def __init__(self, parent, presenter):
        """Inicializa el panel de lista."""
        super().__init__(parent)
        
        self.presenter = presenter
        self.personas = []
        
        self._setup_ui()
        self._bind_events()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configura UI con diseño profesional."""
        # Sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # ===== HEADER =====
        header_panel = wx.Panel(self)
        header_panel.SetBackgroundColour(COLORS['table_header'])
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Título con icono
        title = wx.StaticText(header_panel, label=f"{ICONS['users']} PERSONAS")
        title_font = title.GetFont()
        title_font.SetPointSize(11)
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(COLORS['text_primary'])
        header_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 12)
        
        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND)
        
        # Separador
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        
        # ===== BUSCADOR =====
        search_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_search = wx.StaticText(self, label="Buscar:")
        lbl_search.SetForegroundColour(COLORS['text_secondary'])
        search_sizer.Add(lbl_search, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12)

        lbl_search_hint = wx.StaticText(
            self,
            label="Filtre la cartera por nombre o apellido y seleccione una ficha para editarla.",
        )
        lbl_search_hint.SetForegroundColour(COLORS['text_muted'])
        search_sizer.Add(lbl_search_hint, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12)
        
        self.search_ctrl = wx.SearchCtrl(
            self,
            style=wx.TE_PROCESS_ENTER
        )
        self.search_ctrl.SetDescriptiveText("Nombre o apellido...")
        self.search_ctrl.ShowCancelButton(True)
        self.search_ctrl.SetToolTip("Filtrar personas por nombre o apellido")
        self.search_ctrl.SetMinSize((-1, DIMENSIONS['input_height'] + 6))
        search_sizer.Add(self.search_ctrl, 0, wx.EXPAND | wx.ALL, 12)
        
        main_sizer.Add(search_sizer, 0, wx.EXPAND)
        
        # Separador
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        
        # ===== LISTA DE PERSONAS =====
        # Usar ListCtrl para más control visual
        self.list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.BORDER_NONE
        )
        self.list_ctrl.SetMinSize((280, 260))
        self.list_ctrl.InsertColumn(0, "Persona", width=300)
        self.list_ctrl.SetToolTip("Seleccione una persona para ver detalles")
        
        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        
        # Separador
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.TOP, 6)
        
        # ===== BOTÓN NUEVA PERSONA =====
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.new_button = wx.Button(
            self,
            label=f"{ICONS['add']} Nueva Persona",
            size=(-1, DIMENSIONS['button_height'] + 6)
        )
        self.new_button.SetBackgroundColour(COLORS['success'])
        self.new_button.SetForegroundColour(COLORS['text_inverse'])
        self.new_button.SetToolTip("Crear una nueva persona (Ctrl+N)")
        btn_sizer.Add(self.new_button, 1, wx.EXPAND | wx.ALL, 10)
        
        main_sizer.Add(btn_sizer, 0, wx.EXPAND)
        
        # Separador
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        
        # ===== CONTADOR =====
        self.lbl_count = wx.StaticText(
            self,
            label="Total: 0 personas",
            style=wx.ALIGN_CENTER
        )
        self.lbl_count.SetForegroundColour(COLORS['text_muted'])
        self.lbl_count.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        main_sizer.Add(self.lbl_count, 0, wx.EXPAND | wx.ALL, 10)
        
        # Aplicar layout
        self.SetSizer(main_sizer)
    
    def _apply_styles(self):
        """Aplica estilos visuales profesionales."""
        self.SetBackgroundColour(COLORS['panel_bg'])
        
        # Configurar colores de la lista
        self.list_ctrl.SetBackgroundColour(COLORS['panel_bg'])
        
        # Colores según estado
        self._normal_bg = COLORS['panel_bg']
        self._selected_bg = COLORS['primary']
        self._hover_bg = COLORS['primary_light']
    
    def _bind_events(self):
        """Conecta eventos."""
        # Búsqueda
        self.search_ctrl.Bind(wx.EVT_TEXT, self._on_search)
        self.search_ctrl.Bind(wx.EVT_SEARCH_CANCEL, self._on_search_cancel)
        
        # Selección en lista
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_select_person)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_select_person)
        
        # Botón nueva
        self.new_button.Bind(wx.EVT_BUTTON, self._on_new_person)
    
    def update_list(self, personas: List[Persona]):
        """Actualiza lista con datos."""
        self.personas = personas
        self.list_ctrl.DeleteAllItems()
        
        for i, persona in enumerate(personas):
            display_text = f"{persona.apellidos}, {persona.nombres}"
            index = self.list_ctrl.InsertItem(i, f"{ICONS['person']} {display_text}")
            # Guardar referencia al objeto
            self.list_ctrl.SetItemData(index, persona.id)
        
        # Actualizar contador
        count = len(personas)
        self.lbl_count.SetLabel(f"Total: {count} persona{'s' if count != 1 else ''}")
    
    def get_selected_person(self) -> Persona:
        """Obtiene persona seleccionada."""
        selection = self.list_ctrl.GetFirstSelected()
        if selection >= 0:
            persona_id = self.list_ctrl.GetItemData(selection)
            for persona in self.personas:
                if persona.id == persona_id:
                    return persona
        return None
    
    def select_person(self, persona_id: int):
        """Selecciona persona por ID."""
        for i, persona in enumerate(self.personas):
            if persona.id == persona_id:
                self.list_ctrl.Select(i)
                self._on_select_person(None)
                break

    def clear_selection(self):
        """Limpia la selección actual de la lista."""
        selected = self.list_ctrl.GetFirstSelected()
        if selected >= 0:
            self.list_ctrl.Select(selected, on=False)
    
    # ===== EVENT HANDLERS =====
    
    def _on_search(self, event):
        """Búsqueda en tiempo real."""
        search_term = self.search_ctrl.GetValue()
        self.presenter.search_personas(search_term)
    
    def _on_search_cancel(self, event):
        """Cancelar búsqueda."""
        self.search_ctrl.SetValue("")
        self.presenter.load_personas()
    
    def _on_select_person(self, event):
        """Seleccionar persona."""
        persona = self.get_selected_person()
        if persona:
            self.presenter.select_persona(persona.id)
    
    def _on_new_person(self, event):
        """Crear nueva persona."""
        self.presenter.create_new_persona()
