import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SITE = "https://verdadmilanesa.uy"
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
    (public / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    urls = "".join(f"  <url><loc>{SITE}/{page}</loc><lastmod>{data['consultado']}</lastmod></url>\n"
                   for page in ("", "informe.html"))
    (public / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                        f"{urls}</urlset>\n", encoding="utf-8")
    print("Validados 33 incisos y rubros, 84 organismos y 270 unidades. Generados la portada, el informe y los CSV.")


if __name__ == "__main__":
    main()
