# La verdad de la milanesa · verdadmilanesa.uy

Análisis independiente del gasto del Estado uruguayo con información pública. Los números no tienen partido. Ejercicio 2025, con dotación al 31 de diciembre de 2025 y fuentes consultadas al 12 de noviembre de 2026.

## Abrir el proyecto

Abrí `publico/index.html` en el navegador. Las páginas y sus filtros funcionan localmente. `Analisis_2025.md` reúne los hallazgos, escenarios y propuestas.

- `publico/index.html` es la portada: el costo del Palacio Legislativo, tres datos de impacto con su fuente y un botón para objetarlos, los casos y la fe de erratas pública.
- `publico/intendencias.html` es el caso de las 19 intendencias: gasto 2022 de OPP, ranking por habitante, fichas por departamento con lo observado por el Tribunal de Cuentas y las promesas, y el seguimiento de los pedidos de acceso. Se genera desde `datos/intendencias_2022.json`. El texto del pedido está en `pedidos/pedido_ley_18381_intendencias.md`.
- `publico/puerto.html` es el caso del puerto de Montevideo: serie de la ANP 2015-2025, concesiones, paros, comparación con seis puertos de la región y obras. Se genera desde `datos/puerto.json`. La investigación y su verificación están en `investigacion_puerto/`.
- `publico/ute.html` es el caso de UTE: serie 2015-2025 de resultados, inversiones y pagos a Rentas Generales, el fondo de estabilización, la tarifa 2026 con facturas tipo, costos, pérdidas de energía, escenarios de cuánto podría costar y lo cuestionado (Gas Sayago, energía no usada). Se genera desde `datos/ute.json`. La investigación y su verificación están en `investigacion_ute/`.
- `publico/ancap.html` es el caso de ANCAP: qué pagás en un litro de nafta y de gasoil (desglose de URSEA), cuánto saldría sin impuestos, la comparación con la región, el resultado de ANCAP 2012-2025, los impuestos que paga contra las ganancias que gira, el precio contra la paridad de importación y lo que pierde (pórtland, ALUR, parada de la refinería, desulfurizadora, Gas Sayago). Se genera desde `datos/ancap.json`. La investigación y su verificación están en `investigacion_ancap/`.
- `publico/movilidad.html` es el Informe especial 1, movilidad eléctrica: qué subsidia el Estado al auto eléctrico, qué le cobra al de nafta, cuánto recauda y deja de cobrar, el costo de uso, los gastos fijos y las emisiones. Se genera desde `datos/movilidad.json`.
- `publico/transporte.html` es el Informe especial 2, la reforma del transporte metropolitano: qué se va a hacer (BRT eléctrico en 8 de Octubre y Av. Italia), cuánto cuesta frente a tranvía y metro, cuánta capacidad y energía requiere, el sistema actual, las otras propuestas y lo que se discute. Se genera desde `datos/transporte.json`. La investigación y su verificación están en `investigacion_transporte/`.
- `publico/justicia.html` es el Informe especial 3, justicia penal y seguridad: delitos 2025-2026 (AECA), tiempos de Fiscalía, cárceles y censo penitenciario, reincidencia, drogas y calle, comparación internacional y lo que dice la ley. Se genera desde `datos/justicia.json`. El borrador original (ChatGPT) y su verificación están en `investigacion_justicia/`.
- `publico/estado.html` es el Informe especial 4, "Un Estado que rinde": empleo público, gasto, salida natural de funcionarios, escenarios a 2035 sin despidos, tecnología, fondo de inversión e impuestos. Se genera desde `datos/estado.json` y `web/estado.template.html`. Se hizo cruzando los trabajos de Claude, ChatGPT y DeepSeek; los tres y la comparación están en `investigacion_estado/`.
- `publico/hif.html` es el Informe especial 5, HIF Global y el precio de la energía: el borrador a US$ 45 el MWh frente a los US$ 86 de Google y Solaria, la pérdida que calculan UTE y el MIEM, la tabla por precio, lo que recibe y paga el país, el veredicto y diez condiciones para el contrato. Es una página estática (`web/hif.html`); sus CSV salen de `datos/hif.json`. El informe original (DeepSeek) y su verificación están en `investigacion_hif/`.
- `publico/patente.html` es el Informe especial 6, la patente de rodados y el SUCIVE: qué es, cuánto se recauda, en qué se usa, cómo se calcula (aforo, dólar de referencia, 4,5 %, descuentos y multas), por qué no baja con el auto, la comparación con São Paulo, Chile y Buenos Aires y el debate de la patente 2027. Se genera desde `web/patente.template.html` y `datos/patente.json`. El borrador original (DeepSeek) y su verificación están en `investigacion_patente/`.
- `publico/basura.html` es el Informe especial 7, la basura en Montevideo: contenedores sin vaciar, quién dice qué (IM, Adeom, oposición), seis causas de fondo, la serie de multas 2016-2026, por qué empeora, responsables por acción y omisión, Canelones, Maldonado, Rocha, Buenos Aires y Liubliana, y soluciones. Es una página estática (`web/basura.html`). Se hizo cruzando los trabajos de Claude, DeepSeek y ChatGPT; los borradores están en `investigacion_basura/`.
- `publico/informe.html` es el informe completo: Presupuesto Nacional, ingresos, empleo, Parlamento, Montevideo, Tribunal de Cuentas, escenarios de ahorro y aportes. Los importes de portada están redondeados a millones de pesos y los enlaces llevan a las cifras exactas.
- `datos/correcciones.json` es el registro de objeciones que se muestra en la fe de erratas. Cada entrada lleva `fecha`, `dato`, `estado` (`recibida`, `en_revision`, `aceptada` o `rechazada`) y `resultado`.
- `og.png` es la imagen que aparece al compartir el enlace; `og-solaria.png`, `og-hif.png` y `og-patente.png` son las de esos casos (las de HIF y la patente se generan desde `bocetos/og_hif.html` y `bocetos/og_patente.html` con una captura de 1200×630). `robots.txt` y `sitemap.xml` sirven para que Google indexe el sitio. `generar.py` pone en cada caso e informe los datos estructurados de schema.org (Article) y en el sitemap la fecha real de cada página, tomadas del historial de git (`PAGINAS_SEO`). Al sumar una página nueva, agregala a `PAGINAS_SEO`.

