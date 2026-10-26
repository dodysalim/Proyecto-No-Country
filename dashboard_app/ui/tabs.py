"""Pestañas de análisis.

Cada pestaña es una función `render(ctx)` registrada en `TABS`. Para añadir una vista
nueva basta con escribir su función y agregarla a la lista (abierto a extensión,
cerrado a modificación).
"""
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

import pandas as pd
import streamlit as st

from dashboard_app.ui.charts import counts, donut, hbar
from dashboard_app.ui.exports import render_exports
from dashboard_app.data.processing import skills_to_text
from dashboard_app import config


@dataclass
class TabContext:
    jobs: pd.DataFrame
    trends: pd.DataFrame
    latest_date: Optional[pd.Timestamp]


def _show(fig):
    st.plotly_chart(fig, width='stretch')


def _has(df: pd.DataFrame, col: str) -> bool:
    return col in df.columns and not df[col].empty


def _pie_and_bar(data, label, value, pie_title, bar_title, scale, bar_labels, pie_rows=None, bar_rows=None):
    left, right = st.columns(2)
    with left:
        _show(donut(data.head(pie_rows) if pie_rows else data, value, label, pie_title))
    with right:
        _show(hbar(data.head(bar_rows) if bar_rows else data, value, label, bar_title, scale, bar_labels))


def sector_tab(ctx):
    st.subheader("📊 Distribución de Vacantes por Sector")
    if not _has(ctx.jobs, 'sector'):
        return st.info("No hay datos de sector disponibles para mostrar.")
    data = counts(ctx.jobs['sector'], 'Sector')
    _show(hbar(data.head(15), 'Número de Vacantes', 'Sector', '<b>Top Sectores con Vacantes</b>',
               config.SEQUENTIAL_SCALE, {'Número de Vacantes': 'Vacantes', 'Sector': 'Sector'},
               color_discrete_sequence=config.VIBRANT_COLORS))


def company_tab(ctx):
    st.subheader("🏆 Top Empresas con Vacantes")
    if not _has(ctx.jobs, 'company_name'):
        return st.info("No hay datos de empresa disponibles para mostrar.")
    top_n = st.slider("Top N Compañías", 5, 30, 15, key="top_companies_slider_tab")
    data = counts(ctx.jobs['company_name'], 'Empresa').head(top_n)
    _show(hbar(data, 'Número de Vacantes', 'Empresa', f'<b>Top {top_n} Compañías Contratando</b>',
               config.SEQUENTIAL_SCALE, {'Número de Vacantes': 'Vacantes', 'Empresa': 'Empresa'}))


def country_tab(ctx):
    st.subheader("🌍 Distribución de Vacantes por País")
    if not _has(ctx.jobs, 'country'):
        return st.info("No hay datos de país disponibles para mostrar.")
    _pie_and_bar(counts(ctx.jobs['country'], 'País'), 'País', 'Número de Vacantes',
                 '<b>Top 10 Países (Gráfico de Pie)</b>', '<b>Top 15 Países (Gráfico de Barras)</b>',
                 config.SEQUENTIAL_SCALE, {'Número de Vacantes': 'Vacantes', 'País': 'País'},
                 pie_rows=10, bar_rows=15)


def seniority_tab(ctx):
    st.subheader("📶 Distribución de Nivel de Experiencia")
    if not _has(ctx.jobs, 'seniority_level'):
        return st.info("No hay datos de nivel de experiencia disponibles para mostrar.")
    _pie_and_bar(counts(ctx.jobs['seniority_level'], 'Nivel de Seniority', 'Conteo'), 'Nivel de Seniority', 'Conteo',
                 '<b>Distribución por Seniority (Pie)</b>', '<b>Distribución por Seniority (Barras)</b>',
                 config.SEQUENTIAL_SCALE, {'Conteo': 'Vacantes', 'Nivel de Seniority': 'Seniority'})


def _trend_tab(subheader, metric, title, scale, value_label, axis_label, empty_msg):
    """Crea una pestaña que muestra el top de una métrica de tendencias."""
    def render(ctx):
        st.subheader(subheader)
        if ctx.trends.empty or not ctx.latest_date:
            return st.info("No hay datos de tendencias disponibles o están incompletos. Ejecuta el análisis de tendencias.")
        rows = ctx.trends[ctx.trends['metric_name'] == metric]
        if rows.empty:
            return st.info(empty_msg)
        top = rows.sort_values('count', ascending=False).head(15)
        _show(hbar(top, 'count', 'metric_value',
                   f'<b>{title}</b><br><sub>{ctx.latest_date.strftime("%Y-%m-%d")}</sub>',
                   scale, {'count': value_label, 'metric_value': axis_label}))
    return render


