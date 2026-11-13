import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SITE = "https://verdadmilanesa.uy"
STATIC_PAGES = ("solaria.html",)
CORRECTION_STATES = {"recibida", "en_revision", "aceptada", "rechazada"}
FIELDS = (
    "id",
    "name",
    "grupo",
    "credito_miles_uyu",
    "ejecutado_miles_uyu",
    "remuneraciones_miles_uyu",
)
TOTALS = {
    "credito_miles_uyu": 1_028_742_295,
    "ejecutado_miles_uyu": 997_951_745,
    "remuneraciones_miles_uyu": 288_451_278,
}


def load_data(name):
    return json.loads((ROOT / "datos" / name).read_text(encoding="utf-8"))


def write_csv(public, name, rows):
    with (public / name).open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=tuple(rows[0]), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def build_employment(data, spending):
    employment = load_data("empleo_2025.json")
    figures_by_id = {row["id"]: row for row in data["incisos"]}
    payroll = spending["desglose_remuneraciones_por_inciso"]
    if len(employment["organismos"]) != 84 or len(employment["unidades"]) != 270:
        raise ValueError("La cobertura por organismo o unidad no coincide con los cuadros oficiales.")
    for field, total in {"fp": 305097, "nfp": 13172, "vinculos": 318269,
                         "politico_p": 1174, "confianza_q": 893, "administrativo_c": 33063}.items():
        if sum(row[field] for row in employment["organismos"]) != total:
            raise ValueError(f"El total de {field} no concilia con ONSC.")
    for row in employment["organismos"]:
        figure = figures_by_id.get(row["id"], {})
        row.update({key: figure.get(key) for key in FIELDS[3:]})
        row.update({key: payroll.get(row["id"], {}).get(key) for key in next(iter(payroll.values()))})
    return employment


def build_optimization(data):
    options = load_data("optimizacion_2025.json")
    for row in options["rubros"]:
        row["ahorro_bruto_uyu"] = [
            round(row["base_uyu"] * row["cobertura_pct"] * rate / 10000)
            for rate in row["reducciones_pct"]
        ]
    options["ahorro_bruto_uyu"] = [
        sum(row["ahorro_bruto_uyu"][index] for row in options["rubros"])
        for index in range(len(options["escenarios"]))
    ]
    options["base_rubros_uyu"] = sum(row["base_uyu"] for row in options["rubros"])
    options["gasto_modelado_rubros_uyu"] = [
        options["base_rubros_uyu"] - savings for savings in options["ahorro_bruto_uyu"]
    ]
    pilot = data["observacion"].copy()
    pilot["monto_involucrado_uyu"] = pilot.pop("monto_observado_uyu")
    pilot["base_monto"] = "Factura observada, importe nominal."
    pilot["url"] = data["fuentes"]["tcr"]["url"]
    options["observaciones"].append(pilot)
    options["observaciones"].sort(key=lambda row: row["fecha"])
    bps = options["caso_bps"]
    bps["tramites"] = bps["reconocimientos"] + bps["jubilaciones"]
    difference = bps["tramites"] * (bps["minutos_antes"] - bps["minutos_despues"])
    bps["horas_estimadas"], bps["minutos_estimados_restantes"] = divmod(difference, 60)
    return options


