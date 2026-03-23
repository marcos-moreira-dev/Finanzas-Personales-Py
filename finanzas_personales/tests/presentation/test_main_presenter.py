import unittest
from unittest.mock import Mock

from src.domain.persona import Persona
from src.presentation.presenters.main_presenter import MainPresenter


class FakeView:
    def __init__(self):
        self.new_form_shown = False
        self.updated_lists = []
        self.selected_person_ids = []
        self.status_messages = []
        self.error_messages = []
        self.clear_detail_calls = 0

    def show_new_person_form(self):
        self.new_form_shown = True

    def update_person_list(self, personas):
        self.updated_lists.append(personas)

    def select_person(self, persona_id: int):
        self.selected_person_ids.append(persona_id)

    def show_status(self, message: str, field: int = 0):
        self.status_messages.append((message, field))

    def clear_person_detail(self):
        self.clear_detail_calls += 1

    def show_error(self, message: str):
        self.error_messages.append(message)


class MainPresenterTestCase(unittest.TestCase):
    def setUp(self):
        self.view = FakeView()
        self.persona_service = Mock()
        self.movimiento_service = Mock()
        self.presenter = MainPresenter(self.view, self.persona_service, self.movimiento_service)

    def test_create_new_persona_shows_blank_form(self):
        self.presenter.current_persona = Persona(id=4, nombres="Ana", apellidos="Lopez")

        self.presenter.create_new_persona()

        self.assertIsNone(self.presenter.current_persona)
        self.assertTrue(self.view.new_form_shown)

    def test_save_persona_creates_and_selects_saved_record(self):
        persona = Persona(id=10, nombres="Pedro", apellidos="Gomez")
        self.persona_service.crear_persona.return_value = persona
        self.persona_service.listar_personas.return_value = [persona]

        saved = self.presenter.save_persona(
            {
                "nombres": "Pedro",
                "apellidos": "Gomez",
                "identificacion": None,
                "telefono": None,
                "correo": None,
                "observaciones": None,
            }
        )

        self.assertTrue(saved)
        self.assertEqual(self.presenter.current_persona, persona)
        self.assertEqual(self.view.selected_person_ids, [10])
        self.assertEqual(self.view.updated_lists[-1], [persona])
        self.assertTrue(any("Pedro Gomez" in message for message, _ in self.view.status_messages))

    def test_delete_persona_clears_detail_when_successful(self):
        self.persona_service.listar_personas.return_value = []

        deleted = self.presenter.delete_persona(7)

        self.assertTrue(deleted)
        self.persona_service.eliminar_persona.assert_called_once_with(7)
        self.assertEqual(self.view.clear_detail_calls, 1)
        self.assertTrue(any(message == "Persona eliminada" for message, _ in self.view.status_messages))

    def test_save_persona_reports_errors_through_view(self):
        self.persona_service.crear_persona.side_effect = ValueError("Nombre inválido")

        saved = self.presenter.save_persona(
            {
                "nombres": "",
                "apellidos": "Lopez",
                "identificacion": None,
                "telefono": None,
                "correo": None,
                "observaciones": None,
            }
        )

        self.assertFalse(saved)
        self.assertEqual(len(self.view.error_messages), 1)
        self.assertIn("Error al guardar", self.view.error_messages[0])


if __name__ == "__main__":
    unittest.main()
