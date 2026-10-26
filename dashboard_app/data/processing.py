"""Transformaciones puras de vacantes y tendencias (sin Streamlit, fáciles de probar)."""
import datetime
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from dashboard_app import config


@dataclass(frozen=True)
class ViewFilters:
    """Filtros elegidos por el usuario en la barra lateral."""
    continent: str = config.ALL
    country: str = config.ALL
    start_date: datetime.date = config.MIN_FILTER_DATE
    end_date: datetime.date = datetime.date.today()


def flatten_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Serializa listas/diccionarios a JSON y normaliza nulos antes de crear el DataFrame."""
    cleaned = []
    for record in records:
        row = {}
        for key, value in record.items():
            if isinstance(value, (list, dict)):
                row[key] = json.dumps(value, ensure_ascii=False)
            elif value is None or pd.isna(value):
                row[key] = None
            else:
                row[key] = value
        cleaned.append(row)
    return cleaned


def _as_text(series: pd.Series) -> pd.Series:
    return series.astype(str).replace('nan', config.UNKNOWN).replace('None', config.UNKNOWN)


def prepare_jobs(records: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    """Convierte registros crudos de vacantes en un DataFrame tipado y ordenado."""
    rows = flatten_records(records)
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)

    for col in config.JOB_DATE_COLUMNS:
        if col in df.columns:
            parsed = pd.to_datetime(df[col], errors='coerce', utc=True)
            if pd.api.types.is_datetime64_any_dtype(parsed) and parsed.dt.tz is not None:
                df[col] = parsed.dt.tz_localize(None)
            else:
                df[col] = parsed

    for col in config.JOB_TEXT_COLUMNS:
        df[col] = _as_text(df[col]) if col in df.columns else config.UNKNOWN

    df['is_active'] = df['is_active'].fillna(False).astype(bool) if 'is_active' in df.columns else False
    return df.sort_values('scraped_at', ascending=False)


def prepare_trends(records: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    """Convierte registros crudos de tendencias en un DataFrame tipado y ordenado."""
    rows = flatten_records(records)
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    for col in config.TREND_REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None
    for col in config.TREND_TEXT_COLUMNS:
        df[col] = _as_text(df[col])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['count'] = pd.to_numeric(df['count'], errors='coerce').fillna(0).astype(int)
    return df.sort_values('date', ascending=False)


def parse_skills(value: Any) -> list:
    """Lee la columna `skills` serializada; devuelve [] si no es una lista JSON válida."""
    try:
        if isinstance(value, str) and value.strip() and value != config.UNKNOWN:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
    except (json.JSONDecodeError, ValueError):
        pass
    return []


def skills_to_text(value: Any, fallback: str = '') -> str:
    """Convierte una lista de habilidades ({'skill_name': ...} o texto) en 'a, b, c'."""
    if not isinstance(value, list):
        return fallback if fallback is not None else str(value)
    return ", ".join(s.get('skill_name', str(s)) if isinstance(s, dict) else str(s) for s in value)


def apply_filters(df: pd.DataFrame, filters: ViewFilters, geo: Dict[str, List[str]],
                  warn=lambda msg: None) -> pd.DataFrame:
    """Aplica continente, país y rango de fechas. `warn` recibe avisos para la UI."""
    out = df.copy()
    if out.empty:
        return out
    if 'skills' in out.columns:
        out['skills'] = out['skills'].apply(parse_skills)

    has_country = 'country' in out.columns
    if filters.continent != config.ALL:
        if has_country:
            allowed = [c.lower() for c in geo.get(filters.continent, [])]
            out = out[out['country'].str.lower().isin(allowed)]
        else:
            warn("La columna 'country' no está disponible en los datos para filtrar por continente.")

    if filters.country != config.ALL:
        if has_country:
            out = out[out['country'].str.contains(filters.country, case=False, na=False)]
        else:
            warn("La columna 'country' no está disponible en los datos para filtrar por país.")

    if 'posted_date' in out.columns and pd.api.types.is_datetime64_any_dtype(out['posted_date']):
        dates = out['posted_date'].dt.date
        out = out[(dates >= filters.start_date) & (dates <= filters.end_date)]
    else:
        warn("La columna 'posted_date' no es de tipo fecha o no existe, el filtro de rango de fechas no se aplicará.")
    return out


def latest_trends(df_trends: pd.DataFrame, warn=lambda msg: None):
    """Devuelve (tendencias de la fecha más reciente, esa fecha)."""
    out = df_trends.copy()
    if out.empty:
        return out, None
    if 'date' not in out.columns or out['date'].empty:
        warn("La columna 'date' no está disponible en los datos de tendencias para filtrar por la fecha más reciente.")
        return out, None
    latest = out['date'].max()
    return out[out['date'] == latest], latest


def source_label(platforms: Iterable[str]) -> str:
    """'Fuente: LinkedIn' / 'Fuentes: LinkedIn y CompuTrabajo' para el reporte de IA."""
    names = []
    for source in platforms:
        if not source or source == config.UNKNOWN:
            continue
        low = source.lower()
        names.append('LinkedIn' if 'linkedin' in low else 'CompuTrabajo' if 'computrabajo' in low else source)
    if not names:
        return ""
    if len(names) == 1:
        return f"Fuente: {names[0]}"
    return f"Fuentes: {', '.join(names[:-1])} y {names[-1]}"


def kpi_summary(df: pd.DataFrame, today: Optional[datetime.date] = None,
                now: Optional[datetime.datetime] = None) -> Dict[str, Any]:
    """Calcula los cinco indicadores principales."""
    today = today or datetime.date.today()
    now = now or datetime.datetime.now()
    has_posted = 'posted_date' in df.columns and df['posted_date'].notna().any()
    has_scraped = 'scraped_at' in df.columns and df['scraped_at'].notna().any()
    return {
        'total': len(df),
        'companies': df['company_name'].nunique() if 'company_name' in df.columns else 0,
        'last_update': df['scraped_at'].max().strftime("%Y-%m-%d %H:%M") if has_scraped else "N/A",
        'new_today': int((df['posted_date'].dt.date == today).sum()) if has_posted else 0,
        'avg_age': f"{(now.replace(tzinfo=None) - df['posted_date']).dt.days.mean():.1f} días" if has_posted else "N/A",
    }
