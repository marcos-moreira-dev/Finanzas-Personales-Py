#!/bin/bash
# Script de instalación para Linux/macOS
# Instala la aplicación Finanzas Personales

echo "=========================================="
echo "Instalador de Finanzas Personales"
echo "=========================================="
echo ""

# Detectar sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "Sistema detectado: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "Sistema detectado: macOS"
else
    echo "Sistema operativo no soportado: $OSTYPE"
    exit 1
fi

# Verificar Python
echo ""
echo "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oP '\d+\.\d+')
echo "Python encontrado: $PYTHON_VERSION"

# Verificar versión mínima (3.8)
REQUIRED_VERSION="3.8"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo "ERROR: Se requiere Python $REQUIRED_VERSION o superior"
    exit 1
fi

# Crear entorno virtual
echo ""
echo "Creando entorno virtual..."
INSTALL_DIR="$HOME/.local/share/finanzas_personales_app"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

if [ -d "venv" ]; then
    echo "El entorno virtual ya existe, usando existente..."
else
    $PYTHON_CMD -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo ""
echo "Instalando dependencias..."
pip install --upgrade pip

# Instalar wxPython (puede tardar en compilar)
echo "Instalando wxPython (esto puede tardar varios minutos)..."
pip install wxPython

# Instalar otras dependencias
echo "Instalando otras dependencias..."
pip install matplotlib numpy opencv-python Pillow

# Crear directorio de la aplicación
echo ""
echo "Configurando aplicación..."
APP_DIR="$INSTALL_DIR/app"
mkdir -p "$APP_DIR"

# Copiar archivos de la aplicación (asumiendo que están en el directorio actual)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -d "$SCRIPT_DIR/src" ]; then
    cp -r "$SCRIPT_DIR/src" "$APP_DIR/"
    cp -r "$SCRIPT_DIR/assets" "$APP_DIR/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/docs" "$APP_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR/README.md" "$APP_DIR/" 2>/dev/null || true
fi

# Crear script de lanzamiento
cat > "$INSTALL_DIR/finanzas-personales" << 'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.local/share/finanzas_personales_app"
cd "$INSTALL_DIR/app"
source "$INSTALL_DIR/venv/bin/activate"
python src/main.py
EOF

chmod +x "$INSTALL_DIR/finanzas-personales"

# Crear acceso directo en el escritorio
DESKTOP_DIR="$HOME/Desktop"
if [ -d "$DESKTOP_DIR" ]; then
    cat > "$DESKTOP_DIR/FinanzasPersonales.desktop" << EOF
[Desktop Entry]
Name=Finanzas Personales
Comment=Aplicación para gestionar finanzas personales
Exec=$INSTALL_DIR/finanzas-personales
Icon=$INSTALL_DIR/app/assets/icons/app_icon.png
Terminal=false
Type=Application
Categories=Office;Finance;
EOF
    chmod +x "$DESKTOP_DIR/FinanzasPersonales.desktop"
    echo "Acceso directo creado en el escritorio"
fi

# Agregar al PATH
echo ""
echo "Agregando al PATH..."
SHELL_RC=""
if [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "finanzas_personales_app" "$SHELL_RC"; then
        echo '' >> "$SHELL_RC"
        echo '# Finanzas Personales' >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/share/finanzas_personales_app:$PATH"' >> "$SHELL_RC"
        echo "Agregado a $SHELL_RC"
    fi
fi

echo ""
echo "=========================================="
echo "¡Instalación completada!"
echo "=========================================="
echo ""
echo "Para ejecutar la aplicación:"
echo "  - Desde terminal: finanzas-personales"
echo "  - Desde el menú de aplicaciones"
echo "  - Desde el escritorio (acceso directo)"
echo ""
echo "Datos se guardarán en: ~/.local/share/finanzas_personales"
echo ""

# Preguntar si desea ejecutar ahora
read -p "¿Desea ejecutar la aplicación ahora? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    "$INSTALL_DIR/finanzas-personales"
fi
