"""Constantes del dashboard. Cambiar un valor aquí no requiere tocar la interfaz."""
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PAGE_CONFIG = dict(
    page_title="Market Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📈",
)

AVAILABLE_SPIDERS = ["linkedin", "computrabajo"]
DEFAULT_SPIDERS = ["linkedin"]
CONTINENT_PLACEHOLDER = "Selecciona un Continente"
ALL_COUNTRIES = "Todos los Países"
ALL = "Todos"
UNKNOWN = "Desconocido"

DATA_CACHE_TTL_SECONDS = 3600
AI_REPORT_CACHE_TTL_SECONDS = 3600
AI_SAMPLE_SIZE = 50
MIN_FILTER_DATE = datetime.date(2023, 1, 1)

# Paleta (coherente con el portafolio): turquesa, azul, violeta, ámbar, coral
KPI_COLORS = ['#75E6CE', '#88B7FF', '#C99BFF', '#F8D66D', '#FF8A80']
VIBRANT_COLORS = ['#75E6CE', '#88B7FF', '#C99BFF', '#F8D66D', '#FF8A80',
                  '#5BC0EB', '#9BE564', '#F49AC2', '#B8C1EC', '#FFB870']
SEQUENTIAL_SCALE = ['#1B2A44', '#2E5E7E', '#3FA3A8', '#75E6CE']
TEXT_COLOR = '#E6ECF5'
MUTED_COLOR = '#93A1BD'
GRID_COLOR = 'rgba(147,161,189,0.15)'

JOB_DATE_COLUMNS = ['posted_date', 'scraped_at']
JOB_TEXT_COLUMNS = [
    'title', 'company_name', 'location', 'country', 'sector', 'job_type',
    'seniority_level', 'source_platform', 'role_category', 'salary_range',
    'company_size', 'company_industry', 'company_hq_country', 'company_type', 'company_website',
    'id', 'job_id', 'source_url', 'company_id',
    'description', 'requirements', 'skills',
]
TREND_REQUIRED_COLUMNS = ['date', 'metric_name', 'metric_value', 'count', 'sector', 'country']
TREND_TEXT_COLUMNS = ['metric_name', 'metric_value', 'sector', 'country']
DISPLAY_COLUMNS = [
    'title', 'company_name', 'location', 'country', 'source_platform',
    'seniority_level', 'role_category', 'sector', 'salary_range',
    'posted_date', 'scraped_at', 'source_url', 'skills',
]
AI_SAMPLE_COLUMNS = ['title', 'company_name', 'sector', 'location', 'source_platform']
