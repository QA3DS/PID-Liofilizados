"""
Dashboard Integral — Proyecto PID PP9884 Liofilizados UTN FRTDF
Dash + Plotly + Bootstrap. Lee datos de pid_liofilizados.db (generado por etl.py).

Uso:
    python app.py                # http://127.0.0.1:8050
    python app.py --port 8888    # Puerto alternativo
"""
import argparse, sqlite3
from pathlib import Path
from datetime import date, datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc

# ── Config ───────────────────────────────────────────────────────────
DB_PATH = Path(__file__).resolve().parent / "pid_liofilizados.db"
COLORES = {"FRESCO": "#2196F3", "CONGELADO": "#4CAF50", "ULTRACONGELADO": "#FF9800"}
COLOR_UTN = "#003366"
COLOR_QA3DS = "#1565C0"

# ── Data Layer ───────────────────────────────────────────────────────
def query(sql: str) -> pd.DataFrame:
    con = sqlite3.connect(str(DB_PATH))
    df = pd.read_sql_query(sql, con)
    con.close()
    return df

def load_all():
    """Carga todas las tablas en un dict."""
    return {
        "obs":      query("SELECT * FROM observaciones"),
        "cin":      query("SELECT * FROM cinetica"),
        "page":     query("SELECT * FROM modelo_page"),
        "tests":    query("SELECT * FROM tests_estadisticos"),
        "anova":    query("SELECT * FROM anova"),
        "plateau":  query("SELECT * FROM plateau"),
        "cond_op":  query("SELECT * FROM condiciones_op"),
        "miss":     query("SELECT * FROM missings"),
        "outliers": query("SELECT * FROM outliers"),
        "proy":     query("SELECT * FROM proyecto"),
        "equipo":   query("SELECT * FROM equipo"),
        "entreg":   query("SELECT * FROM entregables"),
        "publi":    query("SELECT * FROM publicaciones"),
        "hitos":    query("SELECT * FROM hitos"),
        "escalado": query("SELECT * FROM escalado"),
        "meta":     query("SELECT * FROM _etl_meta"),
    }

DATA = load_all()

# ═════════════════════════════════════════════════════════════════════
#  COMPONENTES — KPI Cards
# ═════════════════════════════════════════════════════════════════════
def kpi_card(title, value, subtitle="", color=COLOR_UTN, icon=""):
    return dbc.Card([
        dbc.CardBody([
            html.Div(icon, style={"fontSize": "1.6rem", "opacity": 0.7}),
            html.H3(str(value), className="card-title mb-0",
                     style={"color": color, "fontWeight": "bold"}),
            html.P(title, className="card-text mb-0",
                   style={"fontSize": "0.85rem", "fontWeight": "600"}),
            html.Small(subtitle, className="text-muted") if subtitle else None,
        ], className="text-center py-2")
    ], className="shadow-sm h-100")

# ═════════════════════════════════════════════════════════════════════
#  FIGURAS
# ═════════════════════════════════════════════════════════════════════
def fig_cinetica():
    cin = DATA["cin"]
    fig = go.Figure()
    markers = {"FRESCO": "circle", "CONGELADO": "square", "ULTRACONGELADO": "diamond"}
    for pt in ["FRESCO", "CONGELADO", "ULTRACONGELADO"]:
        sub = cin[cin["PRETRATAMIENTO"] == pt].sort_values("HORAS")
        fig.add_trace(go.Scatter(
            x=sub["HORAS"], y=sub["media"]*100,
            mode="lines+markers", name=pt.capitalize(),
            marker=dict(symbol=markers[pt], size=7),
            line=dict(color=COLORES[pt], width=2.5),
            error_y=dict(type="data", array=(sub["sd"]*100).values, visible=True,
                         color=COLORES[pt], thickness=1),
        ))
    # Plateau markers
    for _, row in DATA["plateau"].iterrows():
        if row["horas_optimo"]:
            fig.add_vline(x=row["horas_optimo"], line_dash="dot",
                          line_color=COLORES.get(row["pretratamiento"], "gray"),
                          opacity=0.5, annotation_text=f"{int(row['horas_optimo'])}h")
    fig.update_layout(
        title="Cinética de secado por pretratamiento",
        xaxis_title="Tiempo de liofilización (h)",
        yaxis_title="Pérdida de peso (%)",
        template="plotly_white", height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        hovermode="x unified",
    )
    return fig


