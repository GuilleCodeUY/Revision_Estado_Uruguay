"""Importa cuadros agregados de ONSC 2025 desde el informe oficial en PDF."""

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parent
NUMBER = r"[\d.]+"
TOTALS = {"vinculos": 318_269, "personas": 275_898, "fp": 305_097, "nfp": 13_172}
ESCALAS = "A B C D E F G H J K L M N P Q R S otros".split()
FISCAL_GROUPS = {
    "01": "Poder Legislativo",
    **{f"{i:02d}": "Poder Ejecutivo" for i in [*range(2, 16), 36]},
    **{f"{i:02d}": "Organismos del art. 220" for i in [16, 17, 18, 19, 25, 26, 27, 29, 31, 32, 33, 34, 35]},
}


def integer(text):
    return int(text.replace(".", ""))


def label_key(code, name):
    if code is None:
        return "congreso-intendentes"
    if int(code) < 80:
        return code
    return code + ("-junta" if name.startswith("Junta") else "-intendencia")


def read_people(page):
    half = 295
    results = {}
    for x0, x1 in [(0, half), (half, page.rect.width)]:
        clip = pymupdf.Rect(x0, 190, x1, 739)
        content = page.get_text(clip=clip, sort=True)
        for line in content.splitlines():
            match = re.fullmatch(rf"\s*(?:(\d{{2}})\s+)?(.+?)\s+({NUMBER})\s+({NUMBER})\s*", line)
            if match:
                code, name, links, people = match.groups()
                key = label_key(code, name)
                if key in results:
                    raise ValueError(f"Fila de personas duplicada en {key}.")
                results[key] = (integer(links), integer(people))
    return results


def read_scales(document):
    rows = []
    for index in (144, 145):
        for line in document[index].get_text(sort=True).splitlines():
            cells = re.split(r"\s{2,}", line.strip())
            if len(cells) == 21 and re.fullmatch(r"\d{2}", cells[0]):
                code, name = cells[:2]
                values = cells[2:]
            elif len(cells) == 20 and cells[0] == "Congreso de Intendentes":
                code, name = None, cells[0]
                values = cells[1:]
            else:
                continue
            scale = dict(zip(ESCALAS, map(integer, values[:-1]), strict=True))
            total = integer(values[-1])
            if total != sum(scale.values()):
                raise ValueError(f"Los escalafones no cierran en {name}.")
            rows.append((code, name, scale, total))
    return rows


def read_units(document):
    units = []
    current = None
    for index in range(118, 125):
        page = document[index]
        columns = (482, 771, 806) if index < 121 else (443, 760, 795)
        words = page.get_text("words")
        for anchor in sorted(words, key=lambda word: word[1]):
            x, y, _, _, unit_code, *_ = anchor
            if not (x < 38 and 105 < y < 525 and re.fullmatch(r"\d{2,3}", unit_code)):
                continue
            if len(unit_code) == 2:
                current = unit_code
                continue
            line = sorted((w for w in words if abs(w[1] - y) < 1.1), key=lambda w: w[0])
            values = []
            for edge in columns:
                matches = [w[4] for w in line if abs((w[0] + w[2]) / 2 - edge) < 5 and re.fullmatch(NUMBER, w[4])]
                if len(matches) != 1:
                    break
                values.append(integer(matches[0]))
            source_page = index + 1
            if len(values) != 3 and (current, unit_code) == ("29", "077"):
                detail = document[285].get_text(sort=True)
                if re.search(r"077 Hospital del Cerro\s+142\s+189\s+106\s+437\s+0", detail):
                    values = [437, 0, 437]
                    source_page = 286
            if len(values) != 3:
                raise ValueError(f"No se pudo leer la unidad {current}/{unit_code} en pág. {index + 1}.")
            fp, nfp, links = values
            if fp + nfp != links:
                raise ValueError(f"La unidad {current}/{unit_code} no cierra en pág. {index + 1}.")
            name = " ".join(w[4] for w in line if x < w[0] < 143)
            units.append({"inciso": current, "unidad": unit_code, "organismo": name, "fp": fp,
                          "nfp": nfp, "vinculos": links, "pagina_pdf": source_page})
    return units


