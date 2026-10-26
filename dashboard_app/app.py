"""Composición del dashboard: conecta datos, servicios y componentes."""
import logging

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from config.geo import COMMON_GEO_DATA
from dashboard_app import config
from dashboard_app.data.processing import apply_filters, latest_trends
from dashboard_app.data.repository import JobMarketRepository, SupabaseJobRepository
from dashboard_app.services.cache import TimedCache
from dashboard_app.services.market_data import load_market_data
from dashboard_app.styles import CSS, HERO
from dashboard_app.ui.ai_report import render_ai_report
from dashboard_app.ui.kpis import render_kpis
from dashboard_app.ui.sidebar import render_sidebar
from dashboard_app.ui.tabs import TabContext, render_tabs


def _safe_load(repo_factory):
    try:
        return load_market_data(repo_factory())
    except Exception as e:  # sin credenciales o sin conexión, la app sigue abierta
        st.error(f"❌ Error al conectar o cargar datos de Supabase: {e}")
        return pd.DataFrame(), pd.DataFrame()


def run(repo_factory=SupabaseJobRepository) -> None:
    """Punto de entrada. `repo_factory` permite inyectar otra fuente de datos."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    load_dotenv()
    st.set_page_config(**config.PAGE_CONFIG)
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HERO, unsafe_allow_html=True)

    data_cache = TimedCache(st.session_state, 'data_cache', config.DATA_CACHE_TTL_SECONDS)
    filters = render_sidebar(repo_factory, data_cache)
    jobs, trends = data_cache.get_or_load(lambda: _safe_load(repo_factory))

    filtered = apply_filters(jobs, filters, COMMON_GEO_DATA, warn=st.warning)
    recent_trends, latest_date = latest_trends(trends, warn=st.warning)

    if filtered.empty:
        st.info("La base de datos está vacía o no hay datos que coincidan con los filtros aplicados. "
                "Ejecuta los scrapers para obtener datos y refrescar el dashboard.")
        return
    render_kpis(filtered)
    render_ai_report(filtered)
    render_tabs(TabContext(filtered, recent_trends, latest_date))