def fig_page_model():
    obs = DATA["obs"]
    page = DATA["page"]
    t_fit = np.linspace(1, 100, 300)
    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=["Fresco", "Congelado", "Ultracongelado"],
                        shared_yaxes=True)
    for i, pt in enumerate(["FRESCO", "CONGELADO", "ULTRACONGELADO"], 1):
        sub = obs[obs["PRETRATAMIENTO"] == pt]
        fig.add_trace(go.Scatter(
            x=sub["HORAS"], y=sub["MR"],
            mode="markers", name="Observado" if i == 1 else None,
            marker=dict(color=COLORES[pt], size=4, opacity=0.3),
            showlegend=(i == 1),
        ), row=1, col=i)
        r = page[page["pretratamiento"] == pt].iloc[0]
        mr_fit = np.exp(-r["k"] * t_fit**r["n"])
        fig.add_trace(go.Scatter(
            x=t_fit, y=mr_fit, mode="lines",
            name=f"Page R²={r['R2']:.3f}" if i == 1 else None,
            line=dict(color=COLORES[pt], width=2.5),
            showlegend=(i == 1),
            hovertemplate=f"k={r['k']:.4f} n={r['n']:.4f}<br>R²={r['R2']:.4f}<extra></extra>",
        ), row=1, col=i)
    fig.update_yaxes(title_text="Moisture Ratio", row=1, col=1)
    fig.update_xaxes(title_text="Tiempo (h)")
    fig.update_layout(title="Ajuste Modelo de Page", template="plotly_white",
                      height=360)
    return fig


def fig_boxplot():
    obs = DATA["obs"]
    fig = px.box(obs, x="HORAS", y="PERDIDA_PESO_FRAC", color="PRETRATAMIENTO",
                 color_discrete_map=COLORES,
                 labels={"HORAS": "Tiempo (h)", "PERDIDA_PESO_FRAC": "Pérdida de peso (fracción)",
                         "PRETRATAMIENTO": "Pretratamiento"},
                 category_orders={"PRETRATAMIENTO": ["FRESCO", "CONGELADO", "ULTRACONGELADO"]})
    fig.update_layout(title="Distribución por tiempo y pretratamiento",
                      template="plotly_white", height=400,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02))
    return fig


def fig_missings():
    miss = DATA["miss"]
    miss = miss[miss["pct_missing"] > 0].sort_values("pct_missing")
    fig = px.bar(miss, x="pct_missing", y="variable", orientation="h",
                 text="pct_missing", color="pct_missing",
                 color_continuous_scale="Reds",
                 labels={"pct_missing": "% Faltantes", "variable": ""})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(title="Valores faltantes por variable",
                      template="plotly_white", height=350, showlegend=False,
                      coloraxis_showscale=False)
    return fig


def fig_operacionales():
    obs = DATA["obs"].dropna(subset=["TEMPERATURA_C", "PRESION_mmHg"])
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["T° vs Pérdida de peso", "Presión vs Pérdida de peso"])
    for pt in ["FRESCO", "CONGELADO", "ULTRACONGELADO"]:
        sub = obs[obs["PRETRATAMIENTO"] == pt]
        fig.add_trace(go.Scatter(
            x=sub["TEMPERATURA_C"], y=sub["PERDIDA_PESO_FRAC"]*100,
            mode="markers", name=pt.capitalize(),
            marker=dict(color=COLORES[pt], size=5, opacity=0.5),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=sub["PRESION_mmHg"], y=sub["PERDIDA_PESO_FRAC"]*100,
            mode="markers", name=pt.capitalize(),
            marker=dict(color=COLORES[pt], size=5, opacity=0.5),
            showlegend=False,
        ), row=1, col=2)
    cond = DATA["cond_op"]
    t_row = cond[cond["variable"] == "TEMPERATURA_C"].iloc[0]
    p_row = cond[cond["variable"] == "PRESION_mmHg"].iloc[0]
    fig.update_xaxes(title_text=f"T° condensador (°C) — r={t_row['spearman_r']:.3f}", row=1, col=1)
    fig.update_xaxes(title_text=f"Presión (mmHg) — r={p_row['spearman_r']:.3f}", row=1, col=2)
    fig.update_yaxes(title_text="Pérdida de peso (%)", row=1, col=1)
    fig.update_layout(title="Condiciones operacionales (RIFICOR LT-8)",
                      template="plotly_white", height=380)
    return fig


