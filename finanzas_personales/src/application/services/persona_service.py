"""
Servicio de Persona - Capa de Aplicación

Implementa los casos de uso relacionados con la gestión de personas.
Coordina entre la capa de presentación y los repositorios.

Patrón: Service Layer
- Encapsula la lógica de aplicación
- Orquesta múltiples repositorios si es necesario
- Proporciona una API clara para la presentación
"""
from typing import List, Optional

from ...domain.persona import Persona
from ...infrastructure.repositories.persona_repository import PersonaRepository


class PersonaService:
    """
    Servicio para operaciones de negocio de Persona.
    
    Responsabilidades:
    - Validaciones de negocio
    - Coordinación entre repositorios
    - Transacciones que involucran múltiples operaciones
    
    Nota: No contiene lógica de presentación ni de persistencia directa.
    """
    
    def __init__(self, persona_repo: PersonaRepository):
        """
        Inicializa el servicio con sus dependencias.
        
        Args:
            persona_repo: Repositorio de personas inyectado
        """
        self._repo = persona_repo
    
    def crear_persona(
        self,
        nombres: str,
        apellidos: str,
        identificacion: str = None,
        telefono: str = None,
        correo: str = None,
        observaciones: str = None
    ) -> Persona:
        """
        Caso de uso: Crear una nueva persona.
        
        Args:
            nombres: Nombres de la persona
            apellidos: Apellidos de la persona
            identificacion: ID opcional (cédula, pasaporte, etc.)
            telefono: Teléfono de contacto
            correo: Correo electrónico
            observaciones: Notas adicionales
            
        Returns:
            Persona creada con ID asignado
            
        Raises:
            ValueError: Si los datos son inválidos
        """
        # Crear entidad de dominio (valida automáticamente)
        persona = Persona(
            nombres=nombres,
            apellidos=apellidos,
            identificacion=identificacion,
            telefono=telefono,
            correo=correo,
            observaciones=observaciones
        )
        
        # Persistir
        return self._repo.save(persona)
    
    def actualizar_persona(
        self,
        persona_id: int,
        nombres: str = None,
        apellidos: str = None,
        identificacion: str = None,
        telefono: str = None,
        correo: str = None,
        observaciones: str = None
    ) -> Persona:
        """
        Caso de uso: Actualizar datos de una persona existente.
        
        Args:
            persona_id: ID de la persona a actualizar
            ...campos opcionales a actualizar
            
        Returns:
            Persona actualizada
            
        Raises:
            ValueError: Si la persona no existe
        """
        # Obtener persona existente
        persona = self._repo.find_by_id(persona_id)
        if not persona:
            raise ValueError(f"No existe persona con ID {persona_id}")

        cambios = {}
        if nombres is not None:
            cambios["nombres"] = nombres
        if apellidos is not None:
            cambios["apellidos"] = apellidos
        if identificacion is not None:
            cambios["identificacion"] = identificacion
        if telefono is not None:
            cambios["telefono"] = telefono
        if correo is not None:
            cambios["correo"] = correo
        if observaciones is not None:
            cambios["observaciones"] = observaciones

        persona_actualizada = persona.actualizada(**cambios) if cambios else persona
        return self._repo.save(persona_actualizada)
    
    def obtener_persona(self, persona_id: int) -> Optional[Persona]:
        """
        Caso de uso: Obtener una persona por ID.
        
        Args:
            persona_id: ID de la persona
            
        Returns:
            Persona si existe, None si no
        """
        return self._repo.find_by_id(persona_id)
    
    def listar_personas(self, busqueda: str = None) -> List[Persona]:
        """
        Caso de uso: Listar todas las personas.
        
        Args:
            busqueda: Filtro opcional por nombre/apellido
            
        Returns:
            Lista de personas
        """
        return self._repo.find_all(busqueda)
    
    def eliminar_persona(self, persona_id: int) -> bool:
        """
        Caso de uso: Eliminar una persona.
        
        Nota: Los movimientos asociados se eliminan en cascada
        por la configuración de foreign keys en la BD.
        
        Args:
            persona_id: ID de la persona a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        return self._repo.delete(persona_id)
    
    def actualizar_foto(self, persona_id: int, foto_path: str) -> Persona:
        """
        Caso de uso: Actualizar la foto de perfil.
        
        Args:
            persona_id: ID de la persona
            foto_path: Ruta al archivo de imagen
            
        Returns:
            Persona actualizada
        """
        persona = self._repo.find_by_id(persona_id)
        if not persona:
            raise ValueError(f"No existe persona con ID {persona_id}")
        
        persona.actualizar_foto(foto_path)
        return self._repo.save(persona)
    
    def eliminar_foto(self, persona_id: int) -> Persona:
        """
        Caso de uso: Eliminar la foto de perfil.
        
        Args:
            persona_id: ID de la persona
            
        Returns:
            Persona actualizada
        """
        persona = self._repo.find_by_id(persona_id)
        if not persona:
            raise ValueError(f"No existe persona con ID {persona_id}")
        
        persona.eliminar_foto()
        return self._repo.save(persona)
