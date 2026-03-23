"""
Generador de Reportes PDF - Infraestructura

Este módulo genera reportes PDF profesionales y visualmente atractivos
con gráficos, tablas y análisis financiero completo.

Características:
- Portada profesional con logo e información del reporte
- Tablas formateadas con estilos corporativos
- Gráficos integrados (barras, pastel, líneas)
- Análisis automático con insights
- Exportación multiperíodo
- Diseño responsive para diferentes tamaños de página

Dependencias:
- reportlab: Generación de PDF
- matplotlib: Gráficos (integrados como imágenes)
- PIL: Procesamiento de imágenes

Ejemplo de uso:
    >>> from src.infrastructure.reports.pdf_generator import PDFReportGenerator
    >>> generator = PDFReportGenerator()
    >>> generator.generar_reporte_mensual(persona_id=1, anio=2024, mes=3, 
    ...                                   output_path="reporte_marzo.pdf")
"""
import os
import io
import logging
from datetime import datetime, date
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie

# Matplotlib para gráficos
import matplotlib
matplotlib.use('Agg')  # Backend no-interactivo
import matplotlib.pyplot as plt

# PIL para imágenes
from PIL import Image as PILImage

# Configurar logging
logger = logging.getLogger(__name__)


class PDFStyles:
    """
    Colección de estilos para reportes PDF.
    
    Define colores, fuentes y estilos consistentes para toda la aplicación.
    """
    
    # Colores corporativos
    PRIMARY_COLOR = colors.HexColor('#2c3e50')
    SECONDARY_COLOR = colors.HexColor('#3498db')
    ACCENT_COLOR = colors.HexColor('#27ae60')
    WARNING_COLOR = colors.HexColor('#f39c12')
    DANGER_COLOR = colors.HexColor('#e74c3c')
    TEXT_COLOR = colors.HexColor('#2c3e50')
    LIGHT_GRAY = colors.HexColor('#ecf0f1')
    DARK_GRAY = colors.HexColor('#95a5a6')
    
    # Fuentes
    FONT_TITLE = 'Helvetica-Bold'
    FONT_HEADING = 'Helvetica-Bold'
    FONT_BODY = 'Helvetica'
    FONT_MONO = 'Courier'
    
    def __init__(self):
        """Inicializa y configura todos los estilos."""
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Configura estilos personalizados."""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontName=self.FONT_TITLE,
            fontSize=24,
            textColor=self.PRIMARY_COLOR,
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontName=self.FONT_HEADING,
            fontSize=16,
            textColor=self.PRIMARY_COLOR,
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Estilo para subtítulos 3
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontName=self.FONT_HEADING,
            fontSize=13,
            textColor=self.SECONDARY_COLOR,
            spaceAfter=10,
            spaceBefore=10
        ))
        
        # Estilo para texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontName=self.FONT_BODY,
            fontSize=10,
            textColor=self.TEXT_COLOR,
            spaceAfter=6
        ))
        
        # Estilo para texto pequeño
        self.styles.add(ParagraphStyle(
            name='SmallText',
            parent=self.styles['Normal'],
            fontName=self.FONT_BODY,
            fontSize=8,
            textColor=self.DARK_GRAY,
            spaceAfter=3
        ))
        
        # Estilo para números (moneda)
        self.styles.add(ParagraphStyle(
            name='MoneyPositive',
            fontName=self.FONT_BODY,
            fontSize=10,
            textColor=self.ACCENT_COLOR,
            alignment=TA_RIGHT
        ))
        
        self.styles.add(ParagraphStyle(
            name='MoneyNegative',
            fontName=self.FONT_BODY,
            fontSize=10,
            textColor=self.DANGER_COLOR,
            alignment=TA_RIGHT
        ))


class PDFReportGenerator:
    """
    Generador de reportes PDF profesionales.
    
    Esta clase proporciona métodos para crear diferentes tipos de reportes
    financieros con formato profesional y visualmente atractivo.
    
    Attributes:
        styles: Colección de estilos para el reporte
        page_size: Tamaño de página (por defecto A4)
        margins: Márgenes de la página
    
    Example:
        >>> generator = PDFReportGenerator()
        >>> generator.generar_reporte_anual(
        ...     persona_id=1,
        ...     anio=2024,
        ...     output_path="reporte_2024.pdf",
        ...     incluir_graficos=True
        ... )
    """
    
    def __init__(self, page_size=A4, margins: Tuple[float, float] = (2*cm, 2*cm)):
        """
        Inicializa el generador de reportes.
        
        Args:
            page_size: Tamaño de página (A4, letter, etc.)
            margins: Tupla (horizontal, vertical) en cm
        """
        self.styles = PDFStyles()
        self.page_size = page_size
        self.margins = margins
        self.temp_images = []  # Lista de imágenes temporales a limpiar
        
        logger.info("PDFReportGenerator inicializado")
    
    def generar_reporte_mensual(
        self,
        persona_id: int,
        persona_nombre: str,
        anio: int,
        mes: int,
        movimientos: List[Dict],
        resumen: Dict,
        output_path: str,
        incluir_graficos: bool = True
    ) -> str:
        """
        Genera un reporte mensual completo.
        
        Args:
            persona_id: ID de la persona
            persona_nombre: Nombre completo de la persona
            anio: Año del reporte
            mes: Mes del reporte (1-12)
            movimientos: Lista de movimientos del mes
            resumen: Diccionario con totales y estadísticas
            output_path: Ruta donde guardar el PDF
            incluir_graficos: Si True, incluye gráficos visuales
            
        Returns:
            Ruta al archivo PDF generado
        """
        logger.info(f"Generando reporte mensual: {mes}/{anio} para {persona_nombre}")
        
        # Crear documento
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self.page_size,
            rightMargin=self.margins[0],
            leftMargin=self.margins[0],
            topMargin=self.margins[1],
            bottomMargin=self.margins[1]
        )
        
        # Contenedor de elementos
        elements = []
        
        # 1. PORTADA
        elements.extend(self._crear_portada(
            persona_nombre, f"Reporte Mensual - {self._nombre_mes(mes)} {anio}"
        ))
        
        elements.append(PageBreak())
        
        # 2. RESUMEN EJECUTIVO
        elements.extend(self._crear_resumen_ejecutivo(resumen))
        
        # 3. GRÁFICOS (si se solicitan)
        if incluir_graficos:
            elements.extend(self._crear_graficos(resumen))
        
        # 4. TABLA DE MOVIMIENTOS
        elements.extend(self._crear_tabla_movimientos(movimientos))
        
        # 5. ANÁLISIS Y RECOMENDACIONES
        elements.extend(self._crear_analisis(resumen))
        
        # 6. PIE DE PÁGINA
        elements.extend(self._crear_footer())
        
        # Construir PDF
        try:
            doc.build(elements)
            logger.info(f"Reporte generado exitosamente: {output_path}")
            
            # Limpiar imágenes temporales
            self._limpiar_temporales()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generando PDF: {e}")
            self._limpiar_temporales()
            raise
    
    def generar_reporte_anual(
        self,
        persona_id: int,
        persona_nombre: str,
        anio: int,
        datos_mensuales: List[Dict],
        resumen_anual: Dict,
        output_path: str
    ) -> str:
        """
        Genera un reporte anual completo con análisis comparativo.
        
        Args:
            persona_id: ID de la persona
            persona_nombre: Nombre completo
            anio: Año del reporte
            datos_mensuales: Lista con datos de cada mes
            resumen_anual: Totales y estadísticas del año
            output_path: Ruta de salida
            
        Returns:
            Ruta al PDF generado
        """
        logger.info(f"Generando reporte anual {anio} para {persona_nombre}")
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self.page_size,
            rightMargin=self.margins[0],
            leftMargin=self.margins[0],
            topMargin=self.margins[1],
            bottomMargin=self.margins[1]
        )
        
        elements = []
        
        # Portada
        elements.extend(self._crear_portada(
            persona_nombre, f"Reporte Anual {anio}"
        ))
        elements.append(PageBreak())
        
        # Resumen anual
        elements.extend(self._crear_resumen_anual(resumen_anual))
        
        # Gráfico de evolución mensual
        elements.extend(self._crear_grafico_evolucion_anual(datos_mensuales))
        
        # Tabla mensual
        elements.extend(self._crear_tabla_mensual(datos_mensuales))
        
        # Análisis anual
        elements.extend(self._crear_analisis_anual(datos_mensuales, resumen_anual))
        
        # Footer
        elements.extend(self._crear_footer())
        
        doc.build(elements)
        self._limpiar_temporales()
        
        return output_path
    
    def _crear_portada(self, persona_nombre: str, titulo: str) -> List:
        """Crea la portada del reporte."""
        elements = []
        
        # Espacio superior
        elements.append(Spacer(1, 2*inch))
        
        # Título principal
        elements.append(Paragraph(
            "Finanzas Personales",
            self.styles.styles['CustomTitle']
        ))
        
        # Subtítulo
        elements.append(Paragraph(
            titulo,
            self.styles.styles['CustomHeading2']
        ))
        
        # Línea decorativa
        elements.append(Spacer(1, 0.5*inch))
        elements.append(HRFlowable(
            width="60%",
            thickness=2,
            color=self.styles.PRIMARY_COLOR,
            spaceBefore=10,
            spaceAfter=10,
            hAlign='CENTER'
        ))
        
        # Nombre de la persona
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph(
            f"<b>Generado para:</b> {persona_nombre}",
            self.styles.styles['CustomHeading3']
        ))
        
        # Fecha de generación
        elements.append(Paragraph(
            f"<b>Fecha:</b> {datetime.now().strftime('%d de %B de %Y')}",
            self.styles.styles['CustomBody']
        ))
        
        # Versión
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(
            "Generado por Finanzas Personales v0.1.0",
            self.styles.styles['SmallText']
        ))
        
        return elements
    
    def _crear_resumen_ejecutivo(self, resumen: Dict) -> List:
        """Crea la sección de resumen ejecutivo."""
        elements = []
        
        elements.append(Paragraph(
            "Resumen Ejecutivo",
            self.styles.styles['CustomHeading2']
        ))
        
        # Tabla de totales
        data = [
            ['Concepto', 'Monto'],
            ['Total Ingresos', f"${resumen.get('total_ingresos', 0):,.2f}"],
            ['Total Gastos', f"${resumen.get('total_gastos', 0):,.2f}"],
            ['Saldo Neto', f"${resumen.get('saldo', 0):,.2f}"],
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.styles.PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), self.styles.LIGHT_GRAY),
            ('GRID', (0, 0), (-1, -1), 1, self.styles.DARK_GRAY),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _crear_graficos(self, resumen: Dict) -> List:
        """Crea gráficos usando matplotlib y los integra al PDF."""
        elements = []
        
        elements.append(Paragraph(
            "Distribución de Gastos",
            self.styles.styles['CustomHeading3']
        ))
        
        # Crear gráfico de pastel con matplotlib
        if 'gastos_por_categoria' in resumen:
            fig, ax = plt.subplots(figsize=(6, 4))
            
            categorias = [g['nombre'] for g in resumen['gastos_por_categoria'][:5]]
            valores = [g['total'] for g in resumen['gastos_por_categoria'][:5]]
            colores = [g['color'] for g in resumen['gastos_por_categoria'][:5]]
            
            ax.pie(valores, labels=categorias, colors=colores, autopct='%1.1f%%')
            ax.set_title('Top 5 Categorías de Gasto')
            
            # Guardar en buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            
            # Agregar al PDF
            img = Image(buf, width=5*inch, height=3.5*inch)
            elements.append(img)
            
            plt.close(fig)
            buf.close()
        
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _crear_tabla_movimientos(self, movimientos: List[Dict]) -> List:
        """Crea la tabla detallada de movimientos."""
        elements = []
        
        elements.append(Paragraph(
            "Detalle de Movimientos",
            self.styles.styles['CustomHeading2']
        ))
        
        # Encabezados
        data = [['Fecha', 'Tipo', 'Categoría', 'Descripción', 'Monto']]
        
        # Datos
        for mov in movimientos[:50]:  # Limitar a 50 por página
            data.append([
                mov.get('fecha', ''),
                mov.get('tipo', ''),
                mov.get('categoria', ''),
                mov.get('descripcion', '')[:30],  # Truncar descripción
                f"${mov.get('monto', 0):,.2f}"
            ])
        
        if len(movimientos) > 50:
            data.append(['...', '...', '...', f'Y {len(movimientos) - 50} más...', ''])
        
        # Crear tabla
        table = Table(data, colWidths=[1*inch, 0.8*inch, 1.2*inch, 2*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.styles.SECONDARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, self.styles.DARK_GRAY),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.styles.LIGHT_GRAY]),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _crear_analisis(self, resumen: Dict) -> List:
        """Crea sección de análisis y recomendaciones."""
        elements = []
        
        elements.append(Paragraph(
            "Análisis y Recomendaciones",
            self.styles.styles['CustomHeading2']
        ))
        
        # Generar insights automáticos
        insights = []
        
        if resumen.get('total_gastos', 0) > resumen.get('total_ingresos', 0):
            insights.append("⚠️ <b>Alerta:</b> Los gastos superan los ingresos este mes.")
        
        if resumen.get('saldo', 0) > 0:
            porcentaje_ahorro = (resumen['saldo'] / resumen.get('total_ingresos', 1)) * 100
            if porcentaje_ahorro >= 20:
                insights.append(f"✅ <b>Excelente:</b> Estás ahorrando el {porcentaje_ahorro:.1f}% de tus ingresos.")
            elif porcentaje_ahorro >= 10:
                insights.append(f"✓ <b>Buen trabajo:</b> Estás ahorrando el {porcentaje_ahorro:.1f}% de tus ingresos.")
            else:
                insights.append(f"ℹ️ Estás ahorrando el {porcentaje_ahorro:.1f}% de tus ingresos. Intenta llegar al 20%.")
        
        # Mostrar insights
        for insight in insights:
            elements.append(Paragraph(
                insight,
                self.styles.styles['CustomBody']
            ))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _crear_footer(self) -> List:
        """Crea el pie de página del reporte."""
        elements = []
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(HRFlowable(
            width="100%",
            thickness=1,
            color=self.styles.DARK_GRAY
        ))
        elements.append(Paragraph(
            f"Reporte generado el {datetime.now().strftime('%d/%m/%Y %H:%M')} | "
            "Finanzas Personales - Aplicación de Gestión Financiera",
            self.styles.styles['SmallText']
        ))
        
        return elements
    
    def _nombre_mes(self, mes: int) -> str:
        """Retorna el nombre del mes en español."""
        meses = [
            '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        return meses[mes]
    
    def _limpiar_temporales(self):
        """Limpia archivos temporales creados durante la generación."""
        for temp_file in self.temp_images:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.debug(f"Archivo temporal eliminado: {temp_file}")
            except Exception as e:
                logger.warning(f"No se pudo eliminar temporal {temp_file}: {e}")
        
        self.temp_images = []


# Función de conveniencia
def generar_reporte_mensual_pdf(
    persona_id: int,
    persona_nombre: str,
    anio: int,
    mes: int,
    movimientos: List[Dict],
    resumen: Dict,
    output_path: str
) -> str:
    """
    Función de conveniencia para generar reporte mensual.
    
    Args:
        persona_id: ID de la persona
        persona_nombre: Nombre completo
        anio: Año
        mes: Mes (1-12)
        movimientos: Lista de movimientos
        resumen: Diccionario con totales
        output_path: Ruta de salida
        
    Returns:
        Ruta al PDF generado
    """
    generator = PDFReportGenerator()
    return generator.generar_reporte_mensual(
        persona_id=persona_id,
        persona_nombre=persona_nombre,
        anio=anio,
        mes=mes,
        movimientos=movimientos,
        resumen=resumen,
        output_path=output_path
    )
