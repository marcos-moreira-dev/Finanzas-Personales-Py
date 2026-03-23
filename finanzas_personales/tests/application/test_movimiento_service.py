import unittest
from datetime import date, timedelta

from src.application.services.movimiento_service import MovimientoService
from src.application.services.persona_service import PersonaService
from src.domain.movimiento import TipoMovimiento
from src.infrastructure.db.database import Database
from src.infrastructure.repositories.categoria_repository import CategoriaRepository
from src.infrastructure.repositories.movimiento_repository import MovimientoRepository
from src.infrastructure.repositories.persona_repository import PersonaRepository


class MovimientoServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.database = Database(":memory:")
        self.database.init_schema()
        connection = self.database.get_connection()

        self.persona_service = PersonaService(PersonaRepository(connection))
        self.movimiento_service = MovimientoService(MovimientoRepository(connection))
        self.categoria_repository = CategoriaRepository(connection)

        self.persona = self.persona_service.crear_persona("Luis", "Torres")
        self.categoria_ingreso = self.categoria_repository.find_by_tipo_movimiento("INGRESO")[0]
        self.categoria_gasto = self.categoria_repository.find_by_tipo_movimiento("GASTO")[0]

    def tearDown(self) -> None:
        self.database.close()

    def test_crear_movimiento_despacha_por_tipo(self) -> None:
        movimiento = self.movimiento_service.crear_movimiento(
            persona_id=self.persona.id,
            fecha=date.today(),
            tipo=TipoMovimiento.GASTO,
            categoria_id=self.categoria_gasto.id,
            monto=25.5,
            descripcion="Cafe"
        )

        self.assertEqual(TipoMovimiento.GASTO, movimiento.tipo)
        self.assertEqual(1, len(self.movimiento_service.listar_movimientos(self.persona.id)))

    def test_actualizar_movimiento_revalida_y_permite_cambiar_tipo(self) -> None:
        movimiento = self.movimiento_service.crear_movimiento(
            persona_id=self.persona.id,
            fecha=date.today(),
            tipo="INGRESO",
            categoria_id=self.categoria_ingreso.id,
            monto=100,
            descripcion="Pago"
        )

        actualizado = self.movimiento_service.actualizar_movimiento(
            movimiento.id,
            tipo="GASTO",
            categoria_id=self.categoria_gasto.id,
            monto=40,
        )
        self.assertEqual(TipoMovimiento.GASTO, actualizado.tipo)
        self.assertEqual(40, actualizado.monto)

        with self.assertRaises(ValueError):
            self.movimiento_service.actualizar_movimiento(
                movimiento.id,
                fecha=date.today() + timedelta(days=1),
            )

        persisted = self.movimiento_service.obtener_movimiento(movimiento.id)
        self.assertEqual(TipoMovimiento.GASTO, persisted.tipo)
        self.assertEqual(40, persisted.monto)
