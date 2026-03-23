# 📦 Guía de Instalación

Esta guía te ayudará a instalar la aplicación "Finanzas Personales" en tu computadora, sin importar si usas **Windows**, **Linux** o **macOS**.

## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación en Windows](#instalación-en-windows)
3. [Instalación en Linux](#instalación-en-linux)
4. [Instalación en macOS](#instalación-en-macos)
5. [Solución de Problemas](#solución-de-problemas)

---

## 📋 Requisitos del Sistema

### Mínimos

- **Sistema Operativo**: Windows 7+, Linux (Ubuntu 18.04+), macOS 10.14+
- **Memoria RAM**: 2 GB
- **Espacio en disco**: 200 MB
- **Python**: 3.8 o superior (solo instalación desde código fuente)

### Recomendados

- **Sistema Operativo**: Windows 10/11, Ubuntu 20.04+, macOS 11+
- **Memoria RAM**: 4 GB
- **Espacio en disco**: 500 MB
- **Resolución de pantalla**: 1280x720 o superior

---

## 🪟 Instalación en Windows

### Opción 1: Instalador MSI (Recomendado)

1. **Descarga** el archivo `FinanzasPersonales-0.1.0-win64.msi`

2. **Ejecuta** el archivo descargado haciendo doble clic

3. **Sigue el asistente** de instalación:

   - Acepta los términos de licencia
   - Selecciona la carpeta de instalación (o deja la predeterminada)
   - Haz clic en "Instalar"

4. **Finaliza** y busca "Finanzas Personales" en el menú Inicio

### Opción 2: Ejecución Rápida del Proyecto

1. **Descarga** y descomprime el archivo del proyecto

2. **Abre** la carpeta del proyecto en el Explorador de archivos

3. **Ejecuta** `run.bat` haciendo doble clic

4. **Espera** mientras se crea el entorno y se instalan las dependencias (puede tardar varios minutos)

5. **Listo!** La aplicación abrirá directamente

### Opción 3: Instalación Manual desde Código Fuente

```cmd
:: 1. Descarga el proyecto
:: Descarga y descomprime el ZIP del proyecto

:: 2. Abre CMD o PowerShell en la carpeta del proyecto

:: 3. Crea entorno virtual
python -m venv venv

:: 4. Activa el entorno
venv\Scripts\activate

:: 5. Instala dependencias
pip install wxPython matplotlib numpy opencv-python Pillow

:: 6. Ejecuta
python src\main.py
```

---

## 🐧 Instalación en Linux

### Opción 1: Script de Instalación Automática (Recomendado)

1. **Descarga** y descomprime el proyecto

2. **Abre** una terminal en la carpeta del proyecto

3. **Ejecuta** el script de instalación:

```bash
chmod +x install.sh
./install.sh
```

4. **Sigue las instrucciones** en pantalla

5. **Ejecuta** desde el menú de aplicaciones o con:

```bash
finanzas-personales
```

### Opción 2: Instalación Manual (Ubuntu/Debian)

```bash
# 1. Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-dev
sudo apt-get install -y libgtk-3-dev libwebkitgtk-3.0-dev
sudo apt-get install -y libjpeg-dev libtiff-dev libgstreamer1.0-dev

# 2. Descargar el proyecto
cd ~/Descargas
git clone <url-del-repositorio>
cd finanzas_personales

# 3. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 4. Instalar dependencias de Python
pip install --upgrade pip

# wxPython puede tardar en compilar (10-30 minutos)
pip install wxPython

pip install matplotlib numpy opencv-python Pillow

# 5. Ejecutar
python src/main.py
```

### Opción 3: Instalación Manual (Fedora/RHEL)

```bash
# 1. Instalar dependencias del sistema
sudo dnf install -y python3-pip python3-virtualenv gcc-c++
sudo dnf install -y gtk3-devel webkitgtk3-devel
sudo dnf install -y libjpeg-turbo-devel libtiff-devel

# 2-5. Mismos pasos que Ubuntu (ver arriba)
```

### Opción 4: AppImage (Próximamente)

Descargará un único archivo ejecutable que funciona en cualquier distribución Linux sin necesidad de instalar dependencias.

---

## 🍎 Instalación en macOS

### Opción 1: Instalación Manual

```bash
# 1. Instalar Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependencias
brew install python3

# 3. Descargar el proyecto
cd ~/Downloads
git clone <url-del-repositorio>
cd finanzas_personales

# 4. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 5. Instalar dependencias
pip install --upgrade pip
pip install wxPython matplotlib numpy opencv-python Pillow

# 6. Ejecutar
python src/main.py
```

### Opción 2: Aplicación .app (Próximamente)

Descargar `FinanzasPersonales.app` y arrastrar a la carpeta Aplicaciones.

---

## 🔧 Solución de Problemas

### Windows

#### "Python no está instalado"

- Descarga Python desde https://python.org
- Durante la instalación, marca "Add Python to PATH"

#### "MSVCP140.dll no encontrado"

- Instala Visual C++ Redistributable:
  https://aka.ms/vs/17/release/vc_redist.x64.exe

#### La aplicación no inicia

1. Abre CMD en la carpeta del proyecto
2. Activa el entorno virtual: `venv\Scripts\activate`
3. Ejecuta: `python src\main.py`
4. Copia el error que aparezca

### Linux

#### Error al instalar wxPython

```bash
# Instalar dependencias de compilación
sudo apt-get install -y build-essential libgtk-3-dev
sudo apt-get install -y libwebkitgtk-3.0-dev libwebkitgtk-4.0-dev
sudo apt-get install -y libjpeg-dev libtiff-dev

# Intentar instalar nuevamente
pip install wxPython
```

#### "No module named 'wx'"

```bash
# Asegúrate de activar el entorno virtual
source venv/bin/activate

# Verificar instalación
python -c "import wx; print(wx.version())"
```

#### Error de display (en servidores sin GUI)

Esta aplicación requiere interfaz gráfica. No funcionará en servidores SSH sin X11 forwarding.

### macOS

#### "Aplicación descargada de internet no verificada"

1. Ve a Preferencias del Sistema > Seguridad y Privacidad
2. Haz clic en "Abrir de todas formas"

#### Error al importar wx

```bash
# Instalar con brew
brew install wxpython

# O usar pip con flags específicos
pip install --upgrade --no-cache-dir wxPython
```

---

## 📁 Ubicación de Datos

La aplicación guarda tus datos en estas ubicaciones:

| Sistema | Ubicación                                                      |
| ------- | -------------------------------------------------------------- |
| Windows | `%APPDATA%\FinanzasPersonales\finanzas.db`                     |
| Linux   | `~/.local/share/finanzas_personales/finanzas.db`               |
| macOS   | `~/Library/Application Support/FinanzasPersonales/finanzas.db` |

### ¿Cómo hacer backup?

Simplemente copia el archivo `finanzas.db` a una ubicación segura (USB, nube, etc.)

### ¿Cómo restaurar?

1. Cierra la aplicación
2. Copia tu archivo de backup a la ubicación correspondiente
3. Sobrescribe el archivo existente
4. Abre la aplicación

---

## ❓ Preguntas Frecuentes

**¿Puedo usar la aplicación sin internet?**
Sí, es una aplicación 100% offline. Tus datos se guardan localmente.

**¿Puedo instalarla en varias computadoras?**
Sí, puedes instalarla en todas las computadoras que quieras.

**¿Se pueden compartir los datos entre computadoras?**
Sí, copiando el archivo `finanzas.db` entre computadoras.

**¿Hay versión móvil?**
No, actualmente solo existe versión de escritorio.

**¿Cómo desinstalo la aplicación?**

- **Windows (MSI)**: Panel de Control > Programas > Desinstalar
- **Windows (script)**: Elimina la carpeta `%LOCALAPPDATA%\FinanzasPersonales`
- **Linux**: Elimina `~/.local/share/finanzas_personales_app`
- **macOS**: Arrastra la aplicación a la Papelera

---

## 🆘 ¿Necesitas más ayuda?

Si tienes problemas durante la instalación:

1. Revisa los logs de error en la consola/terminal
2. Consulta la sección de Solución de Problemas arriba
3. Abre un issue en el repositorio con:
   - Tu sistema operativo y versión
   - El mensaje de error completo
   - Los pasos que seguiste

---

**¡Listo para comenzar!** 🚀

Una vez instalada, consulta la guía de uso para aprender a utilizar todas las funciones.
