#!/bin/bash
# Script Maestro - Ejecuta TODO automáticamente
# Uso: ./run.sh

set -e  # Detenerse si hay error

echo "=========================================="
echo " FINANZAS PERSONALES - LANZADOR AUTOMATICO"
echo "=========================================="
echo ""

# Detectar Python
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python no esta instalado"
    echo "Instala con: sudo apt-get install python3 python3-venv"
    exit 1
fi

echo "[1/5] Python detectado: $($PYTHON_CMD --version)"

# Crear entorno virtual si no existe
echo ""
echo "[2/5] Verificando entorno virtual..."
if [ ! -d "venv" ]; then
    echo "    Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
fi
echo "    ✓ Entorno virtual listo"

# Activar entorno virtual
echo ""
echo "[3/5] Activando entorno..."
source venv/bin/activate
echo "    ✓ Entorno activado"

# Verificar/Instalar dependencias
echo ""
echo "[4/5] Verificando dependencias..."
if python -c "import wx" 2>/dev/null; then
    echo "    ✓ Dependencias ya instaladas"
else
    echo "    Instalando dependencias (esto puede tardar varios minutos)..."
    pip install -r requirements.txt
fi

# Inicializar base de datos
echo ""
echo "[5/5] Inicializando base de datos..."
python -c "
from src.infrastructure.db.database import Database
from src.infrastructure.config.settings import Config
import os
os.makedirs(Config.DATA_DIR, exist_ok=True)
db = Database(str(Config.DB_PATH))
db.init_schema()
print('    ✓ Base de datos lista')
"

echo ""
echo "=========================================="
echo " 🚀 INICIANDO APLICACION..."
echo "=========================================="
echo ""

# Ejecutar aplicacion
python src/main.py

echo ""
echo "=========================================="
echo " 👋 Aplicacion cerrada"
echo "=========================================="