def build_income_and_territory(data):
    review = load_data("ingresos_y_territorio_2025.json")
    amounts = {row["id"]: row["monto_miles_uyu"] for row in review["ingresos"]}
    components = [row["monto_miles_uyu"] for row in review["ingresos"] if row["nivel"] == "componente"]
    if (sum(components) != amounts["total"] or amounts["directos"] + amounts["indirectos"] != amounts["impuestos"]
            or amounts["impuestos"] + amounts["tasas"] != amounts["tributarios"]):
        raise ValueError("Las cifras de recursos no concilian con los cuadros 24 y 25.")
    review["impuestos_miles_uyu"] = amounts["impuestos"]
    review["recursos_miles_uyu"] = amounts["total"]
    for row in review["ingresos"]:
        row["porcentaje_recursos"] = round(100 * row["monto_miles_uyu"] / amounts["total"], 2)
        page = {24: 56, 25: 57}[row["cuadro"]]
        row["fuente"] = f"{data['fuentes']['rendicion']['url']}#page={page}"

    employment = data["empleo"]
    locations = {row["territorio"]: row for row in employment["territorios"]}
    departments = review["departamentos"]
    if len(departments) != 19 or len({row["departamento"] for row in departments}) != 19:
        raise ValueError("Se esperan los 19 departamentos sin duplicados.")
    if sum(row["area_km2"] for row in departments) != review["area_terrestre_km2"]:
        raise ValueError("La superficie por departamento no concilia con el total terrestre.")
    # Los valores publicados por departamento suman un habitante más que el total nacional.
    if abs(sum(row["poblacion"] for row in departments) - data["poblacion"]) > 1:
        raise ValueError("La población departamental no concilia con el total publicado.")
    for row in departments:
        location = locations[row["departamento"]]
        row["vinculos"] = location["vinculos"]
        row["vinculos_fp"] = location["fp"]
        row["habitantes_por_km2"] = round(row["poblacion"] / row["area_km2"], 1)
        row["vinculos_por_mil_hab"] = round(1000 * row["vinculos"] / row["poblacion"], 1)
    outside = employment["totales"]["vinculos"] - sum(row["vinculos"] for row in departments)
    if outside != sum(locations[name]["vinculos"] for name in ("Exterior", "Itinerantes", "Sin Clasificar")):
        raise ValueError("La distribución de vínculos por lugar de trabajo no concilia.")
    review["vinculos_fuera_del_cruce"] = outside
    review["personas_por_mil_hab"] = round(1000 * employment["totales"]["personas"] / data["poblacion"], 1)
    data["fuentes"].update(review.pop("fuentes"))
    return review


def build_parliament(data):
    parliament = load_data("parlamento_2025.json")
    expenses = ("remuneraciones_uyu", "funcionamiento_uyu", "inversion_uyu")
    for row in parliament["programas"]:
        row["total_uyu"] = sum(row[field] for field in expenses)
    parliament["unidades"] = [
        {
            **unit,
            "ejecutado_uyu": sum(row["total_uyu"] for row in parliament["programas"]
                                 if row["unidad"] == unit["unidad"]),
        }
        for unit in data["empleo"]["unidades"] if unit["inciso"] == "01"
    ]
    parliament["total_uyu"] = sum(unit["ejecutado_uyu"] for unit in parliament["unidades"])
    spending = next(row for row in data["incisos"] if row["id"] == "01")
    if round(parliament["total_uyu"] / 1000) != spending["ejecutado_miles_uyu"]:
        raise ValueError("La ejecución legislativa debe conciliar entre los tomos I y III.")
    parliament["bancas_total"] = sum(parliament["bancas"].values())
    parliament["habitantes_por_banca"] = round(data["poblacion"] / parliament["bancas_total"])
    parliament["costo_por_habitante_uyu"] = round(parliament["total_uyu"] / data["poblacion"])
    months = parliament["actividad_diputados"]
    totals = {key: sum(row[key] for row in months) for key in months[0] if key != "mes"}
    totals["sesiones_plenario"] = totals["ordinarias"] + totals["extraordinarias"] + totals["solemnes_especiales"]
    totals["registros_comisiones"] = (totals["comisiones_permanentes"] + totals["comisiones_especiales"]
                                      + totals["comisiones_preinvestigadoras"])
    parliament["actividad_diputados_total"] = totals
    requests = parliament["pedidos_acceso"]
    request_ids = {row["id"] for row in requests["pedidos"]}
    states = {"esperando", "prorroga", "respondido", "parcial", "sin_respuesta"}
    if len(request_ids) != len(requests["pedidos"]) or any(row["estado"] not in states for row in requests["pedidos"]):
        raise ValueError("Los pedidos de acceso deben tener número único y un estado válido.")
    if any(not set(topic["pedidos"]) <= request_ids for topic in requests["temas"]):
        raise ValueError("Cada tema debe referir a pedidos de acceso registrados.")
    parliament["empleo_montevideo"] = [
        row for row in data["empleo"]["organismos"] if row["id"] in ("98-intendencia", "98-junta")
    ]
    data["fuentes"].update(parliament.pop("fuentes"))
    return parliament


