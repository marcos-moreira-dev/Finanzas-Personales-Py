import unittest

from src.application.services.persona_service import PersonaService
from src.infrastructure.db.database import Database
from src.infrastructure.repositories.movimiento_repository import MovimientoRepository
from src.infrastructure.repositories.persona_repository import PersonaRepository


class MovimientoRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.database = Database(":memory:")
        self.database.init_schema()
        connection = self.database.get_connection()
        self.repository = MovimientoRepository(connection)
        self.persona_service = PersonaService(PersonaRepository(connection))
        self.persona = self.persona_service.crear_persona("Marta", "Lopez")

    def tearDown(self) -> None:
        self.database.close()

    def test_rechaza_order_by_inseguro(self) -> None:
        with self.assertRaises(ValueError):
            self.repository.find_by_persona(
                self.persona.id,
                order_by="fecha DESC; DROP TABLE movimiento"
            )
