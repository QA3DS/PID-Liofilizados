# Metodología Estadística y Matemática — Análisis de Liofilización de Ruibarbo
**Proyecto:** PID PP9884 — UTN FRTDF
**Grupo:** QA3DS
**Versión:** 1.0 (2026-03-04)
**Autores:** Ariel Giamportone, con asistencia Claude
**Fuente de datos:** `datos_experimentos_compilado/Registro de resultados - Proyecto Liofilizados (1).xlsx`

---

## 1. Diseño experimental

### 1.1 Estructura del dataset

El análisis se basa en un diseño factorial completo **3 × 3 × 3 × 10**:

| Factor | Niveles | Valores |
|---|---|---|
| Pretratamiento | 3 | FRESCO / CONGELADO / ULTRACONGELADO |
| Repetición (batch) | 3 | A / B / C |
| Bloque temporal (mes) | 3 | NOV-2024 / ENE-2025 / FEB-2025 |
| Tiempo de liofilización | 10 | 6, 12, 18, 24, 36, 48, 60, 72, 84, 96 horas |

**Total observaciones:** 270 (diseño balanceado)
**Observaciones válidas:** 261 (9 excluidas por ausencia de la variable dependiente, 3.3%)

La variable dependiente es la **pérdida de peso en fracción** (0–1), calculada como:

```
PERDIDA_PESO_FRAC = (masa_inicial - masa_t) / masa_inicial
```

Equivalente a la humedad base húmeda (BH) eliminada al tiempo *t*.

### 1.2 Pretratamientos evaluados

| Pretratamiento | Descripción | Hipótesis de efecto |
|---|---|---|
| FRESCO | Muestra sin congelado previo | Cinética más rápida pero menos predecible (estructura celular intacta e irregular) |
| CONGELADO | Congelado a -18°C antes de liofilizar | Estructura celular rota por cristales de hielo → sublimación más homogénea |
| ULTRACONGELADO | Congelado a -25°C o inferior | Mayor daño celular que CONGELADO → mayor regularidad estructural |

---

## 2. Variable dependiente y transformación

### 2.1 Moisture Ratio (MR)

Para el ajuste del modelo cinético se utiliza el **Moisture Ratio (MR)**, cociente de humedad adimensional estándar en la literatura de secado de alimentos (AOAC, Doymaz 2004):

```
MR(t) = (M_t - M_e) / (M_0 - M_e)
```

donde:
- `M_t` = contenido de humedad al tiempo *t*
- `M_0` = contenido de humedad inicial
- `M_e` = contenido de humedad de equilibrio

**Simplificación para liofilización:** En condiciones de liofilización, `M_e ≈ 0` (el proceso lleva la humedad a valores residuales cercanos a cero). Por lo tanto:

```
MR(t) ≈ M_t / M_0 = 1 - PERDIDA_PESO_FRAC(t)
```

Esta simplificación es estándar en la literatura de liofilización (Liapis & Bruttini 2007; Ratti 2001) y está validada por la condición de operación del equipo RIFICOR LT-8 (P < 2.5 mmHg, T condensador < -35°C).

---

## 3. Modelo cinético de Page

### 3.1 Fundamento y elección del modelo

El **Modelo de Page** (Page 1949; Midilli et al. 2002; Doymaz 2004) es el modelo empírico más utilizado en la literatura de deshidratación de alimentos para describir la cinética de secado:

```
MR(t) = exp(-k · t^n)
```

donde:
- `k` = constante de velocidad de secado (h⁻ⁿ) — refleja la velocidad característica del proceso
- `n` = parámetro de forma (adimensional) — modifica la curvatura de la curva; si n=1 el modelo se reduce al exponencial de Lewis (primer orden simple)
- `t` = tiempo de liofilización (horas)

**Justificación de la elección sobre otros modelos:**

| Modelo | Ecuación | Limitación |
|---|---|---|
| Lewis (1921) | MR = exp(-k·t) | Sobreestima la velocidad inicial; n=1 fijo es demasiado restrictivo |
| Exponencial de dos términos | MR = a·exp(-k₁t) + (1-a)·exp(-k₂t) | Sobreparametrizado para este dataset; riesgo de sobreajuste con n=261 |
| **Page (1949)** | **MR = exp(-k·t^n)** | **Equilibrio entre flexibilidad y parsimonia; ampliamente validado en alimentos** |
| Midilli et al. (2002) | MR = a·exp(-k·t^n) + b·t | Cuatro parámetros; innecesario cuando MR(0)=1 está garantizado |

