"""
Design Tokens - Finanzas Personales

Sistema de diseño programático para mantener consistencia visual.
Tamaños ajustados para nitidez en pantallas modernas (96-144 DPI).

Uso:
    >>> from src.shared.design_tokens import COLORS, DIMENSIONS, FONTS
    >>> panel.SetBackgroundColour(COLORS['panel_bg'])
    >>> button.SetMinSize((DIMENSIONS['button_min_width'], DIMENSIONS['button_height']))
"""

# ============================================================================
# PALETA DE COLORES
# ============================================================================

COLORS = {
    # Fondos principales
    'window_bg': '#F0F0F0',        # Fondo ventana principal (gris clásico Windows)
    'panel_bg': '#FFFFFF',          # Fondo paneles/contenido
    'dialog_bg': '#F5F5F5',         # Fondo diálogos
    
    # Bordes y separadores
    'border': '#C0C0C0',           # Bordes generales
    'border_light': '#E0E0E0',     # Bordes sutiles
    'border_dark': '#808080',      # Bordes oscuros (efecto 3D)
    'divider': '#D0D0D0',          # Líneas divisorias
    
    # Texto
    'text_primary': '#000000',      # Texto principal (máximo contraste)
    'text_secondary': '#333333',    # Texto secundario
    'text_muted': '#666666',        # Texto deshabilitado/atenuado
    'text_disabled': '#999999',     # Texto no editable
    'text_inverse': '#FFFFFF',      # Texto sobre fondos oscuros
    
    # Primario (Azul corporativo)
    'primary': '#2E5C8A',          # Azul principal
    'primary_hover': '#3D7AB5',     # Hover botones
    'primary_active': '#1E3D5C',    # Click/Active
    'primary_light': '#E3F2FD',     # Fondo selección ligera
    'primary_dark': '#1A3A5C',      # Azul muy oscuro
    
    # Secundario (Gris)
    'secondary': '#E0E0E0',        # Botones secundarios
    'secondary_hover': '#D0D0D0',   # Hover secundario
    'secondary_active': '#BDBDBD',  # Active secundario
    
    # Éxito/Ingresos (Verde)
    'success': '#2E7D32',          # Verde éxito
    'success_light': '#E8F5E9',     # Fondo éxito
    'success_dark': '#1B5E20',      # Verde oscuro
    'success_text': '#1B5E20',      # Texto verde
    
    # Error/Gastos (Rojo)
    'error': '#C62828',            # Rojo error
    'error_light': '#FFEBEE',       # Fondo error
    'error_dark': '#B71C1C',        # Rojo oscuro
    'error_text': '#C62828',        # Texto error
    
    # Advertencia (Amarillo/Ámbar)
    'warning': '#F9A825',          # Amarillo advertencia
    'warning_light': '#FFFDE7',     # Fondo advertencia
    'warning_dark': '#F57F17',      # Amarillo oscuro
    'warning_text': '#F57F17',      # Texto advertencia
    
    # Información (Azul claro)
    'info': '#0288D1',             # Azul info
    'info_light': '#E1F5FE',        # Fondo info
    
    # Tablas
    'table_header': '#E8E8E8',     # Header tabla
    'table_row_odd': '#FFFFFF',     # Fila impar
    'table_row_even': '#F8F8F8',    # Fila par
    'table_hover': '#E3F2FD',       # Hover fila
    'table_selected': '#2E5C8A',    # Fila seleccionada
    'table_selected_text': '#FFFFFF', # Texto fila seleccionada
    'table_border': '#D0D0D0',      # Bordes tabla
    
    # Estado de campos
    'input_bg': '#FFFFFF',          # Fondo input normal
    'input_border': '#C0C0C0',      # Borde input
    'input_focus': '#2E5C8A',       # Borde input focus
    'input_error': '#C62828',       # Borde input error
    'input_error_bg': '#FFEBEE',    # Fondo input error
    'input_disabled': '#F5F5F5',    # Fondo input deshabilitado
    
    # Toolbar y menú
    'toolbar_bg': '#F0F0F0',        # Fondo toolbar
    'menu_bg': '#FFFFFF',           # Fondo menú
    'menu_hover': '#E3F2FD',        # Hover menú
    'menu_selected': '#2E5C8A',     # Seleccionado menú
    
    # Status bar
    'statusbar_bg': '#F0F0F0',      # Fondo status bar
    'statusbar_text': '#333333',    # Texto status bar
    
    # Misceláneos
    'shadow': '#000000',           # Sombra (con alpha)
    'overlay': 'rgba(0,0,0,0.5)',  # Overlay modal
}

# ============================================================================
# DIMENSIONES Y ESPACIADO
# ============================================================================

