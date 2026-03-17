"""
ETL — Proyecto PID PP9884 Liofilizados UTN FRTDF
Extrae datos del Excel revisado, ejecuta análisis estadístico completo,
y carga todo en una base SQLite local para el dashboard y reporting.

Uso:
    python etl.py                       # ETL completo
    python etl.py --xlsx <ruta>         # Excel alternativo
    python etl.py --db <ruta.db>        # DB destino alternativa
"""
import argparse, os, sys, sqlite3, json
from datetime import datetime, date
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy import stats as sp_stats
import warnings
warnings.filterwarnings("ignore")

# ── Rutas por defecto ────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent          # workspace root
XLSX_DEFAULT = BASE / "datos_experimentos_compilado" / \
    "Registro de resultados - Proyecto Liofilizados - revisado.xlsx"
DB_DEFAULT   = Path(__file__).resolve().parent / "pid_liofilizados.db"
FIG_DIR      = Path(__file__).resolve().parent / "figuras"

# ── CLI ──────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description="ETL PID Liofilizados")
    p.add_argument("--xlsx", type=Path, default=XLSX_DEFAULT)
    p.add_argument("--db",   type=Path, default=DB_DEFAULT)
    return p.parse_args()

# =====================================================================
#  1. EXTRACCIÓN — Lectura de Excel
# =====================================================================
def extract(xlsx: Path) -> pd.DataFrame:
    print(f"[1/6] Leyendo {xlsx.name} …")
    df = pd.read_excel(xlsx, sheet_name="Registro", header=0)
    rename = {
        "A\xd1O":              "AÑO",
        "TEMPERATURA [\xb0C]": "TEMPERATURA_C",
        "PRESI\xd3N [mmHg]":   "PRESION_mmHg",
        "PERDIDA DE PESO %":   "PERDIDA_PESO_FRAC",
    }
    df.rename(columns=rename, inplace=True)
    df["MES_AÑO"] = df["MES"].str.title() + "-" + df["AÑO"].astype(str)
    print(f"      {df.shape[0]} filas, {df.shape[1]} columnas")
    return df

# =====================================================================
#  2. TRANSFORMACIÓN — Limpieza + análisis
# =====================================================================
def modelo_page(t, k, n):
    return np.exp(-k * t**n)


