# Revisión del Estado y Gasto Público · Uruguay

Auditoría ciudadana de la estructura, el gasto y los servicios del Estado uruguayo. Ejercicio 2025, con dotación al 31 de diciembre de 2025 y fuentes consultadas al 12 de noviembre de 2026.

## Abrir el proyecto

Descomprimí el archivo y abrí `publico/index.html` en el navegador. La página y sus filtros funcionan localmente. `Analisis_2025.md` reúne los hallazgos, escenarios y propuestas.

La portada muestra primero el gasto ejecutado del Presupuesto Nacional y el rango de ahorro bruto anual estimado en cuatro rubros. Los importes de portada están redondeados a millones de pesos. Los enlaces llevan a las cifras exactas, los supuestos y las fuentes.

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
