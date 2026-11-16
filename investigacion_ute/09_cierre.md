# Cierre de UTE: lo que falta

Estado: verificado

Lo demás del caso ya está verificado y publicado (auditoría del 16/11/2026). Queda un solo dato.

## A. Pérdidas de energía de 2020

### Prompt para DeepSeek

UTE (Uruguay), Memoria anual 2020 (portal.ute.com.uy, sección memorias; probá https://portal.ute.com.uy/sites/default/files/memorias/Memoria%20anual%202020.pdf y, si no abre, buscá "Memoria anual 2020 UTE"). Copiá para el cierre de 2020:
- Pérdidas de Distribución y Comercial (técnicas más no técnicas), en % y en GWh si figura.
- Pérdidas totales de UTE (generación, trasmisión, distribución y comercial), en %.
- Si están separadas: pérdidas técnicas y no técnicas.

Cuidado: copiá la cifra del cierre del año (diciembre o "año móvil" a diciembre), no el pico mensual. El pico de julio de 2020 (18,5 %) ya lo tenemos y no sirve para este dato. Indicá textualmente cómo lo llama la memoria (por ejemplo "pérdidas globales", "año móvil") y copiá la frase donde aparece. Si la Memoria 2020 no trae el dato, buscalo en la Memoria 2021 como comparativo del año anterior.

Reglas: cada dato con fuente, URL exacta, número de página, fecha del documento y tipo (oficial / estimación de terceros / prensa). Abrí cada URL y cada PDF antes de citarlo y copiá la cifra tal como figura en la página, no de memoria. Si no lo encontrás, escribí NO ENCONTRADO; no inventes ni estimes. Si dos fuentes se contradicen, poné las dos. Sin opiniones. Tabla: dato | valor | año | fuente | URL | página | fecha | tipo.

### Respuesta de DeepSeek

Consultado: 16/11/2026

| dato | valor | año | fuente | URL | página | fecha | tipo |
|---|---|---|---|---|---|---|---|
| Pérdidas de Distribución y Comercial (técnicas + no técnicas), cierre diciembre 2020 | 18,3 % | 2020 | UTE, Memoria anual 2020 | https://portal.ute.com.uy/sites/default/files/memorias/Memoria%20anual%202020.pdf | 47 | 2021 | OFICIAL |
| Pérdidas totales de la Empresa (incluye generación y transmisión), cierre diciembre 2020 | 19,8 % | 2020 | UTE, Memoria anual 2020 | https://portal.ute.com.uy/sites/default/files/memorias/Memoria%20anual%202020.pdf | 47 | 2021 | OFICIAL |
| Pérdidas en zonas de vulnerabilidad socioeconómica | 6,1 % | 2020 | UTE, Memoria anual 2020 | https://portal.ute.com.uy/sites/default/files/memorias/Memoria%20anual%202020.pdf | 47 | 2021 | OFICIAL |
| Pérdidas de Distribución y Comercial, en GWh | 1.942 GWh | 2020 | UTE, Memoria anual 2020, balance energético | https://portal.ute.com.uy/sites/default/files/memorias/Memoria%20anual%202020.pdf | 24 | 2021 | OFICIAL |
| Pérdidas en transmisión, en GWh | 378 GWh | 2020 | UTE, Memoria anual 2020, balance energético | https://portal.ute.com.uy/sites/default/files/memorias/Memoria%20anual%202020.pdf | 24 | 2021 | OFICIAL |
| Pérdidas totales (distribución y comercial + transmisión), en GWh | 2.320 GWh (suma de 1.942 + 378) | 2020 | UTE, Memoria anual 2020, balance energético (cálculo) | https://portal.ute.com.uy/sites/default/files/memorias/Memoria%20anual%202020.pdf | 24 | 2021 | OFICIAL (cálculo) |
| Pérdidas técnicas y no técnicas separadas | NO ENCONTRADO | 2020 | — | — | — | — | — |

**Cita textual (p. 47):** «A nivel Empresa los valores porcentuales de pérdidas de energía, al mes de diciembre de 2020 fueron: - Distribución y Comercial 18,3% - Zonas de vulnerabilidad socioeconómica 6,1% - Total Empresa (incluye GEN y TRA) 19,8%». Es el cierre de diciembre, no el pico de julio (18,5%).

**Aclaración:** la Memoria 2020 no separa pérdidas técnicas y no técnicas; solo publica el total de Distribución y Comercial. Los GWh de 1.942 y 378 figuran en el balance energético de la p. 24; la suma de 2.320 es cálculo propio.

## NO ENCONTRADO

- Pérdidas técnicas y no técnicas separadas para 2020: la memoria no las desagrega.

## Verificación de Claude

Verificado: 16/11/2026. Estado: **confiable**.

- Abrí la Memoria anual 2020: la frase de la pág. 47 coincide (18,3 % Distribución y Comercial, 6,1 % zonas de vulnerabilidad, 19,8 % total empresa, a diciembre de 2020). Los 1.942 y 378 GWh de la pág. 24 también coinciden, y suman los 2.320 GWh del diagrama.
- **Publicado:** fila 2020 en la tabla de pérdidas de `ute.html` (18,3 % y 19,8 %). La nota ya no dice que falta 2020 y se sacó el pico de julio (18,5 %), que es otra medida y confundía.
- Técnicas y no técnicas por separado: la memoria no las abre. No hace falta para la página.