def fig_entregables():
    e = DATA["entreg"].sort_values("avance")
    colors = ["#4CAF50" if x == 100 else "#FF9800" if x >= 50 else "#EF5350" for x in e["avance"]]
    fig = go.Figure(go.Bar(
        x=e["avance"], y=e["codigo"] + " — " + e["titulo"],
        orientation="h", marker_color=colors,
        text=e["avance"].apply(lambda x: f"{x}%"),
        textposition="outside",
    ))
    fig.add_vline(x=100, line_dash="dash", line_color="green", opacity=0.3)
    fig.update_layout(title="Avance de entregables",
                      xaxis_title="% Avance", xaxis_range=[0, 110],
                      template="plotly_white", height=400, showlegend=False)
    return fig


def fig_timeline():
    h = DATA["hitos"].copy()
    h["fecha"] = pd.to_datetime(h["fecha"])
    tipo_color = {
        "Administrativo": "#003366", "Experimental": "#4CAF50",
        "Difusión": "#FF9800", "Equipamiento": "#9C27B0",
        "Formación": "#00BCD4", "Alianza": "#795548",
        "Publicación": "#E91E63", "Análisis": "#3F51B5",
        "Entregable": "#009688", "Datos": "#607D8B", "Software": "#FF5722",
    }
    fig = go.Figure()
    for tipo in h["tipo"].unique():
        sub = h[h["tipo"] == tipo]
        fig.add_trace(go.Scatter(
            x=sub["fecha"], y=[tipo]*len(sub),
            mode="markers+text", name=tipo,
            marker=dict(size=12, color=tipo_color.get(tipo, "#999")),
            text=sub["hito"], textposition="top center",
            textfont=dict(size=8),
        ))
    fig.add_vline(x=datetime.now().isoformat(), line_dash="dash", line_color="red",
                  opacity=0.5)
    fig.update_layout(title="Línea de tiempo del proyecto",
                      template="plotly_white", height=420,
                      xaxis_title="", yaxis_title="",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02),
                      showlegend=True)
    return fig


def fig_equipo_composicion():
    eq = DATA["equipo"]
    activos = eq[eq["estado"] == "Activo"]
    by_tipo = activos["tipo"].value_counts().reset_index()
    by_tipo.columns = ["tipo", "n"]
    fig = px.pie(by_tipo, values="n", names="tipo",
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 hole=0.4)
    fig.update_layout(title="Composición del equipo activo",
                      template="plotly_white", height=300)
    return fig


def fig_publicaciones_pipeline():
    p = DATA["publi"]
    estado_order = ["Presentado", "Dictado", "Completado", "Publicado",
                    "Redactado", "En preparación", "En desarrollo"]
    by_estado = p["estado"].value_counts().reindex(estado_order).dropna().reset_index()
    by_estado.columns = ["estado", "n"]
    color_map = {"Presentado": "#4CAF50", "Dictado": "#4CAF50",
                 "Completado": "#4CAF50", "Publicado": "#2196F3",
                 "Redactado": "#FF9800", "En preparación": "#EF5350",
                 "En desarrollo": "#EF5350"}
    fig = px.bar(by_estado, x="estado", y="n", color="estado",
                 color_discrete_map=color_map,
                 text="n")
    fig.update_layout(title="Pipeline de publicaciones y productos",
                      template="plotly_white", height=320, showlegend=False,
                      xaxis_title="", yaxis_title="Cantidad")
    return fig


