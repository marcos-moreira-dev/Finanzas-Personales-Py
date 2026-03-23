"""
Módulo de Cámara - Captura de Fotos para Perfil

Utiliza OpenCV para captura de video y selección de fotos.
Compatible con Windows, Linux y macOS.

Uso:
    >>> from src.infrastructure.camera.camera_capture import CameraCapture
    >>> camera = CameraCapture()
    >>> photo_path = camera.capture_photo(persona_id=1)
"""
import os
import cv2
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from ...infrastructure.config.settings import Config

logger = logging.getLogger(__name__)


class CameraCapture:
    """
    Gestiona la captura de fotos desde webcam.
    
    Features:
    - Preview en tiempo real
    - Captura con contador
    - Guardado automático en directorio configurado
    - Redimensión opcional
    - Múltiples formatos (JPG, PNG)
    """
    
    def __init__(self):
        """Inicializa el capturador de cámara."""
        self.photos_dir = Config.PHOTOS_DIR
        self.photos_dir.mkdir(parents=True, exist_ok=True)
        
        self.camera = None
        self.is_preview_active = False
        
        logger.info("CameraCapture inicializado")
    
    def is_camera_available(self) -> bool:
        """
        Verifica si hay una cámara disponible.
        
        Returns:
            True si hay cámara, False si no
        """
        try:
            # Intentar abrir cámara 0 (default)
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                cap.release()
                return True
            return False
        except Exception as e:
            logger.error(f"Error verificando cámara: {e}")
            return False
    
    def list_cameras(self) -> list:
        """
        Lista todas las cámaras disponibles.
        
        Returns:
            Lista de índices de cámaras disponibles
        """
        available = []
        for i in range(5):  # Verificar primeras 5 cámaras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available.append(i)
                cap.release()
        
        logger.info(f"Cámaras disponibles: {available}")
        return available
    
    def capture_photo(
        self,
        persona_id: int,
        filename: Optional[str] = None,
        format: str = "jpg",
        size: tuple = (400, 400)
    ) -> Optional[str]:
        """
        Captura una foto desde la cámara.
        
        Muestra preview y permite al usuario tomar la foto
        presionando ESPACIO o clic en botón.
        
        Args:
            persona_id: ID de la persona para la foto
            filename: Nombre de archivo opcional
            format: Formato de imagen (jpg, png)
            size: Tamaño de la imagen (ancho, alto)
            
        Returns:
            Ruta al archivo guardado, o None si falló
        """
        if not self.is_camera_available():
            logger.error("No hay cámara disponible")
            return None
        
        try:
            # Abrir cámara
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                logger.error("No se pudo abrir la cámara")
                return None
            
            # Configurar resolución
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            logger.info("Cámara abierta. Mostrando preview...")
            
            # Crear ventana de preview
            window_name = "Captura de Foto - Presione ESPACIO para tomar, ESC para cancelar"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 640, 520)
            
            photo_taken = False
            frame_captured = None
            
            while True:
                # Leer frame
                ret, frame = self.camera.read()
                
                if not ret:
                    logger.error("Error leyendo frame de cámara")
                    break
                
                # Agregar instrucciones en pantalla
                instructions = [
                    "ESPACIO: Tomar foto",
                    "ESC: Cancelar",
                    "S: Cambiar tamano"
                ]
                
                y_pos = 30
                for instruction in instructions:
                    cv2.putText(
                        frame,
                        instruction,
                        (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2
                    )
                    y_pos += 25
                
                # Mostrar frame
                cv2.imshow(window_name, frame)
                
                # Esperar tecla
                key = cv2.waitKey(1) & 0xFF
                
                if key == 27:  # ESC - Cancelar
                    logger.info("Captura cancelada por usuario")
                    break
                    
                elif key == 32:  # ESPACIO - Tomar foto
                    frame_captured = frame.copy()
                    photo_taken = True
                    logger.info("Foto capturada")
                    break
                
                elif key == ord('s') or key == ord('S'):  # Cambiar tamaño
                    # Toggle entre tamaños
                    if size == (400, 400):
                        size = (600, 600)
                    else:
                        size = (400, 400)
                    logger.info(f"Tamano cambiado a: {size}")
            
            # Cerrar ventana
            cv2.destroyWindow(window_name)
            
            if photo_taken and frame_captured is not None:
                # Generar nombre de archivo
                if filename is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"persona_{persona_id}_{timestamp}.{format}"
                
                # Guardar foto
                filepath = self._save_photo(
                    frame_captured,
                    filename,
                    format,
                    size
                )
                
                if filepath:
                    logger.info(f"Foto guardada: {filepath}")
                    return filepath
            
            return None
            
        except Exception as e:
            logger.error(f"Error capturando foto: {e}", exc_info=True)
            return None
            
        finally:
            # Liberar cámara
            if self.camera:
                self.camera.release()
                self.camera = None
            
            # Cerrar todas las ventanas
            cv2.destroyAllWindows()
    
    def _save_photo(
        self,
        frame,
        filename: str,
        format: str,
        size: tuple
    ) -> Optional[str]:
        """
        Guarda el frame capturado como archivo de imagen.
        
        Args:
            frame: Frame de OpenCV
            filename: Nombre del archivo
            format: Formato (jpg, png)
            size: Tamaño final (ancho, alto)
            
        Returns:
            Ruta completa al archivo
        """
        try:
            # Redimensionar
            resized = cv2.resize(frame, size)
            
            # Ruta completa
            filepath = self.photos_dir / filename
            
            # Guardar
            success = cv2.imwrite(str(filepath), resized)
            
            if success:
                return str(filepath)
            else:
                logger.error("Error guardando imagen")
                return None
                
        except Exception as e:
            logger.error(f"Error guardando foto: {e}")
            return None
    
    def load_existing_photo(self, photo_path: str) -> Optional[object]:
        """
        Carga una foto existente para mostrar.
        
        Args:
            photo_path: Ruta a la foto
            
        Returns:
            Imagen de OpenCV o None
        """
        try:
            if not os.path.exists(photo_path):
                return None
            
            image = cv2.imread(photo_path)
            return image
            
        except Exception as e:
            logger.error(f"Error cargando foto: {e}")
            return None
    
    def delete_photo(self, photo_path: str) -> bool:
        """
        Elimina una foto del sistema.
        
        Args:
            photo_path: Ruta a la foto
            
        Returns:
            True si se eliminó, False si no
        """
        try:
            if os.path.exists(photo_path):
                os.remove(photo_path)
                logger.info(f"Foto eliminada: {photo_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error eliminando foto: {e}")
            return False
    
    def release(self):
        """Libera recursos de la cámara."""
        if self.camera:
            self.camera.release()
            self.camera = None
        
        cv2.destroyAllWindows()
        logger.info("Recursos de cámara liberados")


# Función de conveniencia para uso simple
def capture_profile_photo(persona_id: int) -> Optional[str]:
    """
    Función simple para capturar foto de perfil.
    
    Args:
        persona_id: ID de la persona
        
    Returns:
        Ruta a la foto guardada
        
    Example:
        >>> photo_path = capture_profile_photo(1)
        >>> if photo_path:
        ...     print(f"Foto guardada en: {photo_path}")
    """
    camera = CameraCapture()
    
    if not camera.is_camera_available():
        print("❌ No se detectó cámara web")
        return None
    
    print("📷 Iniciando captura de foto...")
    print("   Presione ESPACIO para tomar la foto")
    print("   Presione ESC para cancelar")
    
    return camera.capture_photo(persona_id)


if __name__ == "__main__":
    # Test del módulo
    print("Probando módulo de cámara...")
    
    camera = CameraCapture()
    
    # Verificar cámaras disponibles
    cameras = camera.list_cameras()
    print(f"\nCámaras disponibles: {cameras}")
    
    if cameras:
        print("\nIniciando captura de prueba...")
        photo = camera.capture_photo(
            persona_id=999,
            filename="test_photo.jpg"
        )
        
        if photo:
            print(f"✅ Foto guardada: {photo}")
        else:
            print("❌ No se pudo capturar la foto")
    else:
        print("❌ No hay cámaras disponibles")
