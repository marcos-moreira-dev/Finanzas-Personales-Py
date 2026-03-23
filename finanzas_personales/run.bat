@echo off
:: Script Maestro - Ejecuta TODO automáticamente
:: Uso: simplemente hacer doble clic en este archivo

:: Configurar UTF-8 para caracteres especiales
chcp 65001 >nul

:: Cambiar a directorio del script
cd /d "%~dp0"

echo ==========================================
echo  FINANZAS PERSONALES - LANZADOR AUTOMATICO
echo ==========================================
echo.

:: Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Descarga desde: https://python.org
    echo.
    pause
    exit /b 1
)
echo     OK - Python detectado

:: Crear entorno virtual si no existe
echo.
echo [2/5] Verificando entorno virtual...
if not exist "venv" (
    echo     Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)
echo     OK - Entorno virtual listo

:: Activar entorno virtual
echo.
echo [3/5] Activando entorno...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno
    pause
    exit /b 1
)
echo     OK - Entorno activado

:: Verificar/Instalar dependencias
echo.
echo [4/5] Verificando dependencias...
python -c "import wx" >nul 2>&1
if errorlevel 1 (
    echo     Instalando dependencias. Puede tardar 5-10 minutos...
    echo     Por favor espera...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Fallo la instalacion de dependencias
        pause
        exit /b 1
    )
) else (
    echo     OK - Dependencias ya instaladas
)

:: Inicializar base de datos
echo.
echo [5/5] Inicializando base de datos...
python -c "from src.infrastructure.db.database import Database; from src.infrastructure.config.settings import Config; db = Database(str(Config.DB_PATH)); db.init_schema(); print('OK - Base de datos lista')"

echo.
echo ==========================================
echo  >> INICIANDO APLICACION...
echo ==========================================
echo.

:: Ejecutar aplicacion
python src\main.py

:: Si llega aqui, la app se cerro
echo.
echo ==========================================
echo  >> Aplicacion cerrada
echo ==========================================
pause