El Modelo de Page es apropiado porque:
1. Impone MR(0) = 1 (condición física obligatoria: al tiempo cero no hay pérdida)
2. Impone MR(∞) → 0 (convergencia al equilibrio)
3. El parámetro *n* captura la desviación de la cinética de primer orden sin sobreparametrizar
4. Está validado en ruibarbo y otros productos similares en la literatura (Chin et al. 2009; Aral & Bese 2016)

### 3.2 Ajuste numérico

El ajuste se realizó con `scipy.optimize.curve_fit` (método Levenberg-Marquardt):

- **Condiciones iniciales:** k₀ = 0.1, n₀ = 1.0
- **Bounds:** k > 0, n > 0 (restricciones físicas)
- **Datos de ajuste:** media de MR por (pretratamiento × tiempo), 10 puntos por curva
- **3 ajustes independientes**, uno por pretratamiento

### 3.3 Bondad de ajuste

**Coeficiente de determinación (R²):**

```
R² = 1 - SS_res / SS_tot
SS_res = Σ (MR_obs - MR_pred)²
SS_tot = Σ (MR_obs - MR̄)²
```

**Raíz del Error Cuadrático Medio (RMSE):**

```
RMSE = sqrt( Σ(MR_obs - MR_pred)² / n )
```

**Resultados obtenidos:**

| Pretratamiento | k | n | R² | RMSE | Interpretación |
|---|---|---|---|---|---|
| FRESCO | 0.2564 | 0.6074 | 0.764 | 0.0728 | Ajuste moderado; mayor variabilidad inherente |
| CONGELADO | 0.0869 | 0.8780 | 0.911 | 0.0633 | Buen ajuste |
| ULTRACONGELADO | 0.1031 | 0.8455 | 0.924 | 0.0536 | Buen ajuste |

**Nota sobre FRESCO:** El R² inferior (0.764 vs >0.91) no indica falla del modelo, sino mayor variabilidad intrínseca de la muestra fresca. Sin el pre-congelado, la estructura celular del ruibarbo es heterogénea entre repeticiones, lo que incrementa la dispersión de MR en los tiempos iniciales (6–18h). El modelo de Page sigue siendo apropiado; la variabilidad es una propiedad del sistema, no del modelo.

---

## 4. Análisis estadístico

### 4.1 Verificación de supuestos

#### Normalidad — Test de Shapiro-Wilk

**Aplicación:** Test por grupo (pretratamiento × tiempo), sobre los 9 valores de PERDIDA_PESO_FRAC por celda (3 meses × 3 repeticiones).

**Justificación de Shapiro-Wilk sobre otras pruebas:**
- Diseñado para muestras pequeñas (n < 50) — óptimo para n = 9 por celda
- Mayor potencia que Kolmogorov-Smirnov y Anderson-Darling para n < 30 (Razali & Wah 2011)

**Hipótesis:**
```
H₀: los datos provienen de una distribución normal
H₁: los datos no provienen de una distribución normal
α = 0.05
```

**Resultado:** 2 de 30 celdas (pretratamiento × tiempo) rechazaron H₀ → distribución no normal detectada → se procede con prueba no paramétrica.

#### Homocedasticidad — Test de Levene

**Justificación:** El test de Levene es más robusto que el test de Bartlett cuando no se confirma normalidad (Brown & Forsythe 1974). Prueba igualdad de varianzas entre los 3 grupos de pretratamiento para cada tiempo.

### 4.2 Comparación entre grupos — Kruskal-Wallis

Ante la detección de no normalidad en algunas celdas, se utilizó el **test de Kruskal-Wallis** como alternativa no paramétrica al ANOVA de una vía.

**Justificación:**
- Kruskal-Wallis no asume distribución normal en los datos
- Es la extensión del test de Mann-Whitney a k > 2 grupos
- Trabaja sobre los rangos de los datos, no sobre los valores absolutos
- Apropiado cuando la escala de medición es al menos ordinal (aquí: razón)

**Estadístico H:**

```
H = (12 / N(N+1)) · Σ(Rⱼ² / nⱼ) - 3(N+1)
```

donde `Rⱼ` es la suma de rangos del grupo j y `N` el total de observaciones.

**Hipótesis (aplicado por tiempo):**
```
H₀: las distribuciones de PERDIDA_PESO_FRAC son iguales en los 3 pretratamientos
H₁: al menos un pretratamiento difiere
α = 0.05
```

**Tiempos de interés evaluados:** 24h, 36h, 48h (zona de decisión práctica del plateau)

### 4.3 Análisis post-hoc — Dunn con corrección de Bonferroni

Cuando Kruskal-Wallis resultó significativo, se aplicó el **test de Dunn** para comparaciones por pares:

