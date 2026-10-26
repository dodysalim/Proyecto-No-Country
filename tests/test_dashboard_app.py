"""Pruebas de la lógica del dashboard (sin Streamlit ni Supabase)."""
import datetime
import json

import pandas as pd
import pytest

from dashboard_app import config
from dashboard_app.data.processing import (ViewFilters, apply_filters, flatten_records, kpi_summary,
                                           latest_trends, parse_skills, prepare_jobs, prepare_trends,
                                           skills_to_text, source_label)
from dashboard_app.data.repository import SupabaseJobRepository
from dashboard_app.services.cache import TimedCache
from dashboard_app.services.commands import ScrapeRequest, build_scrape_command, scrape_saved_data
from dashboard_app.services.market_data import load_market_data

GEO = {"Sudamérica": ["Colombia", "Ecuador"], "Europa": ["Spain"]}


def job(i, country, posted, skills=("Python",)):
    return {"id": i, "title": "Data Analyst", "company_name": f"E{i % 3}", "country": country,
            "posted_date": posted, "scraped_at": f"2026-10-2{i % 6}T10:00:00Z",
            "skills": [{"skill_name": s} for s in skills], "is_active": None}


@pytest.fixture
def jobs():
    return prepare_jobs([job(1, "Colombia", "2026-10-25T00:00:00Z"),
                         job(2, "Ecuador", "2026-09-01T00:00:00Z", ("SQL", "Excel")),
                         job(3, "Spain", "2026-10-26T00:00:00Z")])


def test_flatten_serializes_nested_values():
    row = flatten_records([{"a": [1, 2], "b": {"x": 1}, "c": None, "d": "ok"}])[0]
    assert json.loads(row["a"]) == [1, 2] and row["c"] is None and row["d"] == "ok"


def test_prepare_jobs_types_and_defaults(jobs):
    assert pd.api.types.is_datetime64_any_dtype(jobs["posted_date"])
    assert jobs["posted_date"].dt.tz is None
    assert (jobs["sector"] == config.UNKNOWN).all()          # columna ausente → 'Desconocido'
    assert jobs["is_active"].dtype == bool
    assert jobs["scraped_at"].is_monotonic_decreasing


def test_prepare_empty_inputs():
    assert prepare_jobs([]).empty and prepare_trends([]).empty


def test_parse_and_format_skills():
    assert parse_skills('[{"skill_name": "SQL"}]') == [{"skill_name": "SQL"}]
    assert parse_skills("no-json") == [] and parse_skills(config.UNKNOWN) == []
    assert skills_to_text([{"skill_name": "SQL"}, "Python"]) == "SQL, Python"
    assert skills_to_text("x") == "" and skills_to_text("x", fallback=None) == "x"


def test_filters_by_continent_country_and_dates(jobs):
    f = ViewFilters("Sudamérica", config.ALL, datetime.date(2026, 10, 1), datetime.date(2026, 10, 31))
    out = apply_filters(jobs, f, GEO)
    assert list(out["country"]) == ["Colombia"]
    assert out["skills"].iloc[0] == [{"skill_name": "Python"}]
    only_spain = apply_filters(jobs, ViewFilters(config.ALL, "spain", datetime.date(2026, 1, 1),
                                                 datetime.date(2026, 12, 31)), GEO)
    assert list(only_spain["country"]) == ["Spain"]


def test_filters_warn_when_columns_missing():
    warnings = []
    apply_filters(pd.DataFrame({"x": [1]}), ViewFilters("Europa", "Spain"), GEO, warn=warnings.append)
    assert len(warnings) == 3


def test_latest_trends_keeps_most_recent_date():
    trends = prepare_trends([{"date": "2026-10-01", "metric_name": "m", "metric_value": "a", "count": "3"},
                             {"date": "2026-10-20", "metric_name": "m", "metric_value": "b", "count": 5}])
    recent, date = latest_trends(trends)
    assert list(recent["metric_value"]) == ["b"] and date == pd.Timestamp("2026-10-20")
    assert trends["count"].dtype.kind == "i"


def test_source_label_variants():
    assert source_label(["linkedin"]) == "Fuente: LinkedIn"
    assert source_label(["linkedin_es", "computrabajo"]) == "Fuentes: LinkedIn y CompuTrabajo"
    assert source_label([config.UNKNOWN]) == ""


def test_kpi_summary(jobs):
    k = kpi_summary(jobs, today=datetime.date(2026, 10, 26), now=datetime.datetime(2026, 10, 27))
    assert k["total"] == 3 and k["companies"] == 3 and k["new_today"] == 1
    assert k["avg_age"].endswith("días")


def test_build_scrape_command():
    req = ScrapeRequest(["linkedin", "computrabajo"], "Sudamérica", config.ALL_COUNTRIES,
                        datetime.date(2026, 10, 1), datetime.date(2026, 10, 2), 50)
    cmd = build_scrape_command(req, python="py")
    assert cmd == ["py", "main.py", "--spiders", "linkedin,computrabajo", "--continent", "Sudamérica",
                   "--country", config.ALL_COUNTRIES, "--start_date", "2026-10-01",
                   "--end_date", "2026-10-02", "--max_jobs", "50"]
    with pytest.raises(ValueError):
        build_scrape_command(ScrapeRequest([], None, None, None, None, 1))


def test_scrape_log_detection():
    assert scrape_saved_data("Vacante X guardada con éxito")
    assert not scrape_saved_data("sin novedades")


def test_timed_cache_expires():
    now = [0.0]
    cache = TimedCache({}, "k", ttl_seconds=10, clock=lambda: now[0])
    calls = []
    loader = lambda: calls.append(1) or len(calls)
    assert cache.get_or_load(loader) == 1
    now[0] = 5
    assert cache.get_or_load(loader) == 1
    now[0] = 20
    assert cache.get_or_load(loader) == 2


class FakeClient:
    class R:
        def __init__(self, data): self.data = data

    def get_jobs(self, limit=None): return self.R([job(1, "Colombia", "2026-10-25T00:00:00Z")])
    def get_trends(self, limit=None): return self.R(None)
    def clear_jobs_table(self): return True


def test_repository_adapter_and_use_case():
    repo = SupabaseJobRepository(client=FakeClient())
    jobs_df, trends_df = load_market_data(repo)
    assert len(jobs_df) == 1 and trends_df.empty and repo.clear_all() is True
