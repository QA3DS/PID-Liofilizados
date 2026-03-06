# A5 — Resultados Experimentales: Ruibarbo Liofilizado

**Estado:** 🔄 En proceso — avance ~50%
**Responsable:** Angélica Cárcamo · Facundo Gutiérrez · Matías Álvarez
**Issue GitHub:** #5
**Objetivo PID:** OE3

---

## 1. Alcance

Este documento consolida los resultados analíticos que caracterizan el producto liofilizado de ruibarbo (*Rheum rhabarbarum* L.) obtenido mediante el protocolo desarrollado en A2. Incluye análisis internos (laboratorio UTN FRTDF) y análisis externos (servicios de terceros).

---

## 2. Muestras analizadas

| Muestra | Experimento | Tiempo liofilización | Origen |
|---|---|---|---|
| Ruibarbo fresco — Exp3 | Exp3 oct-nov 2024 | 0 h (control) | Estancia Viamonte |
| Ruibarbo liofilizado — Exp3 | Exp3 oct-nov 2024 | 36 h (óptimo) | Estancia Viamonte |
| Ruibarbo liofilizado — Exp4 | Exp4 (en proceso) | 36 h | A confirmar |

---

## 3. Análisis internos — Laboratorio UTN FRTDF

### 3.1 Humedad (% BH)

**Método:** Gravimétrico indirecto (García Martínez & Fernández Segovia, 2012)
**Equipo:** OHAUS AR2140 (210g, 0.1mg)

| Muestra | % Humedad BH | Fecha análisis |
|---|---|---|
| Fresco (promedio Exp1-3) | 94.3–94.6% | — |
| Liofilizado 36h (Exp3) | ~5.5% | — |

> **Pendiente:** completar tabla con datos de Exp4 y análisis formal de triplicados.

### 3.2 Proteínas totales

**Método:** Lowry et al. (1951) — estándar seroalbúmina
**Estado:** ⏳ Pendiente

| Muestra | Proteínas totales (g/100g) | Fecha análisis |
|---|---|---|
| Fresco | — | — |
| Liofilizado | — | — |

### 3.3 Carbohidratos totales

**Método:** Antrona (Fraga, 1956; Yemm & Willis, 1954) — estándar glucosa
**Estado:** ⏳ Pendiente

| Muestra | Carbohidratos totales (g/100g) | Fecha análisis |
|---|---|---|
| Fresco | — | — |
| Liofilizado | — | — |

### 3.4 Lípidos totales

**Método:** Gravimétrico Folch et al. (1957) — extracción cloroformo-metanol
**Estado:** ⏳ Pendiente

| Muestra | Lípidos totales (g/100g) | Fecha análisis |
|---|---|---|
| Fresco | — | — |
| Liofilizado | — | — |

### 3.5 pH

**Equipo:** pHmetro disponible en FRTDF
**Estado:** ⏳ Pendiente

| Muestra | pH | Fecha análisis |
|---|---|---|
| Fresco | — | — |
| Liofilizado | — | — |

---

## 4. Análisis externos — Servicios de terceros

### 4.1 Actividad de agua (aw)

**Servicio:** IIByT CONICET-UNC (Córdoba) — técnica DVS (adsorción/desorción dinámica de vapores)
**Estado:** ⏳ Pendiente — coordinar envío de muestras

| Muestra | aw | Fecha análisis |
|---|---|---|
| Fresco | — | — |
| Liofilizado 36h | — | — |

> **Nota:** el valor de aw del producto final debe ser ≤ 0.6 para garantizar conservación sin cadena de frío.

**Referencia in-house:** método estático con sales saturadas desarrollado por Michael Trujillo (`E:/Investigacion 24 Javi/.../actividad de agua/PLANILLA DE CONTROL.xlsx`)

### 4.2 Calidad microbiológica

**Servicio:** CIATI (Bariloche)
**Estado:** ⏳ Pendiente — coordinar envío de muestras

Análisis requeridos:
- [ ] Recuento de aerobios totales (UFC/g)
- [ ] Hongos y levaduras (UFC/g)
- [ ] Coliformes totales (UFC/g)
- [ ] *Salmonella* spp. (presencia/ausencia en 25g)
- [ ] *E. coli* (UFC/g)

