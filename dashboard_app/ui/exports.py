"""Descarga de datos en CSV y Excel."""
from io import BytesIO

import pandas as pd
import streamlit as st

from dashboard_app.data.processing import skills_to_text


def jobs_to_csv(df: pd.DataFrame) -> bytes:
    out = df.copy()
    if 'skills' in out.columns:
        out['skills'] = out['skills'].apply(lambda x: skills_to_text(x, fallback=None))
    return out.to_csv(index=False).encode('utf-8')


def jobs_to_excel(df: pd.DataFrame) -> BytesIO:
    out = df.copy()
    if 'skills' in out.columns:
        out['skills'] = out['skills'].apply(skills_to_text)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        out.to_excel(writer, index=False, sheet_name='Job Data')
    buffer.seek(0)
    return buffer


def render_exports(jobs: pd.DataFrame, trends: pd.DataFrame, columns) -> None:
    st.markdown("---")
    st.header("⬇️ Descargar Datos")
    if jobs.empty:
        st.info("No hay datos de vacantes para descargar.")
    else:
        st.download_button("📥 Descargar datos de Vacantes como CSV", jobs_to_csv(jobs[columns]),
                           file_name="job_market_data.csv", mime="text/csv", key="download_csv_tab")
        st.download_button("📥 Descargar datos de Vacantes como Excel", jobs_to_excel(jobs[columns]),
                           file_name="job_market_data.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           key="download_excel_tab")
    if not trends.empty:
        st.download_button("📥 Descargar datos de Tendencias como CSV", trends.to_csv(index=False).encode('utf-8'),
                           file_name="job_trends_data.csv", mime="text/csv", key="download_csv_trends_tab")
