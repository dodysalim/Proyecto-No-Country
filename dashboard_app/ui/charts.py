"""Fábrica de gráficos: un solo lugar define el estilo de todas las barras y tortas."""
import pandas as pd
import plotly.express as px

from dashboard_app import config

_LAYOUT = dict(
    font=dict(family="Inter, system-ui, sans-serif", size=13, color=config.TEXT_COLOR),
    title=dict(font=dict(size=16, color=config.TEXT_COLOR), x=0.01, xanchor='left'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=60, b=10),
    hoverlabel=dict(bgcolor='#121B2A', bordercolor='#75E6CE', font=dict(color=config.TEXT_COLOR)),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=config.MUTED_COLOR)),
)
_AXES = dict(gridcolor=config.GRID_COLOR, zeroline=False, linecolor=config.GRID_COLOR,
             tickfont=dict(color=config.MUTED_COLOR), title_font=dict(color=config.MUTED_COLOR))


def counts(series: pd.Series, label: str, value: str = 'Número de Vacantes') -> pd.DataFrame:
    """value_counts() como DataFrame de dos columnas con nombres legibles."""
    out = series.value_counts().reset_index()
    out.columns = [label, value]
    return out


def hbar(df, x, y, title, scale=None, labels=None, color=None, **extra):
    """Barras horizontales ordenadas de mayor a menor."""
    kwargs = dict(x=x, y=y, orientation='h', title=title, labels=labels or {})
    if color is not None:
        kwargs.update(color=color, color_discrete_sequence=config.VIBRANT_COLORS)
    else:
        kwargs.update(color=x, color_continuous_scale=scale or config.SEQUENTIAL_SCALE)
    kwargs.update(extra)
    fig = px.bar(df, **kwargs)
    fig.update_traces(marker_line_width=0, hovertemplate=None)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, bargap=0.25, coloraxis_showscale=False, **_LAYOUT)
    fig.update_xaxes(**_AXES)
    fig.update_yaxes(**_AXES, showgrid=False)
    return fig


def donut(df, values, names, title):
    fig = px.pie(df, values=values, names=names, title=title, hole=0.55,
                 color_discrete_sequence=config.VIBRANT_COLORS)
    fig.update_traces(marker=dict(line=dict(color='#0B1220', width=2)), textfont=dict(color='#0B1220'))
    fig.update_layout(**_LAYOUT)
    return fig
