"""
Módulo de Análisis Financiero Avanzado

Proporciona métricas detalladas y análisis completo de finanzas personales.
Incluye: tendencias, proyecciones, comparativas, ratios financieros, etc.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import statistics

from ...domain.movimiento import Movimiento, TipoMovimiento
from ...domain.categoria import Categoria


@dataclass
class MetricasMensuales:
    """Métricas financieras de un mes específico."""
    mes: int
    anio: int
    ingresos: float
    gastos: float
    balance: float
    num_transacciones: int
    promedio_transaccion: float
    dia_mayor_gasto: Optional[Tuple[int, float]]
    categoria_mayor_gasto: Optional[Tuple[str, float]]


@dataclass
class AnalisisFinanciero:
    """Análisis completo de finanzas personales."""
    # Métricas básicas
    saldo_total: float
    total_ingresos: float
    total_gastos: float
    
    # Métricas de transacciones
    num_transacciones: int
    num_ingresos: int
    num_gastos: int
    promedio_ingreso: float
    promedio_gasto: float
    promedio_diario_gasto: float
    
    # Métricas temporales
    fecha_inicio: datetime
    fecha_fin: datetime
    dias_actividad: int
    
    # Ratios y porcentajes
    tasa_ahorro: float  # % de ingresos que se ahorra
    ratio_gasto_ingreso: float  # Gastos/Ingresos
    porcentaje_gastos_necesarios: float  # Gastos básicos vs total
    
    # Análisis por categoría
    gastos_por_categoria: Dict[str, float]
    ingresos_por_categoria: Dict[str, float]
    top_5_gastos: List[Tuple[str, float]]
    top_5_ingresos: List[Tuple[str, float]]
    
    # Tendencias mensuales
    tendencia_mensual: List[MetricasMensuales]
    cambio_mes_anterior: Dict[str, float]  # % de cambio vs mes anterior
    
    # Proyecciones
    proyeccion_mes_siguiente: Dict[str, float]
    ahorro_proyectado_12m: float
    
    # Alertas y recomendaciones
    alertas: List[str]
    recomendaciones: List[str]
    
    # Estadísticas avanzadas
    desviacion_estandar_gastos: float
    variabilidad_ingresos: float
    dias_consecutivos_negativos: int
    mejor_dia_semana: str  # Día con mejor balance promedio
    peor_dia_semana: str


class AnalisisFinancieroService:
    """
    Servicio para análisis financiero avanzado.
    
    Calcula métricas complejas, tendencias, proyecciones y alertas.
    """
    
    DIAS_SEMANA = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    def __init__(self, movimiento_service, categoria_repo):
        """
        Inicializa el servicio de análisis.
        
        Args:
            movimiento_service: Servicio de movimientos
            categoria_repo: Repositorio de categorías
        """
        self.movimiento_service = movimiento_service
        self.categoria_repo = categoria_repo
    
    def analizar(self, persona_id: int) -> AnalisisFinanciero:
        """
        Realiza análisis completo de finanzas.
        
        Args:
            persona_id: ID de la persona a analizar
            
        Returns:
            AnalisisFinanciero con todas las métricas
        """
        # Obtener todos los movimientos
        movimientos = self.movimiento_service.listar_movimientos(persona_id)
        
        if not movimientos:
            return self._analisis_vacio()
        
        # Ordenar por fecha
        movimientos.sort(key=lambda x: x.fecha)
        
        # Calcular métricas básicas
        total_ingresos, total_gastos = self.movimiento_service.obtener_totales(persona_id)
        saldo_total = total_ingresos - total_gastos
        
        # Separar por tipo
        ingresos = [m for m in movimientos if m.tipo == TipoMovimiento.INGRESO]
        gastos_list = [m for m in movimientos if m.tipo == TipoMovimiento.GASTO]
        
        num_ingresos = len(ingresos)
        num_gastos = len(gastos_list)
        num_transacciones = len(movimientos)
        
        # Promedios
        promedio_ingreso = total_ingresos / num_ingresos if num_ingresos > 0 else 0
        promedio_gasto = total_gastos / num_gastos if num_gastos > 0 else 0
        
        # Métricas temporales
        fecha_inicio = movimientos[0].fecha
        fecha_fin = movimientos[-1].fecha
        dias_actividad = (fecha_fin - fecha_inicio).days + 1
        promedio_diario_gasto = total_gastos / dias_actividad if dias_actividad > 0 else 0
        
        # Ratios
        tasa_ahorro = ((total_ingresos - total_gastos) / total_ingresos * 100) if total_ingresos > 0 else 0
        ratio_gasto_ingreso = (total_gastos / total_ingresos) if total_ingresos > 0 else 0
        
        # Análisis por categoría
        gastos_por_categoria = self._calcular_por_categoria(gastos_list)
        ingresos_por_categoria = self._calcular_por_categoria(ingresos)
        
        top_5_gastos = sorted(gastos_por_categoria.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_ingresos = sorted(ingresos_por_categoria.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Tendencias mensuales
        tendencia_mensual = self._calcular_tendencia_mensual(movimientos)
        
        # Comparativa mes anterior
        cambio_mes_anterior = self._calcular_cambio_mes_anterior(tendencia_mensual)
        
        # Proyecciones
        proyeccion = self._calcular_proyecciones(tendencia_mensual, total_ingresos, total_gastos)
        
        # Estadísticas avanzadas
        desviacion_gastos = statistics.stdev([m.monto for m in gastos_list]) if len(gastos_list) > 1 else 0
        variabilidad = (desviacion_gastos / promedio_gasto * 100) if promedio_gasto > 0 else 0
        
        # Días consecutivos negativos
        dias_negativos = self._calcular_dias_consecutivos_negativos(movimientos)
        
        # Mejor y peor día de la semana
        mejor_dia, peor_dia = self._analizar_dias_semana(movimientos)
        
        # Alertas y recomendaciones
        alertas = self._generar_alertas(saldo_total, tasa_ahorro, ratio_gasto_ingreso, 
                                       gastos_por_categoria, dias_negativos)
        recomendaciones = self._generar_recomendaciones(tasa_ahorro, ratio_gasto_ingreso,
                                                       top_5_gastos, promedio_diario_gasto)
        
        return AnalisisFinanciero(
            saldo_total=saldo_total,
            total_ingresos=total_ingresos,
            total_gastos=total_gastos,
            num_transacciones=num_transacciones,
            num_ingresos=num_ingresos,
            num_gastos=num_gastos,
            promedio_ingreso=promedio_ingreso,
            promedio_gasto=promedio_gasto,
            promedio_diario_gasto=promedio_diario_gasto,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            dias_actividad=dias_actividad,
            tasa_ahorro=tasa_ahorro,
            ratio_gasto_ingreso=ratio_gasto_ingreso,
            porcentaje_gastos_necesarios=self._calcular_gastos_necesarios(gastos_por_categoria, total_gastos),
            gastos_por_categoria=gastos_por_categoria,
            ingresos_por_categoria=ingresos_por_categoria,
            top_5_gastos=top_5_gastos,
            top_5_ingresos=top_5_ingresos,
            tendencia_mensual=tendencia_mensual,
            cambio_mes_anterior=cambio_mes_anterior,
            proyeccion_mes_siguiente=proyeccion,
            ahorro_proyectado_12m=proyeccion.get('balance', 0) * 12,
            alertas=alertas,
            recomendaciones=recomendaciones,
            desviacion_estandar_gastos=desviacion_gastos,
            variabilidad_ingresos=variabilidad,
            dias_consecutivos_negativos=dias_negativos,
            mejor_dia_semana=mejor_dia,
            peor_dia_semana=peor_dia
        )
    
    def _analisis_vacio(self) -> AnalisisFinanciero:
        """Crea análisis vacío cuando no hay datos."""
        return AnalisisFinanciero(
            saldo_total=0, total_ingresos=0, total_gastos=0,
            num_transacciones=0, num_ingresos=0, num_gastos=0,
            promedio_ingreso=0, promedio_gasto=0, promedio_diario_gasto=0,
            fecha_inicio=datetime.now(), fecha_fin=datetime.now(), dias_actividad=0,
            tasa_ahorro=0, ratio_gasto_ingreso=0, porcentaje_gastos_necesarios=0,
            gastos_por_categoria={}, ingresos_por_categoria={},
            top_5_gastos=[], top_5_ingresos=[],
            tendencia_mensual=[], cambio_mes_anterior={},
            proyeccion_mes_siguiente={}, ahorro_proyectado_12m=0,
            alertas=["No hay datos suficientes para el análisis"],
            recomendaciones=["Comience registrando sus ingresos y gastos"],
            desviacion_estandar_gastos=0, variabilidad_ingresos=0,
            dias_consecutivos_negativos=0, mejor_dia_semana="N/A", peor_dia_semana="N/A"
        )
    
    def _calcular_por_categoria(self, movimientos: List[Movimiento]) -> Dict[str, float]:
        """Calcula totales por categoría."""
        totales = defaultdict(float)
        for mov in movimientos:
            cat = self.categoria_repo.find_by_id(mov.categoria_id)
            nombre = cat.nombre if cat else f"Categoría {mov.categoria_id}"
            totales[nombre] += mov.monto
        return dict(totales)
    
    def _calcular_tendencia_mensual(self, movimientos: List[Movimiento]) -> List[MetricasMensuales]:
        """Calcula métricas mensuales para tendencias."""
        if not movimientos:
            return []
        
        # Agrupar por mes
        datos_mensuales = defaultdict(lambda: {'ingresos': 0, 'gastos': 0, 'transacciones': 0, 
                                                'dias': defaultdict(float),
                                                'categorias': defaultdict(float)})
        
        for mov in movimientos:
            clave = (mov.fecha.year, mov.fecha.month)
            datos_mensuales[clave]['transacciones'] += 1
            
            if mov.tipo == TipoMovimiento.INGRESO:
                datos_mensuales[clave]['ingresos'] += mov.monto
            else:
                datos_mensuales[clave]['gastos'] += mov.monto
                datos_mensuales[clave]['dias'][mov.fecha.day] += mov.monto
                cat = self.categoria_repo.find_by_id(mov.categoria_id)
                cat_nombre = cat.nombre if cat else f"Cat {mov.categoria_id}"
                datos_mensuales[clave]['categorias'][cat_nombre] += mov.monto
        
        # Crear objetos MetricasMensuales
        metricas = []
        for (anio, mes), datos in sorted(datos_mensuales.items()):
            ingresos = datos['ingresos']
            gastos = datos['gastos']
            balance = ingresos - gastos
            num_trans = datos['transacciones']
            
            # Día con mayor gasto
            dia_mayor = max(datos['dias'].items(), key=lambda x: x[1]) if datos['dias'] else None
            
            # Categoría con mayor gasto
            cat_mayor = max(datos['categorias'].items(), key=lambda x: x[1]) if datos['categorias'] else None
            
            metricas.append(MetricasMensuales(
                mes=mes, anio=anio,
                ingresos=ingresos, gastos=gastos, balance=balance,
                num_transacciones=num_trans,
                promedio_transaccion=(ingresos + gastos) / num_trans if num_trans > 0 else 0,
                dia_mayor_gasto=dia_mayor,
                categoria_mayor_gasto=cat_mayor
            ))
        
        return metricas
    
    def _calcular_cambio_mes_anterior(self, tendencias: List[MetricasMensuales]) -> Dict[str, float]:
        """Calcula porcentaje de cambio vs mes anterior."""
        if len(tendencias) < 2:
            return {'ingresos': 0, 'gastos': 0, 'balance': 0}
        
        actual = tendencias[-1]
        anterior = tendencias[-2]
        
        def calcular_cambio(actual_val, anterior_val):
            if anterior_val == 0:
                return 100 if actual_val > 0 else 0
            return ((actual_val - anterior_val) / anterior_val) * 100
        
        return {
            'ingresos': calcular_cambio(actual.ingresos, anterior.ingresos),
            'gastos': calcular_cambio(actual.gastos, anterior.gastos),
            'balance': calcular_cambio(actual.balance, anterior.balance)
        }
    
    def _calcular_proyecciones(self, tendencias: List[MetricasMensuales], 
                              total_ingresos: float, total_gastos: float) -> Dict[str, float]:
        """Calcula proyecciones para el mes siguiente."""
        if not tendencias:
            return {'ingresos': 0, 'gastos': 0, 'balance': 0}
        
        # Promedio de últimos 3 meses si hay suficientes datos
        n = min(3, len(tendencias))
        ultimos = tendencias[-n:]
        
        promedio_ingresos = sum(m.ingresos for m in ultimos) / n
        promedio_gastos = sum(m.gastos for m in ultimos) / n
        
        return {
            'ingresos': promedio_ingresos,
            'gastos': promedio_gastos,
            'balance': promedio_ingresos - promedio_gastos
        }
    
    def _calcular_gastos_necesarios(self, gastos_por_categoria: Dict[str, float], 
                                   total_gastos: float) -> float:
        """Calcula porcentaje de gastos básicos/necesarios."""
        if total_gastos == 0:
            return 0
        
        categorias_necesarias = ['Alimentación', 'Vivienda', 'Transporte', 'Salud', 
                                'Educación', 'Impuestos', 'Seguros']
        
        gastos_necesarios = sum(monto for cat, monto in gastos_por_categoria.items() 
                               if any(nec in cat for nec in categorias_necesarias))
        
        return (gastos_necesarios / total_gastos) * 100
    
    def _calcular_dias_consecutivos_negativos(self, movimientos: List[Movimiento]) -> int:
        """Calcula racha actual de días con balance negativo."""
        if not movimientos:
            return 0
        
        # Agrupar por día
        balance_diario = defaultdict(float)
        for mov in movimientos:
            if mov.tipo == TipoMovimiento.INGRESO:
                balance_diario[mov.fecha] += mov.monto
            else:
                balance_diario[mov.fecha] -= mov.monto
        
        # Contar días consecutivos negativos desde el final
        fechas_ordenadas = sorted(balance_diario.keys(), reverse=True)
        consecutivos = 0
        
        for fecha in fechas_ordenadas:
            if balance_diario[fecha] < 0:
                consecutivos += 1
            else:
                break
        
        return consecutivos
    
    def _analizar_dias_semana(self, movimientos: List[Movimiento]) -> Tuple[str, str]:
        """Analiza cuál es el mejor y peor día de la semana."""
        if not movimientos:
            return "N/A", "N/A"
        
        # Balance por día de semana
        balance_dias = defaultdict(float)
        for mov in movimientos:
            dia_semana = mov.fecha.weekday()
            if mov.tipo == TipoMovimiento.INGRESO:
                balance_dias[dia_semana] += mov.monto
            else:
                balance_dias[dia_semana] -= mov.monto
        
        if not balance_dias:
            return "N/A", "N/A"
        
        mejor = max(balance_dias.items(), key=lambda x: x[1])
        peor = min(balance_dias.items(), key=lambda x: x[1])
        
        return self.DIAS_SEMANA[mejor[0]], self.DIAS_SEMANA[peor[0]]
    
    def _generar_alertas(self, saldo: float, tasa_ahorro: float, ratio: float,
                        gastos_categoria: Dict[str, float], dias_negativos: int) -> List[str]:
        """Genera alertas basadas en las métricas."""
        alertas = []
        total_gastos = sum(gastos_categoria.values())
        umbral_gasto_discrecional = total_gastos * 0.30
        
        if saldo < 0:
            alertas.append(f"⚠️ SALDO NEGATIVO: ${saldo:,.2f}")
        
        if tasa_ahorro < 10:
            alertas.append(f"⚠️ Tasa de ahorro muy baja ({tasa_ahorro:.1f}%). Ideal: 20%+")
        
        if ratio > 0.9:
            alertas.append(f"⚠️ Está gastando el {ratio*100:.1f}% de sus ingresos")
        
        if dias_negativos >= 5:
            alertas.append(f"⚠️ {dias_negativos} días consecutivos con balance negativo")
        
        # Alerta por categoría con gasto excesivo
        for categoria, monto in gastos_categoria.items():
            if (
                total_gastos > 0
                and categoria in ['Entretenimiento', 'Ropa', 'Viajes']
                and monto >= umbral_gasto_discrecional
            ):
                alertas.append(f"⚠️ Gasto alto en {categoria}: ${monto:,.2f}")
        
        return alertas if alertas else ["✅ Sin alertas importantes"]
    
    def _generar_recomendaciones(self, tasa_ahorro: float, ratio: float,
                                top_gastos: List[Tuple[str, float]], 
                                promedio_diario: float) -> List[str]:
        """Genera recomendaciones personalizadas."""
        recomendaciones = []
        
        if tasa_ahorro < 20:
            objetivo = 20 - tasa_ahorro
            recomendaciones.append(f"💡 Intente reducir gastos en {objetivo:.1f}% para ahorrar el 20% ideal")
        
        if ratio > 0.8:
            recomendaciones.append("💡 Sus gastos superan el 80% de sus ingresos. Revise gastos discrecionales")
        
        if top_gastos:
            mayor_categoria = top_gastos[0]
            recomendaciones.append(f"💡 Su mayor gasto es '{mayor_categoria[0]}' (${mayor_categoria[1]:,.2f}). Considere reducirlo")
        
        if promedio_diario > 100:
            recomendaciones.append(f"💡 Promedio diario de gastos: ${promedio_diario:,.2f}. Busque oportunidades de ahorro diario")
        
        recomendaciones.append("💡 Meta de ahorro recomendada: 6 meses de gastos como fondo de emergencia")
        
        return recomendaciones
