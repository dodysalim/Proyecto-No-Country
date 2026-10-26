"""Caso de uso: obtener vacantes y tendencias listas para mostrar."""
from typing import Tuple

import pandas as pd

from dashboard_app.data.processing import prepare_jobs, prepare_trends
from dashboard_app.data.repository import JobMarketRepository


def load_market_data(repo: JobMarketRepository) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return prepare_jobs(repo.fetch_jobs()), prepare_trends(repo.fetch_trends())
