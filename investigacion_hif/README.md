# Informe especial 5 · HIF Global y el precio de la energía — investigación

| Archivo | Quién | Estado |
|---|---|---|
| `01_deepseek.pdf` | DeepSeek | Recibido 18/11/2026 (14 págs., "HIF Global en Uruguay") |
| `../web/hif.html` | Claude | Versión verificada y corregida, publicada como Informe especial 5 |

## Verificación (18/11/2026)

### Cuentas rehechas: dan bien
- Volumen del módulo 1: 290 MW × 8.760 h × 95 % = 2.413,38 GWh.
- Costo implícito de UTE: 45 + 90 / 2,41338 = US$ 82,3 por MWh.
- Ingreso a US$ 45: US$ 108,6 M; a US$ 86: US$ 207,6 M; diferencia US$ 98,9 M por año.
- Tabla de sensibilidad completa (US$ 40 a 86, a 15 y 20 años).
- Solaria: 500 MW × 8.760 h × 90 % = 3.942 GWh.

### Verificado contra la fuente
- Precios US$ 40 (HIF), US$ 45 con peaje (borrador), US$ 53 sin peaje (2024), US$ 86 (Google y Solaria): El Observador 14/11/2026 y la nota de Solaria.
- Pérdida de US$ 90 M por año y mínima de US$ 1.300 M, US$ 450 M antes de la decisión, más de US$ 600 M de partidas, decisión hasta fines de 2028, operación a fines de 2031, red en 2033, otros proyectos no antes de 2032: El Observador 14/11/2026.
- Inversión 5.385 = 2.881 + 1.277 + 1.226, 4 módulos de 280 MW, solar 1.162 MWp y eólico 1.137 MW, 1.400 y 300 empleos, exportaciones 253 y 1.012, beneficios fiscales pedidos, cánones por disponibilidad: memorando ROU-HIF.
- Ramón Méndez, cerca de US$ 1.000 M en unos 20 años: ICI Forestal 17/09/2026.

### Corregido
| Punto | Qué decía | Qué quedó |
|---|---|---|
| Transferencias | La pérdida equivale a "3,7 años de transferencias" | Cuenta invertida. US$ 90 M ≈ 51 % del giro a Rentas Generales de 2025 ($ 7.208 M ≈ US$ 175 M, EEFF) |
| Grandes consumidores | "Entre US$ 60 y 90" y, en otra tabla, US$ 135,5 | Rango sin fuente quitado; tarifa industrial US$ 148 (Prensa Latina, abril 2026) |
| Costo US$ 82,3 | Presentado como dato | Marcado como estimación deducida |
| Centros de datos | Mismo costo que HIF | Aclaración: probablemente menor para un centro de datos |
| AUTE US$ 80 | Sin fuente abierta | Reemplazado por eólica privada US$ 80 (set. 2025) y 82 (ene. 2026), monitor UCU |
| Demanda 2025 | 12.467 GWh | 12.533 GWh (UTE en cifras 2025) |
| Ventas de UTE | 10.429 GWh | 10.527 GWh (EEFF 2025, ya usado en `datos/ute.json`) |
| Producción | 876.000 t de e-metanol | 880.000 t de e-combustibles (memorando) |
| Planilla | `Modelo-HIF-UTE-2026-11.xlsx` | No existía; la tabla se publica como `hif_sensibilidad.csv` |
| Tabla "UTE en 2025" | Ingresos 1.926,3, costos 1.482,7, transferencias 355,4 | No se usó: solo la ganancia (US$ 341 M) y el giro, que coinciden con los EEFF |

### Pendiente
- El Estudio de Impacto Ambiental no se pudo abrir (el sitio bloquea la descarga automática). El volumen de 2.413 GWh se toma de su tabla 5-57 según el informe original. Con 280 MW al 90 % da 2.200 GWh y unos US$ 82 M por año: el orden no cambia.
- El borrador del memorando, el plazo del contrato y el costo auditado de UTE no son públicos.