| Parámetro | Límite CAA | Resultado | Fecha |
|---|---|---|---|
| Aerobios totales | — | — | — |
| Hongos y levaduras | — | — | — |
| Coliformes totales | — | — | — |
| *Salmonella* | Ausencia | — | — |

### 4.3 Composición nutricional y rotulado

**Servicio:** CIATI (Bariloche)
**Estado:** ⏳ Pendiente

- [ ] Análisis composicional completo (según normas CAA / ANMAT)
- [ ] Diseño de rótulo nutricional
- [ ] Declaración de propiedades nutricionales si corresponde

### 4.4 Evaluación sensorial

**Servicio:** ICTA — FCEFyN UNC (Córdoba)
**Estado:** ⏳ Pendiente

Atributos a evaluar:
- [ ] Color (comparación fresco vs. liofilizado)
- [ ] Aroma
- [ ] Sabor / gusto
- [ ] Textura (crujiente, friable)
- [ ] Apariencia general

---

## 5. Análisis comparativo

### 5.1 Fresco vs. liofilizado

| Parámetro | Fresco | Liofilizado 36h | Retención (%) |
|---|---|---|---|
| Humedad (%) | 94.3–94.6 | ~5.5 | — |
| Proteínas (g/100g) | — | — | — |
| Lípidos (g/100g) | — | — | — |
| Carbohidratos (g/100g) | — | — | — |
| aw | — | — | — |

### 5.2 Comparación entre formatos de corte

> ⏳ Pendiente — diseñar experimento comparativo

### 5.3 Comparación entre ecotipos (invernadero vs. exterior)

> ⏳ Pendiente — diseñar experimento comparativo

---

## 6. Análisis cinético y estadístico — Dataset compilado Exp1–Exp3

> **Estado:** ✅ Completado — Marzo 2026
> **Fuente:** `analisis_experimentos_compilado.ipynb` · `resultados_clave.md`
> **Metodología detallada:** [`docs/metodologia-estadistica.md`](../metodologia-estadistica.md)

### 6.1 Dataset

270 observaciones (261 válidas) de diseño factorial balanceado **3 pretratamientos × 3 repeticiones × 3 meses × 10 tiempos (6–96h)**.

### 6.2 Pérdida de peso a tiempo de estabilización

| Pretratamiento | Pérdida @ 36h (media ± SD) | Pérdida @ 96h (media ± SD) |
|---|---|---|
| FRESCO | 91.84% ± 0.93% | 92.24% ± 1.12% |
| CONGELADO | 91.96% ± 0.37% | 92.14% ± 0.46% |
| ULTRACONGELADO | 91.62% ± 1.02% | 92.11% ± 0.70% |

### 6.3 Parámetros del Modelo de Page — `MR(t) = exp(−k·tⁿ)`

| Pretratamiento | k | n | R² | RMSE | Interpretación |
|---|---|---|---|---|---|
| FRESCO | 0.2564 | 0.6074 | 0.764 | 0.0728 | Velocidad inicial alta; mayor variabilidad |
| CONGELADO | 0.0869 | 0.8780 | 0.911 | 0.0633 | Cinética predecible |
| ULTRACONGELADO | 0.1031 | 0.8455 | 0.924 | 0.0536 | Mejor ajuste del modelo |

> FRESCO presenta k ≈ 3× mayor que los pretratamientos con congelado previo: seca más rápido al inicio pero con mayor variabilidad entre repeticiones (R²=0.764 vs >0.91). El pre-congelado homogeniza la estructura celular del ruibarbo.

### 6.4 Análisis estadístico — Kruskal-Wallis por tiempo

| Tiempo | H | p-valor | Conclusión |
|---|---|---|---|
| 24h | 15.633 | **0.0004 (\*\*\*)** | FRESCO seca significativamente más rápido |
| 36h | 1.334 | 0.5131 (ns) | Los tres pretratamientos son equivalentes |
| 48h | 3.756 | 0.1529 (ns) | Los tres pretratamientos son equivalentes |

