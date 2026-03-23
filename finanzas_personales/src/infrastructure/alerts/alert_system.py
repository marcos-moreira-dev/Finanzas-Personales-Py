"""
Sistema de Alertas y Notificaciones - Infraestructura

Proporciona alertas inteligentes sobre la salud financiera:
- Alertas de presupuesto excedido
- Notificaciones de metas alcanzadas
- Advertencias de gastos inusuales
- Recordatorios de pagos recurrentes

Características:
- Sistema de reglas configurable
- Niveles de prioridad (INFO, WARNING, CRITICAL)
- Historial de alertas
- Notificaciones en UI

Ejemplo:
    >>> from src.infrastructure.alerts.alert_system import AlertSystem
    >>> alert_system = AlertSystem()
    >>> alert_system.check_alerts(persona_id=1)
    >>> alerts = alert_system.get_active_alerts(persona_id=1)
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class AlertPriority(Enum):
    """Niveles de prioridad de alertas."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(Enum):
    """Tipos de alertas disponibles."""
    BUDGET_EXCEEDED = "budget_exceeded"
    GOAL_ACHIEVED = "goal_achieved"
    UNUSUAL_SPENDING = "unusual_spending"
    LOW_BALANCE = "low_balance"
    PAYMENT_DUE = "payment_due"
    SAVINGS_OPPORTUNITY = "savings_opportunity"


@dataclass
class Alert:
    """
    Representa una alerta financiera.
    
    Attributes:
        id: Identificador único
        persona_id: ID de la persona
        type: Tipo de alerta
        priority: Nivel de prioridad
        title: Título corto
        message: Mensaje descriptivo
        created_at: Fecha de creación
        expires_at: Fecha de expiración (opcional)
        is_read: Si ya fue leída
        is_active: Si está activa
        data: Datos adicionales específicos del tipo
    """
    id: str
    persona_id: int
    type: AlertType
    priority: AlertPriority
    title: str
    message: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    is_read: bool = False
    is_active: bool = True
    data: Dict = field(default_factory=dict)


class AlertRule:
    """
    Regla para generar alertas automáticamente.
    
    Las reglas se evalúan periódicamente para detectar
    condiciones que requieran alertar al usuario.
    """
    
    def __init__(
        self,
        name: str,
        alert_type: AlertType,
        priority: AlertPriority,
        condition: Callable,
        message_template: str
    ):
        """
        Inicializa una regla de alerta.
        
        Args:
            name: Nombre identificador de la regla
            alert_type: Tipo de alerta que genera
            priority: Prioridad por defecto
            condition: Función que evalúa si se debe alertar
            message_template: Template del mensaje
        """
        self.name = name
        self.alert_type = alert_type
        self.priority = priority
        self.condition = condition
        self.message_template = message_template
    
    def evaluate(self, persona_id: int, **context) -> Optional[Alert]:
        """
        Evalúa la regla y genera alerta si aplica.
        
        Args:
            persona_id: ID de la persona
            **context: Datos adicionales para la evaluación
            
        Returns:
            Alerta si la condición se cumple, None si no
        """
        try:
            result = self.condition(persona_id, **context)
            
            if result:
                # Generar mensaje con datos
                message = self.message_template.format(**result) if isinstance(result, dict) else self.message_template
                
                return Alert(
                    id=f"{self.name}_{persona_id}_{datetime.now().timestamp()}",
                    persona_id=persona_id,
                    type=self.alert_type,
                    priority=self.priority,
                    title=self._get_title(),
                    message=message,
                    data=result if isinstance(result, dict) else {}
                )
            
        except Exception as e:
            logger.error(f"Error evaluando regla {self.name}: {e}")
        
        return None
    
    def _get_title(self) -> str:
        """Retorna título según el tipo de alerta."""
        titles = {
            AlertType.BUDGET_EXCEEDED: "Presupuesto Excedido",
            AlertType.GOAL_ACHIEVED: "Meta Alcanzada",
            AlertType.UNUSUAL_SPENDING: "Gasto Inusual",
            AlertType.LOW_BALANCE: "Saldo Bajo",
            AlertType.PAYMENT_DUE: "Pago Próximo",
            AlertType.SAVINGS_OPPORTUNITY: "Oportunidad de Ahorro",
        }
        return titles.get(self.alert_type, "Alerta Financiera")


