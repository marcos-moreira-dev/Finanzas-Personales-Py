"""
Entidad Persona - Dominio
Representa al titular de la ficha financiera.
"""
from dataclasses import dataclass, field, replace
from datetime import date
from typing import Any, Optional


@dataclass
class Persona:
    """Entidad que representa a una persona con sus datos personales."""
    
    nombres: str
    apellidos: str
    id: Optional[int] = None
    identificacion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    fecha_registro: date = field(default_factory=date.today)
    observaciones: Optional[str] = None
    foto_path: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones iniciales."""
        if not self.nombres or not self.nombres.strip():
            raise ValueError("El nombre es obligatorio")
        if not self.apellidos or not self.apellidos.strip():
            raise ValueError("El apellido es obligatorio")
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo de la persona."""
        return f"{self.nombres} {self.apellidos}".strip()

    def actualizada(self, **cambios: Any) -> "Persona":
        """Retorna una copia validada con los cambios aplicados."""
        return replace(self, **cambios)
    
    def actualizar_foto(self, foto_path: str) -> None:
        """Actualiza la ruta de la foto de perfil."""
        self.foto_path = foto_path
    
    def eliminar_foto(self) -> None:
        """Elimina la referencia a la foto de perfil."""
        self.foto_path = None
    
    def __str__(self) -> str:
        return self.nombre_completo
    
    def __repr__(self) -> str:
        return f"Persona(id={self.id}, nombre='{self.nombre_completo}')"
