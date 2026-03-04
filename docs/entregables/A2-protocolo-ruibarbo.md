# A2 — Protocolo de Liofilización: Ruibarbo (*Rheum rhabarbarum* L.)

**Estado:** 🔄 En proceso — avance ~75%
**Responsable:** Javier Alfarano (coord.) · Facundo Gutiérrez · Matías Álvarez
**Issue GitHub:** #2
**Objetivo PID:** OE2

---

## 1. Alcance

Este protocolo describe el proceso estandarizado de liofilización para ruibarbo de producción local en Tierra del Fuego, desde la recepción de la materia prima hasta el producto final envasado. Es aplicable al liofilizador RIFICOR LT-8 disponible en UTN FRTDF Río Grande.

---

## 2. Materia prima

### 2.1 Criterios de selección

- **Variedad:** *Rheum rhabarbarum* L. (ruibarbo común)
- **Parte utilizada:** peciolos (tallos)
- **Estado:** frescos, sin daños físicos visibles, sin podredumbre
- **Madurez:** peciolos completamente desarrollados

### 2.2 Orígenes validados

| Origen | Tipo de cultivo | Observaciones |
|---|---|---|
| Virginia Saldivia (Río Grande) | Huerta doméstica, invernadero | Mayor turgencia, mayor humedad inicial |
| Estancia Viamonte (30 km de RG) | Exterior | Más blanda, menor humedad inicial — Exp2, 3, 4+ |

### 2.3 Recepción y muestreo

- Protocolo de muestreo: método de cuadrantes (promedio móvil)
- Registrar: fecha de cosecha, origen, condiciones de transporte
- Temperatura de conservación previo al proceso: refrigerado o a temperatura ambiente (máx. 24h)

---

## 3. Preprocesamiento

1. **Lavado:** agua potable corriente, eliminar restos de tierra y hojas
2. **Secado superficial:** papel absorbente o reposo en superficie limpia
3. **Corte:** peciolos cortados transversalmente en secciones de ~1 cm
4. **Pesado inicial:** balanza analítica OHAUS AR2140 (0.1 mg)
5. **Colocación en frascos:** ~50 g por frasco del liofilizador (capacidad: 8 frascos)
6. **Congelamiento previo:** -18 a -25°C (freezer estándar) — mínimo 12 horas

> **Nota:** el congelamiento previo es crítico para garantizar la formación correcta de cristales de hielo antes de la sublimación.

---

## 4. Proceso de liofilización

### 4.1 Equipo

- **Modelo:** RIFICOR LT-8 (Argentina)
- **Configuración:** 8 frascos/compartimientos independientes retirables sin romper vacío
- **Ubicación:** Laboratorio UTN FRTDF, Río Grande

### 4.2 Parámetros del proceso (según Exp3 — protocolo mejorado)

| Parámetro | Valor |
|---|---|
| Temperatura del condensador | -36 a -41°C |
| Presión de vacío | 0.94 a 2.432 mmHg |
| Tiempo total de proceso | **36 horas** (tiempo óptimo confirmado) |
| Formato de muestra | Cubos ~1 cm, ~50 g por frasco |
| Barquillo | Papel aluminio doble (evita escurrimiento del jugo) |

> **Nota técnica:** el equipo no siempre alcanza las especificaciones del manual. Registrar T y P reales en cada ciclo. Si la presión supera 3 mmHg o la temperatura del condensador supera -30°C, el proceso puede ser ineficiente.

### 4.3 Seguimiento gravimétrico (curva de humedad vs. tiempo)

**Método:** gravimétrico indirecto (García Martínez & Fernández Segovia, 2012)

**Procedimiento:**
1. Pesar cada frasco antes de iniciar el proceso (masa inicial)
2. Retirar un frasco a cada intervalo de tiempo, pesar (balanza analítica)
3. Registrar masa y calcular % pérdida BH

**Intervalos de extracción:**

| Frasco | Tiempo de extracción |
|---|---|
| Frasco 1 | 12 h |
| Frasco 2 | 24 h |
| Frasco 3 | 36 h ← **tiempo óptimo** |
| Frasco 4 | 48 h |
| Frasco 5 | 60 h |
| Frasco 6 | 72 h |
| Frasco 7 | 84 h |
| Frasco 8 | 96 h |