def read_territory(page):
    rows = []
    for line in page.get_text(sort=True).splitlines():
        match = re.fullmatch(rf"\s*(.+?)\s+({NUMBER})\s+({NUMBER})\s+({NUMBER})\s*", line)
        if match and match[1] != "TOTAL":
            name, fp, nfp, links = match.groups()
            rows.append({"territorio": name, "fp": integer(fp), "nfp": integer(nfp), "vinculos": integer(links)})
    return rows


def read_municipal(document):
    rows = []
    department = None
    for index in range(139, 144):
        words = document[index].get_text("words")
        anchors = [w for w in words if abs((w[0] + w[2]) / 2 - 770.5) < 3 and re.fullmatch(NUMBER, w[4])]
        for anchor in sorted(anchors, key=lambda word: word[1]):
            line = sorted((w for w in words if abs(w[1] - anchor[1]) < 1.2), key=lambda w: w[0])
            label = " ".join(w[4] for w in line if w[0] < 168)
            if re.match(r"\d{2}_001\b", label):
                department = label[:2]
                continue
            if department is None or not label or label.lower().startswith("total"):
                continue
            values = []
            for center in (379, 731.4, 770.5):
                matches = [w[4] for w in line if abs((w[0] + w[2]) / 2 - center) < 5 and re.fullmatch(NUMBER, w[4])]
                if len(matches) > 1:
                    raise ValueError(f"No se pudo leer el total municipal de {department}, {label}.")
                values.append(integer(matches[0]) if matches else 0)
            fp, nfp, links = values
            note = None
            if department == "87" and label == "Mariscala" and values == [0, 0, 0]:
                components = [integer(w[4]) for w in line if 168 < w[0] < 340 and re.fullmatch(NUMBER, w[4])]
                if components == [8, 5]:
                    fp = links = sum(components)
                    note = "Subtotal reconstruido con 8 + 5. El cuadro imprime 0 en el total de esta fila."
            if fp + nfp != links:
                raise ValueError(f"No cierran los vínculos municipales de {department}, {label}.")
            rows.append({"inciso": department, "dependencia": label,
                         "tipo": "Oficinas centrales" if label == "Oficinas Centrales" else "Local",
                         "fp": fp, "nfp": nfp, "vinculos": links, "pagina_pdf": index + 1, "nota": note})
    return rows


def read_related(document):
    rows = []
    nonstate = "Personas públicas no estatales"
    subsidiaries = "Entidades de participación estatal mayoritaria"
    for index in (111, 112):
        for line in document[index].get_text(sort=True).splitlines():
            cells = re.split(r"\s{2,}", line.strip())
            if cells == ["49", "262", "311"]:
                cells.insert(0, "Comisión Honoraria para la Lucha Antituberculosa y Enfermedades Prevalentes (CHLA-EP)")
            if (len(cells) not in (4, 5) or cells[0] == "Total"
                    or any(not re.fullmatch(NUMBER, cell) for cell in cells[1:])):
                continue
            name = cells[0]
            if name.endswith("Para Los"):
                name += " Funcionarios de OSE (CHASSFOSE)"
            if name.startswith("Instituto de Promoción"):
                name += " (Uruguay XXI)"
            rows.append({"organismo": name, "grupo": nonstate, "vinculos": integer(cells[-1]),
                         "integrantes_directorio": None, "pagina_pdf": index + 1})
    for line in document[115].get_text(sort=True).splitlines():
        cells = re.split(r"\s{2,}", line.strip())
        if cells[-1] == "47Estado":
            cells[-1] = "47"
        if "15Desarrollo" in cells:
            cells = ["CONAFIN - AFISA", "3", "0", "3", "4", "11", "15"]
        if "Fundación LATITUD" in cells:
            cells = ["Fundación LATITUD", "1", "0", "1", "13", "23", "36"]
        if (len(cells) < 7 or cells[0] == "Total"
                or any(not re.fullmatch(NUMBER, cell) for cell in cells[-6:])):
            continue
        rows.append({"organismo": cells[-7], "grupo": subsidiaries, "vinculos": integer(cells[-1]),
                     "integrantes_directorio": integer(cells[-4]), "pagina_pdf": 116})
    if sum(r["vinculos"] for r in rows if r["grupo"] == nonstate) != 6607:
        raise ValueError("Los vínculos de las personas públicas no estatales no cierran.")
    subsidiary_links = sum(r["vinculos"] for r in rows if r["grupo"] == subsidiaries)
    directors = sum(r["integrantes_directorio"] or 0 for r in rows)
    if (subsidiary_links, directors) != (2669, 75):
        raise ValueError(f"Los vínculos y directorios de las entidades mayoritarias no cierran: {subsidiary_links}, {directors}.")
    return rows