def transform(df_raw: pd.DataFrame) -> dict:
    """Retorna dict con todos los DataFrames resultado."""
    out = {}

    # ── 2a. Dataset limpio ──
    print("[2/6] Limpieza y validaciones …")
    df = df_raw.dropna(subset=["PERDIDA_PESO_FRAC"]).copy()
    df["PRETRATAMIENTO"] = df["PRETRATAMIENTO"].str.upper().str.strip()
    df["MR"] = 1 - df["PERDIDA_PESO_FRAC"]
    out["observaciones"] = df

    n_raw, n_clean = len(df_raw), len(df)
    print(f"      Raw: {n_raw} | Limpio: {n_clean} | Excluidas: {n_raw - n_clean}")

    # ── 2b. Missings ──
    miss = (df_raw.isnull().sum()).reset_index()
    miss.columns = ["variable", "n_missing"]
    miss["pct_missing"] = (miss["n_missing"] / n_raw * 100).round(2)
    out["missings"] = miss

    # ── 2c. Cinética agregada ──
    print("[3/6] Cinética y estadísticas descriptivas …")
    cin = df.groupby(["PRETRATAMIENTO", "HORAS"])["PERDIDA_PESO_FRAC"].agg(
        media="mean", sd="std", n="count",
    ).reset_index()
    cin["se"] = cin["sd"] / np.sqrt(cin["n"])
    cin["media_pct"] = (cin["media"] * 100).round(3)
    out["cinetica"] = cin

    # ── 2d. Outliers (IQR) ──
    Q1 = df["PERDIDA_PESO_FRAC"].quantile(0.25)
    Q3 = df["PERDIDA_PESO_FRAC"].quantile(0.75)
    IQR = Q3 - Q1
    mask_out = (df["PERDIDA_PESO_FRAC"] < Q1 - 1.5*IQR) | \
               (df["PERDIDA_PESO_FRAC"] > Q3 + 1.5*IQR)
    out["outliers"] = df[mask_out].copy()

    # ── 2e. Modelo de Page ──
    print("[4/6] Ajuste Modelo de Page …")
    page_rows = []
    for pt in ["FRESCO", "CONGELADO", "ULTRACONGELADO"]:
        sub = df[df["PRETRATAMIENTO"] == pt]
        t_d = sub["HORAS"].values.astype(float)
        mr_d = sub["MR"].values.astype(float)
        valid = mr_d > 0
        t_d, mr_d = t_d[valid], mr_d[valid]
        try:
            popt, pcov = curve_fit(modelo_page, t_d, mr_d,
                                   p0=[0.05, 1.0],
                                   bounds=([0.001, 0.1], [10, 5]),
                                   maxfev=10000)
            k, n = popt
            perr = np.sqrt(np.diag(pcov))
            mr_pred = modelo_page(t_d, k, n)
            ss_res = np.sum((mr_d - mr_pred)**2)
            ss_tot = np.sum((mr_d - np.mean(mr_d))**2)
            r2 = 1 - ss_res / ss_tot
            rmse = np.sqrt(np.mean((mr_d - mr_pred)**2))
            page_rows.append(dict(pretratamiento=pt, k=round(k, 6),
                                  n=round(n, 6), k_err=round(perr[0], 6),
                                  n_err=round(perr[1], 6), R2=round(r2, 6),
                                  RMSE=round(rmse, 6), n_datos=len(t_d)))
            print(f"      {pt}: k={k:.4f} n={n:.4f} R²={r2:.4f}")
        except Exception as e:
            print(f"      ERROR {pt}: {e}")
    out["modelo_page"] = pd.DataFrame(page_rows)

    # ── 2f. Tests estadísticos ──
    print("[5/6] Tests estadísticos …")
    tiempos_clave = [24, 36, 48]
    test_rows = []
    for h in tiempos_clave:
        grupos = [
            df[(df["PRETRATAMIENTO"] == pt) & (df["HORAS"] == h)
               ]["PERDIDA_PESO_FRAC"].values
            for pt in ["FRESCO", "CONGELADO", "ULTRACONGELADO"]
        ]
        stat, p = sp_stats.kruskal(*grupos)
        sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
        test_rows.append(dict(horas=h, metodo="Kruskal-Wallis",
                              estadistico=round(stat, 4), p_valor=round(p, 6),
                              significancia=sig))
    out["tests_estadisticos"] = pd.DataFrame(test_rows)

    # ANOVA tipo II
    try:
        import statsmodels.formula.api as smf
        import statsmodels.api as sm_api
        modelo_ols = smf.ols(
            "PERDIDA_PESO_FRAC ~ C(PRETRATAMIENTO) + C(HORAS) + C(MES_AÑO)",
            data=df).fit()
        anova_t = sm_api.stats.anova_lm(modelo_ols, typ=2).reset_index()
        anova_t.columns = ["fuente", "sum_sq", "df", "F", "PR_F"]
        anova_t["R2_modelo"] = round(modelo_ols.rsquared, 4)
        anova_t["R2_adj"] = round(modelo_ols.rsquared_adj, 4)
        out["anova"] = anova_t
        print(f"      ANOVA R²={modelo_ols.rsquared:.4f}")
    except Exception as e:
        print(f"      ANOVA error: {e}")

    # ── 2g. Plateau ──
    plateau_rows = []
    for pt in ["FRESCO", "CONGELADO", "ULTRACONGELADO"]:
        sub = cin[cin["PRETRATAMIENTO"] == pt].sort_values("HORAS")
        horas = sub["HORAS"].values
        medias = sub["media"].values
        delta = np.abs(np.diff(medias) / medias[:-1])
        idx = np.where(delta <= 0.01)[0]
        if len(idx) > 0:
            t_opt = int(horas[idx[0] + 1])
            plateau_rows.append(dict(pretratamiento=pt, horas_optimo=t_opt,
                                     perdida_media=round(float(medias[idx[0]+1]), 6),
                                     delta_rel_pct=round(float(delta[idx[0]]*100), 4)))
        else:
            plateau_rows.append(dict(pretratamiento=pt, horas_optimo=None,
                                     perdida_media=None, delta_rel_pct=None))
    out["plateau"] = pd.DataFrame(plateau_rows)

    # ── 2h. Condiciones operacionales ──
    df_op = df.dropna(subset=["TEMPERATURA_C", "PRESION_mmHg"]).copy()
    r_T, p_T = sp_stats.spearmanr(df_op["TEMPERATURA_C"], df_op["PERDIDA_PESO_FRAC"])
    r_P, p_P = sp_stats.spearmanr(df_op["PRESION_mmHg"], df_op["PERDIDA_PESO_FRAC"])
    out["condiciones_op"] = pd.DataFrame([
        dict(variable="TEMPERATURA_C", spearman_r=round(r_T, 4), p_valor=round(p_T, 4),
             media=round(df_op["TEMPERATURA_C"].mean(), 2),
             sd=round(df_op["TEMPERATURA_C"].std(), 2),
             minimo=round(df_op["TEMPERATURA_C"].min(), 2),
             maximo=round(df_op["TEMPERATURA_C"].max(), 2),
             n=len(df_op)),
        dict(variable="PRESION_mmHg", spearman_r=round(r_P, 4), p_valor=round(p_P, 4),
             media=round(df_op["PRESION_mmHg"].mean(), 3),
             sd=round(df_op["PRESION_mmHg"].std(), 3),
             minimo=round(df_op["PRESION_mmHg"].min(), 3),
             maximo=round(df_op["PRESION_mmHg"].max(), 3),
             n=len(df_op)),
    ])

    return out