| Archivo en `publico/` | Contenido |
|---|---|
| `ejecucion_2025.csv` | 33 filas presupuestales de gasto, crédito y remuneraciones. |
| `ingresos_presupuestales_2025.csv` | Recursos, impuestos, tasas y otros ingresos, con su cuadro de origen y peso en los recursos totales. |
| `gasto_parlamento_2025.csv` | Remuneraciones, funcionamiento e inversiones de los ocho programas del Poder Legislativo. |
| `pedidos_acceso_parlamento.csv` | Seguimiento de los pedidos de acceso a la información (Ley 18.381) al Senado, Diputados y la Comisión Administrativa: número, fechas y estado. |
| `actividad_diputados_2025.csv` | Conteo mensual por tipo de registro en el balance legislativo de la 50.ª Legislatura. |
| `dotacion_por_organismo_2025.csv` | 84 organismos y dependencias, personas, vínculos, escalafones y gasto donde corresponde. |
| `empleo_y_poblacion_departamental_2025.csv` | Población, superficie terrestre, densidad y vínculos laborales por departamento de trabajo. |
| `empleo_unidades_2025.csv` | 270 unidades ejecutoras incluidas en el cuadro de ONSC. |
| `empleo_territorios_2025.csv` | Lugar de trabajo de los vínculos, con los 19 departamentos, exterior, itinerantes y sin clasificar. |
| `empleo_municipios_2025.csv` | 19 oficinas centrales de intendencias y 136 dependencias locales según el cuadro de ONSC. |
| `empleo_entidades_relacionadas_2025.csv` | 70 personas públicas no estatales y entidades de participación estatal mayoritaria. |
| `balances_institucionales_2025.csv` | Cifras de personal y egresos de BPS, UTE, URSEA y URSEC con su criterio contable. |
| `costos_de_conduccion_identificados_2025.csv` | Diez registros de JUTEP, UTE, BPS, ANCAP, URSEA y ACCESA, con su base y su fuente. |
| `intendencias_2022.csv` | Gasto, sueldos, inversiones, ingresos propios y nacionales de las 19 intendencias en 2022 (OPP). |
| `intendencias_hallazgos.csv` | Hallazgos por departamento con tipo, fuente y solidez. |
| `intendencias_transparencia_intai.csv` | Índice de transparencia de la UAIP (INTAI) 2024, 2023 y 2022 de las 19 intendencias. Un 0 es que no respondió. |
| `intendencias_denuncias_uaip.csv` | Resoluciones de la UAIP desde 2025 en que le dio la razón a un denunciante contra una intendencia, con enlace. |
| `puerto_anp_2015_2025.csv` | Ingresos, resultado, inversiones, transferencias a Rentas Generales y funcionarios de la ANP, 2015-2025 (estados financieros). |
| `puerto_comparacion.csv` | Contenedores 2024 (CEPAL) y puesto de eficiencia 2024 y 2025 (Banco Mundial) de siete puertos. |
| `puerto_fuentes.csv` | Fuentes del caso del puerto, con tipo (oficial, prensa, gremial, partido). |
| `ute_2015_2025.csv` | Ingresos, resultado, inversiones, pagos a Rentas Generales y funcionarios de UTE, 2015-2025 (estados financieros). |
| `ute_fuentes.csv` | Fuentes del caso UTE, con tipo (oficial, prensa). |
| `ancap_resultados_2012_2025.csv` | Resultado neto de ANCAP por año, en millones de dólares, con la fuente de cada año. |
| `ancap_estado_2021_2025.csv` | Ingresos, impuestos pagados, ganancias giradas y contribución fiscal de ANCAP 2021-2025 (UCU). |
| `ancap_litro_2026.csv` | Desglose del precio del litro de nafta Súper y gasoil 50S, febrero 2026 (URSEA y cálculo propio). |
| `ancap_fuentes.csv` | Fuentes del caso ANCAP, con tipo (oficial, prensa, terceros, parte). |
| `transporte_comparacion.csv` | CAPEX por km, capacidad, inversión, operación, costo a 30 años, energía y emisiones de BRT, tranvía y metro. |
| `transporte_fuentes.csv` | Fuentes del caso transporte, con tipo (oficial, prensa, parte, cálculo propio). |
| `movilidad_costos.csv` | Costo de energía, patente, seguro y CO2 por año, nafta contra eléctrico (fuente y cálculo propio). |
| `movilidad_estado.csv` | Lo que el Estado recauda por combustibles y autos, lo que deja de cobrar por los eléctricos y lo que recupera desde 2027. |
| `movilidad_fuentes.csv` | Fuentes del informe de movilidad eléctrica, con tipo (oficial, prensa, gremial, terceros, cálculo propio). |
| `justicia_indicadores.csv` | Delitos de enero a setiembre 2025 y 2026 (AECA). |
| `justicia_carceles.csv` | Datos de justicia, cárceles y reincidencia con su fuente. |
| `justicia_fuentes.csv` | Las 68 fuentes del informe de justicia, con tipo (oficial, prensa, internacional). |
| `estado_escenarios.csv` | Escenarios moderado, central y fuerte a 2030 y 2035: reglas de reposición, vínculos, ahorro bruto y neto. |
| `estado_fuentes.csv` | Las fuentes del informe de Estado optimizado, con tipo. |
| `hif_sensibilidad.csv` | Ingreso y resultado de UTE por año y a 15 y 20 años según el precio del MWh, sobre el volumen del módulo 1 de HIF (cálculo propio). |
| `hif_fuentes.csv` | Fuentes del informe de HIF, con tipo (oficial, prensa, parte, terceros). |
| `patente_parametros.csv` | Dólar de referencia, cambio de la tabla de valores, cambio de la patente de un mismo auto e inflación, patente 2023 a 2027 (Congreso de Intendentes; el cambio de la patente es cálculo propio). |
| `patente_calculos.csv` | Ejemplo de la patente 2026 de un auto usado de US$ 12.800, con descuentos (cálculo propio). |
| `patente_comparacion.csv` | Lo que pagaría el mismo auto en Uruguay, São Paulo, Chile y la provincia de Buenos Aires (cálculo propio con las reglas oficiales de cada lugar). |
| `patente_fuentes.csv` | Fuentes del informe de la patente, con tipo (oficial, prensa, terceros, internacional). |
| `pedidos_acceso_intendencias.csv` | Seguimiento de los 19 pedidos de acceso (Ley 18.381). |
| `tribunal_muestra_2025.csv` | Cuatro expedientes con motivo, importe y estado documentado. |

