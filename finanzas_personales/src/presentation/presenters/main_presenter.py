"""
Presentador Principal - Capa de Presentación

El Presenter es el "intermediario" entre la Vista (UI) y el Modelo (datos).
Su trabajo es:
- Recibir acciones del usuario desde la Vista
- Coordinar con los Servicios para obtener/modificar datos
- Actualizar la Vista con los resultados

Patrón: MVP (Model-View-Presenter)
- Model: Los datos y reglas de negocio (Persona, Movimiento)
- View: La interfaz gráfica (ventanas, botones)
- Presenter: Este archivo, coordina entre ambos

¿Por qué usar MVP?
- Separa la lógica de la UI de la lógica de negocio
- Facilita hacer pruebas (podemos probar el Presenter sin UI)
- Permite cambiar la interfaz sin tocar la lógica
"""
from typing import Optional

from ...domain.persona import Persona


class MainPresenter:
    """
    Presentador principal de la aplicación.
    
    Coordina todas las interacciones entre la interfaz de usuario
    y los servicios de la aplicación.
    
    Analogía: Es como el maître de un restaurante:
    - Recibe a los clientes (usuarios)
    - Coordina con la cocina (servicios)
    - Entrega los platillos (actualiza la vista)
    """
    
    def __init__(self, view, persona_service, movimiento_service):
        """
        Inicializa el presentador con sus dependencias.
        
        Args:
            view: La ventana principal (MainWindow)
            persona_service: Servicio para operaciones de personas
            movimiento_service: Servicio para operaciones de movimientos
        """
        self.view = view
        self.persona_service = persona_service
        self.movimiento_service = movimiento_service
        
        # Estado actual
        self.current_persona: Optional[Persona] = None
    
    def load_personas(self):
        """
        Carga todas las personas y actualiza la lista.
        
        Este método se llama al iniciar la aplicación o cuando
        se necesita refrescar la lista completa.
        """
        try:
            # Obtener personas del servicio
            personas = self.persona_service.listar_personas()
            
            # Actualizar la vista
            self.view.update_person_list(personas)
            
        except Exception as e:
            self._show_error(f"Error al cargar personas: {e}")
    
    def search_personas(self, search_term: str):
        """
        Busca personas por término de búsqueda.
        
        Args:
            search_term: Texto a buscar en nombres/apellidos
        """
        try:
            personas = self.persona_service.listar_personas(search_term)
            self.view.update_person_list(personas)
        except Exception as e:
            self._show_error(f"Error al buscar: {e}")
    
    def select_persona(self, persona_id: int):
        """
        Selecciona una persona y muestra sus detalles.
        
        Args:
            persona_id: ID de la persona seleccionada
        """
        try:
            persona = self.persona_service.obtener_persona(persona_id)
            if persona:
                self.current_persona = persona
                self.view.show_person_detail(persona)
        except Exception as e:
            self._show_error(f"Error al cargar persona: {e}")
    
    def create_new_persona(self):
        """
        Prepara la interfaz para crear una nueva persona.
        """
        self.current_persona = None
        if hasattr(self.view, "show_new_person_form"):
            self.view.show_new_person_form()
    
    def save_persona(self, datos: dict) -> bool:
        """
        Guarda una persona (nueva o existente).
        
        Args:
            datos: Diccionario con los datos de la persona
                  (nombres, apellidos, telefono, etc.)
        
        Returns:
            True si se guardó exitosamente
        """
        try:
            if self.current_persona:
                # Actualizar persona existente
                persona = self.persona_service.actualizar_persona(
                    persona_id=self.current_persona.id,
                    **datos
                )
            else:
                # Crear nueva persona
                persona = self.persona_service.crear_persona(**datos)

            # Guardamos el agregado devuelto por el servicio porque ahi vive
            # la version validada y persistida del objeto.
            self.current_persona = persona
            self.load_personas()
            if hasattr(self.view, "select_person"):
                # Re-seleccionar evita que la UI quede apuntando a una ficha
                # vieja despues de refrescar la lista lateral.
                self.view.select_person(persona.id)
            elif hasattr(self.view, "show_person_detail"):
                self.view.show_person_detail(persona)
            if hasattr(self.view, "show_status"):
                self.view.show_status(f"Ficha guardada: {persona.nombre_completo}", 0)
            return True
            
        except Exception as e:
            self._show_error(f"Error al guardar: {e}")
            return False
    
    def delete_persona(self, persona_id: int) -> bool:
        """
        Elimina una persona después de confirmar.
        
        Args:
            persona_id: ID de la persona a eliminar
            
        Returns:
            True si se eliminó
        """
        try:
            # Confirmar eliminación
            # (la vista debería mostrar un diálogo de confirmación)
            
            self.persona_service.eliminar_persona(persona_id)
            self.current_persona = None
            self.load_personas()
            if hasattr(self.view, "clear_person_detail"):
                self.view.clear_person_detail()
            if hasattr(self.view, "show_status"):
                self.view.show_status("Persona eliminada", 0)
            return True
            
        except Exception as e:
            self._show_error(f"Error al eliminar: {e}")
            return False
    
    def _show_error(self, message: str):
        """
        Muestra un mensaje de error al usuario.
        
        En una implementación completa, esto mostraría un diálogo
        gráfico de error usando wx.MessageBox.
        
        Args:
            message: Mensaje de error a mostrar
        """
        if hasattr(self.view, "show_error"):
            self.view.show_error(message)
        else:
            print(f"ERROR: {message}")