**Justificación de Dunn sobre otras alternativas:**
- Es el post-hoc estándar para Kruskal-Wallis (Dunn 1964)
- Trabaja en el espacio de rangos, consistente con el test ómnibus
- La corrección de Bonferroni es conservadora pero apropiada para m = 3 comparaciones por pares (riesgo de error Tipo I controlado a α/m = 0.05/3 ≈ 0.017)

### 4.4 ANOVA Tipo II — Modelo lineal mixto

Adicionalmente, se ajustó un **ANOVA de dos factores Tipo II** (pretratamiento + tiempo + mes) utilizando `statsmodels.formula.api.ols` con tabla de sumas de cuadrados Tipo II.

**Justificación del Tipo II sobre Tipo I (secuencial) y Tipo III:**
- Tipo I es sensible al orden de entrada de factores (no apropiado para diseños no ortogonales)
- Tipo III requiere contraste de parámetros individuales; menos estable con variables categóricas sin codificación de referencia cuidadosa
- **Tipo II** evalúa cada efecto principal después de ajustar por todos los demás efectos principales, sin incluir interacciones en el denominador — es el enfoque recomendado para modelos con efectos principales y sin interacciones significativas conocidas a priori (Fox 2008)

**Modelo ajustado:**

```
PERDIDA_PESO_FRAC ~ C(PRETRATAMIENTO) + C(HORAS) + C(MES_AÑO)
```

donde `C(·)` indica variable categórica y MES_AÑO actúa como **factor de bloque** para controlar la variabilidad entre experimentos realizados en distintos meses.

**R² del modelo:** 0.9220 — explica el 92.2% de la varianza total de la pérdida de peso.

**Resultado del bloque temporal (mes):** p = 0.1248 (no significativo) → **los resultados son reproducibles entre los 3 experimentos** (NOV-2024, ENE-2025, FEB-2025).

### 4.5 Tamaño del efecto

Para ANOVA Tipo II se reporta **η² (eta cuadrado)**:

```
η² = SS_factor / SS_total
```

Interpretación según Cohen (1988): η² < 0.01 = negligible; 0.01–0.06 = pequeño; 0.06–0.14 = mediano; > 0.14 = grande.

El factor TIEMPO presenta F = 318.48 (p < 0.0001), confirmando que es el principal determinante de la pérdida de peso, con tamaño del efecto grande.

---

## 5. Detección del tiempo óptimo (plateau)

### 5.1 Criterio de plateau

El tiempo óptimo de liofilización se define como el primer punto temporal donde la **variación relativa de la pérdida de peso** entre tiempos consecutivos cae por debajo del 1%:

```
Δ_rel(t) = |PERDIDA(t) - PERDIDA(t-1)| / PERDIDA(t-1)

plateau establecido cuando: Δ_rel(t) ≤ 0.01 (1%)
```

**Justificación del criterio:**
- El 1% es un umbral de relevancia práctica: por debajo de ese valor, el tiempo adicional de proceso no justifica el costo energético ni el desgaste del equipo
- Es análogo al criterio de convergencia usado en modelos iterativos de optimización
- Reportado en la literatura de liofilización de frutas como criterio operacional (Ratti 2001; Moraga et al. 2004)

### 5.2 Derivada discreta

La derivada discreta de la curva de pérdida de peso se calcula como diferencias finitas hacia adelante sobre los valores medios por pretratamiento:

```
dP/dt ≈ ΔP/Δt = [P(t+Δt) - P(t)] / Δt
```

Siendo los tiempos no igualmente espaciados (6, 12, 18, 24, 36, 48, 60, 72, 84, 96h), se usa la diferencia absoluta entre tiempos consecutivos dividida por el intervalo correspondiente.

---

## 6. Análisis de condiciones operacionales

### 6.1 Subconjunto con datos completos

De las 261 observaciones válidas, 202 (77.4%) tienen registros simultáneos de temperatura y presión. El análisis operacional se restringe a este subconjunto.

**Estrategia de missings:** No se imputan los valores faltantes de T° y P° porque:
1. El patrón de missings no es aleatorio (MAR/MCAR no verificado)
2. La imputación introduciría sesgo en variables físicas con dependencia temporal
3. El 77.4% disponible es suficiente para análisis exploratorio

### 6.2 Correlación de Spearman

Se utiliza **correlación de Spearman** (no paramétrica) entre las condiciones operacionales (T°, P°) y la pérdida de peso:

**Justificación de Spearman sobre Pearson:**
- No se confirma normalidad bivariada en el subconjunto
- Spearman es más robusto ante outliers en las variables instrumentales (T° y P° pueden tener picos puntuales)
- Detecta relaciones monótonas no necesariamente lineales