# =====================================================================
#  3. METADATOS DEL PROYECTO (hard-coded de CLAUDE.md)
# =====================================================================
def project_metadata() -> dict:
    """Retorna DataFrames con metadatos del proyecto."""
    out = {}

    out["proyecto"] = pd.DataFrame([dict(
        codigo="PP9884",
        titulo="Análisis del Proceso de Liofilizado Aplicado a Alimentos de Producción Local/Regional en TDF",
        institucion="UTN FRTDF",
        grupo="QA3DS",
        director="Ing. Pesq. Ariel Luján Giamportone",
        inicio="2023-04-01",
        fin_original="2025-03-31",
        prorroga="Sí — DISPOSICIÓN-1-2025",
        estado="En ejecución (prórroga)",
        fecha_etl=date.today().isoformat(),
    )])

    out["equipo"] = pd.DataFrame([
        dict(nombre="Ariel L. Giamportone", rol="Director", titulo="Ing. Pesquero", tipo="Docente", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="Pamela R. Flores", rol="Investigadora", titulo="Ing. Química", tipo="Docente", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="María Victoria Cornejo", rol="Investigadora", titulo="Ing. Química", tipo="Docente", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="Javier Alfarano", rol="Investigador Apoyo", titulo="Ing. Industrial", tipo="Docente", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="Milagro Mottola", rol="Investigadora", titulo="Dra. en Química", tipo="Docente", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="Tomás Chalde", rol="Investigador Apoyo", titulo="Doctor", tipo="Docente", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="Emanuel Silva Naveas", rol="Alumno", titulo="Est. Ing. Electromecánica", tipo="Becario BINID", estado="Activo", ingreso="2024-07-01"),
        dict(nombre="Gabriel F. Costilla", rol="Alumno", titulo="Est. Ing. Pesquera", tipo="Becario Gabriel y Jorge", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="Jorge Rojas Flores", rol="Alumno", titulo="—", tipo="Becario Gabriel y Jorge", estado="Activo", ingreso="2023-04-01"),
        dict(nombre="Angélica Cárcamo", rol="Alumno", titulo="Ing. Química (graduada)", tipo="Becaria BINID", estado="Activo", ingreso="2025-03-01"),
        dict(nombre="Ricardo A. Heredia", rol="Alumno", titulo="Est. Ing. Electromecánica", tipo="Becario BINID", estado="Activo", ingreso="2024-07-01"),
        dict(nombre="Facundo N. Gutiérrez", rol="Alumno", titulo="Est. Ing. Química", tipo="Alumno", estado="Activo", ingreso="2024-04-01"),
        dict(nombre="Matías I. Álvarez", rol="Alumno", titulo="Est. Ing. Química", tipo="Becario BINID", estado="Activo", ingreso="2024-04-01"),
        dict(nombre="Michael Trujillo Burgos", rol="Alumno", titulo="—", tipo="Alumno", estado="Retirado", ingreso="2023-04-01"),
        dict(nombre="Federico D. Cejas", rol="Alumno", titulo="—", tipo="Alumno", estado="Retirado", ingreso="2023-04-01"),
        dict(nombre="Roxana B. Barrionuevo", rol="Alumno", titulo="—", tipo="Alumno", estado="Retirada", ingreso="2023-04-01"),
        dict(nombre="Franco Guereta", rol="Alumno", titulo="—", tipo="Alumno", estado="Retirado", ingreso="2023-04-01"),
        dict(nombre="Erika G. Mamaní Mejía", rol="Alumno", titulo="—", tipo="Alumno", estado="Retirada", ingreso="2023-04-01"),
    ])

    out["entregables"] = pd.DataFrame([
        dict(codigo="A1", titulo="Propuesta PID aprobada", avance=100, estado="Completado", fecha_fin="2023-04-01"),
        dict(codigo="A2", titulo="Relevamiento bibliográfico", avance=100, estado="Completado", fecha_fin="2024-06-01"),
        dict(codigo="A3", titulo="Diseño experimental", avance=100, estado="Completado", fecha_fin="2024-06-01"),
        dict(codigo="A4", titulo="Experimentos de liofilización", avance=85, estado="En progreso", fecha_fin=None),
        dict(codigo="A5", titulo="Resultados ruibarbo", avance=70, estado="En progreso", fecha_fin=None),
        dict(codigo="A6", titulo="Análisis multivariado (PCA)", avance=10, estado="Pendiente", fecha_fin=None),
        dict(codigo="B1", titulo="Manual técnico-económico", avance=60, estado="En progreso", fecha_fin=None),
        dict(codigo="B2", titulo="Artículo científico", avance=15, estado="Pendiente", fecha_fin=None),
        dict(codigo="C1", titulo="Presentaciones/divulgación", avance=90, estado="En progreso", fecha_fin=None),
        dict(codigo="C2", titulo="Capacitaciones internas", avance=100, estado="Completado", fecha_fin="2024-10-15"),
    ])

    out["publicaciones"] = pd.DataFrame([
        dict(titulo="Liofilización en TDF (divulgación)", tipo="Artículo revista", destino="La Lupa", estado="Redactado", fecha="2025-06-01"),
        dict(titulo="Conservando el Futuro Alimentario de TDF", tipo="Artículo revista", destino="La Lupa", estado="Redactado", fecha="2025-06-01"),
        dict(titulo="Artículo breve La Lupa 2025", tipo="Artículo revista", destino="La Lupa", estado="En preparación", fecha=None),
        dict(titulo="Presentación Jornadas CyT 2023", tipo="Presentación congreso", destino="UTN FRTDF", estado="Presentado", fecha="2023-10-20"),
        dict(titulo="Semana del Ambiente Muni RG 2025", tipo="Presentación", destino="Municipio Río Grande", estado="Presentado", fecha="2025-06-05"),
        dict(titulo="Poster QA3DS", tipo="Poster", destino="Institucional", estado="Completado", fecha="2024-01-01"),
        dict(titulo="Poster Colegio de Ingenieros", tipo="Poster", destino="CPTDF", estado="Completado", fecha="2024-01-01"),
        dict(titulo="Capacitación liofilizador", tipo="Curso interno", destino="UTN FRTDF", estado="Dictado", fecha="2024-10-15"),
        dict(titulo="Guía uso rápido liofilizador", tipo="Documento técnico", destino="Interno", estado="Completado", fecha="2024-10-15"),
        dict(titulo="Notebook Jupyter análisis", tipo="Software/datos", destino="GitHub", estado="Publicado", fecha="2026-03-04"),
        dict(titulo="Estudio de escalado (5 docs)", tipo="Estudio técnico", destino="Interno", estado="Completado", fecha="2025-12-01"),
        dict(titulo="Dashboard PID", tipo="Software/datos", destino="GitHub", estado="En desarrollo", fecha=None),
    ])

    out["hitos"] = pd.DataFrame([
        dict(fecha="2023-04-01", hito="Inicio PID PP9884", tipo="Administrativo"),
        dict(fecha="2023-10-20", hito="Presentación Jornadas CyT", tipo="Difusión"),
        dict(fecha="2023-12-01", hito="Exp1 ruibarbo completado", tipo="Experimental"),
        dict(fecha="2024-04-01", hito="Exp2 ruibarbo completado", tipo="Experimental"),
        dict(fecha="2024-06-01", hito="Compra balanza OHAUS CR + termómetro", tipo="Equipamiento"),
        dict(fecha="2024-10-15", hito="Capacitación interna liofilizador", tipo="Formación"),
        dict(fecha="2024-11-01", hito="Exp3 ruibarbo completado", tipo="Experimental"),
        dict(fecha="2025-01-01", hito="Exp4 ruibarbo completado", tipo="Experimental"),
        dict(fecha="2025-02-01", hito="Convenio Estancia Viamonte activo", tipo="Alianza"),
        dict(fecha="2025-03-15", hito="Prórroga aprobada (DISP-1-2025)", tipo="Administrativo"),
        dict(fecha="2025-06-01", hito="Artículos La Lupa redactados", tipo="Publicación"),
        dict(fecha="2025-06-05", hito="Semana del Ambiente Muni RG", tipo="Difusión"),
        dict(fecha="2026-03-04", hito="Análisis estadístico compilado", tipo="Análisis"),
        dict(fecha="2026-03-09", hito="A5 + B1 actualizados con datos", tipo="Entregable"),
        dict(fecha="2026-03-16", hito="Datos revisados incorporados", tipo="Datos"),
        dict(fecha="2026-03-16", hito="Dashboard integral generado", tipo="Software"),
    ])

    out["escalado"] = pd.DataFrame([
        dict(fase="Piloto", inversion_usd=40250, produccion_kg_año=92.5,
             costo_unitario_usd=680, precio_venta_usd=150,
             margen_bruto_pct=None, payback_años=None),
        dict(fase="Industrial", inversion_usd=471500, produccion_kg_año=8500,
             costo_unitario_usd=75.57, precio_venta_usd=150,
             margen_bruto_pct=49.6, payback_años=4.2),
        dict(fase="Industrial (snack 50g)", inversion_usd=471500, produccion_kg_año=8500,
             costo_unitario_usd=75.57, precio_venta_usd=130,
             margen_bruto_pct=66.0, payback_años=3.1),
    ])

    return out

