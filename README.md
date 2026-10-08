![LatAm Insights](docs/cover.svg)

# LatAm Insights

**De vacantes dispersas a información útil sobre perfiles, habilidades y sectores.**

NO COUNTRY · MERCADO LABORAL · Python · Scrapy · Supabase · Streamlit

[Portafolio](https://dodysalim.github.io/) · [Caso y alcance](docs/PORTFOLIO_CASE.md) · [Verificación](docs/VALIDATION.md)

## La pregunta

¿Qué habilidades y perfiles aparecen en las ofertas recolectadas, y cómo cambian por ubicación?

## Qué puedes revisar

- ETL de limpieza, normalización de seniority y extracción de habilidades.
- Dashboard con filtros, exportación y análisis de tendencias.
- Scrapers de LinkedIn y Computrabajo; reportes de IA opcionales.

## Inicio local

Usa Python 3.11 o 3.12 en un entorno independiente. Desde la raíz:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Después de configurar los datos:

```bash
python -m streamlit run dashboard.py
```

## Datos y configuración

Requiere SUPABASE_URL y SUPABASE_SERVICE_KEY en un .env local. GEMINI_API_KEY es opcional. La ausencia de credenciales se informa; no se inventan vacantes.

## Power BI · PC y móvil

[Archivos e instrucciones](powerbi/README.md). Descarga el repositorio completo y abre `powerbi/Abrir-PowerBI.bat` en Windows; después pulsa **Actualizar**. Incluye A4 horizontal a tamaño real (100 %) y diseño móvil vertical. El archivo `.pbip` necesita sus carpetas Report, SemanticModel y data.

## Recorrido por el código

| Ruta | Qué contiene |
| --- | --- |
| [etl/](etl/) | Transformaciones y extracción de habilidades |
| [scrapers/](scrapers/) | Recolección por fuente |
| [dashboard.py](dashboard.py) | Aplicación de análisis |
| [tests/](tests/) | Pruebas de componentes ETL |

## Comprobación y alcance

14 pruebas ETL y reportes aprobadas. Arranque del dashboard comprobado sin credenciales: muestra la falta de conexión, sin excepción no controlada.

No se comprobó una extracción en vivo ni la escritura en Supabase. La disponibilidad depende de las fuentes, permisos y credenciales.

Para repetir las pruebas desde la raíz:

```bash
python -m pytest tests -q
```

## Autoría

Simulación laboral de No Country. Se conserva la documentación y autoría del proyecto colectivo.

[Documentación anterior](docs/ORIGINAL_README.md), conservada como referencia histórica.