Los CSV usan punto y coma y codificación UTF-8 con BOM. Los montos con sufijo `_miles_uyu` se expresan en miles de pesos uruguayos. Los que llevan `_uyu` están en pesos. Un campo vacío indica que el dato queda fuera de la cobertura de la fuente o está pendiente de validar.

## Reproducir los datos

1. Ejecutá `python generar.py` para reconstruir la página y los CSV desde los JSON. La generación usa solo la biblioteca estándar de Python.
2. Para rehacer la importación de ONSC, descargá el PDF oficial, instalá PyMuPDF en tu entorno de Python y ejecutá `python importar_onsc.py Informe_Vinculos_2025.pdf`. Luego ejecutá de nuevo `python generar.py`.
3. El archivo `datos/empleo_2025.json` registra la huella SHA-256 del PDF. Los totales nacionales por tipo de vínculo, escalafón y lugar de trabajo se reconcilian con los publicados. Las unidades listadas concilian con los incisos a los que pertenecen.

## Cómo leer las cifras

- **Personas y vínculos.** ONSC contabiliza 275.898 personas con 318.269 vínculos en el universo principal. Los 305.097 vínculos con calidad de funcionario y los 13.172 restantes forman ese total. El conteo de personas por organismo puede incluir a la misma persona en más de una institución.
- **Población y territorio.** El cruce usa población residente proyectada al 30 de junio y vínculos por lugar de trabajo al cierre de 2025. El indicador por mil habitantes sirve para seleccionar servicios a revisar. La dotación necesaria se calcula con demanda, turnos, horas productivas y cobertura.
- **Organismos y dependencias.** Las filas de intendencias y juntas se desagregan. Las unidades, lugares de trabajo y municipios son aperturas del mismo universo y no se agregan a la dotación nacional. Los vínculos de las entidades relacionadas se publican por separado.
- **Remuneraciones.** El cruce de dotación y costo cubre 29 organismos con correspondencia directa entre CGN y ONSC. El cuadro 28 de la CGN redistribuye $ 182.156.000 del inciso 24 a Udelar. El cuadro 4 muestra ese importe antes de reasignarlo, por eso los dos campos pueden diferir. El total general de remuneraciones sigue siendo $ 288.451.278.000.
- **Alcance fiscal.** Los $ 997.951.745.000 corresponden a la ejecución del Presupuesto Nacional. El perímetro fiscal Gobierno Central-BPS, las cuentas departamentales y las empresas públicas siguen metodologías diferentes. Los balances institucionales están en un CSV propio. Para un total de gasto de todo el Estado hace falta conciliar y depurar las transferencias entre ellos.
- **Impuestos.** El cuadro 25 de CGN distingue impuestos de tasas. Los impuestos suman el 85,31 % de los recursos presupuestales. El CSV identifica los subtotales y sus desgloses.
- **Cargos políticos.** P y Q se toman de los escalafones oficiales, incluidas equivalencias de organismos. Sueldos, aportes, adscriptos, asesorías, subsidios y costos de apoyo necesitan conciliarse con las liquidaciones y los conceptos del gasto. Los recuentos de plazas por norma y de vínculos P/Q pueden superponerse.
- **Productividad.** El caso BPS usa tiempos de atención informados y trámites registrados hasta febrero de 2026. La diferencia calculada sirve para simular la carga de esa etapa. El costo de nómina y la dotación efectiva se verifican con datos de cada servicio.
- **Incidencias de la fuente.** El cuadro de unidades deja en blanco subtotales del Hospital del Cerro. Se recuperaron 437 vínculos con calidad de funcionario y cero de las demás modalidades desde el formulario de ASSE, pág. 286 del PDF. Para Mariscala se reconstruyó un subtotal de 13 con las dos columnas de la fila, 8 y 5, aunque el total impreso es cero. El CSV municipal deja constancia del ajuste.
- **Participación.** El piloto descarga el aporte y el adjunto a un archivo local. La recepción compartida, la revisión y el historial público requieren la versión conectada.

