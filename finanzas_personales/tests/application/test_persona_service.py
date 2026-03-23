import unittest

from src.application.services.persona_service import PersonaService
from src.infrastructure.db.database import Database
from src.infrastructure.repositories.persona_repository import PersonaRepository


class PersonaServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.database = Database(":memory:")
        self.database.init_schema()
        self.repository = PersonaRepository(self.database.get_connection())
        self.service = PersonaService(self.repository)

    def tearDown(self) -> None:
        self.database.close()

    def test_actualizar_persona_revalida_campos_obligatorios(self) -> None:
        persona = self.service.crear_persona("Ana", "Perez")

        with self.assertRaises(ValueError):
            self.service.actualizar_persona(persona.id, nombres="   ")

        persisted = self.service.obtener_persona(persona.id)
        self.assertIsNotNone(persisted)
        self.assertEqual("Ana", persisted.nombres)