def group_for(code):
    if code in FISCAL_GROUPS:
        return FISCAL_GROUPS[code]
    if code is None or int(code) >= 80:
        return "Gobiernos departamentales"
    return "Organismos del art. 221"


def import_data(path):
    with pymupdf.open(path) as document:
        if len(document) != 589:
            raise ValueError("Se requiere la edición ONSC 2025 de 589 páginas.")
        people = read_people(document[32])
        scales = read_scales(document)
        rows = []
        for code, name, scale, fp in scales:
            key = label_key(code, name)
            links, individuals = people.pop(key)
            if not 0 <= fp <= links or not 0 < individuals <= links:
                raise ValueError(f"Los vínculos y las personas son incompatibles en {name}.")
            rows.append({"id": key, "inciso": code, "organismo": name, "grupo": group_for(code),
                         "personas": individuals, "vinculos": links, "fp": fp,
                         "nfp": links - fp, "politico_p": scale["P"], "confianza_q": scale["Q"],
                         "administrativo_c": scale["C"], "escalafones": scale})
        if people:
            raise ValueError(f"Faltan filas escalafonarias para {list(people)}.")
        units = read_units(document)
        territory = read_territory(document[49])
        municipal = read_municipal(document)
        related = read_related(document)

    for key in ("vinculos", "fp", "nfp"):
        if sum(row[key] for row in rows) != TOTALS[key] or sum(row[key] for row in territory) != TOTALS[key]:
            raise ValueError(f"El total de {key} difiere del publicado.")
    for key, value in {"politico_p": 1174, "confianza_q": 893, "administrativo_c": 33063}.items():
        if sum(row[key] for row in rows) != value:
            raise ValueError(f"El total de {key} difiere del publicado.")
    if len({(u["inciso"], u["unidad"]) for u in units}) != len(units):
        raise ValueError("Hay unidades ejecutoras duplicadas.")
    for field in ("vinculos", "fp", "nfp"):
        by_inciso = Counter()
        by_unit = Counter()
        for row in rows:
            by_inciso[row["inciso"]] += row[field]
        for row in units:
            by_unit[row["inciso"]] += row[field]
        if any(by_inciso[code] != value for code, value in by_unit.items()):
            raise ValueError(f"Las unidades ejecutoras no concilian con sus incisos en {field}.")
    if sum(row["vinculos"] for row in municipal if row["tipo"] == "Local") != 7394:
        raise ValueError("Los vínculos municipales no concilian con el cuadro 5.")
    return {"fecha_corte": "2025-12-31", "totales": TOTALS,
            "sha256_pdf": hashlib.sha256(path.read_bytes()).hexdigest(),
            "organismos": rows, "unidades": units, "territorios": territory,
            "municipios": municipal, "entidades_relacionadas": related}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    data = import_data(args.pdf)
    output = ROOT / "datos" / "empleo_2025.json"
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(data['organismos'])} organismos, {len(data['unidades'])} unidades y {len(data['territorios'])} territorios.")


if __name__ == "__main__":
    main()