def fig_escalado():
    esc = DATA["escalado"]
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["Inversión vs Producción", "Costo unitario"])
    fig.add_trace(go.Bar(
        x=esc["fase"], y=esc["inversion_usd"],
        name="Inversión (USD)", marker_color="#1565C0",
        text=esc["inversion_usd"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside"
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=esc["fase"], y=esc["costo_unitario_usd"],
        name="Costo/kg (USD)", marker_color="#EF5350",
        text=esc["costo_unitario_usd"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside"
    ), row=1, col=2)
    fig.update_layout(title="Plan de escalado — Comparativo de fases",
                      template="plotly_white", height=350, showlegend=False)
    return fig


# ═════════════════════════════════════════════════════════════════════
#  KPIs CALCULADOS
# ═════════════════════════════════════════════════════════════════════
def compute_kpis():
    obs = DATA["obs"]
    eq = DATA["equipo"]
    entreg = DATA["entreg"]
    proy = DATA["proy"].iloc[0]
    publi = DATA["publi"]

    # Proyecto
    inicio = pd.Timestamp("2023-04-01")
    hoy = pd.Timestamp.now()
    dias_proyecto = (hoy - inicio).days
    avance_tiempo = min(100, round(dias_proyecto / (365 * 3) * 100, 1))

    # Equipo
    activos = eq[eq["estado"] == "Activo"]
    docentes = activos[activos["rol"] != "Alumno"]
    alumnos = activos[activos["rol"] == "Alumno"]
    becarios = activos[activos["tipo"].str.contains("Becar", case=False, na=False)]
    retirados = eq[eq["estado"].str.contains("Retirad", case=False, na=False)]

    # Entregables
    avance_medio = round(entreg["avance"].mean(), 1)
    completados = (entreg["avance"] == 100).sum()
    total_entreg = len(entreg)

    # Publicaciones
    pub_completadas = publi[publi["estado"].isin(
        ["Presentado", "Dictado", "Completado", "Publicado"])].shape[0]

    # Experimental
    n_obs = len(obs)
    n_pretrat = obs["PRETRATAMIENTO"].nunique()
    n_tiempos = obs["HORAS"].nunique()
    n_meses = obs["MES_AÑO"].nunique()
    miss_pct = round(DATA["miss"]["pct_missing"].mean(), 1)

    # Page model best R²
    best_r2 = DATA["page"]["R2"].max()

    return dict(
        dias_proyecto=dias_proyecto,
        avance_tiempo=avance_tiempo,
        n_activos=len(activos),
        n_docentes=len(docentes),
        n_alumnos=len(alumnos),
        n_becarios=len(becarios),
        n_retirados=len(retirados),
        avance_medio=avance_medio,
        completados=completados,
        total_entreg=total_entreg,
        pub_completadas=pub_completadas,
        pub_total=len(publi),
        n_obs=n_obs,
        n_pretrat=n_pretrat,
        n_tiempos=n_tiempos,
        n_meses=n_meses,
        miss_pct=miss_pct,
        best_r2=best_r2,
        n_outliers=len(DATA["outliers"]),
    )

KPI = compute_kpis()

# ═════════════════════════════════════════════════════════════════════
#  LAYOUT
# ═════════════════════════════════════════════════════════════════════
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
           title="PID PP9884 — Dashboard")

HEADER = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div([
                html.H4("PID PP9884 — Dashboard Integral", className="mb-0 text-white",
                         style={"fontWeight": "bold"}),
                html.Small("Liofilización de alimentos regionales — UTN FRTDF | QA3DS",
                           className="text-light", style={"opacity": 0.8}),
            ]), width="auto"),
        ], align="center"),
    ], fluid=True),
    color=COLOR_UTN, dark=True, className="mb-3",
)

# ── Tab 1: Resumen ejecutivo ──
tab_resumen = dbc.Container([
    dbc.Row([
        dbc.Col(kpi_card("Días de proyecto", KPI["dias_proyecto"],
                         f"{KPI['avance_tiempo']}% del tiempo", COLOR_UTN, "📅"), md=2),
        dbc.Col(kpi_card("Equipo activo", KPI["n_activos"],
                         f"{KPI['n_docentes']} doc + {KPI['n_alumnos']} alum", "#4CAF50", "👥"), md=2),
        dbc.Col(kpi_card("Observaciones", KPI["n_obs"],
                         f"{KPI['n_pretrat']} pretrat × {KPI['n_tiempos']} tiempos", "#2196F3", "🔬"), md=2),
        dbc.Col(kpi_card("Avance entregables", f"{KPI['avance_medio']}%",
                         f"{KPI['completados']}/{KPI['total_entreg']} completos", "#FF9800", "📋"), md=2),
        dbc.Col(kpi_card("Publicaciones", f"{KPI['pub_completadas']}/{KPI['pub_total']}",
                         "completadas", "#9C27B0", "📄"), md=2),
        dbc.Col(kpi_card("Mejor R² (Page)", f"{KPI['best_r2']:.3f}",
                         "ULTRACONGELADO", "#E91E63", "📈"), md=2),
    ], className="g-3 mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_timeline()), md=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_entregables()), md=6),
        dbc.Col([
            dcc.Graph(figure=fig_equipo_composicion()),
            dcc.Graph(figure=fig_publicaciones_pipeline()),
        ], md=6),
    ]),
], fluid=True)

