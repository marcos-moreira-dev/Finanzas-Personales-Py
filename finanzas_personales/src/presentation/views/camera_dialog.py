"""
Diálogo de Captura de Foto Integrado en wxPython

Este módulo proporciona un diálogo modal que integra la captura
de video desde OpenCV directamente dentro de la aplicación wxPython,
sin ventanas separadas.
"""
import wx
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Optional

from ...infrastructure.config.settings import Config


class CameraCaptureDialog(wx.Dialog):
    """
    Diálogo modal para captura de foto con vista previa integrada.
    
    Muestra el video en tiempo real dentro de un panel wxPython,
    permitiendo una experiencia completamente integrada.
    """
    
    def __init__(self, parent, persona_id: int, title="Capturar Foto"):
        """
        Inicializa el diálogo de captura.
        
        Args:
            parent: Ventana padre
            persona_id: ID de la persona para la foto
            title: Título del diálogo
        """
        super().__init__(
            parent,
            title=title,
            size=(700, 600),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        
        self.persona_id = persona_id
        self.captured_photo_path: Optional[str] = None
        self.camera: Optional[cv2.VideoCapture] = None
        self.timer: Optional[wx.Timer] = None
        self.is_capturing = False
        
        self._setup_ui()
        self._init_camera()
    
    def _setup_ui(self):
        """Configura la interfaz del diálogo."""
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Panel de video
        video_box = wx.StaticBox(panel, label="Vista Previa")
        video_sizer = wx.StaticBoxSizer(video_box, wx.VERTICAL)
        
        # Bitmap para mostrar el video
        self.video_bitmap = wx.StaticBitmap(
            video_box,
            size=(640, 480)
        )
        video_sizer.Add(self.video_bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        # Label de estado
        self.lbl_status = wx.StaticText(
            video_box,
            label="Iniciando cámara...",
            style=wx.ALIGN_CENTER
        )
        video_sizer.Add(self.lbl_status, 0, wx.EXPAND | wx.ALL, 5)
        
        main_sizer.Add(video_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_capture = wx.Button(panel, label="📷 Capturar Foto")
        self.btn_capture.SetToolTip("Espacio - Capturar foto")
        self.btn_capture.Bind(wx.EVT_BUTTON, self._on_capture)
        self.btn_capture.Enable(False)
        btn_sizer.Add(self.btn_capture, 0, wx.RIGHT, 10)
        
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, label="Cancelar")
        btn_sizer.Add(btn_cancel, 0, wx.RIGHT, 10)
        
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        # Instrucciones
        lbl_help = wx.StaticText(
            panel,
            label="ESPACIO: Capturar  |  ESC: Cancelar",
            style=wx.ALIGN_CENTER
        )
        font = lbl_help.GetFont()
        font.SetPointSize(9)
        font.SetStyle(wx.FONTSTYLE_ITALIC)
        lbl_help.SetFont(font)
        main_sizer.Add(lbl_help, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        panel.SetSizer(main_sizer)
        
        # Bind teclas
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key)
        self.Bind(wx.EVT_CLOSE, self._on_close)
    
    def _init_camera(self):
        """Inicializa la cámara y el timer."""
        try:
            # Intentar abrir cámara
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                wx.MessageBox(
                    "No se pudo abrir la cámara",
                    "Error",
                    wx.OK | wx.ICON_ERROR,
                    self
                )
                self.EndModal(wx.ID_CANCEL)
                return
            
            # Configurar resolución
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Crear timer para actualizar video (30 FPS)
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self._on_timer, self.timer)
            self.timer.Start(33)  # ~30 FPS
            
            self.is_capturing = True
            self.btn_capture.Enable(True)
            self.lbl_status.SetLabel("Cámara lista - Presione ESPACIO para capturar")
            
        except Exception as e:
            wx.MessageBox(
                f"Error al inicializar cámara:\n{str(e)}",
                "Error",
                wx.OK | wx.ICON_ERROR,
                self
            )
            self.EndModal(wx.ID_CANCEL)
    
    def _on_timer(self, event):
        """Actualiza el frame del video."""
        if not self.is_capturing or not self.camera:
            return
        
        ret, frame = self.camera.read()
        
        if not ret:
            self.lbl_status.SetLabel("Error leyendo frame de cámara")
            return
        
        # Convertir BGR (OpenCV) a RGB (wxPython)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Crear wx.Image desde el frame
        height, width = frame_rgb.shape[:2]
        image = wx.Image(width, height)
        image.SetData(frame_rgb.tobytes())
        
        # Redimensionar al tamaño del bitmap
        bitmap_width = 640
        bitmap_height = 480
        image = image.Scale(bitmap_width, bitmap_height, wx.IMAGE_QUALITY_HIGH)
        
        # Actualizar bitmap
        self.video_bitmap.SetBitmap(wx.Bitmap(image))
        self.video_bitmap.Refresh()
    
    def _on_capture(self, event):
        """Captura la foto."""
        if not self.camera:
            return
        
        ret, frame = self.camera.read()
        
        if not ret:
            wx.MessageBox(
                "Error al capturar frame",
                "Error",
                wx.OK | wx.ICON_ERROR,
                self
            )
            return
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"persona_{self.persona_id}_{timestamp}.jpg"
        filepath = Config.PHOTOS_DIR / filename
        
        # Asegurar que existe el directorio
        Config.PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Guardar foto (redimensionar a 400x400)
        resized = cv2.resize(frame, (400, 400))
        success = cv2.imwrite(str(filepath), resized)
        
        if success:
            self.captured_photo_path = str(filepath)
            self._cleanup()
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox(
                "Error al guardar la foto",
                "Error",
                wx.OK | wx.ICON_ERROR,
                self
            )
    
    def _on_key(self, event):
        """Maneja teclas del diálogo."""
        key_code = event.GetKeyCode()
        
        if key_code == wx.WXK_SPACE:
            # Capturar foto
            self._on_capture(event)
        elif key_code == wx.WXK_ESCAPE:
            # Cancelar
            self._cleanup()
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()
    
    def _on_close(self, event):
        """Maneja el cierre del diálogo."""
        self._cleanup()
        event.Skip()
    
    def _cleanup(self):
        """Libera recursos."""
        self.is_capturing = False
        
        if self.timer:
            self.timer.Stop()
            self.timer = None
        
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def get_photo_path(self) -> Optional[str]:
        """
        Retorna la ruta de la foto capturada.
        
        Returns:
            Ruta al archivo de foto o None si se canceló
        """
        return self.captured_photo_path


def capture_photo_dialog(parent, persona_id: int) -> Optional[str]:
    """
    Función de conveniencia para mostrar el diálogo de captura.
    
    Args:
        parent: Ventana padre
        persona_id: ID de la persona
        
    Returns:
        Ruta a la foto capturada o None si se canceló
        
    Example:
        >>> photo_path = capture_photo_dialog(self, persona_id=1)
        >>> if photo_path:
        ...     print(f"Foto guardada: {photo_path}")
    """
    dialog = CameraCaptureDialog(parent, persona_id)
    result = dialog.ShowModal()
    
    photo_path = None
    if result == wx.ID_OK:
        photo_path = dialog.get_photo_path()
    
    dialog.Destroy()
    return photo_path
