# Dashboard Integral — PID PP9884

Dashboard interactivo para el proyecto de liofilización de alimentos regionales (UTN FRTDF, Grupo QA3DS).

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| ETL | Python + pandas + openpyxl |
| Análisis | scipy (curve_fit, Kruskal-Wallis), statsmodels (ANOVA II), pingouin |
| Base de datos | SQLite (15 tablas, ~400 registros) |
| Dashboard | Dash (Plotly) + Bootstrap |
| Visualización | Plotly (gráficos interactivos) |

## Estructura

```
dashboard/
├── etl.py                  # ETL: Excel → análisis → SQLite
├── app.py                  # Dashboard Dash (4 tabs, 12+ gráficos)
├── run.bat                 # Launcher Windows (ETL + dashboard)
├── pid_liofilizados.db     # Base SQLite generada
└── README.md               # Este archivo
```

## Uso rápido

```bash
# Opción 1: doble-click en run.bat

# Opción 2: manual
python dashboard/etl.py          # genera pid_liofilizados.db
python dashboard/app.py          # abre http://127.0.0.1:8050
```

## Tabs del dashboard

1. **Resumen ejecutivo** — KPIs clave, timeline, entregables, equipo, publicaciones
2. **Experimentos** — Cinética de secado, Modelo de Page, boxplots, missings, condiciones operacionales, tests estadísticos
3. **Gestión** — Equipo, becarios, publicaciones, pipeline
4. **Escalado** — Plan de fases, inversión, costos, márgenes

## Base de datos SQLite

| Tabla | Filas | Descripción |
|---|---|---|
| `observaciones` | 261 | Datos experimentales limpios |
| `cinetica` | 30 | Estadísticas por pretratamiento × hora |
| `modelo_page` | 3 | Parámetros del modelo de Page |
| `tests_estadisticos` | 3 | Kruskal-Wallis por tiempo clave |
| `anova` | 4 | ANOVA Tipo II completo |
| `plateau` | 3 | Tiempo óptimo por pretratamiento |
| `condiciones_op` | 2 | T° y P° del equipo RIFICOR |
| `missings` | 21 | % valores faltantes por variable |
| `outliers` | ~25 | Outliers detectados (IQR) |
| `proyecto` | 1 | Metadatos del proyecto |
| `equipo` | 18 | Integrantes (activos + histórico) |
| `entregables` | 10 | Avance de entregables |
| `publicaciones` | 12 | Pipeline de publicaciones |
| `hitos` | 16 | Línea de tiempo del proyecto |
| `escalado` | 3 | Plan de fases productivas |

## Dependencias

```
dash>=2.0
dash-bootstrap-components>=1.0
plotly>=5.0
pandas>=2.0
numpy>=1.24
scipy>=1.10
statsmodels>=0.14
openpyxl>=3.1
pingouin>=0.5
missingno>=0.5
```