# ── Tab 2: Experimentos ──
tab_experimentos = dbc.Container([
    dbc.Row([
        dbc.Col(kpi_card("Observaciones válidas", KPI["n_obs"],
                         f"{KPI['n_meses']} meses de datos", "#2196F3", "📊"), md=3),
        dbc.Col(kpi_card("Outliers (IQR)", KPI["n_outliers"],
                         f"de {KPI['n_obs']} obs", "#EF5350", "⚠️"), md=3),
        dbc.Col(kpi_card("Missing data (media)", f"{KPI['miss_pct']}%",
                         "por variable", "#FF9800", "❓"), md=3),
        dbc.Col(kpi_card("Matrices activas", "1/3",
                         "Ruibarbo (Salicornia y Erizo descartados)", "#795548", "🌿"), md=3),
    ], className="g-3 mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_cinetica()), md=7),
        dbc.Col(dcc.Graph(figure=fig_missings()), md=5),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_page_model()), md=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_boxplot()), md=7),
        dbc.Col(dcc.Graph(figure=fig_operacionales()), md=5),
    ], className="mb-3"),

    # Tablas de resultados
    dbc.Row([
        dbc.Col([
            html.H6("Parámetros Modelo de Page", className="text-center"),
            dash_table.DataTable(
                data=DATA["page"].round(4).to_dict("records"),
                columns=[{"name": c, "id": c} for c in DATA["page"].columns],
                style_cell={"textAlign": "center", "fontSize": "0.85rem", "padding": "4px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
            ),
        ], md=6),
        dbc.Col([
            html.H6("Tests estadísticos (Kruskal-Wallis)", className="text-center"),
            dash_table.DataTable(
                data=DATA["tests"].round(4).to_dict("records"),
                columns=[{"name": c, "id": c} for c in DATA["tests"].columns],
                style_cell={"textAlign": "center", "fontSize": "0.85rem", "padding": "4px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
            ),
        ], md=6),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.H6("Detección de plateau (criterio Δ ≤ 1%)", className="text-center"),
            dash_table.DataTable(
                data=DATA["plateau"].round(4).to_dict("records"),
                columns=[{"name": c, "id": c} for c in DATA["plateau"].columns],
                style_cell={"textAlign": "center", "fontSize": "0.85rem", "padding": "4px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
            ),
        ], md=6),
        dbc.Col([
            html.H6("ANOVA Tipo II", className="text-center"),
            dash_table.DataTable(
                data=DATA["anova"].round(4).to_dict("records"),
                columns=[{"name": c, "id": c} for c in DATA["anova"].columns],
                style_cell={"textAlign": "center", "fontSize": "0.85rem", "padding": "4px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
            ),
        ], md=6),
    ]),
], fluid=True)

# ── Tab 3: Gestión ──
eq_activos = DATA["equipo"][DATA["equipo"]["estado"] == "Activo"]
tab_gestion = dbc.Container([
    dbc.Row([
        dbc.Col(kpi_card("Becarios activos", KPI["n_becarios"],
                         "BINID + Gabriel y Jorge", "#4CAF50", "🎓"), md=3),
        dbc.Col(kpi_card("Rotación", f"{KPI['n_retirados']}/{len(DATA['equipo'])}",
                         f"{round(KPI['n_retirados']/len(DATA['equipo'])*100)}% histórica", "#EF5350", "🔄"), md=3),
        dbc.Col(kpi_card("Alianzas activas", "2",
                         "Estancia Viamonte + INTI", "#795548", "🤝"), md=3),
        dbc.Col(kpi_card("Repositorio GitHub", "13 issues",
                         "3 milestones activos", "#333", "💻"), md=3),
    ], className="g-3 mb-4"),

    dbc.Row([
        dbc.Col([
            html.H6("Equipo activo", className="mb-2"),
            dash_table.DataTable(
                data=eq_activos[["nombre", "rol", "titulo", "tipo", "ingreso"]].to_dict("records"),
                columns=[
                    {"name": "Nombre", "id": "nombre"},
                    {"name": "Rol", "id": "rol"},
                    {"name": "Título", "id": "titulo"},
                    {"name": "Tipo", "id": "tipo"},
                    {"name": "Ingreso", "id": "ingreso"},
                ],
                style_cell={"textAlign": "left", "fontSize": "0.85rem", "padding": "6px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
                style_data_conditional=[
                    {"if": {"column_id": "tipo", "filter_query": '{tipo} contains "BINID"'},
                     "backgroundColor": "#E8F5E9"},
                ],
            ),
        ], md=7),
        dbc.Col([
            dcc.Graph(figure=fig_equipo_composicion()),
        ], md=5),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.H6("Publicaciones y productos", className="mb-2"),
            dash_table.DataTable(
                data=DATA["publi"].to_dict("records"),
                columns=[
                    {"name": "Título", "id": "titulo"},
                    {"name": "Tipo", "id": "tipo"},
                    {"name": "Destino", "id": "destino"},
                    {"name": "Estado", "id": "estado"},
                ],
                style_cell={"textAlign": "left", "fontSize": "0.82rem", "padding": "4px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
                style_data_conditional=[
                    {"if": {"filter_query": '{estado} = "Presentado" || {estado} = "Completado" || {estado} = "Publicado" || {estado} = "Dictado"'},
                     "backgroundColor": "#E8F5E9"},
                    {"if": {"filter_query": '{estado} = "En preparación" || {estado} = "En desarrollo"'},
                     "backgroundColor": "#FFF3E0"},
                ],
            ),
        ], md=12),
    ]),
], fluid=True)

