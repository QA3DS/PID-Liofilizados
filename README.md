# Liofilización de Alimentos de Producción Local en Tierra del Fuego
### PID PP9884 — UTN Facultad Regional Tierra del Fuego

[![Estado del proyecto](https://img.shields.io/badge/Estado-Cierre%20en%20pr%C3%B3rroga%20%C2%B7%20informe%20v2%20en%20revisi%C3%B3n-orange)](preprint/informe_cierre.pdf)
[![UTN FRTDF](https://img.shields.io/badge/Institución-UTN%20FRTDF-lightgrey)](https://frtdf.utn.edu.ar)
[![Grupo QA3DS](https://img.shields.io/badge/Grupo-QA3DS-green)](https://github.com/QA3DS)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-QA3DS-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/company/qu%C3%ADmica-aplicada-al-ambiente-los-alimentos-y-el-desarrollo-sostenible)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-QA3DS_Lab-00CCBB?logo=researchgate&logoColor=white)](https://www.researchgate.net/lab/Quimica-aplicada-al-Ambiente-los-Alimentos-y-el-Desarrollo-Sostenible-Ariel-Lujan-Giamportone)

---

## Sobre el proyecto

Este repositorio documenta el **Proyecto de Investigación y Desarrollo (PID PP9884)** de la UTN Facultad Regional Tierra del Fuego:

> **"Análisis del Proceso de Liofilizado Aplicado a Alimentos de Producción Local/Regional en la Provincia de Tierra del Fuego"**

El proyecto estudia la aplicación del proceso de **liofilización (freeze-drying)** para la conservación y valorización de productos alimentarios locales de la Patagonia Austral, con foco en el desarrollo de protocolos reproducibles para productores regionales.

| Campo | Detalle |
|---|---|
| **Código** | PP9884 (PIDPP UTN) · Código SCyT PAPPTF0009884 |
| **Homologación** | Disposición SCyT 1/2023 (10/03/2023) |
| **Período original** | 1/04/2023 – 31/03/2025 (24 meses) |
| **Prórroga** | Disposición SCyT N.º 0001/2025 (10/03/2025) · fecha de finalización a confirmar |
| **Sede experimental** | Laboratorio UTN FRTDF, Río Grande |
| **Financiamiento** | Sistema PIDPP — UTN |

**Documento rector del estado actual:** [`preprint/informe_cierre.pdf`](preprint/informe_cierre.pdf) — Informe de cierre, **borrador v2 (septiembre 2026)**, revisado contra la propuesta homologada, la Disposición SCyT 0001/2025 y la planilla de resultados, con aportes de la Dra. Milagro Mottola. Este README resume ese documento.

---

## ⚠️ Corrección en curso: fórmula de pérdida de peso

La revisión de septiembre de 2026 detectó un **error sistemático en la planilla de resultados**: la fórmula de pérdida de peso resta el barquillo de aluminio de la masa inicial pero no de la masa final (269 de 270 filas). La pérdida queda **subestimada en 1,1 puntos porcentuales en promedio** (rango 0,1–2,4).

- Los tiempos de estabilización y **todas las conclusiones se mantienen**.
- Cambian las cifras absolutas: por ejemplo, la pérdida en la meseta pasa de 92,0–92,3 % a 93,1–93,4 %.
- La corrección **todavía no está aplicada** en el notebook, el ETL del dashboard, las figuras ni los documentos. Se aplicará cuando se confirme el protocolo de pesada (responsables: Cornejo, Alfarano).
- Hasta entonces, las cifras de este README, de `resultados_clave.md`, del preprint y del dashboard son las de la planilla original.

---

## Grupo de investigación

**QA3DS — Química Aplicada al Ambiente, los Alimentos y el Desarrollo Sostenible**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-QA3DS-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/company/qu%C3%ADmica-aplicada-al-ambiente-los-alimentos-y-el-desarrollo-sostenible) [![ResearchGate](https://img.shields.io/badge/ResearchGate-QA3DS_Lab-00CCBB?logo=researchgate&logoColor=white)](https://www.researchgate.net/lab/Quimica-aplicada-al-Ambiente-los-Alimentos-y-el-Desarrollo-Sostenible-Ariel-Lujan-Giamportone)

### Equipo docente (cargos según la propuesta homologada por la SCyT)

| Nombre | Título | Rol |
|---|---|---|
| Ariel Luján Giamportone | Ing. Pesquero | Director |
| Tomás Chalde | Dr. | Co-director |
| María Victoria Cornejo | Ing. Química | Investigadora de apoyo |
| Pamela Rocío Flores | Ing. Química | Investigadora de apoyo |
| Milagro Mottola | Dra. en Química | Investigadora de apoyo |
| Javier Alfarano | Ing. Industrial | Investigador de apoyo |
| Teresita Mabel Quiroga | a confirmar | Investigadora de apoyo (situación actual a confirmar) |

### Alumnos investigadores activos al cierre

| Nombre | Carrera | Ingreso | Beca |
|---|---|---|---|
| Angélica Cárcamo | Ing. Química (graduada) | Mar 2025 | BINID 2025 |
| Emanuel Silva Naveas | Ing. Electromecánica | Jul 2024 | BINID 2025 |
| Ricardo A. Heredia | Ing. Electromecánica | Jul 2024 | BINID 2025 |
| Matías I. Álvarez | Ing. Química | Abr 2024 | BINID 2025 |
| Gabriel F. Costilla | Ing. Pesquera | Abr 2023 | Beca "Gabriel y Jorge" 2025 |
| Jorge Rojas Flores | Ing. Pesquera | Abr 2023 | Beca "Gabriel y Jorge" 2025 |
| Facundo N. Gutiérrez | Ing. Química | Abr 2024 | — |

A lo largo del proyecto participaron 7 docentes investigadores y 17 alumnos (10 bajas o egresos, detallados en el informe de cierre). Se gestionaron 6 becas (4 BINID 2025 y 2 "Gabriel y Jorge" 2025).

---

## Matriz de investigación

El proyecto trabajó con **ruibarbo** (*Rheum rhabarbarum* L.) como única matriz activa. El alcance original se redujo de tres matrices a una.

| Matriz | Estado | Experimentos |
|---|---|---|
| 🌿 Ruibarbo | ✅ Activa | 3 ensayos exploratorios (2023–2024) + diseño compilado de 3 baterías (2024–2025) |
| 🌱 Salicornia (*Sarcocornia magellanica*) | ❌ Descartada | Motivos y fecha a precisar en el informe de cierre |
| 🦔 Erizo de mar (*Loxechinus albus*, *Pseudechinus magellanicus*) | ❌ Descartada | Logística y bibliografía avanzadas; motivos y fecha a precisar |

**Origen de las muestras:** huerta doméstica (Río Grande, invernadero, ecotipo más turgente) y Estancia Viamonte (30 km de Río Grande, exterior, ecotipo más blando).

### Trabajo experimental

**Ensayos exploratorios**

| Exp. | Fecha | Origen | Diseño | Resultado principal |
|---|---|---|---|---|
| Exp1 | 4 dic 2023 | Huerta doméstica (RG) | 4 muestras, punto único | Humedad del ruibarbo fresco: 94,3–94,6 % BH |
| Exp2 | 20–24 may 2024 | Estancia Viamonte | 8 frascos, 6–90 h | Primera curva de secado |
| Exp3 | 28 oct – 4 nov 2024 | Estancia Viamonte | 8 frascos, 12–96 h | Protocolo con doble barquillo; meseta desde 36 h (una sola repetición) |

**Diseño compilado (base del análisis estadístico)**

Tres baterías (nov 2024, ene 2025, feb 2025) × 3 pretratamientos (fresco, congelado a −18 °C, ultracongelado a ≤ −25 °C) × 3 repeticiones × 10 tiempos (6–96 h) = 270 registros. Se excluyeron 9 por goteo (ene 2025, congelado, 12/36/48 h): **261 observaciones válidas**.

### Resultados clave (cifras de la planilla original, ver corrección en curso)

| Parámetro | Valor |
|---|---|
| Humedad fresca | 94,3–94,6 % BH |
| Tiempo de estabilización (Δrel ≤ 1 %) | **48 h** (congelado y ultracongelado) · 72 h (fresco) |
| Rango práctico recomendado | 36–48 h |
| Pérdida de peso en la meseta | 92,0–92,3 % (→ 93,1–93,4 % con la fórmula corregida) |
| Condiciones del equipo (diseño compilado) | T condensador −41 a −35 °C · P 1,116–2,432 mmHg (202/261 obs.) · sin efecto significativo |

**Modelo de Page** — MR(t) = exp(−k·tⁿ), ajuste sobre medias de MR:

| Pretratamiento | k (h⁻ⁿ) | n | R² | RMSE |
|---|---|---|---|---|
| Fresco | 0,2564 | 0,6074 | 0,764 | 0,0728 |
| Congelado | 0,0869 | 0,8780 | 0,911 | 0,0633 |
| Ultracongelado | 0,1067 | 0,8323 | 0,924 | 0,0531 |

**Efecto del pretratamiento:** a 24 h el fresco pierde más peso que los precongelados (Kruskal-Wallis p = 0,0004; Dunn-Bonferroni fresco vs. congelado p = 0,0007, vs. ultracongelado p = 0,006). Desde 36 h los tres son equivalentes (p > 0,18). El precongelado no acelera el secado: aporta una cinética más predecible y el mismo resultado final.

**Reproducibilidad:** ANOVA Tipo II, R² = 0,923. Pretratamiento F = 25,18\*\*\* · Tiempo F = 322,97\*\*\* · Mes (bloque) p = 0,10 (ns) → resultados reproducibles entre baterías.

**Alcance:** toda la evidencia se apoya en una sola variable, la pérdida de peso. No se midieron aún humedad inicial por batería, humedad residual, actividad de agua ni parámetros de calidad, y no hay registro fotográfico estandarizado. Estas mediciones completan el OE3 y son necesarias para publicar.

Ver [`resultados_clave.md`](resultados_clave.md) y el preprint [`preprint/main.pdf`](preprint/main.pdf) para el detalle.

---

## Objetivos específicos homologados: cumplimiento

| OE | Objetivo | Estado |
|---|---|---|
| OE1 | Caracterización normativa de calidad | ✅ Cumplido (A1) |
| OE2 | Evaluar protocolos y seleccionar el más adecuado | ✅ Cumplido para ruibarbo: precongelado + ciclo 36–48 h. Falta validar con parámetros de calidad (OE3) |
| OE3 | Parámetros de calidad nutricionales, fisicoquímicos y organolépticos | ⏳ **Pendiente**: sin análisis bioquímicos, microbiológicos ni sensoriales. Método de aw desarrollado sin resultados informados. Análisis químicos previstos en el CIDCA |
| OE4 | Manual técnico-económico para el sector productivo | 🔄 En proceso (B1) |
| OE5 | Vinculación y transferencia | 🔄 Cumplido parcialmente (B3) |

---

## Equipamiento

- **Liofilizador:** RIFICOR LT-8 (Argentina) — 8 frascos independientes — laboratorio UTN FRTDF Río Grande. No siempre alcanzó las especificaciones del manual.
- **Balanza analítica:** OHAUS AR2140 (210 g, 0,1 mg). Sin mesa antivibratoria.
- **Balanza portátil:** OHAUS CR (2200 g, 1 g) — solicitud jun 2024
- **Termómetro digital:** Alla France −50 a +70 °C — solicitud jun 2024
- **Selladora al vacío:** Turbosaver + bolsas/rollos gofrados

---

## Estado de entregables (informe de cierre v2, septiembre 2026)

```
GRUPO A — TÉCNICO-CIENTÍFICOS
  A1 Marco normativo de calidad         ✅ Completado (abr–may 2023)
  A2 Protocolo liofilización — Ruibarbo 🔄 En proceso (~75%) — protocolo funcional, falta formalización final
  A3 Protocolo Salicornia               ❌ Cancelado (matriz descartada)
  A4 Protocolo Erizo de mar             ❌ Cancelado (matriz descartada)
  A5 Resultados experimentales          🔄 En proceso (~75%) — 261 obs.; corregir fórmula; faltan humedad
                                           residual, aw y análisis químicos
  A6 Resultados productos animales      ❌ Cancelado (matriz descartada)

GRUPO B — TRANSFERENCIA AL MEDIO
  B1 Manual técnico-económico           🔄 En proceso (~65%) — Cap. 1–6 + Anexos A, C, D; falta Anexo B y revisión
  B2 Informe final del PID              ⏳ Pendiente [OBLIGATORIO] — borrador v2 del informe de cierre en revisión
  B3 Vinculación y transferencia        🔄 En proceso (~70%) — Viamonte, productora local (2026), eventos, sitio web

GRUPO C — FORMACIÓN Y DIFUSIÓN
  C1 Consolidación grupo QA3DS          ✅ Completado
  C2 Artículos de divulgación           🔄 En proceso (~80%) — 2 artículos La Lupa redactados, pendiente envío
  C3 Presentaciones en jornadas         🔄 En proceso (~60%)

GRUPO D — EMERGENTES
  D1 Estudio de escalado                ✅ Completado (5 documentos técnico-económicos)
  D2 Artículo científico indexado       🔄 En proceso (~30%) — faltan datos fisicoquímicos, discusión y revista
  D3 Propuesta nuevo PID 2026           ⏳ Pendiente
  D4 Dashboard integral del proyecto    ✅ Completado (ETL + Dash, 4 pestañas)
  D5 Manuscrito científico (LaTeX)      🔄 En proceso (~50%) — requiere corrección de cifras, MR en base seca
                                           y reescritura por los autores
```

**Resumen:** 14 entregables activos (3 cancelados): 4 completados, 8 en proceso, 2 pendientes (B2 y D3).

👉 Ver los [issues](../../issues) y el [tablero del proyecto](../../projects) para el seguimiento.

### Actividades pendientes (prioridad según el informe v2)

| # | Actividad | Prioridad | Plazo |
|---|---|---|---|
| 1 | Cerrar las confirmaciones marcadas en rojo en el informe: protocolo de pesada, crédito, fin de la prórroga, plantel, convenio, motivos de descarte | Crítica | Inmediato |
| 2 | Corregir el cálculo de pérdida de peso en el código y regenerar resultados, figuras y documentos | Crítica | Tras confirmar el protocolo de pesada |
| 3 | Batería de caracterización en la condición recomendada (congelado, 48 h): humedad inicial y residual, aw, rehidratación, contracción | Alta | 1–2 meses |
| 4 | Registro fotográfico estandarizado de las tres condiciones | Alta | Junto con 3 |
| 5 | Análisis químicos en el CIDCA y comparación con secado tradicional | Alta | Según fondos |
| 6 | Completar B1 (Anexo B y revisión docente) | Alta | 1–2 meses |
| 7 | Enviar los artículos de La Lupa | Media | 1 mes |
| 8 | Manuscrito: discusión comparada, reescritura por los autores, revista de costo viable (Q3 o sin cargo) | Media | 3–4 meses |
| 9 | Formalizar B2 a partir del informe de cierre | Crítica | Al cierre de la prórroga |
| 10 | Formular propuesta de nuevo PID (D3) | Media | 3–6 meses |
| 11 | Avanzar con la propuesta de planta piloto (Fase 1 del escalado) | Baja | 6–12 meses |

**Presupuesto:** saldo al 31/12/2025 de ARS 243.561,48 (insumos, servicios y equipamiento; monto de insumos a verificar). Alcanza para una sola muestra del panel químico del CIDCA (ARS 224.750 por muestra), insuficiente para comparar. Se solicitó apoyo adicional a la Secretaría para un diseño mínimo de tres muestras.

---

## Estructura del repositorio

```
/
├── README.md
├── resultados_clave.md                    ← resumen de resultados estadísticos (cifras pre-corrección)
├── analisis_experimentos_compilado.ipynb  ← notebook de análisis (261 obs.)
├── docs/
│   ├── metodologia-estadistica.md
│   ├── B1-manual-tecnico-economico.md     ← manual extendido (borrador v0.1)
│   ├── protocolos/
│   │   └── SOP-LIO-RUI-v1.md              ← protocolo formal de liofilización de ruibarbo
│   └── entregables/
│       ├── A2-protocolo-ruibarbo.md
│       ├── A5-resultados-ruibarbo.md
│       ├── B1-manual-tecnico.md
│       └── B2-informe-final.md
├── preprint/
│   ├── informe_cierre.tex / .pdf          ← INFORME DE CIERRE, borrador v2 (sep 2026)
│   ├── main.tex / .pdf                    ← manuscrito científico (D5)
│   └── referencias.bib
├── dashboard/
│   ├── etl.py                             ← pipeline Excel → análisis → SQLite
│   ├── app.py                             ← aplicación Dash (4 pestañas)
│   ├── run.bat
│   └── README.md
├── figuras/                               ← 6 figuras PNG del análisis
└── .github/ISSUE_TEMPLATE/                ← plantillas de reporte de avance e insumos
```

Los datos crudos (planilla Excel de resultados) no están versionados en este repositorio. El ETL y el notebook los leen desde el espacio de trabajo local.

---

## Metodología

1. **Selección de materia prima** — criterios de calidad, origen y preparación (peciolos cortados a ~1 cm)
2. **Pretratamientos** — fresco, congelado (−18 °C), ultracongelado (≤ −25 °C)
3. **Liofilización** — curvas de pérdida de peso vs. tiempo (método gravimétrico)
4. **Análisis estadístico** — Modelo de Page, Kruskal-Wallis + Dunn-Bonferroni, ANOVA Tipo II, correlaciones de Spearman
5. **Caracterización del producto** — humedad residual, aw, rehidratación y análisis químicos (pendiente, OE3)
6. **Transferencia** — manual técnico-económico para productores de TDF

---

## Alianzas estratégicas

| Organización | Rol |
|---|---|
| Estancia Viamonte (Río Grande) | Proveedor de materia prima — convenio: firmado o en trámite, a confirmar |
| Productora local (2026) | Línea de trabajo 2026 para transferencia |
| CIDCA (CONICET-UNLP) | Panel de análisis químicos previsto (vitamina C, polifenoles, antioxidantes, antocianinas) |
| IIByT CONICET-UNC (Córdoba) | Análisis de actividad de agua (DVS) — previsto |
| CIATI (Bariloche) | Análisis microbiológico y rotulado nutricional — previsto |
| ICTA — FCEFyN UNC (Córdoba) | Evaluación sensorial — previsto |
| CADIC-CONICET (Ushuaia) | Capacitación inicial (nov 2022) |

---

## Publicaciones y presentaciones

- **Informe de cierre** — borrador v2 (sep 2026) en revisión por el equipo
- **Manuscrito científico** — "Cinética de liofilización de ruibarbo patagónico", borrador LaTeX (D5)
- **La Lupa** — 2 artículos de divulgación redactados, pendientes de envío
- **Jornadas CyT UTN FRTDF** — presentación oct 2023
- **Colegio de Ingenieros TDF** — poster QA3DS
- **Semana del Ambiente** — Municipio de Río Grande 2025

---

## Contacto

**Director del proyecto:** Ing. Pesq. Ariel Luján Giamportone
**Co-director:** Dr. Tomás Chalde
**Institución:** UTN Facultad Regional Tierra del Fuego
**Grupo QA3DS:** [GitHub](https://github.com/QA3DS) · [LinkedIn](https://www.linkedin.com/company/qu%C3%ADmica-aplicada-al-ambiente-los-alimentos-y-el-desarrollo-sostenible) · [ResearchGate](https://www.researchgate.net/lab/Quimica-aplicada-al-Ambiente-los-Alimentos-y-el-Desarrollo-Sostenible-Ariel-Lujan-Giamportone)

---

*PID PP9884 — UTN FRTDF · Río Grande, Tierra del Fuego, Argentina*
*Última actualización: noviembre 2026, según el informe de cierre v2 (septiembre 2026)*