**ANOVA Tipo II** (pretratamiento + tiempo + bloque mes): R² = 0.922
- Pretratamiento: F=24.34, p<0.0001 ✅
- Tiempo: F=318.48, p<0.0001 ✅
- Bloque mes: p=0.125 ns → **resultados reproducibles entre los 3 experimentos**

### 6.5 Tiempo óptimo de liofilización (criterio Δ relativo ≤ 1%)

| Pretratamiento | Tiempo óptimo (dataset compilado) | Pérdida media |
|---|---|---|
| FRESCO | 72h | 92.11% |
| CONGELADO | **48h** | 92.29% |
| ULTRACONGELADO | 72h | 91.81% |

> **Rango práctico recomendado: 36–48h.** El Exp3 mostró estabilización a 36h para una repetición; el dataset compilado (3 experimentos × 3 repeticiones) confirma plateau entre 48–72h, con CONGELADO como el pretratamiento más eficiente.

### 6.6 Condiciones operacionales (RIFICOR LT-8)

Las condiciones registradas (T° -41 a -35°C; P 1.1 a 2.4 mmHg) **no tienen efecto significativo** sobre la pérdida de peso dentro del rango de operación normal del equipo (Spearman: T° r=0.107 p=0.130; P° r=-0.124 p=0.079).

### 6.7 Alerta de calidad de datos

⚠️ 3 muestras de ENE-2025 (AC1, BC1, CC1) tienen anotación *"El código en cuaderno es de Fresco"*. Verificar etiquetado correcto en cuaderno de laboratorio antes de publicar.

---

## 7. Checklist de tareas

**Análisis internos:**
- [ ] Proteínas (Lowry) — Responsable: Cárcamo / Gutiérrez
- [ ] Carbohidratos (Antrona) — Responsable: Gutiérrez / Álvarez
- [ ] Lípidos (Folch) — Responsable: Cárcamo
- [ ] pH

**Análisis externos:**
- [ ] Solicitar presupuesto a IIByT para aw
- [ ] Solicitar presupuesto a CIATI para microbiológico + nutricional
- [ ] Solicitar presupuesto a ICTA para sensorial
- [ ] Coordinar envío de muestras
- [ ] Recibir resultados y completar tablas

**Análisis de datos:**
- [x] Análisis cinético compilado (Exp1–Exp3) — Sección 6, marzo 2026
- [x] Modelo de Page ajustado por pretratamiento
- [x] Análisis estadístico Kruskal-Wallis + ANOVA Tipo II
- [x] Detección de tiempo óptimo (plateau)
- [ ] Completar dataset con análisis bioquímicos (Lowry, Antrona, Folch)
- [ ] Análisis comparativo fresco vs. liofilizado (una vez completos análisis bioquímicos)
- [ ] Preparar tablas y figuras para B1 y D2

---

## 8. Archivos relacionados

| Archivo | Descripción |
|---|---|
| `analisis_experimentos_compilado.ipynb` | Notebook análisis estadístico completo (Exp1–Exp3) |
| `resultados_clave.md` | Síntesis de resultados del análisis compilado |
| `docs/metodologia-estadistica.md` | Justificación estadística y matemática de los análisis |
| `figuras/fig3_cinetica_curvas.png` | Curvas cinéticas medias ± SD (figura publicación) |
| `figuras/fig4_modelo_page.png` | Ajuste Modelo de Page por pretratamiento |
| `E:/Investigacion 24 Javi/.../actividad de agua/PLANILLA DE CONTROL.xlsx` | Datos aw in-house |
| `scripts/proyecto_liofilizados_data.ipynb` | Framework de análisis en Python |
| `Articulo Liof LUPA/Efecto de las condiciones de liofilizacion...pdf` | Referencia metodológica |

---

## 9. Referencias

- Lowry, O.H. et al. (1951). Protein measurement with the Folin phenol reagent. *J. Biol. Chem.*, 193(1), 265–275.
- Folch, J. et al. (1957). A simple method for the isolation and purification of total lipides from animal tissues. *J. Biol. Chem.*, 226(1), 497–509.
- Fraga, C.G. (1956). Method for carbohydrate determination.

---

*Última actualización: marzo 2026*