def validate(data):
    rows = data["incisos"]
    if len(rows) != 33 or len({row["id"] for row in rows}) != 33:
        raise ValueError("Se esperan las 33 filas presupuestales del cuadro 27 sin duplicados.")
    if data["totales"] != TOTALS or data["poblacion"] != 3_485_931:
        raise ValueError("El total del cuadro 27/28 o la población INE no coincide con la fuente.")
    for row in rows:
        credit = row["credito_miles_uyu"]
        spent = row["ejecutado_miles_uyu"]
        wages = row["remuneraciones_miles_uyu"]
        if not 0 <= spent <= credit or (wages is not None and not 0 <= wages <= spent):
            raise ValueError(f"Valores de ejecución incompatibles en inciso {row['id']}.")
    # La CGN presenta los totales en miles de pesos, con redondeo por fila.
    for field, published in TOTALS.items():
        summed = sum(row[field] or 0 for row in rows)
        if abs(summed - published) > 3:
            raise ValueError(f"El total de {field} difiere del publicado en más de $ 3.000.")
    inisa = next(row for row in rows if row["id"] == "35")
    if (inisa["ejecutado_miles_uyu"], inisa["remuneraciones_miles_uyu"]) != (3_099_536, 2_549_991):
        raise ValueError("La fila de INISA debe cuadrar con el detalle del Tomo I.")
    if data["observacion"]["inciso"] != inisa["id"]:
        raise ValueError("La observación piloto debe estar vinculada al inciso de INISA.")


PEDIDO_ESTADOS = {"por_enviar": "Por enviar", "esperando": "Esperando", "prorroga": "Prórroga",
                  "respondido": "Respondido", "incompleto": "Respuesta incompleta", "vencido": "Vencido sin respuesta"}
ETIQUETAS = {"tcr": "Tribunal de Cuentas", "finanzas": "Finanzas", "promesa": "Promesa pendiente",
             "vigilar": "Promesa a vigilar", "auditoria": "Auditoría", "pedido": "Pedido de auditoría"}


def slug(text):
    import unicodedata
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return "-".join(plain.lower().split())