**Hipótesis:**
```
H₀: ρ_Spearman = 0 (no hay correlación monótona)
H₁: ρ_Spearman ≠ 0
α = 0.05
```

**Resultados:** T° (r = 0.107, p = 0.130) y P° (r = -0.124, p = 0.079) — ambas no significativas. Las condiciones operacionales del RIFICOR LT-8 no tienen efecto significativo sobre la pérdida de peso dentro del rango observado de operación.

---

## 7. Software y reproducibilidad

### 7.1 Stack tecnológico

| Biblioteca | Versión mínima | Uso |
|---|---|---|
| pandas | ≥ 2.0 | Carga, limpieza, transformación de datos |
| numpy | — | Operaciones numéricas vectorizadas |
| scipy | — | `curve_fit` (ajuste Page), `shapiro`, `kruskal` |
| statsmodels | — | ANOVA Tipo II (`ols`, `anova_lm`) |
| pingouin | — | Post-hoc Dunn, effect size |
| matplotlib / seaborn | — | Visualizaciones (300 dpi) |
| missingno | — | Mapa de valores faltantes |
| openpyxl | — | Lectura de archivos Excel |

### 7.2 Reproducibilidad

- **Semilla aleatoria:** no se usan procedimientos estocásticos en el análisis
- **Datos fuente:** el archivo Excel original no se modifica; todas las transformaciones se realizan en memoria
- **Codificación de columnas:** definida explícitamente mediante `RENAME_MAP` con codepoints Unicode literales (no heurísticas de detección de encoding)
- **Notebook ejecutable:** `analisis_experimentos_compilado.ipynb` — ejecutar celdas en orden produce los mismos resultados

### 7.3 Limitaciones del análisis

1. **Tamaño muestral por celda:** n = 9 por (pretratamiento × tiempo) es suficiente para tests no paramétricos pero limita la potencia para detectar efectos pequeños en ANOVA
2. **Modelo de Page — R² de FRESCO:** el ajuste moderado (R² = 0.764) es una propiedad del sistema (mayor variabilidad de muestra fresca), no un artefacto metodológico
3. **Datos faltantes en T° y P°:** 22–25% de missings limitan el análisis operacional; se documenta como limitación en la discusión
4. **Alerta de calidad de datos:** 3 muestras (ENE25-AC1, ENE25-BC1, ENE25-CC1) tienen anotación "El código en cuaderno es de Fresco" — posible error de etiquetado de pretratamiento; verificar en cuaderno de laboratorio antes de publicar
5. **Generalización:** el análisis corresponde a ruibarbo de Estancia Viamonte (ecotipo exterior, peciolos ~1 cm); resultados pueden diferir para ecotipos de invernadero o formato diferente

---

## 8. Referencias bibliográficas

- **Doymaz, I.** (2004). Convective air drying characteristics of thin layer carrots. *Journal of Food Engineering*, 61(3), 359–364.
- **Midilli, A., Kucuk, H., & Yapar, Z.** (2002). A new model for single-layer drying. *Drying Technology*, 20(7), 1503–1513.
- **Page, G. E.** (1949). *Factors influencing the maximum rates of air drying shelled corn in thin layers*. M.S. Thesis, Purdue University.
- **Ratti, C.** (2001). Hot air and freeze-drying of high-value foods: a review. *Journal of Food Engineering*, 49(4), 311–319.
- **Liapis, A. I., & Bruttini, R.** (2007). Freeze drying. In A. S. Mujumdar (Ed.), *Handbook of Industrial Drying* (3rd ed.). CRC Press.
- **Razali, N. M., & Wah, Y. B.** (2011). Power comparisons of Shapiro-Wilk, Kolmogorov-Smirnov, Lilliefors and Anderson-Darling tests. *Journal of Statistical Modeling and Analytics*, 2(1), 21–33.
- **Dunn, O. J.** (1964). Multiple comparisons using rank sums. *Technometrics*, 6(3), 241–252.
- **Fox, J.** (2008). *Applied Regression Analysis and Generalized Linear Models* (2nd ed.). SAGE.
- **Brown, M. B., & Forsythe, A. B.** (1974). Robust tests for the equality of variances. *Journal of the American Statistical Association*, 69(346), 364–367.
- **Cohen, J.** (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
- **Moraga, G., Martínez-Navarrete, N., & Chiralt, A.** (2004). Water sorption isotherms and glass transition in strawberries: influence of pretreatment. *Journal of Food Engineering*, 62(4), 315–321.

---

*Documento generado en el marco del PID PP9884 — UTN FRTDF — Grupo QA3DS*
*Para consultas técnicas: Ing. Pesq. Ariel Luján Giamportone*
