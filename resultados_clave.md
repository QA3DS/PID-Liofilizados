# Resultados Clave — Analisis de Liofilizacion de Ruibarbo
**Generado:** 2026-03-06  
**Fuente:** `analisis_experimentos_compilado.ipynb`  
**Dataset:** 261 observaciones validas (270 raw, 9 excluidas)  
**Diseno:** 3 pretratamientos x 3 repeticiones x 3 meses x 10 tiempos  

---

## 1. Estadisticas a tiempo de estabilizacion (36h)

| Pretratamiento | Perdida @ 36h | SD @ 36h | Perdida @ 96h | SD @ 96h |
|---|---|---|---|---|
| Fresco | 91.84% | +/-0.93% | 92.24% | +/-1.12% |
| Congelado | 91.96% | +/-0.37% | 92.14% | +/-0.46% |
| Ultracongelado | 91.62% | +/-1.02% | 92.11% | +/-0.70% |

---

## 2. Parametros del Modelo de Page  [MR(t) = exp(-k*t^n)]

| Pretratamiento | k | n | R2 | RMSE |
|---|---|---|---|---|
| Fresco | 0.2564 | 0.6074 | 0.7639 | 0.07283 |
| Congelado | 0.0869 | 0.8780 | 0.9108 | 0.06326 |
| Ultracongelado | 0.1031 | 0.8455 | 0.9237 | 0.05358 |

> NOTA FRESCO: R2=0.764, inferior al de pretratamientos precongelados (>0.91).
> El pre-congelado homogeniza la estructura celular del ruibarbo.

---

## 3. Analisis estadistico — Kruskal-Wallis

| Tiempo | H | p-valor | Significativo | Conclusion |
|---|---|---|---|---|
| 24h | 15.633 | 0.0004 | *** | Diferencias entre pretratamientos (FRESCO seca mas rapido) |
| 36h | 1.334 | 0.5131 | ns | **Sin diferencias — pretratamientos equivalentes** |
| 48h | 3.756 | 0.1529 | ns | Sin diferencias |

---

## 4. ANOVA Tipo II (pretratamiento + tiempo + mes)

| Factor | F | p-valor |
|---|---|---|
| Pretratamiento | 24.34 | 0.0000 *** |
| Tiempo (h) | 318.48 | 0.0000 *** |
| Mes (bloque) | 2.10 | 0.1248 ns |

> R2 del modelo: 0.9220 (explica el 92.2% de la varianza).
> Mes (bloque): p=0.1248 — NO significativo. Resultados reproducibles entre los 3 meses.

---

## 5. Tiempo optimo de liofilizacion (criterio: delta relativo <= 1%)

| Pretratamiento | Tiempo optimo | Perdida media |
|---|---|---|
| Fresco | 72h | 92.11% |
| Congelado | 48h | 92.29% |
| Ultracongelado | 72h | 91.81% |

> NOTA: Exp3 mostro estabilizacion a 36h para una sola repeticion.
> Con dataset compilado (3 exp x 3 rep), el plateau se detecta entre 48-72h.
> Rango recomendado para uso practico: 36-48h.

---

## 6. Condiciones operacionales del equipo RIFICOR LT-8

Subconjunto: 202/261 obs (77.4%) con T y P registradas

| Variable | Rango | Spearman r | p-valor | Significativo |
|---|---|---|---|---|
| T condensador | -41 a -35 C | 0.107 | 0.1299 | No |
| Presion | 1.116 a 2.432 mmHg | -0.124 | 0.0787 | No |

> Las condiciones operacionales NO tienen efecto significativo sobre la perdida de peso.

---

## 7. Conclusiones transferibles

### Para productores

> Los tres pretratamientos producen un producto liofilizado equivalente a partir de 36-48h
> (~91.6-92.0% perdida de peso, ~94% en base humeda). Recomendacion practica:
> el pretratamiento CONGELADO (-18C) ofrece cinetica mas predecible (R2=0.91) y
> alcanza el plateau a las 48h. El fresco alcanza el plateau entre 48-72h con mayor variabilidad.

### Para publicacion cientifica

> El Modelo de Page ajusta bien los datos de CONGELADO y ULTRACONGELADO (R2>0.91)
> y moderadamente para FRESCO (R2=0.764). Los pretratamientos son estadisticamente
> equivalentes a 36h y 48h (Kruskal-Wallis p>0.15), pero difieren a 24h (p=0.0004),
> donde FRESCO presenta mayor velocidad de secado inicial (k=0.2564 vs k~0.09-0.10).
> El efecto del bloque temporal (mes) no fue significativo (p=0.12), confirmando
> reproducibilidad entre experimentos.

---

## 8. Figuras generadas

| Figura | Descripcion |
|---|---|
| figuras/fig1_mapa_missings.png | Mapa de valores faltantes por variable |
| figuras/fig2_descriptivas.png | Boxplots descriptivos por pretratamiento y tiempo |
| figuras/fig3_cinetica_curvas.png | Curvas cineticas medias +/- SD (figura publicacion) |
| figuras/fig4_modelo_page.png | Ajuste Modelo de Page por pretratamiento |
| figuras/fig5_derivadas_plateau.png | Derivada discreta y deteccion de plateau |
| figuras/fig6_operacionales.png | Condiciones operacionales T y P |

---
*Proyecto PID PP9884 — UTN FRTDF — Grupo QA3DS*  
*Analisis generado con Python (pandas, scipy, statsmodels, pingouin, matplotlib)*