def build_intendencias(public):
    """Genera intendencias.html y sus CSV desde datos/intendencias_2022.json."""
    from html import escape
    data = load_data("intendencias_2022.json")
    deps = data["departamentos"]
    if len(deps) != 19 or len({d["departamento"] for d in deps}) != 19:
        raise ValueError("Tienen que estar los 19 departamentos, sin repetir.")
    for d in deps:
        for h in d["hallazgos"]:
            if h["tipo"] not in ETIQUETAS or not h.get("url") or not h.get("fuente"):
                raise ValueError(f"Hallazgo sin tipo válido o sin fuente en {d['departamento']}.")
    totals = data["totales_2022"]
    for key, field in (("gasto_ejecutado_miles_uyu", "gasto_ejecutado_2022_miles_uyu"),
                       ("remuneraciones_miles_uyu", "remuneraciones_2022_miles_uyu"),
                       ("ingresos_nacionales_miles_uyu", "ingresos_nacionales_2022_miles_uyu")):
        if sum(d[field] for d in deps) != totals[key]:
            raise ValueError(f"El total {key} no coincide con la suma de los 19 departamentos.")

    num = lambda n: f"{n:,.0f}".replace(",", ".")
    mill = lambda miles: num(round(miles / 1000))
    pct = lambda x: f"{x:.1f}".replace(".", ",")
    rows = []
    for d in sorted(deps, key=lambda x: -x["gasto_por_habitante_uyu"]):
        dif = d["diferencia_ingreso_gasto_2022_miles_uyu"]
        rows.append(
            f'<tr><td><a href="#{slug(d["departamento"])}">{escape(d["departamento"])}</a></td>'
            f'<td class="n">{mill(d["gasto_ejecutado_2022_miles_uyu"])}</td>'
            f'<td class="n"><b>{num(d["gasto_por_habitante_uyu"])}</b></td>'
            f'<td class="n"><span class="bar" style="--w:{d["pct_remuneraciones"]}%"></span>{pct(d["pct_remuneraciones"])} %</td>'
            f'<td class="n">{pct(d["pct_ingreso_nacional"])} %</td>'
            f'<td class="n{" neg" if dif < 0 else ""}">{"+" if dif > 0 else ""}{mill(dif)}</td></tr>')
    cards = []
    for d in deps:
        sid = slug(d["departamento"])
        t = data["transparencia"]["intai"]["intendencias"]
        t = next(x for x in t if x["departamento"] == d["departamento"])
        nden = sum(1 for r in data["transparencia"]["uaip"]["resoluciones"] if r["departamento"] == d["departamento"])
        transp_line = (f'<p class="transp">Transparencia 2024: '
                       + (f'<b>{t["puntaje_2024"]:.2f}</b> de 1 (puesto {t["posicion_2024"]})'.replace(".", ",", 1)
                          if t["respondio_2024"] else '<b class="cero">no respondió el índice</b>')
                       + f' · Denuncias que le dio la razón la UAIP desde 2025: <b>{nden}</b></p>')
        items = "".join(
            f'<li class="h {h["tipo"]}"><span class="tag">{ETIQUETAS[h["tipo"]]}</span><p>{escape(h["texto"])}</p>'
            f'<small><a href="{escape(h["url"])}" target="_blank" rel="noopener">{escape(h["fuente"])}</a> · {escape(h["solidez"])}</small></li>'
            for h in d["hallazgos"]) or '<li class="h vacio"><p>Sin hallazgos verificados todavía. Si tenés un documento oficial, aportalo.</p></li>'
        cards.append(
            f'<article class="ficha" id="{sid}"><header><h3>{escape(d["departamento"])}</h3>'
            f'<span class="est {"ok" if d["hallazgos"] else "rel"}">{d["estado"]}</span></header>'
            f'<div class="mini"><div><b>$ {mill(d["gasto_ejecutado_2022_miles_uyu"])} M</b><span>gasto 2022</span></div>'
            f'<div><b>{pct(d["pct_remuneraciones"])} %</b><span>en sueldos</span></div>'
            f'<div><b>{pct(d["pct_ingreso_nacional"])} %</b><span>plata nacional</span></div></div>{transp_line}<ul>{items}</ul>'
            f'<div class="acciones"><a class="obj" href="informe.html?aporte=intendencia-{sid}&amp;tipo=correccion#aportes">⚑ Objetar un dato</a>'
            f'<a href="informe.html?aporte=intendencia-{sid}&amp;tipo=opinion#aportes">Aportar información</a></div></article>')
    pedidos = data["pedidos_acceso"]
    # Transparencia: índice de la UAIP y denuncias resueltas contra cada intendencia.
    transp = data["transparencia"]
    intai = {t["departamento"]: t for t in transp["intai"]["intendencias"]}
    if set(intai) != {d["departamento"] for d in deps}:
        raise ValueError("El INTAI tiene que traer las 19 intendencias con el mismo nombre que los departamentos.")
    denuncias = {}
    for r in transp["uaip"]["resoluciones"]:
        denuncias.setdefault(r["departamento"], []).append(r)
    p3 = lambda x: f"{x:.2f}".replace(".", ",")
    transp_rows = []
    for t in sorted(intai.values(), key=lambda x: (-x["puntaje_2024"], x["departamento"])):
        dep = t["departamento"]
        res = denuncias.get(dep, [])
        sil = sum(1 for r in res if r["tipo"] == "silencio positivo")
        estado = (f'<b>{p3(t["puntaje_2024"])}</b>' if t["respondio_2024"]
                  else '<b class="cero">0 · no respondió</b>')
        hist = " / ".join(p3(v) for v in (t["puntaje_2023"], t["puntaje_2022"]))
        links = " ".join(f'<a href="{escape(r["url"])}" target="_blank" rel="noopener" title="{escape(r["tipo"])} · {r["fecha"]}">{r["numero"]}</a>' for r in res)
        transp_rows.append(
            f'<tr><td><a href="#{slug(dep)}">{escape(dep)}</a></td><td class="n">{estado}</td>'
            f'<td class="n">{t["posicion_2024"]}.º</td><td class="n">{hist}</td>'
            f'<td class="n{" neg" if res else ""}">{len(res)}</td><td class="n">{sil}</td>'
            f'<td class="res">{links or "—"}</td></tr>')
    no_resp = [t["departamento"] for t in intai.values() if not t["respondio_2024"]]
    nunca = [t["departamento"] for t in intai.values()
             if t["puntaje_2024"] == 0 and t["puntaje_2023"] == 0 and t["puntaje_2022"] == 0]
    pedido_rows = "".join(
        f'<tr><td>{escape(p["intendencia"])}</td><td>{p["id"] or "—"}</td><td>{p["fecha_envio"] or "—"}</td>'
        f'<td>{p["vencimiento"] or "—"}</td><td><span class="estado-pedido">{PEDIDO_ESTADOS[p["estado"]]}</span></td></tr>'
        for p in pedidos["pedidos"])
    top = sorted(deps, key=lambda x: -x["pct_ingreso_nacional"])[:2]
    notas = [
        "Montos en pesos corrientes de cada año.",
        "“Por habitante” divide el gasto 2022 por la población proyectada a 2025 (INE): es una aproximación.",
        "“Diferencia” compara lo recaudado con lo ejecutado en el año. No es el déficit acumulado oficial.",
        "Los municipios entran en el gasto de la intendencia solo donde la rendición los abre como programa.",
        "Las denuncias de partidos se muestran marcadas como tales hasta verificarlas con documentos oficiales.",
    ]
    values = {
        "ANIO": "2022", "TOTAL_M": mill(totals["gasto_ejecutado_miles_uyu"]),
        "PCT_REM": str(round(100 * totals["remuneraciones_miles_uyu"] / totals["gasto_ejecutado_miles_uyu"])),
        "PCT_INV": str(round(100 * totals["inversiones_miles_uyu"] / totals["gasto_ejecutado_miles_uyu"])),
        "PCT_NAC": pct(100 * totals["ingresos_nacionales_miles_uyu"] / totals["ingresos_miles_uyu"]),
        "TOP_NAC": f'{top[0]["departamento"]} y {top[1]["departamento"]}',
        "TOP_NAC_PCT": str(int(min(t["pct_ingreso_nacional"] for t in top))),
        "RANKING": "".join(rows), "FICHAS": "".join(cards),
        "PEDIDOS": pedido_rows, "PEDIDOS_NOTA": escape(pedidos["nota"]),
        "TRANSP_ROWS": "".join(transp_rows), "N_NO_RESP": str(len(no_resp)),
        "NO_RESP": escape(", ".join(sorted(no_resp))), "NUNCA": escape(", ".join(sorted(nunca))),
        "N_DENUNCIAS": str(len(transp["uaip"]["resoluciones"])),
        "N_SILENCIO": str(sum(1 for r in transp["uaip"]["resoluciones"] if r["tipo"] == "silencio positivo")),
        "INTAI_URL": escape(transp["intai"]["fuente"]["url"]), "UAIP_URL": escape(transp["uaip"]["fuente"]["url"]),
        "UAIP_REF": escape(transp["uaip"]["fuente"]["referencia"]), "CATALOGO": escape(transp["catalogo_saip"]),
        "NOTAS": "".join(f"<li>{n}</li>" for n in notas),
        "FUENTE_URL": data["fuentes"]["opp"]["url"], "FUENTE_NOMBRE": escape(data["fuentes"]["opp"]["nombre"]),
        "CONSULTADO": "/".join(reversed(data["consultado"].split("-"))),
    }
    page = (ROOT / "web" / "intendencias.template.html").read_text(encoding="utf-8")
    for key, value in values.items():
        page = page.replace("{{" + key + "}}", value)
    if "{{" in page:
        raise ValueError("Quedó un marcador sin completar en intendencias.template.html.")
    (public / "intendencias.html").write_text(page, encoding="utf-8")
    write_csv(public, "intendencias_2022.csv",
              [{k: v for k, v in d.items() if k not in ("hallazgos",)} for d in deps])
    write_csv(public, "intendencias_hallazgos.csv",
              [{"departamento": d["departamento"], **h} for d in deps for h in d["hallazgos"]])
    write_csv(public, "pedidos_acceso_intendencias.csv", pedidos["pedidos"])
    write_csv(public, "intendencias_transparencia_intai.csv", transp["intai"]["intendencias"])
    write_csv(public, "intendencias_denuncias_uaip.csv", transp["uaip"]["resoluciones"])
    return data["consultado"]


