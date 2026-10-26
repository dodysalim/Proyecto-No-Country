"""Sección del reporte ejecutivo generado con IA."""
import os

import streamlit as st

from dashboard_app import config
from dashboard_app.data.processing import source_label
from dashboard_app.services.cache import TimedCache


def _quota_error(message: str) -> bool:
    return "429" in message or "quota" in message.lower()


def _sample(df):
    cols = df[config.AI_SAMPLE_COLUMNS]
    return cols.sample(config.AI_SAMPLE_SIZE, random_state=42) if len(df) > config.AI_SAMPLE_SIZE else cols


def render_ai_report(df, generator_factory=None) -> None:
    st.markdown("---")
    st.header("🧠 Reporte de Inteligencia Artificial")
    cache = TimedCache(st.session_state, 'ai_report_cache', config.AI_REPORT_CACHE_TTL_SECONDS)
    with st.expander("Generar y ver Reporte Diario de IA"):
        st.write("Genera un resumen ejecutivo de las tendencias actuales basándose en los datos filtrados.")
        if not os.getenv("GEMINI_API_KEY"):
            st.warning("⚠️ La API de Gemini no está configurada. El reporte de IA no puede ser generado.")
            return
        if not st.button("Generar Reporte de IA", type="primary", key="generate_ai_report_btn"):
            if cache.value and cache.is_fresh:
                st.success("📦 Reporte de IA cacheado disponible (generado hace menos de 1 hora)")
            elif cache.value:
                st.info("📦 Hay un reporte de IA cacheado disponible (expirado, pero usable)")
            st.info("Haz clic en el botón para generar un reporte con IA de los datos actuales.")
            return

        if generator_factory is None:
            from analysis.report_generator import ReportGenerator as generator_factory
        generator = generator_factory()
        if not getattr(generator, 'model', None):
            st.error("Error al inicializar el generador de reportes de IA. Revisa tu clave API o la inicialización del modelo.")
            return
        if cache.is_fresh:
            st.info("📦 Usando reporte de IA cacheado (generado hace menos de 1 hora)")
            st.subheader("📄 Resumen Ejecutivo")
            st.markdown(cache.value)
            return
        with st.spinner("Generando reporte de IA..."):
            try:
                platforms = df['source_platform'].unique() if 'source_platform' in df.columns else []
                report = generator.generate_daily_insight(_sample(df).to_dict('records'))
                cache.set(report)
                st.subheader("📄 Resumen Ejecutivo")
                label = source_label(platforms)
                if label:
                    st.markdown(f"**{label}**")
                st.markdown(report)
            except Exception as e:  # la API externa puede fallar de muchas formas
                if _quota_error(str(e)):
                    st.error("⚠️ **Cuota de Gemini API agotada.** Has alcanzado el límite de 20 peticiones/día.")
                    st.info("💡 Soluciones: 1) Espera 24h para reinicio, 2) Actualiza a plan de pago, 3) Revisa el reporte cacheado manualmente en estado de sesión.")
                    if cache.value:
                        st.success("📦 Mostrando último reporte cacheado:")
                        st.markdown(cache.value)
                else:
                    st.error(f"❌ Error generando reporte: {e}")