DIMENSIONS = {
    # Ventana principal
    'window_min_width': 900,
    'window_min_height': 600,
    'window_default_width': 1280,
    'window_default_height': 860,
    'window_max_width': 1920,
    'window_max_height': 1080,
    
    # Paneles
    'sidebar_width': 320,
    'sidebar_min_width': 220,
    'sidebar_max_width': 400,
    'main_area_min_width': 500,
    
    # Barras
    'toolbar_height': 44,          # era 36
    'menubar_height': 26,          # era 24
    'statusbar_height': 26,        # era 24
    'tabbar_height': 30,           # era 28
    
    # Elementos de formulario
    'button_height': 34,           # era 24
    'button_min_width': 104,       # era 80
    'button_padding_horizontal': 18,
    'input_height': 30,            # era 22
    'input_padding_horizontal': 8,
    'dropdown_height': 28,         # era 24
    'textarea_min_height': 80,
    
    # Tabla
    'table_row_height': 28,        # era 24
    'table_header_height': 30,     # era 28
    'table_padding_horizontal': 8,
    
    # Lista
    'list_item_height': 34,        # era 28
    'list_padding': 10,
    
    # Tarjetas/Contenedores
    'card_padding': 16,
    'card_border_radius': 0,
    'card_shadow': 0,
    
    # Iconos
    'icon_size_small': 16,
    'icon_size_medium': 24,
    'icon_size_large': 32,
    
    # Espaciado (escala 4px)
    'space_0': 0,
    'space_1': 4,    # xs
    'space_2': 8,    # sm
    'space_3': 12,   # md-sm
    'space_4': 16,   # md
    'space_5': 20,
    'space_6': 24,   # lg
    'space_8': 32,   # xl
    'space_10': 40,
    'space_12': 48,  # xxl
    'space_16': 64,
}

# Alias para espaciado (más descriptivos)
SPACING = {
    'xs': DIMENSIONS['space_1'],   # 4px
    'sm': DIMENSIONS['space_2'],   # 8px
    'md': DIMENSIONS['space_4'],   # 16px
    'lg': DIMENSIONS['space_6'],   # 24px
    'xl': DIMENSIONS['space_8'],   # 32px
    'xxl': DIMENSIONS['space_12'], # 48px
}

# ============================================================================
# TIPOGRAFÍA
# ============================================================================

FONTS = {
    # Familias por sistema operativo
    'family_windows': 'Segoe UI',
    'family_linux': 'DejaVu Sans',
    'family_mac': 'Helvetica Neue',
    'family_fallback': 'sans-serif',
    
    # Tamaños (ajustados para legibilidad en 96-144 DPI)
    'size_window_title': 14,       # Título ventana
    'size_panel_title': 12,        # Título panel
    'size_section': 11,            # Subtítulo sección
    'size_normal': 10,             # Texto normal (era 9)
    'size_small': 9,               # Texto pequeño (era 8)
    'size_table': 10,              # Datos tabla (era 9)
    'size_monospace': 10,          # Números/monospace (era 9)
    
    # Pesos
    'weight_normal': 'normal',
    'weight_bold': 'bold',
    
    # Estilos
    'style_normal': 'normal',
    'style_italic': 'italic',
}

# ============================================================================
# BORDES Y EFECTOS
# ============================================================================

BORDERS = {
    # Grosores
    'width_thin': 1,
    'width_normal': 1,
    'width_thick': 2,
    
    # Estilos clásicos (3D)
    'raised': {
        'highlight': '#FFFFFF',     # Borde claro arriba/izq
        'shadow': '#808080',        # Borde oscuro abajo/der
    },
    'sunken': {
        'shadow': '#808080',        # Borde oscuro arriba/izq
        'highlight': '#FFFFFF',     # Borde claro abajo/der
    },
}

# ============================================================================
# Z-INDEX / ORDEN DE APILAMIENTO
# ============================================================================

Z_INDEX = {
    'background': 0,
    'content': 10,
    'sidebar': 20,
    'toolbar': 30,
    'modal': 100,
    'tooltip': 200,
    'dropdown': 150,
}

# ============================================================================
# DURACIONES Y TRANSICIONES
# ============================================================================

# Nota: En wxPython (UI nativa) no usamos CSS transitions,
# pero definimos tiempos para feedback visual

TIMING = {
    'instant': 0,
    'fast': 100,      # ms
    'normal': 200,    # ms
    'slow': 300,      # ms
    'very_slow': 500, # ms
}

# ============================================================================
# ICONOS Y EMOJIS (Mapeo para wxPython)
# ============================================================================