def main():
    data = load_data("2025.json")
    validate(data)
    spending = load_data("estructura_gasto_2025.json")
    data["estructura_gasto"] = spending
    data["empleo"] = build_employment(data, spending)
    data["optimizacion"] = build_optimization(data)
    data["ingresos_y_territorio"] = build_income_and_territory(data)
    data["parlamento"] = build_parliament(data)
    corrections = load_data("correcciones.json")["correcciones"]
    for row in corrections:
        if row.get("estado") not in CORRECTION_STATES or not row.get("fecha") or not row.get("dato"):
            raise ValueError("Cada corrección necesita fecha, dato objetado y un estado válido.")
    data["correcciones"] = sorted(corrections, key=lambda row: row["fecha"], reverse=True)
    data["fuentes"]["onsc_pdf"] = {
        "nombre": "ONSC · Informe original en PDF",
        "url": "https://www.gub.uy/oficina-nacional-servicio-civil/sites/oficina-nacional-servicio-civil/files/documentos/publicaciones/Informe_Vinculos_2025.pdf",
        "referencia": "Tabla 7, cuadros 1, 5 y 6, y tablas 19, 48 y 50."
    }
    data["fuentes"]["escalafones"] = {
        "nombre": "IMPO · Ley 15.809, art. 28",
        "url": "https://www.impo.com.uy/bases/leyes/15809-1986/28",
        "referencia": "Definiciones de los escalafones C, P y Q."
    }
    data["fuentes"]["fiscal"] = {
        "nombre": "MEF · Exposición de Motivos, Rendición 2025",
        "url": "https://presupuestonacional.gub.uy/sites/default/files/2026-07/Exposici%C3%B3n%20de%20Motivos_R2025.pdf",
        "referencia": "Cierre fiscal Gobierno Central-BPS, págs. 42–43."
    }
    public = ROOT / "publico"
    public.mkdir(exist_ok=True)
    write_csv(public, "ejecucion_2025.csv", data["incisos"])
    employment = data["empleo"]
    by_organism = []
    for row in employment["organismos"]:
        record = {key: value for key, value in row.items() if key != "escalafones"}
        record.update({f"escalafon_{key}": value for key, value in row["escalafones"].items()})
        by_organism.append(record)
    write_csv(public, "dotacion_por_organismo_2025.csv", by_organism)
    write_csv(public, "balances_institucionales_2025.csv", spending["balances_institucionales"])
    write_csv(public, "costos_de_conduccion_identificados_2025.csv", data["optimizacion"]["costos_politicos_identificados"])
    review = data["ingresos_y_territorio"]
    write_csv(public, "ingresos_presupuestales_2025.csv", review["ingresos"])
    write_csv(public, "empleo_y_poblacion_departamental_2025.csv", review["departamentos"])
    write_csv(public, "gasto_parlamento_2025.csv", data["parlamento"]["programas"])
    write_csv(public, "actividad_diputados_2025.csv", data["parlamento"]["actividad_diputados"])
    write_csv(public, "pedidos_acceso_parlamento.csv", data["parlamento"]["pedidos_acceso"]["pedidos"])
    if data["parlamento"]["pedidos_acceso"]["gasto_por_banca"]:
        write_csv(public, "gasto_por_banca_2025.csv", data["parlamento"]["pedidos_acceso"]["gasto_por_banca"])
    for key in ("unidades", "territorios", "municipios", "entidades_relacionadas"):
        write_csv(public, f"empleo_{key}_2025.csv", employment[key])
    write_csv(public, "tribunal_muestra_2025.csv", [
        {key: row.get(key) for key in ("resolucion", "fecha", "expediente", "inciso", "organismo",
                                      "concepto", "monto_involucrado_uyu", "base_monto", "motivo",
                                      "normas", "estado", "perjuicio_acreditado_uyu", "url")}
        for row in data["optimizacion"]["observaciones"]
    ])
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    # La portada va en index.html y el informe completo en informe.html.
    for template_name, page in (("portada.template.html", "index.html"), ("index.template.html", "informe.html")):
        template = (ROOT / "web" / template_name).read_text(encoding="utf-8")
        if template.count("<!-- DATOS_2025 -->") != 1:
            raise ValueError(f"La plantilla {template_name} debe tener un marcador de datos.")
        (public / page).write_text(template.replace("<!-- DATOS_2025 -->", payload), encoding="utf-8")
    # Páginas de casos que no dependen de los datos de 2025: se copian tal cual.
    for page in STATIC_PAGES:
        (public / page).write_text((ROOT / "web" / page).read_text(encoding="utf-8"), encoding="utf-8")
    build_intendencias(public)
    (public / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    urls = "".join(f"  <url><loc>{SITE}/{page}</loc><lastmod>{data['consultado']}</lastmod></url>\n"
                   for page in ("", "informe.html", "intendencias.html", *STATIC_PAGES))
    (public / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                        f"{urls}</urlset>\n", encoding="utf-8")
    print("Validados 33 incisos y rubros, 84 organismos y 270 unidades. Generados la portada, el informe, las 19 intendencias y los CSV.")


if __name__ == "__main__":
    main()
