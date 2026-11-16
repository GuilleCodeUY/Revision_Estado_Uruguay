# Energía: cuánto consume cada sistema

Estado: verificado; completado por Claude

## Prompt para DeepSeek

Consumo de energía y emisiones de sistemas de transporte público, aplicado a Uruguay.

1. Consumo por km recorrido y por pasajero-km de: ómnibus diésel, ómnibus eléctrico a batería, BRT eléctrico biarticulado, trolebús, tranvía (LRT) y metro ligero. En kWh (o litros de gasoil). Fuentes: UITP, IEA, ICCT, BID, fabricantes (BYD, Yutong, Stadler, Alstom, CAF) con aclaración de que es dato del fabricante.
2. Costo de la energía por km en Uruguay: tarifa de UTE para transporte o grandes consumidores, precio del gasoil (con y sin el fideicomiso del boleto) a noviembre de 2026.
3. Matriz eléctrica de Uruguay: porcentaje renovable de la generación de los últimos cinco años (MIEM, Balance Energético Nacional; ADME). Qué pasa en los años secos.
4. Flota eléctrica actual de Montevideo y el área metropolitana: cuántos ómnibus eléctricos hay, de qué empresa, subsidios o beneficios fiscales que recibieron (MIEM, IM, MTOP).
5. Infraestructura que necesita cada sistema: cargadores para buses a batería, catenaria para trolebús y tranvía; costo por km si figura.
6. Emisiones evitadas: toneladas de CO2 por año que declara cada proyecto (oficial, Tren Tram, BRT eléctrico).

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
| Matriz eléctrica 2024: participación de combustibles fósiles | 1 % | 2024 | MIEM, Balance Energético Preliminar 2024 | https://www.gub.uy/ministerio-industria-energia-mineria/comunicacion/noticias/uruguay-vuelve-registrar-niveles-record-fuentes-renovables-matriz-generacion | s/p | 25/04/2025 | OFICIAL |
| Matriz eléctrica 2024: hidroelectricidad | 42 % | 2024 | MIEM, Balance Energético Preliminar 2024 | https://www.gub.uy/ministerio-industria-energia-mineria/comunicacion/noticias/uruguay-vuelve-registrar-niveles-record-fuentes-renovables-matriz-generacion | s/p | 25/04/2025 | OFICIAL |
| Matriz eléctrica 2024: eólica | 28 % | 2024 | MIEM, Balance Energético Preliminar 2024 | https://www.gub.uy/ministerio-industria-energia-mineria/comunicacion/noticias/uruguay-vuelve-registrar-niveles-record-fuentes-renovables-matriz-generacion | s/p | 25/04/2025 | OFICIAL |
| Matriz eléctrica 2024: biomasa | 26 % | 2024 | MIEM, Balance Energético Preliminar 2024 | https://www.gub.uy/ministerio-industria-energia-mineria/comunicacion/noticias/uruguay-vuelve-registrar-niveles-record-fuentes-renovables-matriz-generacion | s/p | 25/04/2025 | OFICIAL |
| Flota eléctrica de Montevideo | 177 ómnibus eléctricos sobre 1.547 (≈10 %) | 2025 | Prensa (presentación IMM/CUTCSA) | https://mediospublicos.uy/se-presentaron-nuevos-omnibus-electricos-100-accesibles-y-con-una-autonomia-de-300km/ | s/p | 21/10/2025 | PRENSA |
| Nuevas unidades incorporadas | 50 ómnibus BYD, batería de 385 kWh, autonomía ≈300 km | 2025 | Prensa (presentación IMM/CUTCSA) | https://mediospublicos.uy/se-presentaron-nuevos-omnibus-electricos-100-accesibles-y-con-una-autonomia-de-300km/ | s/p | 21/10/2025 | PRENSA |
| Financiamiento CAF para electrificación de CUTCSA | US$ 20 millones para 60 ómnibus eléctricos e infraestructura de carga | 2025 | CAF | https://www.caf.com/es/actualidad/noticias/caf-financiara-la-incorporacion-de-60-omnibuses-electricos-en-montevideo-en-el-marco-del-programa-e-motion/ | s/p | 28/08/2025 | OFICIAL |

**Aclaración:** la matriz de 2024 es preliminar y mide generación eléctrica, no energía primaria. La flota de 177 unidades es de octubre de 2025 y no distingue por empresa.

## NO ENCONTRADO

- Consumo por km y por pasajero-km de ómnibus diésel, eléctrico, BRT biarticulado, trolebús, tranvía y metro ligero: no encontrado en una fuente abierta comparable.
- Costo de la energía por km en Uruguay (tarifa UTE para transporte y precio del gasoil): no encontrado.
- Qué pasa en años secos con la matriz: no cuantificado.
- Costo de cargadores por km y de catenaria: no encontrado.
- Emisiones evitadas de CO2 por año declaradas por cada proyecto: no encontrado.
- Subsidios o beneficios fiscales recibidos por la flota eléctrica: no encontrado.

## Verificación de Claude

Verificado: 16/11/2026.

**Confirmado**: flota eléctrica (177 de 1.547) y los 50 BYD, CAF US$ 20 M. La matriz 2024 la tomo del MIEM tal como la trajo; revisar en la segunda vuelta con el Balance Energético definitivo.

**Agregado por Claude (Informe Técnico N.º 1 de la ASTM, https://www.gub.uy/ministerio-transporte-obras-publicas/book/6724/download)**
- Energía por año: BRT unos 12 GWh, tranvía unos 25 GWh (pág. 26).
- Gasto en energía por año: BRT menos de US$ 1 M, tranvía US$ 3,3 M (pág. 27).
- Emisiones por año: BRT unas 132 toneladas de CO2, tranvía unas 283 (pág. 27). Son tan bajas porque la red eléctrica uruguaya es casi toda renovable.
- Baterías del BRT: vida de unos 7,5 años (pág. 32).

**Falta**: consumo por km de cada modo con fuente internacional, costo por km del gasoil frente a la electricidad, y cuánto sube el costo en un año seco.
