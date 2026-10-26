<p align="center"><img src="https://dodysalim.github.io/assets/project-covers/market.webp" alt="LatAm Insights" width="100%"></p>

<h1 align="center">LatAm Insights</h1>

<p align="center"><b>De vacantes dispersas a información útil sobre perfiles, habilidades y sectores.</b></p>

<p align="center">
<img src="https://img.shields.io/badge/No_Country_%C2%B7_Equipo_27_%C2%B7_Noviembre_2025-75E6CE?style=for-the-badge&labelColor=0b1222" alt="No Country · Equipo 27 · Noviembre 2025">
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Scrapy-60A839?style=flat-square&logo=scrapy&logoColor=white" alt="Scrapy"> <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white" alt="Supabase"> <img src="https://img.shields.io/badge/SQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL"> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"> <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logoColor=black" alt="Power BI">
</p>

<p align="center"><a href="https://nocountry.tech/showcase/simulacion-laboral-noviembre-2025/equipo-27-datascience"><b>🏆 Showcase No Country</b></a> · <a href="https://dodysalim.github.io/"><b>🌐 Portafolio</b></a> · <a href="docs/PORTFOLIO_CASE.md"><b>📄 Caso de estudio</b></a></p>

---

## 📌 Resumen en 30 segundos

| | |
| --- | --- |
| **🎯 Problema** | Entender qué habilidades y perfiles piden las ofertas de empleo en datos, y cómo varían por ubicación. |
| **🛠️ Solución** | Scrapers de LinkedIn y Computrabajo, ETL con normalización de seniority y extracción de habilidades. |
| **📈 Entregables** | Dashboard con filtros, tendencias y exportación; Power BI para PC y móvil. |
| **🧪 Calidad** | 14 pruebas automatizadas del ETL y reportes. |
| **👤 Mi rol** | Data Analyst en equipo de 3 personas. |

## ❓ La pregunta de negocio

¿Qué habilidades y perfiles aparecen en las ofertas recolectadas, y cómo cambian por ubicación?

## ✨ Qué incluye

- ETL de limpieza, normalización de seniority y extracción de habilidades.
- Dashboard con filtros, exportación y análisis de tendencias.
- Scrapers de LinkedIn y Computrabajo; reportes de IA opcionales.

## 🚀 Cómo ejecutarlo

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

## 🗂️ Datos y configuración

Requiere SUPABASE_URL y SUPABASE_SERVICE_KEY en un .env local. GEMINI_API_KEY es opcional. La ausencia de credenciales se informa; no se inventan vacantes.

## 📊 Power BI · PC y móvil

[Archivos e instrucciones](powerbi/README.md). Descarga el repositorio completo y abre `powerbi/Abrir-PowerBI.bat` en Windows; después pulsa **Actualizar**. Incluye A4 horizontal a tamaño real (100 %) y diseño móvil vertical. El archivo `.pbip` necesita sus carpetas Report, SemanticModel y data.

## 🧭 Estructura del repositorio

| Ruta | Qué contiene |
| --- | --- |
| [etl/](etl/) | Transformaciones y extracción de habilidades |
| [scrapers/](scrapers/) | Recolección por fuente |
| [dashboard.py](dashboard.py) | Aplicación de análisis |
| [tests/](tests/) | Pruebas de componentes ETL |

## ✅ Calidad y alcance

14 pruebas ETL y reportes aprobadas. Arranque del dashboard comprobado sin credenciales: muestra la falta de conexión, sin excepción no controlada.

No se comprobó una extracción en vivo ni la escritura en Supabase. La disponibilidad depende de las fuentes, permisos y credenciales.

Para repetir las pruebas desde la raíz:

```bash
python -m pytest tests -q
```

## 👥 Autoría

Simulación laboral de No Country. Se conserva la documentación y autoría del proyecto colectivo.


### Equipo · Noviembre 2025

| Integrante | Rol publicado |
| --- | --- |
| Juan | Machine Learning Engineer |
| Rosa | Data Scientist |
| Dody | Data analyst |

Créditos basados en el [showcase oficial](https://nocountry.tech/showcase/simulacion-laboral-noviembre-2025/equipo-27-datascience). Se conserva la autoría colectiva.

[Documentación anterior](docs/ORIGINAL_README.md), conservada como referencia histórica.

### Automatización opcional

Las pruebas se ejecutan en cada cambio. Para habilitar los jobs que escriben tendencias en Supabase o ejecutan scraping programado, configura las credenciales y la variable de repositorio `AUTOMATION_ENABLED=true`. Hasta entonces esos jobs permanecen desactivados; la aplicación puede ejecutarse manualmente con su configuración local.

---

<p align="center">
<b>Dody Dueñas Remache</b> · Analista de Datos / Data Scientist<br>
<a href="https://dodysalim.github.io/">Portafolio</a> · <a href="https://github.com/dodysalim">GitHub</a> · <a href="https://www.linkedin.com/in/dody-duenas/">LinkedIn</a> · <a href="mailto:dodydurema67@gmail.com">dodydurema67@gmail.com</a>
</p>
