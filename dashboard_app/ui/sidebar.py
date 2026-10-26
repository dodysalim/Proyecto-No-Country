"""Barra lateral: acciones (scraping, tendencias, mantenimiento) y filtros de visualización."""
import datetime
import time

import streamlit as st

from config.geo import COMMON_GEO_DATA
from dashboard_app import config
from dashboard_app.data.processing import ViewFilters
from dashboard_app.services.commands import (ScrapeRequest, build_scrape_command, build_trends_command,
                                             run_in_project, scrape_saved_data)


def _refresh(data_cache) -> None:
    data_cache.clear()
    time.sleep(1)
    st.rerun()


def _scraper_controls(data_cache) -> None:
    st.subheader("Configuración del Scraper")
    spiders = st.multiselect("Scrapers a Ejecutar", options=config.AVAILABLE_SPIDERS, default=config.DEFAULT_SPIDERS,
                             help="Selecciona uno o más scrapers para ejecutar.")
    continent = st.selectbox("Continente para Scrapear", [config.CONTINENT_PLACEHOLDER] + list(COMMON_GEO_DATA),
                             key="scrape_continent")
    countries = [] if continent == config.CONTINENT_PLACEHOLDER else [config.ALL_COUNTRIES] + COMMON_GEO_DATA[continent]
    country = st.selectbox("País para Scrapear", countries, key="scrape_country")
    today = datetime.date.today()
    start = st.date_input("Fecha de Inicio de Vacantes", value=today - datetime.timedelta(days=7), key="scrape_start_date")
    end = st.date_input("Fecha de Fin de Vacantes", value=today, key="scrape_end_date")
    max_jobs = st.number_input("Número máximo de vacantes por scraper", min_value=1, value=100, step=10,
                               help="El número máximo de vacantes que cada scraper intentará obtener.")

    if not st.button("🔄 Ejecutar Scrapers", type="primary", use_container_width=True, key='run_scraper_btn'):
        return
    if continent == config.CONTINENT_PLACEHOLDER:
        return st.error("Por favor, selecciona un continente para ejecutar el scraper.")
    if not spiders:
        return st.error("Por favor, selecciona al menos un scraper para ejecutar.")
    with st.spinner(f"Extrayendo vacantes ({', '.join(spiders)})... (Esto puede tardar varios minutos por scraper/seguridad)"):
        try:
            result = run_in_project(build_scrape_command(ScrapeRequest(spiders, continent, country, start, end, max_jobs)))
        except Exception as e:
            return st.error(f"Error ejecutando el scraper: {e}")
    logs = result.stderr + "\n" + result.stdout
    if result.returncode != 0:
        st.error("❌ Error en el proceso de scraping")
        return st.text_area("Log de Error", logs, height=200)
    st.success("✅ Proceso de scraping finalizado")
    if scrape_saved_data(logs):
        st.info("📊 Nuevos datos guardados en Supabase.")
    else:
        st.warning("⚠️ El scraper terminó, pero no se encontraron logs de datos guardados. Revisa los detalles.")
    with st.expander("Ver Detalles del Proceso"):
        st.code(logs)
    _refresh(data_cache)


def _trend_controls(data_cache) -> None:
    st.markdown("---")
    st.subheader("📈 Generar Análisis de Tendencias")
    st.write("Calcula métricas de tendencias (habilidades, roles, etc.) y las almacena en la base de datos.")
    if not st.button("✨ Ejecutar Análisis de Tendencias", type="secondary", use_container_width=True,
                     key='run_trend_analysis_btn'):
        return
    with st.spinner("Analizando tendencias y almacenando en Supabase..."):
        try:
            result = run_in_project(build_trends_command())
        except Exception as e:
            return st.error(f"Error ejecutando el análisis de tendencias: {e}")
    if result.returncode != 0:
        st.error("❌ Error al ejecutar el análisis de tendencias.")
        return st.text_area("Log de Error del Análisis", result.stderr, height=200)
    st.success("✅ Análisis de tendencias finalizado y almacenado.")
    st.info("Refresca el dashboard para ver las nuevas visualizaciones de tendencias.")
    with st.expander("Ver Logs del Análisis"):
        st.code(result.stdout + result.stderr)
    _refresh(data_cache)


def _maintenance_controls(repo_factory, data_cache) -> None:
    st.markdown("---")
    st.subheader("⚠️ Mantenimiento de Datos")
    if st.button("🗑️ Limpiar Base de Datos", type="secondary", use_container_width=True, key="clear_db_only_btn"):
        st.session_state['confirm_clear_only_db'] = True
    if not st.session_state.get('confirm_clear_only_db'):
        return
    st.warning("¿Estás seguro de que quieres ELIMINAR TODOS los datos de las tablas 'jobs', 'skills', 'companies' y 'trends'? Esta acción es irreversible.")
    st.info("⚠️ Asegúrate de que tu clave de Supabase tenga **permisos de `delete`** y que no haya políticas de RLS que impidan la eliminación.")
    yes, no = st.columns(2)
    if yes.button("Sí, Eliminar Datos", key="confirm_clear_yes_action"):
        st.session_state['confirm_clear_only_db'] = False
        if repo_factory().clear_all():
            st.success("✅ Base de datos (tablas 'jobs', 'skills', 'companies', 'trends') limpiada exitosamente.")
            _refresh(data_cache)
        else:
            st.error("❌ No se pudo limpiar la base de datos. Por favor, revisa los logs y los permisos de Supabase.")
            time.sleep(1)
            st.rerun()
    if no.button("No, Cancelar", key="confirm_clear_no_action"):
        st.info("Acción cancelada.")
        st.session_state['confirm_clear_only_db'] = False
        st.rerun()


def _view_filters() -> ViewFilters:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filtros de Visualización")
    continent = st.sidebar.selectbox("Filtrar por Continente", [config.ALL] + list(COMMON_GEO_DATA),
                                     key="filter_continent_display")
    countries = [config.ALL] + (COMMON_GEO_DATA.get(continent, []) if continent != config.ALL else [])
    country = st.sidebar.selectbox("Filtrar por País", countries, key="filter_country_display")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Rango de Fechas")
    today = datetime.date.today()
    bounds = dict(min_value=config.MIN_FILTER_DATE, max_value=today)
    start = st.sidebar.date_input("Desde:", value=config.MIN_FILTER_DATE, key="filter_start_date_display", **bounds)
    end = st.sidebar.date_input("Hasta:", value=today, key="filter_end_date_display", **bounds)
    if start > end:
        st.sidebar.error("La fecha de inicio no puede ser posterior a la fecha de fin.")
    return ViewFilters(continent, country, start, end)


def render_sidebar(repo_factory, data_cache) -> ViewFilters:
    st.sidebar.header("⚙️ Panel de Control")
    with st.sidebar:
        st.subheader("⚡ Acciones Rápidas")
        _scraper_controls(data_cache)
        _trend_controls(data_cache)
        _maintenance_controls(repo_factory, data_cache)
    return _view_filters()
