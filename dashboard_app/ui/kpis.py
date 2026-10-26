"""Tarjetas de indicadores clave."""
import streamlit as st

from dashboard_app import config
from dashboard_app.data.processing import kpi_summary

_CARDS = [  # (clave en kpi_summary, etiqueta, texto pequeño)
    ('total', 'Vacantes Filtradas', False),
    ('companies', 'Empresas Únicas', False),
    ('last_update', 'Última Actualización', True),
    ('new_today', 'Nuevas Vacantes (Hoy)', False),
    ('avg_age', 'Edad Promedio Vacantes', True),
]


def _card(value, label, color, small):
    return (f'<div class="metric-card" style="--kpi: {color}">'
            f'<p class="label">{label}</p>'
            f'<p class="value{" small" if small else ""}">{value}</p></div>')


def render_kpis(df):
    st.markdown("---")
    st.header("📈 Métricas Clave del Mercado Laboral")
    summary = kpi_summary(df)
    with st.container():
        for col, (key, label, small), color in zip(st.columns(len(_CARDS)), _CARDS, config.KPI_COLORS):
            with col:
                st.markdown(_card(summary[key], label, color, small), unsafe_allow_html=True)