> **Recomendación pendiente (Exp3):** agregar mediciones adicionales en las primeras 6 horas para caracterizar mejor la curva inicial de sublimación.

**Fórmula:**
```
% Pérdida BH = (Masa inicial − Masa final) / Masa inicial × 100
```

---

## 5. Resultados experimentales (datos reales)

### Experimento 2 (20-24 mayo 2024 — Estancia Viamonte)

| Frasco | Tiempo (h) | % Pérdida BH |
|---|---|---|
| 1 | 6 | 37.27 |
| 2 | 18 | 86.39 |
| 3 | 30 | 91.94 |
| 4 | 42 | 92.27 |
| 5 | 54 | 92.38 |
| 6 | 66 | 92.71 |
| 7 | 78 | 92.73 |
| 8 | 90 | 92.66 |

### Experimento 3 (28 oct – 4 nov 2024 — Estancia Viamonte)

| Frasco | Tiempo (h) | Masa inicial (g) | Masa final (g) | % Pérdida BH |
|---|---|---|---|---|
| C0 | 0 | — | — | 0 |
| C1 | 12 | 50.27 | 16.07 | 68.03 |
| C2 | 24 | 50.60 | 5.78 | 88.59 |
| C3 | 36 | 50.15 | 2.77 | **94.48** |
| C4 | 48 | 50.22 | 2.77 | 94.48 |
| C5 | 60 | 51.19 | 3.14 | 93.86 |
| C6 | 72 | 49.51 | 2.93 | 94.07 |
| C7 | 84 | 53.34 | 3.19 | 94.02 |
| C8 | 96 | 48.96 | 2.78 | 94.32 |

**Condiciones Exp3:** T condensador -36 a -41°C · P 1.024 a 1.384 mmHg

> **Conclusión:** la curva se estabiliza a partir de las 36 horas. El tiempo óptimo de liofilización para ruibarbo en RIFICOR LT-8 es **36 horas**.

---

## 6. Criterio de fin de proceso

El proceso se considera completo cuando:
- La pérdida de peso se estabiliza (variación < 0.5% entre dos pesadas consecutivas)
- O se alcanzan las 36 horas de proceso

---

## 7. Envasado post-liofilización

1. Retirar el producto del frasco inmediatamente al finalizar el proceso
2. Pesar el producto final (balanza analítica)
3. Envasar al vacío:
   - Usar bolsas o rollos gofrados Turbosaver
   - Selladora al vacío
4. Etiquetar: fecha, experimento, condiciones, peso neto
5. Almacenar en lugar fresco, seco, sin luz directa

---

## 8. Pendientes para completar el protocolo

- [ ] Completar y documentar Exp4
- [ ] Agregar mediciones en primeras 6h (Exp5 o ajuste Exp4)
- [ ] Calibrar OHAUS AR2140 con mesa antivibratoria (pendiente de adquisición)
- [ ] Redactar SOP formal unificando Exp1–4
- [ ] Validar con al menos 2 réplicas del protocolo final

---

## 9. Archivos relacionados

| Archivo | Descripción |
|---|---|
| `E:/Investigacion 24 Javi/Liofilizado/Diseño experimental/Exp N2_...pptx` | Datos Exp2 |
| `E:/Investigacion 24 Javi/Liofilizado/Diseño experimental/Exp N3_...pptx` | Datos Exp3 |
| `E:/Investigacion 24 Javi/Liofilizado/Diseño experimental/Registro de resultados...xlsx` | Excel de datos completos |
| `E:/Investigacion 24 Javi/Liofilizado/Capacitación.../Guia de uso rapido v1.docx` | Guía operativa del equipo |
| `scripts/proyecto_liofilizados_data.ipynb` | Análisis de datos en Python |

---

## 10. Referencias

- García Martínez, E. & Fernández Segovia, I. (2012). *Determinación de la humedad de un alimento por el método de desecación en estufa.* Universitat Politècnica de València.
- RIFICOR LT-8 Manual de operación.

---

*Última actualización: marzo 2026*
