import unittest

from src.application.services.analisis_service import AnalisisFinancieroService


class AnalisisFinancieroServiceTests(unittest.TestCase):
    def test_alerta_discrecional_no_depende_de_saldo_negativo(self) -> None:
        service = AnalisisFinancieroService(None, None)

        alertas = service._generar_alertas(
            saldo=-100,
            tasa_ahorro=15,
            ratio=0.5,
            gastos_categoria={
                "Entretenimiento": 30,
                "Ropa": 5,
                "Servicios": 65,
            },
            dias_negativos=0,
        )

        self.assertTrue(any("Entretenimiento" in alerta for alerta in alertas))
        self.assertFalse(any("Ropa" in alerta for alerta in alertas))