# =====================================================================
#  4. CARGA — SQLite
# =====================================================================
def load(tables: dict, db_path: Path):
    print(f"[6/6] Escribiendo {db_path.name} …")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    con = sqlite3.connect(str(db_path))

    # Columnas datetime del Excel que causan problemas → string
    for key in tables:
        df = tables[key]
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
            if df[col].dtype == object:
                df[col] = df[col].where(df[col].notna(), None)

    for name, df in tables.items():
        df.to_sql(name, con, index=False, if_exists="replace")
        print(f"      → {name}: {len(df)} filas")

    # Tabla de metadatos ETL
    pd.DataFrame([dict(
        fecha=datetime.now().isoformat(),
        xlsx=str(XLSX_DEFAULT),
        n_tablas=len(tables),
        version="1.0.0",
    )]).to_sql("_etl_meta", con, index=False, if_exists="replace")

    con.close()
    print(f"      ✓ Base de datos lista: {db_path}")

# =====================================================================
#  MAIN
# =====================================================================
def main():
    args = parse_args()
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # Extract
    df_raw = extract(args.xlsx)

    # Transform — experimental
    tables = transform(df_raw)

    # Transform — metadata
    meta = project_metadata()
    tables.update(meta)

    # Load
    load(tables, args.db)

    # Resumen
    print("\n═══ ETL COMPLETO ═══")
    print(f"  Tablas generadas: {len(tables)}")
    for name, df in sorted(tables.items()):
        print(f"    {name:25s} {len(df):>5d} filas")
    print(f"  Base de datos: {args.db}")
    print(f"  Timestamp: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
