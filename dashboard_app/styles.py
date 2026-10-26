"""Hoja de estilos del dashboard (tema oscuro, coherente con el portafolio)."""

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #0B1220; --surface: #121B2A; --surface-2: #16213A; --line: #24324D;
        --text: #E6ECF5; --muted: #93A1BD; --accent: #75E6CE; --blue: #88B7FF; --violet: #C99BFF;
    }
    html, body, [class*="css"], .stApp { font-family: 'Inter', system-ui, sans-serif; }
    .stApp {
        background:
            radial-gradient(900px 500px at 0% -10%, rgba(117,230,206,.10), transparent 60%),
            radial-gradient(800px 500px at 100% 0%, rgba(143,123,255,.10), transparent 60%),
            var(--bg);
    }
    .block-container { padding-top: 3.5rem; max-width: 1400px; }
    h1, h2, h3 { color: var(--text) !important; font-weight: 700 !important; letter-spacing: -.02em; }
    hr { border-color: var(--line) !important; opacity: .6; }

    /* Encabezado */
    .hero {
        border: 1px solid var(--line); border-radius: 20px; padding: 28px 32px; margin-bottom: 8px;
        background: linear-gradient(135deg, rgba(22,33,58,.95), rgba(18,27,42,.85));
        box-shadow: 0 20px 60px rgba(0,0,0,.35);
    }
    .hero .eyebrow { color: var(--accent); font-size: 12px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
    .hero h1 { font-size: 40px !important; margin: 6px 0 8px !important; padding: 0 !important; }
    .hero h1 span { background: linear-gradient(110deg, var(--accent), var(--blue) 60%, var(--violet));
                    -webkit-background-clip: text; background-clip: text; color: transparent; }
    .hero p { color: var(--muted); font-size: 16px; margin: 0; max-width: 820px; }

    /* Tarjetas de KPI */
    .metric-card {
        position: relative; overflow: hidden;
        background: linear-gradient(160deg, var(--surface-2), var(--surface));
        border: 1px solid var(--line); border-radius: 16px; padding: 18px 20px; min-height: 108px;
        transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
    }
    .metric-card::before { content: ""; position: absolute; inset: 0 0 auto 0; height: 3px; background: var(--kpi); }
    .metric-card:hover { transform: translateY(-4px); border-color: var(--kpi); box-shadow: 0 14px 40px rgba(0,0,0,.35); }
    .metric-card .label { color: var(--muted); font-size: 12px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; margin: 0 0 8px; }
    .metric-card .value { color: var(--text); font-size: 30px; font-weight: 800; line-height: 1.1; margin: 0; font-variant-numeric: tabular-nums; }
    .metric-card .value.small { font-size: 18px; }

    /* Pestañas tipo píldora */
    .stTabs [role="tablist"] { gap: 8px; flex-wrap: wrap; border-bottom: none !important; }
    .stTabs button[role="tab"] {
        background: var(--surface); border: 1px solid var(--line) !important; border-radius: 999px;
        padding: 6px 14px !important; color: var(--muted);
    }
    .stTabs button[role="tab"][aria-selected="true"] { background: rgba(117,230,206,.12); border-color: var(--accent) !important; color: var(--text); }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* Gráficos y tablas en tarjetas */
    [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {
        background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 8px;
    }

    /* Botones */
    .stButton > button, .stDownloadButton > button {
        border-radius: 12px !important; font-weight: 600 !important;
        transition: transform .2s ease, box-shadow .2s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px) !important; box-shadow: 0 10px 28px rgba(117,230,206,.18) !important;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0F1829, #0B1220); border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { font-size: 15px !important; }

    /* Expander */
    [data-testid="stExpander"] { border: 1px solid var(--line) !important; border-radius: 14px !important; background: var(--surface); }
</style>
"""

HERO = """
<div class="hero">
  <div class="eyebrow">Market Intelligence · LatAm</div>
  <h1>LatAm Job Market <span>Intelligence</span></h1>
  <p>Análisis de las vacantes disponibles en el mercado laboral en <b>Latam</b> y más allá,
  con análisis de tendencias e insights generados por IA.</p>
</div>
"""
