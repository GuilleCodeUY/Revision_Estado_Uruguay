# El sistema de hoy: pasajeros, subsidios y boleto

Estado: verificado parcialmente

## Prompt para DeepSeek

Transporte público de Montevideo y el área metropolitana (Uruguay), situación actual. Fuentes: Intendencia de Montevideo (datos abiertos, STM), MTOP (Dirección Nacional de Transporte), MEF (Rendición de Cuentas), fideicomiso del boleto / fideicomiso del gasoil, Tribunal de Cuentas, INE.

1. Pasajeros transportados por año, 2015 a 2025 (urbano de Montevideo y suburbano metropolitano por separado).
2. Precio del boleto común, 2015 a 2026, y cuánto costaría sin subsidio.
3. Subsidios al transporte por año, 2015 a 2025: subsidio al gasoil (fideicomiso del boleto, que se cobra en cada litro de gasoil), aportes de la IM, aportes del gobierno nacional, boletos gratis o rebajados (estudiantes, jubilados). Total en pesos y dólares.
4. Empresas operadoras (CUTCSA, COETC, COME, UCOT, COPSA y otras): flota, participación en pasajeros, cuánto subsidio recibe cada una si se publica.
5. Tiempos de viaje promedio en los corredores de 8 de Octubre y Av. Italia en hora pico.
6. Encuestas de movilidad (por ejemplo la Encuesta de Movilidad del Área Metropolitana): reparto entre ómnibus, auto, moto, bici y a pie.

REGLAS
- Cada dato con: valor, unidad, año, fuente, URL exacta, número de página, fecha del documento y tipo de fuente (OFICIAL / ESTIMACIÓN DE TERCEROS / PRENSA / FUENTE DE PARTE si la publica quien promueve o se opone a un proyecto).
- Abrí cada URL y cada PDF antes de citarlo y copiá la cifra tal como figura en el documento, no de memoria.
- Montos en dólares, indicando el año de la cifra (un costo de 2019 no es igual a uno de 2026). Si la fuente da pesos o euros, poné la moneda original y aclaralo.
- Distinguí siempre: costo de obra (CAPEX), costo de vehículos, costo de operación y mantenimiento por año (OPEX). No los sumes si la fuente no lo hace.
- Si un dato no aparece, escribí NO ENCONTRADO. No estimes ni completes vos.
- Si dos fuentes se contradicen, poné las dos.
- Sin opiniones ni adjetivos. Si una fuente opina, citala como opinión y aclarando quién es.
- Tabla de salida: dato | valor | año | fuente | URL | página | fecha | tipo.

## Respuesta de DeepSeek

Consultado: 16/11/2026

| dato | valor | año | fuente | URL | página | fecha | tipo |
|---|---|---|---|---|---|---|---|
| Boletos vendidos en Montevideo | 208.022.863 | 2022 | INE, Anuario Estadístico 2025, 4.7.7 | https://www.gub.uy/instituto-nacional-estadistica/comunicacion/publicaciones/anuario-estadistico-nacional-2025-vol-102/47-transporte-comunicaciones-5 | s/p | 2025 | OFICIAL |
| Boletos vendidos en Montevideo | 214.860.415 | 2023 | INE, Anuario Estadístico 2025, 4.7.7 | https://www.gub.uy/instituto-nacional-estadistica/comunicacion/publicaciones/anuario-estadistico-nacional-2025-vol-102/47-transporte-comunicaciones-5 | s/p | 2025 | OFICIAL |
| Boletos vendidos en Montevideo | 218.158.425 | 2024 | INE, Anuario Estadístico 2025, 4.7.7 | https://www.gub.uy/instituto-nacional-estadistica/comunicacion/publicaciones/anuario-estadistico-nacional-2025-vol-102/47-transporte-comunicaciones-5 | s/p | 2025 | OFICIAL |
| Viajes vendidos en el STM urbano | 211 millones | 2025 | Intendencia de Montevideo | https://www.montevideo.gub.uy/venta-de-viajes-en-el-sistema-de-transporte-colectivo-urbano | s/p | 2026 | OFICIAL |
| Variación 2025 vs 2024 | -3,2 % | 2025 | Intendencia de Montevideo | https://www.montevideo.gub.uy/venta-de-viajes-en-el-sistema-de-transporte-colectivo-urbano | s/p | 2026 | OFICIAL |
| Variación 2019-2025 | -17,2 % | 2019-2025 | Intendencia de Montevideo | https://www.montevideo.gub.uy/venta-de-viajes-en-el-sistema-de-transporte-colectivo-urbano | s/p | 2026 | OFICIAL |
| Precio del boleto común con tarjeta STM | $ 49 (1 hora) | 2025 | Intendencia de Montevideo / prensa | https://www.subrayado.com.uy/aumenta-el-precio-del-boleto-tarjeta-stm-pasa-49-el-una-hora-y-en-efectivo-60-el-comun-n966595 | s/p | 09/01/2025 | PRENSA |
| Precio del boleto común en efectivo | $ 60 | 2025 | Intendencia de Montevideo / prensa | https://www.subrayado.com.uy/aumenta-el-precio-del-boleto-tarjeta-stm-pasa-49-el-una-hora-y-en-efectivo-60-el-comun-n966595 | s/p | 09/01/2025 | PRENSA |
| Composición de ingresos de las empresas (2024) | 62 % recaudación; 14 % subsidios IM; 13 % Fideicomiso del Boleto; 11 % subsidios del Gobierno Nacional | 2024 | BCU, prospecto informativo | https://www.bcu.gub.uy/_layouts/15/BCU.Registros/handler/FilesHandler.ashx?op=GetDocumentFile&NombreArchivo=RFBfMzk3MDdfMA== | s/p | 2024 | OFICIAL |
| Fideicomiso del boleto: aporte por litro de gasoil | $ 4,984 por litro | 2024 | Decreto MTOP, art. 12 | https://medios.presidencia.gub.uy/legal/2024/decretos/05/mtop_541.pdf | 1 | 15/05/2024 | OFICIAL |

**Aclaración:** los boletos de INE son ventas del transporte colectivo de Montevideo; los 211 millones de 2025 son viajes del STM urbano. No son exactamente la misma unidad, por eso se presentan por separado.

## NO ENCONTRADO

- Pasajeros 2015-2021: no se pudo leer la serie completa del XLS del INE; solo se copiaron 2022-2024.
- Pasajeros del suburbano metropolitano por separado: no encontrado.
- Precio del boleto 2015-2024 y costo sin subsidio: no encontrado.
- Subsidios anuales 2015-2025 en pesos y dólares, desagregados: no encontrado.
- Flota y participación por operador (CUTCSA, COETC, COME, UCOT, COPSA): no encontrado.
- Tiempos de viaje en 8 de Octubre y Av. Italia en hora pico: no encontrado.
- Reparto modal de la Encuesta de Movilidad: no encontrado.

## Verificación de Claude

Verificado: 16/11/2026.

**Confirmado**
- 211 millones de viajes vendidos en 2025, -3,2 % frente a 2024 y -17,2 % frente a 2019 (Intendencia de Montevideo).
- Informe Técnico N.º 1 de la ASTM: los pasajeros cayeron de unos 400 millones por año en los años 90 a unos 200 millones en 2025 (págs. 4 y 10).
- INE 2022-2024 y la composición de ingresos 2024 (BCU) quedan como los trajo; los reviso cuando arme la página.

**Falta**: la serie 2015-2021, los subsidios por año en pesos y dólares, el precio del boleto año por año y la encuesta de movilidad.