class AlertSystem:
    """
    Sistema central de gestión de alertas.
    
    Coordina la evaluación de reglas, almacenamiento
    y presentación de alertas a los usuarios.
    
    Example:
        >>> alert_system = AlertSystem()
        >>> # Registrar regla personalizada
        >>> alert_system.register_rule(AlertRule(...))
        >>> # Evaluar alertas
        >>> alert_system.check_alerts(persona_id=1)
        >>> # Obtener alertas activas
        >>> alerts = alert_system.get_active_alerts(persona_id=1)
    """
    
    def __init__(self):
        """Inicializa el sistema de alertas."""
        self.rules: List[AlertRule] = []
        self.alerts: Dict[int, List[Alert]] = {}  # persona_id -> alerts
        self._setup_default_rules()
        
        logger.info("AlertSystem inicializado")
    
    def _setup_default_rules(self):
        """Configura reglas de alerta por defecto."""
        # Regla: Saldo bajo
        self.register_rule(AlertRule(
            name="low_balance",
            alert_type=AlertType.LOW_BALANCE,
            priority=AlertPriority.WARNING,
            condition=self._check_low_balance,
            message_template="Tu saldo actual es ${saldo:.2f}, está por debajo del mínimo recomendado (${minimo:.2f})"
        ))
        
        # Regla: Gastos mayores a ingresos
        self.register_rule(AlertRule(
            name="overspending",
            alert_type=AlertType.BUDGET_EXCEEDED,
            priority=AlertPriority.CRITICAL,
            condition=self._check_overspending,
            message_template="Has gastado ${gastos:.2f} cuando tus ingresos fueron ${ingresos:.2f}. Diferencia: ${diferencia:.2f}"
        ))
        
        # Regla: Meta de ahorro alcanzada
        self.register_rule(AlertRule(
            name="savings_goal",
            alert_type=AlertType.GOAL_ACHIEVED,
            priority=AlertPriority.INFO,
            condition=self._check_savings_goal,
            message_template="¡Felicidades! Has alcanzado tu meta de ahorro del {porcentaje:.1f}%"
        ))
    
    def register_rule(self, rule: AlertRule):
        """
        Registra una nueva regla de alerta.
        
        Args:
            rule: Instancia de AlertRule
        """
        self.rules.append(rule)
        logger.debug(f"Regla registrada: {rule.name}")
    
    def check_alerts(self, persona_id: int, **context):
        """
        Evalúa todas las reglas para una persona.
        
        Args:
            persona_id: ID de la persona
            **context: Datos adicionales (movimientos, resumen, etc.)
        """
        logger.info(f"Evaluando alertas para persona {persona_id}")
        
        # Inicializar lista si no existe
        if persona_id not in self.alerts:
            self.alerts[persona_id] = []
        
        # Evaluar cada regla
        for rule in self.rules:
            alert = rule.evaluate(persona_id, **context)
            
            if alert:
                # Verificar si ya existe alerta similar activa
                if not self._alert_exists(persona_id, alert):
                    self.alerts[persona_id].append(alert)
                    logger.info(f"Alerta generada: {alert.title} ({alert.priority.value})")
    
    def _alert_exists(self, persona_id: int, new_alert: Alert) -> bool:
        """Verifica si ya existe una alerta similar activa."""
        if persona_id not in self.alerts:
            return False
        
        for alert in self.alerts[persona_id]:
            if (alert.type == new_alert.type and 
                alert.is_active and 
                not alert.is_read and
                (datetime.now() - alert.created_at) < timedelta(hours=24)):
                return True
        
        return False
    
    def get_active_alerts(
        self,
        persona_id: int,
        priority: Optional[AlertPriority] = None
    ) -> List[Alert]:
        """
        Obtiene alertas activas para una persona.
        
        Args:
            persona_id: ID de la persona
            priority: Filtrar por prioridad (opcional)
            
        Returns:
            Lista de alertas activas
        """
        if persona_id not in self.alerts:
            return []
        
        alerts = [
            alert for alert in self.alerts[persona_id]
            if alert.is_active
        ]
        
        if priority:
            alerts = [a for a in alerts if a.priority == priority]
        
        # Ordenar por prioridad y fecha
        priority_order = {AlertPriority.CRITICAL: 0, AlertPriority.WARNING: 1, AlertPriority.INFO: 2}
        alerts.sort(key=lambda a: (priority_order[a.priority], a.created_at), reverse=True)
        
        return alerts
    
    def mark_as_read(self, persona_id: int, alert_id: str):
        """
        Marca una alerta como leída.
        
        Args:
            persona_id: ID de la persona
            alert_id: ID de la alerta
        """
        if persona_id in self.alerts:
            for alert in self.alerts[persona_id]:
                if alert.id == alert_id:
                    alert.is_read = True
                    logger.debug(f"Alerta {alert_id} marcada como leída")
                    break
    
    def dismiss_alert(self, persona_id: int, alert_id: str):
        """
        Desactiva una alerta.
        
        Args:
            persona_id: ID de la persona
            alert_id: ID de la alerta
        """
        if persona_id in self.alerts:
            for alert in self.alerts[persona_id]:
                if alert.id == alert_id:
                    alert.is_active = False
                    logger.debug(f"Alerta {alert_id} desactivada")
                    break
    
    def clear_old_alerts(self, days: int = 30):
        """
        Limpia alertas antiguas.
        
        Args:
            days: Eliminar alertas más antiguas que N días
        """
        cutoff = datetime.now() - timedelta(days=days)
        
        for persona_id in self.alerts:
            self.alerts[persona_id] = [
                alert for alert in self.alerts[persona_id]
                if alert.created_at > cutoff
            ]
        
        logger.info(f"Alertas antiguas eliminadas (> {days} días)")
    
    # ===== CONDICIONES POR DEFECTO =====
    
    def _check_low_balance(self, persona_id: int, **context) -> Optional[Dict]:
        """Verifica si el saldo está bajo."""
        # Obtener datos del contexto o consultar BD
        saldo = context.get('saldo', 0)
        minimo = context.get('saldo_minimo', 100)
        
        if saldo < minimo:
            return {'saldo': saldo, 'minimo': minimo}
        return None
    
    def _check_overspending(self, persona_id: int, **context) -> Optional[Dict]:
        """Verifica si los gastos superan ingresos."""
        ingresos = context.get('total_ingresos', 0)
        gastos = context.get('total_gastos', 0)
        
        if gastos > ingresos:
            return {
                'ingresos': ingresos,
                'gastos': gastos,
                'diferencia': gastos - ingresos
            }
        return None
    
    def _check_savings_goal(self, persona_id: int, **context) -> Optional[Dict]:
        """Verifica si se alcanzó meta de ahorro."""
        meta_ahorro = context.get('meta_ahorro', 20)  # 20% por defecto
        ingresos = context.get('total_ingresos', 0)
        saldo = context.get('saldo', 0)
        
        if ingresos > 0:
            porcentaje_ahorro = (saldo / ingresos) * 100
            if porcentaje_ahorro >= meta_ahorro:
                return {'porcentaje': porcentaje_ahorro}
        return None
