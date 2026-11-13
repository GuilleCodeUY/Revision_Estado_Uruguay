# Pedido de acceso a la información pública · 19 intendencias

El mismo texto sirve para las 19. Solo cambiá el nombre de la intendencia.

## Cómo presentarlo

1. Entrá con tu Usuario gub.uy a **solicitudes.gub.uy** (SAIP), igual que hiciste con el Parlamento, y buscá la intendencia en la lista de organismos.
2. Si la intendencia no aparece en el SAIP, buscá en su web la sección "Acceso a la información pública" o "Transparencia". Algunas tienen un formulario propio (Florida, por ejemplo, publica uno en PDF). Si no tienen, se presenta por nota en Mesa de Entrada o por el correo oficial que indiquen.
3. Guardá el número que te den y anotalo en `datos/intendencias_2022.json`, en `pedidos_acceso`. Completá `id`, `fecha_envio`, `vencimiento` (20 días hábiles) y cambiá `estado` a `esperando`. Después corré `python generar.py` y la tabla de la página se actualiza sola.

Estados posibles: `por_enviar`, `esperando`, `prorroga`, `respondido`, `incompleto` y `vencido`.

---

## Texto del pedido

**Asunto:** Solicitud de acceso a la información pública (Ley N.º 18.381) · gasto y control del gasto 2020-2025

Sr./Sra. Intendente/a de **[NOMBRE DE LA INTENDENCIA]**:

Al amparo de la Ley N.º 18.381 de Acceso a la Información Pública y su decreto reglamentario, solicito la siguiente información. Pido, en lo posible, que la entreguen en formato abierto y editable (planilla Excel, CSV u ODS). Si alguna parte contiene datos personales, pido que se entregue disociada o con el número de ficha o cargo en lugar del nombre, sin que eso impida entregar el resto.

1. **Rendiciones de Cuentas y Balances de Ejecución Presupuestal** de los ejercicios 2023, 2024 y 2025, con los dictámenes del Tribunal de Cuentas de la República correspondientes a cada uno y lo resuelto por la Junta Departamental.

2. **Gastos observados y reiterados.** Listado de los gastos observados por el Tribunal de Cuentas o por sus contadores delegados entre el 1/1/2020 y el 31/12/2025, con: fecha, número de resolución u oficio, objeto o concepto del gasto, proveedor o beneficiario, monto, norma invocada en la observación, y si el gasto fue reiterado por el ordenador (con número y fecha de la resolución de reiteración).

3. **Horas extras.** Monto total pagado por horas extras en cada año entre 2020 y 2025, y cantidad de funcionarios que las cobraron. Para 2025, la distribución por dirección o departamento y los 20 montos individuales anuales más altos, identificados por cargo o ficha.

4. **Cargos políticos y de particular confianza.** Cantidad de cargos al 31/12/2025, con denominación del cargo y remuneración nominal mensual de cada uno.

5. **Funcionarios.** Cantidad de funcionarios al 31/12/2025 por tipo de vínculo (presupuestados, contratados, zafrales, becarios, pasantes y otros), y cantidad de ingresos y egresos durante 2025.

6. **Compras sin licitación.** Contrataciones directas, incluidas las de excepción, realizadas entre 2023 y 2025 por montos superiores al límite de la compra directa común: proveedor, objeto, monto, causal invocada y fecha.

7. **Deuda.** Deuda al 31/12/2025 con proveedores, con bancos e instituciones financieras y por fideicomisos, discriminada por acreedor o instrumento, con plazo y tasa cuando corresponda.

8. **Junta Departamental.** Partidas, viáticos o asignaciones pagadas a ediles en 2025, por concepto, y su rendición de cuentas.

Si parte de la información ya está publicada, alcanza con indicar el enlace exacto donde se encuentra.

Quedo a la espera dentro del plazo legal de 20 días hábiles.

Nombre: **[TU NOMBRE]**
Documento: **[TU C.I.]**
Correo para notificaciones: **[TU CORREO]**
Fecha: **[FECHA]**