ICONS = {
    # Acciones generales
    'save': '\U0001F4BE',        # 💾
    'edit': '\U0001F58A',        # 🖊️
    'delete': '\U0001F5D1',      # 🗑️
    'add': '\U00002795',         # ➕
    'remove': '\U00002796',      # ➖
    'search': '\U0001F50D',      # 🔍
    'close': '\U0000274C',       # ❌
    'back': '\U00002B05',        # ⬅️
    'next': '\U000027A1',        # ➡️
    'up': '\U00002B06',          # ⬆️
    'down': '\U00002B07',        # ⬇️
    'refresh': '\U0001F504',     # 🔄
    'settings': '\U00002699',    # ⚙️
    'help': '\U00002753',        # ❓
    'info': '\U00002139',        # ℹ️
    'warning': '\U000026A0',     # ⚠️
    'error': '\U0000274C',       # ❌
    'success': '\U00002705',     # ✅
    
    # Financieros
    'money': '\U0001F4B0',       # 💰
    'money_bag': '\U0001F4B5',   # 💵
    'money_wings': '\U0001F4B8', # 💸
    'credit_card': '\U0001F4B3', # 💳
    'bank': '\U0001F3E6',        # 🏦
    'chart': '\U0001F4C8',       # 📈
    'chart_down': '\U0001F4C9',  # 📉
    'chart_bar': '\U0001F4CA',   # 📊
    'receipt': '\U0001F9FE',     # 🧾
    'invoice': '\U0001F5F6',     # 🗶
    
    # Usuario
    'user': '\U0001F464',        # 👤
    'users': '\U0001F465',       # 👥
    'person': '\U0001F9D1',      # 🧑
    'photo': '\U0001F4F7',       # 📷
    'camera': '\U0001F4F8',      # 📸
    
    # Categorías - Ingresos
    'briefcase': '\U0001F4BC',   # 💼 (Sueldo)
    'laptop': '\U0001F4BB',      # 💻 (Freelance)
    'trend_up': '\U0001F4C8',    # 📈 (Inversiones)
    'cart': '\U0001F6D2',        # 🛒 (Ventas)
    'gift': '\U0001F381',        # 🎁 (Regalos)
    'undo': '\U000021A9',        # ↩️ (Reembolsos)
    
    # Categorías - Gastos
    'utensils': '\U0001F374',    # 🍽️ (Alimentación)
    'car': '\U0001F697',         # 🚗 (Transporte)
    'home': '\U0001F3E0',        # 🏠 (Vivienda)
    'medical': '\U0001F3E5',     # 🏥 (Salud)
    'books': '\U0001F4DA',       # 📚 (Educación)
    'film': '\U0001F3AC',        # 🎬 (Entretenimiento)
    'shirt': '\U0001F455',       # 👕 (Ropa)
    'computer': '\U0001F4BB',    # 💻 (Tecnología)
    'paw': '\U0001F43E',         # 🐾 (Mascotas)
    'plane': '\U00002708',       # ✈️ (Viajes)
    'piggy_bank': '\U0001F4B0',  # 💰 (Ahorro)
    'receipt_tax': '\U0001F9FE', # 🧾 (Impuestos)
    'shield': '\U0001F6E1',      # 🛡️ (Seguros)
    'page': '\U0001F4C4',        # 📄 (Otros)
    
    # Tipos de transacción
    'arrow_up': '\U00002B06',    # ⬆️ (Ingreso)
    'arrow_down': '\U00002B07',  # ⬇️ (Gasto)
    'transfer': '\U0001F500',    # 🔀 (Transferencia)
}

# ============================================================================
# MAPA DE CATEGORÍAS A ICONOS
# ============================================================================

CATEGORY_ICONS = {
    # Ingresos
    'Sueldo': ICONS['briefcase'],
    'Freelance': ICONS['laptop'],
    'Inversiones': ICONS['trend_up'],
    'Ventas': ICONS['cart'],
    'Regalos': ICONS['gift'],
    'Reembolsos': ICONS['undo'],
    'Otros Ingresos': ICONS['money'],
    
    # Gastos
    'Alimentación': ICONS['utensils'],
    'Transporte': ICONS['car'],
    'Vivienda': ICONS['home'],
    'Salud': ICONS['medical'],
    'Educación': ICONS['books'],
    'Entretenimiento': ICONS['film'],
    'Ropa': ICONS['shirt'],
    'Tecnología': ICONS['computer'],
    'Mascotas': ICONS['paw'],
    'Viajes': ICONS['plane'],
    'Ahorro': ICONS['piggy_bank'],
    'Impuestos': ICONS['receipt_tax'],
    'Seguros': ICONS['shield'],
    'Otros Gastos': ICONS['page'],
    
    # Ambos
    'Transferencias': ICONS['transfer'],
}

