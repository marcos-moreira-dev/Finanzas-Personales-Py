"""Panel lateral con lista de personas y cabecera de marca."""

from typing import List

import wx

from ...domain.persona import Persona
from ...infrastructure.config.settings import Config
from ...shared.design_tokens import COLORS, DIMENSIONS, ICONS


class PersonListPanel(wx.Panel):
    """Panel lateral con buscador, lista y CTA de nueva persona."""

    def __init__(self, parent, presenter):
        super().__init__(parent)
        self.presenter = presenter
        self.personas: List[Persona] = []

        self._setup_ui()
        self._bind_events()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Construye el layout del panel lateral."""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        header_panel = wx.Panel(self)
        header_panel.SetBackgroundColour(COLORS["table_header"])
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)

        logo_bitmap = self._load_logo_bitmap(44)
        if logo_bitmap is not None:
            header_sizer.Add(
                wx.StaticBitmap(header_panel, bitmap=logo_bitmap),
                0,
                wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL,
                12,
            )

        title_block = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(header_panel, label=f"{ICONS['users']} PERSONAS")
        title_font = title.GetFont()
        title_font.SetPointSize(11)
        title_font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(COLORS["text_primary"])
        title_block.Add(title, 0, wx.BOTTOM, 2)

        subtitle = wx.StaticText(header_panel, label="Control local de fichas y movimientos")
        subtitle.SetForegroundColour(COLORS["text_muted"])
        title_block.Add(subtitle, 0)

        header_sizer.Add(title_block, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 12)
        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND)
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)

        search_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_search = wx.StaticText(self, label="Buscar:")
        lbl_search.SetForegroundColour(COLORS["text_secondary"])
        search_sizer.Add(lbl_search, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12)

        lbl_search_hint = wx.StaticText(
            self,
            label="Filtre la cartera por nombre o apellido y seleccione una ficha para editarla.",
        )
        lbl_search_hint.SetForegroundColour(COLORS["text_muted"])
        search_sizer.Add(lbl_search_hint, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12)

        self.search_ctrl = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search_ctrl.SetDescriptiveText("Nombre o apellido...")
        self.search_ctrl.ShowCancelButton(True)
        self.search_ctrl.SetToolTip("Filtrar personas por nombre o apellido")
        self.search_ctrl.SetMinSize((-1, DIMENSIONS["input_height"] + 6))
        search_sizer.Add(self.search_ctrl, 0, wx.EXPAND | wx.ALL, 12)

        main_sizer.Add(search_sizer, 0, wx.EXPAND)
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)

        self.list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER | wx.BORDER_NONE,
        )
        self.list_ctrl.SetMinSize((280, 260))
        self.list_ctrl.InsertColumn(0, "Persona", width=300)
        self.list_ctrl.SetToolTip("Seleccione una persona para ver detalles")

        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.TOP, 6)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.new_button = wx.Button(
            self,
            label=f"{ICONS['add']} Nueva Persona",
            size=(-1, DIMENSIONS["button_height"] + 6),
        )
        self.new_button.SetBackgroundColour(COLORS["success"])
        self.new_button.SetForegroundColour(COLORS["text_inverse"])
        self.new_button.SetToolTip("Crear una nueva persona (Ctrl+N)")
        btn_sizer.Add(self.new_button, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(btn_sizer, 0, wx.EXPAND)

        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)

        self.lbl_count = wx.StaticText(self, label="Total: 0 personas", style=wx.ALIGN_CENTER)
        self.lbl_count.SetForegroundColour(COLORS["text_muted"])
        self.lbl_count.SetFont(
            wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        )
        main_sizer.Add(self.lbl_count, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)

    def _load_logo_bitmap(self, size: int) -> wx.Bitmap | None:
        """Carga el logo principal y lo reescala para el header."""
        if not Config.LOGO_PATH.exists():
            return None

        image = wx.Image(str(Config.LOGO_PATH), wx.BITMAP_TYPE_ANY)
        if not image.IsOk():
            return None

        scaled = image.Scale(size, size, wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(scaled)

    def _apply_styles(self) -> None:
        """Aplica colores base del panel."""
        self.SetBackgroundColour(COLORS["panel_bg"])
        self.list_ctrl.SetBackgroundColour(COLORS["panel_bg"])

    def _bind_events(self) -> None:
        """Conecta eventos de busqueda, seleccion y alta."""
        self.search_ctrl.Bind(wx.EVT_TEXT, self._on_search)
        self.search_ctrl.Bind(wx.EVT_SEARCH_CANCEL, self._on_search_cancel)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_select_person)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_select_person)
        self.new_button.Bind(wx.EVT_BUTTON, self._on_new_person)

    def update_list(self, personas: List[Persona]) -> None:
        """Refresca la lista visual con las personas recibidas."""
        self.personas = personas
        self.list_ctrl.DeleteAllItems()

        for index, persona in enumerate(personas):
            display_text = f"{persona.apellidos}, {persona.nombres}"
            row = self.list_ctrl.InsertItem(index, f"{ICONS['person']} {display_text}")
            self.list_ctrl.SetItemData(row, persona.id)

        count = len(personas)
        suffix = "s" if count != 1 else ""
        self.lbl_count.SetLabel(f"Total: {count} persona{suffix}")

    def get_selected_person(self) -> Persona | None:
        """Obtiene la persona actualmente seleccionada."""
        selection = self.list_ctrl.GetFirstSelected()
        if selection < 0:
            return None

        persona_id = self.list_ctrl.GetItemData(selection)
        for persona in self.personas:
            if persona.id == persona_id:
                return persona
        return None

    def select_person(self, persona_id: int) -> None:
        """Selecciona una persona por su identificador."""
        for index, persona in enumerate(self.personas):
            if persona.id == persona_id:
                self.list_ctrl.Select(index)
                self._on_select_person(None)
                break

    def clear_selection(self) -> None:
        """Limpia la seleccion activa en la lista."""
        selected = self.list_ctrl.GetFirstSelected()
        if selected >= 0:
            self.list_ctrl.Select(selected, on=False)

    def _on_search(self, event) -> None:
        """Filtra la cartera en tiempo real."""
        self.presenter.search_personas(self.search_ctrl.GetValue())

    def _on_search_cancel(self, event) -> None:
        """Restaura la lista completa al limpiar la busqueda."""
        self.search_ctrl.SetValue("")
        self.presenter.load_personas()

    def _on_select_person(self, event) -> None:
        """Abre la ficha asociada a la fila seleccionada."""
        persona = self.get_selected_person()
        if persona is not None:
            self.presenter.select_persona(persona.id)

    def _on_new_person(self, event) -> None:
        """Inicia la creacion de una nueva persona."""
        self.presenter.create_new_persona()