## Fuentes principales

- [Servicio Civil · Informe de vínculos 2025](https://www.gub.uy/oficina-nacional-servicio-civil/comunicacion/publicaciones/vinculos-laborales-estado-altas-bajas-2025) y [planillas del MEF](https://www.gub.uy/ministerio-economia-finanzas/comunicacion/publicaciones/rendicion-cuentas-balance-ejecucion-presupuestal-ejercicio-2025-datos).
- [CGN · Rendición de Cuentas 2025, tomos I, II y III y Exposición de Motivos](https://presupuestonacional.gub.uy/rendicion_2025) y [Ley 20.531 de aprobación](https://www.impo.com.uy/bases/leyes/20531-2026/1).
- [Tribunal de Cuentas](https://www.tcr.gub.uy/resoluciones.php), [compras estatales de ARCE](https://www.gub.uy/agencia-reguladora-compras-estatales/datos-y-estadisticas/datos-abiertos) y [Ley 18.381 de acceso a la información pública](https://www.impo.com.uy/bases/leyes/18381-2008).
- [OPP · Finanzas departamentales y municipales](https://catalogodatos.gub.uy/dataset/opp-ingresos-y-egresos-de-los-gobiernos-departamentales-y-egresos-de-los-gobiernos-municipales) y [empresas públicas](https://opp.gub.uy/es/empresas-publicas).

[Constitución Abierta UY](https://constitucion-abierta.pages.dev/#como) queda como referencia de publicación por sus fichas, fuentes y estado visible de revisión.
