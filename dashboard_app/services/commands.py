"""Construcción y ejecución de comandos de `main.py` (scraping y análisis de tendencias)."""
import datetime
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence

from dashboard_app import config

logger = logging.getLogger(__name__)
Runner = Callable[[List[str]], subprocess.CompletedProcess]


@dataclass(frozen=True)
class ScrapeRequest:
    spiders: Sequence[str]
    continent: Optional[str]
    country: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    max_jobs: int


def build_scrape_command(req: ScrapeRequest, python: str = sys.executable) -> List[str]:
    """Traduce la selección del usuario en argumentos de `main.py` (función pura)."""
    if not req.spiders:
        raise ValueError("Selecciona al menos un scraper para ejecutar.")
    cmd = [python, "main.py", "--spiders", ",".join(req.spiders)]
    continent = str(req.continent).strip() if req.continent is not None else ""
    country = str(req.country).strip() if req.country is not None else ""
    if continent and continent != config.CONTINENT_PLACEHOLDER:
        cmd += ["--continent", continent]
    if country and country != config.ALL_COUNTRIES:
        cmd += ["--country", country]
    elif country == config.ALL_COUNTRIES and continent != config.CONTINENT_PLACEHOLDER:
        cmd += ["--country", config.ALL_COUNTRIES]
    if req.start_date is not None:
        cmd += ["--start_date", req.start_date.strftime("%Y-%m-%d")]
    if req.end_date is not None:
        cmd += ["--end_date", req.end_date.strftime("%Y-%m-%d")]
    cmd += ["--max_jobs", str(req.max_jobs)]
    return cmd


def build_trends_command(python: str = sys.executable) -> List[str]:
    return [python, "main.py", "--analyze-trends"]


def run_in_project(cmd: List[str]) -> subprocess.CompletedProcess:
    """Ejecuta un comando en la raíz del proyecto, capturando su salida."""
    logger.info("Comando subprocess a ejecutar: %s", cmd)
    return subprocess.run(cmd, capture_output=True, text=True, cwd=config.PROJECT_ROOT,
                          env=os.environ.copy(), check=False)


def scrape_saved_data(logs: str) -> bool:
    """Detecta en los logs si el scraper guardó vacantes."""
    return "Vacante" in logs and "guardada con éxito" in logs