# ── Tab 4: Escalado ──
tab_escalado = dbc.Container([
    dbc.Row([
        dbc.Col(kpi_card("Inversión Fase 1", "USD 40.250",
                         "Planta piloto", "#1565C0", "🏭"), md=3),
        dbc.Col(kpi_card("Inversión Fase 2", "USD 471.500",
                         "Escala industrial", "#0D47A1", "🏗️"), md=3),
        dbc.Col(kpi_card("Margen bruto (bulk)", "49,6%",
                         "@ USD 150/kg", "#4CAF50", "💰"), md=3),
        dbc.Col(kpi_card("Payback", "3,1 años",
                         "con subsidios", "#FF9800", "⏱️"), md=3),
    ], className="g-3 mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_escalado()), md=12),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.H6("Comparativo de fases", className="text-center mb-2"),
            dash_table.DataTable(
                data=DATA["escalado"].to_dict("records"),
                columns=[
                    {"name": "Fase", "id": "fase"},
                    {"name": "Inversión (USD)", "id": "inversion_usd", "type": "numeric",
                     "format": {"specifier": "$,.0f"}},
                    {"name": "Producción (kg/año)", "id": "produccion_kg_año", "type": "numeric",
                     "format": {"specifier": ",.1f"}},
                    {"name": "Costo unit. (USD/kg)", "id": "costo_unitario_usd", "type": "numeric",
                     "format": {"specifier": "$,.2f"}},
                    {"name": "Precio venta (USD/kg)", "id": "precio_venta_usd", "type": "numeric",
                     "format": {"specifier": "$,.0f"}},
                    {"name": "Margen bruto (%)", "id": "margen_bruto_pct"},
                    {"name": "Payback (años)", "id": "payback_años"},
                ],
                style_cell={"textAlign": "center", "fontSize": "0.9rem", "padding": "8px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"},
            ),
        ], md=10, className="mx-auto"),
    ]),
], fluid=True)


# ── Footer ──
FOOTER = html.Footer(
    dbc.Container([
        html.Hr(),
        html.P([
            "PID PP9884 — UTN FRTDF | Grupo QA3DS | ",
            html.A("GitHub", href="https://github.com/QA3DS/PID-Liofilizados",
                   target="_blank", rel="noopener noreferrer"),
            f" | Dashboard generado: {date.today().isoformat()} | ",
            f"ETL: {DATA['meta'].iloc[0]['fecha'][:19]}",
        ], className="text-muted text-center", style={"fontSize": "0.8rem"}),
    ]),
)

# ── App layout ──
app.layout = html.Div([
    HEADER,
    dbc.Tabs([
        dbc.Tab(tab_resumen, label="📊 Resumen ejecutivo", tab_id="tab-resumen"),
        dbc.Tab(tab_experimentos, label="🔬 Experimentos", tab_id="tab-exp"),
        dbc.Tab(tab_gestion, label="👥 Gestión", tab_id="tab-gestion"),
        dbc.Tab(tab_escalado, label="🏭 Escalado", tab_id="tab-escalado"),
    ], id="tabs", active_tab="tab-resumen", className="mb-3"),
    FOOTER,
])


# ═════════════════════════════════════════════════════════════════════
#  MAIN
# ═════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8050)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    print(f"\n  PID PP9884 Dashboard — http://127.0.0.1:{args.port}")
    print(f"  DB: {DB_PATH}")
    print(f"  Tablas: {len(DATA)} | Observaciones: {len(DATA['obs'])}\n")

    app.run(host="127.0.0.1", port=args.port, debug=args.debug)