roles_tab = _trend_tab("👔 Roles Más Demandados (Tendencias)", 'most_demanded_role', 'Top Roles Más Demandados',
                       config.SEQUENTIAL_SCALE, 'Vacantes', 'Rol',
                       "No hay datos de tendencias de roles demandados. Ejecuta el análisis de tendencias.")
skills_demand_tab = _trend_tab("💡 Habilidades Más Demandadas", 'most_demanded_skill', 'Top Habilidades Más Demandadas',
                               config.SEQUENTIAL_SCALE, 'Vacantes', 'Habilidad',
                               "No hay datos de tendencias de habilidades demandadas. Ejecuta el análisis de tendencias.")
skills_growth_tab = _trend_tab("📈 Habilidades en Crecimiento", 'growing_skill', 'Top Habilidades en Crecimiento',
                               config.SEQUENTIAL_SCALE, 'Vacantes Actuales', 'Habilidad',
                               "No hay datos de tendencias de habilidades en crecimiento. Ejecuta el análisis de tendencias.")


def platform_sector_tab(ctx):
    st.subheader("🔌 Distribución por Plataforma y Sector")
    if not ('source_platform' in ctx.jobs.columns and 'sector' in ctx.jobs.columns and not ctx.jobs.empty):
        return st.info("No hay datos de plataforma o sector disponibles para mostrar.")
    data = ctx.jobs.groupby(['source_platform', 'sector']).size().reset_index(name='Conteo')
    _show(hbar(data, 'Conteo', 'sector', '<b>Vacantes por Plataforma y Sector</b>',
               labels={'Conteo': 'Vacantes', 'sector': 'Sector', 'source_platform': 'Plataforma'},
               color='source_platform'))


def platform_tab(ctx):
    st.subheader("📱 Distribución de Vacantes por Plataforma")
    if not _has(ctx.jobs, 'source_platform'):
        return st.info("No hay datos de plataforma disponibles para mostrar.")
    _pie_and_bar(counts(ctx.jobs['source_platform'], 'Plataforma'), 'Plataforma', 'Número de Vacantes',
                 '<b>Distribución por Plataforma (Pie)</b>', '<b>Distribución por Plataforma (Barras)</b>',
                 config.SEQUENTIAL_SCALE, {'Número de Vacantes': 'Vacantes', 'Plataforma': 'Plataforma'})


def raw_data_tab(ctx):
    st.subheader("📋 Datos Crudos de Vacantes")
    view = ctx.jobs.copy()
    if 'skills' in view.columns:
        view['skills'] = view['skills'].apply(skills_to_text)
    columns = [c for c in config.DISPLAY_COLUMNS if c in view.columns]
    st.dataframe(view[columns], width='stretch')

    st.markdown("---")
    st.subheader("📊 Datos Crudos de Tendencias")
    if not ctx.trends.empty:
        st.dataframe(ctx.trends, width='stretch')
    else:
        st.info("No hay datos de tendencias disponibles en la base de datos.")
    render_exports(ctx.jobs, ctx.trends, columns)


TABS: List[Tuple[str, Callable[[TabContext], None]]] = [
    ("🏢 Por Sector", sector_tab),
    ("👥 Por Empresa", company_tab),
    ("🌍 Por País", country_tab),
    ("📶 Por Seniority", seniority_tab),
    ("👔 Top Roles", roles_tab),
    ("💡 Skills Demandadas", skills_demand_tab),
    ("📈 Skills en Crecimiento", skills_growth_tab),
    ("🔌 Plataforma vs. Sector", platform_sector_tab),
    ("📱 Distribución por Plataforma", platform_tab),
    ("📋 Datos Crudos", raw_data_tab),
]


def render_tabs(ctx: TabContext) -> None:
    st.markdown("---")
    st.header("📊 Análisis de Tendencias y Distribución")
    for container, (_, render) in zip(st.tabs([label for label, _ in TABS]), TABS):
        with container:
            render(ctx)
