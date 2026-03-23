# 🚀 Guía de Ejecución Rápida

## La forma MÁS FÁCIL de ejecutar el proyecto

### ⭐ MÉTODO RECOMENDADO: Script Automático

Hemos creado scripts que hacen **TODO automáticamente** por ti.

---

## 🪟 Windows

### Opción A: Doble clic (MÁS FÁCIL)

1. Abre la carpeta del proyecto
2. Haz **doble clic** en `run.bat`
3. ¡Listo! Espera a que cargue todo automáticamente

### Opción B: Línea de comandos

```batch
cd "C:\Users\MARCOS MOREIRA\Downloads\Finanzas personales\finanzas_personales"
run.bat
```

### Opción C: Python universal

```batch
python run.py
```

---

## 🐧 Linux / 🍎 macOS

### Opción A: Doble clic (si tu sistema lo permite)

1. Haz clic derecho en `run.sh`
2. Selecciona "Ejecutar como programa"

### Opción B: Terminal

```bash
cd ~/Downloads/Finanzas\ personales/finanzas_personales
./run.sh
```

### Opción C: Python universal

```bash
python3 run.py
```

---

## 📋 ¿Qué hacen estos scripts?

```
┌─────────────────────────────────────┐
│  1. Verificar Python instalado     │
├─────────────────────────────────────┤
│  2. Crear entorno virtual          │
│     (si no existe)                 │
├─────────────────────────────────────┤
│  3. Activar entorno virtual        │
├─────────────────────────────────────┤
│  4. Instalar dependencias          │
│     (solo si faltan)               │
│     • wxPython                     │
│     • matplotlib                   │
│     • etc...                       │
├─────────────────────────────────────┤
│  5. Inicializar base de datos      │
│     (crear tablas y seeds)         │
├─────────────────────────────────────┤
│  6. 🚀 EJECUTAR APLICACIÓN         │
└─────────────────────────────────────┘
```

**⏱️ Tiempo estimado:**

- Primera vez: 5-10 minutos (instalación de dependencias)
- Siguientes veces: 5-10 segundos

---

## ⚡ Método Express (para desarrolladores)

Si ya tienes Python y quieres control total:

```bash
# 1. Ir al directorio
cd finanzas_personales

# 2. Crear entorno (solo primera vez)
python -m venv venv

# 3. Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 5. Ejecutar
python src/main.py
```

---

## 🐳 Alternativa: Docker (Próximamente)

```bash
# Construir imagen
docker build -t finanzas-personales .

# Ejecutar
docker run -v ./data:/app/data finanzas-personales
```

> **Nota:** El soporte Docker está planificado para versión 0.3.0

---

## 🛠️ Solución de Problemas

### Error: "Python no está instalado"

**Windows:**

1. Descarga Python desde https://python.org
2. **IMPORTANTE:** Marca "Add Python to PATH"
3. Reinicia la terminal

**Linux:**

```bash
sudo apt-get install python3 python3-venv
```

**Mac:**

```bash
brew install python3
```

---

### Error: "No se pudo instalar wxPython"

**Windows:**

1. Instala Visual C++ Redistributable:
   https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Reintenta el script

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install build-essential libgtk-3-dev
sudo apt-get install libwebkitgtk-3.0-dev
```

---

### Error: "No se encuentra el módulo src"

Asegúrate de estar en la carpeta correcta:

```bash
# Debes ver los archivos: run.bat, run.sh, src/, requirements.txt
ls  # Linux/Mac
dir # Windows
```

---

## 📝 Resumen de Comandos

| Sistema   | Método     | Comando                                          |
| --------- | ---------- | ------------------------------------------------ |
| Windows   | Automático | `run.bat` o `python run.py`                      |
| Windows   | Manual     | `venv\Scripts\activate && python src/main.py`    |
| Linux/Mac | Automático | `./run.sh` o `python3 run.py`                    |
| Linux/Mac | Manual     | `source venv/bin/activate && python src/main.py` |
| Todos     | Docker     | `docker run finanzas-personales` (próximamente)  |

---

## 🎯 Para la próxima vez

Una vez configurado, solo necesitas:

```bash
# Windows
run.bat

# Linux/Mac
./run.sh

# O en cualquier sistema
python run.py
```

¡Así de simple! 🎉

---

## 💡 Consejos

1. **Primera vez:** El script tardará 5-10 minutos instalando dependencias. ¡Se paciente!

2. **Permisos en Linux/Mac:** Si `run.sh` no ejecuta:

   ```bash
   chmod +x run.sh
   ```

3. **Atajo en Windows:** Crea un acceso directo a `run.bat` en tu escritorio

4. **Atajo en Linux:** Agrega un alias a tu `.bashrc`:
   ```bash
   alias finanzas='cd ~/ruta/al/proyecto && ./run.sh'
   ```

---

**¿Problemas?** Consulta la [Guía de Instalación Completa](INSTALACION.md)
