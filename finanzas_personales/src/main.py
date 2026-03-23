"""Punto de entrada principal de la aplicacion."""

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.shared.logging_config import LogContext, configure_logging, get_logger


# El logging se configura antes de importar la UI para capturar cualquier
# fallo temprano de arranque con el mismo formato y destino.
configure_logging(
    level="DEBUG",
    console_output=True,
    json_format=False,
    max_bytes=10 * 1024 * 1024,
    backup_count=5,
)

logger = get_logger(__name__)

logger.info("=" * 60)
logger.info("FINANZAS PERSONALES - Iniciando aplicacion")
logger.info("=" * 60)

from src.shared.matplotlib_config import configure_matplotlib
from src.shared.platform_config import configure_platform, configure_wx_app

import wx
from src.infrastructure.db.database import Database
from src.infrastructure.db.seeds import ejecutar_seeds
from src.presentation.views.main_window import MainWindow


class ApplicationBootstrap:
    """Coordina el arranque completo de la aplicacion."""

    def __init__(self) -> None:
        self.db_path: Path | None = None
        self.app: wx.App | None = None
        self.main_frame: MainWindow | None = None
        logger.debug("ApplicationBootstrap inicializado")

    def get_data_directory(self) -> Path:
        """Calcula el directorio de datos local segun la plataforma."""
        logger.debug("Detectando directorio de datos...")

        if sys.platform == "win32":
            app_data = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
            data_dir = app_data / "FinanzasPersonales"
            logger.debug("Windows detectado: %s", data_dir)
        elif sys.platform == "darwin":
            data_dir = Path.home() / "Library/Application Support/FinanzasPersonales"
            logger.debug("macOS detectado: %s", data_dir)
        else:
            xdg_data = os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
            data_dir = Path(xdg_data) / "finanzas_personales"
            logger.debug("Linux/Unix detectado: %s", data_dir)

        data_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Directorio de datos: %s", data_dir)
        return data_dir

    def initialize_database(self) -> bool:
        """Crea la base local, inicializa el esquema y ejecuta seeds base."""
        with LogContext(phase="database_initialization"):
            logger.info("Paso 1/4: Inicializando base de datos...")

            try:
                data_dir = self.get_data_directory()
                self.db_path = data_dir / "finanzas.db"
                logger.debug("Ruta de BD: %s", self.db_path)

                with Database(str(self.db_path)) as db:
                    logger.debug("Creando esquema de base de datos...")
                    db.init_schema()

                    logger.debug("Cargando seeds de categorias...")
                    stats = ejecutar_seeds(db.get_connection())

                logger.info("Base de datos lista")
                logger.info("  - Version de seeds: %s", stats["version"])
                logger.info("  - Categorias creadas: %s", stats["ejecutados"])
                logger.info("  - Categorias existentes: %s", stats["omitidos"])

                if stats["errores"]:
                    logger.warning("Errores en seeds: %s", stats["errores"])

                logger.info("Paso 1/4: COMPLETADO - BD: %s", self.db_path)
                return True

            except Exception:
                logger.error("Error inicializando base de datos", exc_info=True)
                raise

    def create_wx_app(self) -> bool:
        """Configura wxPython y la integracion visual de la plataforma."""
        with LogContext(phase="wx_app_creation"):
            logger.info("Paso 2/4: Creando aplicacion wxPython...")

            try:
                # La plataforma se configura antes de crear wx.App porque ahi
                # viven ajustes como DPI awareness y estilos nativos.
                logger.debug("Configurando DPI awareness...")
                configure_platform()

                self.app = wx.App(False)
                self.app.SetAppName("Finanzas Personales")
                self.app.SetVendorName("Usuario")

                logger.debug("Verificando fuente del sistema...")
                configure_wx_app(self.app)

                logger.debug("Configurando matplotlib...")
                configure_matplotlib()

                logger.info("Paso 2/4: COMPLETADO - wx.App creado")
                return True

            except Exception:
                logger.error("Error creando aplicacion wxPython", exc_info=True)
                raise

    def create_main_window(self) -> bool:
        """Construye y muestra la ventana principal."""
        with LogContext(phase="main_window_creation"):
            logger.info("Paso 3/4: Creando ventana principal...")

            try:
                self.main_frame = MainWindow(None, title="Finanzas Personales")
                self.main_frame.Show()

                logger.info("Paso 3/4: COMPLETADO - Ventana principal creada")
                return True

            except Exception:
                logger.error("Error creando ventana principal", exc_info=True)
                raise

    def run(self) -> None:
        """Ejecuta el loop principal de wxPython."""
        with LogContext(phase="main_loop"):
            logger.info("Paso 4/4: Iniciando loop de eventos...")
            logger.info("Aplicacion lista. Cierre la ventana para salir.")
            logger.info("-" * 60)

            try:
                assert self.app is not None
                self.app.MainLoop()
                logger.info("Loop de eventos finalizado")

            except Exception:
                logger.error("Error en loop de eventos", exc_info=True)
                raise

    def bootstrap(self) -> bool:
        """Ejecuta la secuencia completa de arranque."""
        try:
            # El orden importa: la ventana depende de la app wx y la app wx
            # depende de que la base y la configuracion ya esten listas.
            self.initialize_database()
            self.create_wx_app()
            self.create_main_window()
            self.run()
            return True

        except Exception as exc:
            logger.critical("Error fatal durante arranque: %s", exc, exc_info=True)
            return False


def show_error_dialog(message: str, title: str = "Error") -> None:
    """Muestra un error con wx si esta disponible o hace fallback a consola."""
    logger.error("Mostrando dialogo de error: %s", title)

    try:
        app = wx.App.Get()
        if app is None:
            app = wx.App(False)

        wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR)
    except Exception:
        print(f"\n{'=' * 60}")
        print(f"ERROR: {title}")
        print(f"{'=' * 60}")
        print(message)
        print(f"{'=' * 60}\n")


def main() -> None:
    """Punto de entrada invocado por scripts y ejecucion directa."""
    # Mantener main corto deja el flujo de arranque facil de seguir.
    bootstrap = ApplicationBootstrap()
    success = bootstrap.bootstrap()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