# ============================================================================
# FUNCIONES UTILITARIAS
# ============================================================================

def get_color_with_contrast(background_color: str, threshold: float = 4.5) -> str:
    """
    Retorna color de texto (negro o blanco) que tenga suficiente contraste
    con el color de fondo dado.
    
    Args:
        background_color: Color de fondo en hex (#RRGGBB)
        threshold: Ratio mínimo de contraste
        
    Returns:
        '#000000' o '#FFFFFF' según contraste
    """
    # Convertir hex a RGB
    bg = background_color.lstrip('#')
    r, g, b = tuple(int(bg[i:i+2], 16) for i in (0, 2, 4))
    
    # Calcular luminancia relativa
    def luminance(rgb):
        r, g, b = rgb
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0
        
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    bg_lum = luminance((r, g, b))
    
    # Contraste con negro y blanco
    black_lum = 0
    white_lum = 1
    
    contrast_black = (bg_lum + 0.05) / (black_lum + 0.05) if bg_lum > black_lum else (black_lum + 0.05) / (bg_lum + 0.05)
    contrast_white = (white_lum + 0.05) / (bg_lum + 0.05) if white_lum > bg_lum else (bg_lum + 0.05) / (white_lum + 0.05)
    
    return '#000000' if contrast_black >= threshold else '#FFFFFF'


def hex_to_wxcolour(hex_color: str):
    """
    Convierte color hex a wx.Colour.
    
    Args:
        hex_color: String tipo '#RRGGBB'
        
    Returns:
        wx.Colour
    """
    import wx
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return wx.Colour(r, g, b)


# ============================================================================
# VALIDACIÓN WCAG
# ============================================================================

def check_contrast(color1: str, color2: str) -> float:
    """
    Calcula ratio de contraste entre dos colores.
    
    Args:
        color1: Primer color en hex
        color2: Segundo color en hex
        
    Returns:
        Ratio de contraste (ej: 4.5, 7.2, 21.0)
        
    Example:
        >>> check_contrast('#000000', '#FFFFFF')  # 21.0 (AAA)
        >>> check_contrast('#2E5C8A', '#FFFFFF')  # 7.2 (AA)
    """
    def luminance(hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        rgb = [r / 255.0, g / 255.0, b / 255.0]
        for i in range(3):
            if rgb[i] <= 0.03928:
                rgb[i] = rgb[i] / 12.92
            else:
                rgb[i] = ((rgb[i] + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    
    lum1 = luminance(color1)
    lum2 = luminance(color2)
    
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    
    return (lighter + 0.05) / (darker + 0.05)


def validate_wcag_compliance() -> dict:
    """
    Valida que todos los colores cumplan WCAG 2.1 AA.
    
    Returns:
        Dict con resultados de validación
    """
    results = {
        'passed': [],
        'warnings': [],
        'failed': []
    }
    
    # Combinaciones críticas a validar
    combinations = [
        ('text_primary', 'panel_bg', 4.5, 'Texto normal'),
        ('text_secondary', 'panel_bg', 4.5, 'Texto secundario'),
        ('text_inverse', 'primary', 4.5, 'Texto sobre primario'),
        ('success_text', 'success_light', 4.5, 'Texto éxito'),
        ('error_text', 'error_light', 4.5, 'Texto error'),
    ]
    
    for text_key, bg_key, threshold, description in combinations:
        contrast = check_contrast(COLORS[text_key], COLORS[bg_key])
        
        if contrast >= 7.0:
            results['passed'].append(f"{description}: {contrast:.1f}:1 (AAA)")
        elif contrast >= threshold:
            results['passed'].append(f"{description}: {contrast:.1f}:1 (AA)")
        elif contrast >= 3.0:
            results['warnings'].append(f"{description}: {contrast:.1f}:1 (A, necesita AA)")
        else:
            results['failed'].append(f"{description}: {contrast:.1f}:1 (NO CUMPLE)")
    
    return results


# Ejecutar validación al importar
if __name__ == '__main__':
    print("Validando cumplimiento WCAG 2.1 AA...")
    results = validate_wcag_compliance()
    
    print("\n✅ APROBADOS:")
    for item in results['passed']:
        print(f"  ✓ {item}")
    
    if results['warnings']:
        print("\n⚠️ ADVERTENCIAS:")
        for item in results['warnings']:
            print(f"  ⚠ {item}")
    
    if results['failed']:
        print("\n❌ FALLOS:")
        for item in results['failed']:
            print(f"  ✗ {item}")
    
    print("\nTokens de diseño cargados correctamente.")
