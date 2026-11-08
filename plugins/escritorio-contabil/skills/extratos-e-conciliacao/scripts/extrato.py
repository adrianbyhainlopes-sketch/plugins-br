"""Extrato (texto de PDF ou CSV exportado) para tabela com valor com sinal e prova pelo saldo corrido.

Uso:
    python -I extrato.py --formato formato.json --entrada extrato.txt --saida tabela.csv [--xlsx tabela.xlsx] [--ano 2026]

Texto de PDF: gere antes com  pdftotext -enc UTF-8 -table arquivo.pdf extrato.txt  (ou -layout, se as colunas ficarem na mesma linha)
Só lê a entrada e o formato. Só grava o arquivo de --saida, que não pode existir. Só biblioteca padrão.
Saída: CSV com ponto e vírgula e vírgula decimal, em utf-8-sig, que o Excel em português abre certo; com --xlsx, também a planilha.
Código de saída: 0 saldo bate; 2 saldo não bate; 1 erro de uso.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zipfile
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from xml.sax.saxutils import escape

VALOR_SOLTO = re.compile(r"^(?P<valor>-?[\d.,]+\d)\s*(?P<dc>[DC])?(?:\s+(?P<saldo>-?[\d.,]+\d)\s*(?P<saldo_dc>[DC])?)?$", re.I)


def falha(msg: str) -> None:
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def para_decimal(texto: str, dc: str | None = None) -> Decimal:
    """O último separador de um valor com duas casas decide; D ou menos deixa negativo."""
    t = texto.strip().replace("R$", "").replace(" ", "")
    negativo = False
    if t.startswith("(") and t.endswith(")"):
        negativo, t = True, t[1:-1]
    if t.endswith("-"):
        negativo, t = True, t[:-1]
    if t.startswith("-"):
        negativo, t = True, t[1:]
    pos = max(t.rfind(","), t.rfind("."))
    if pos >= 0 and len(t) - pos - 1 == 2:
        inteiro, frac = t[:pos], t[pos + 1:]
    else:
        inteiro, frac = t, "00"
    inteiro = inteiro.replace(".", "").replace(",", "")
    try:
        v = Decimal(f"{inteiro or '0'}.{frac}")
    except InvalidOperation as e:
        raise ValueError(f"valor ilegível: {texto!r}") from e
    if negativo or (dc or "").upper() == "D":
        v = -v
    return v


def br(v: Decimal | None) -> str:
    if v is None:
        return ""
    t = f"{v:,.2f}"
    return t.replace(",", "X").replace(".", ",").replace("X", ".")


def ler_data(texto: str, fmt: str, ano: int | None) -> str:
    t = texto.strip()
    if re.fullmatch(r"\d{2}/\d{2}", t):
        if ano is None:
            falha("a data do extrato não traz o ano: informe --ano")
        t, fmt = f"{t}/{ano}", "%d/%m/%Y"
    return datetime.strptime(t, fmt).strftime("%Y-%m-%d")


def nova_linha(m: re.Match, fmt: dict, n: int, pagina: int, ano: int | None) -> dict:
    g = m.groupdict()
    if fmt.get("sinal", "dc") == "colunas":
        credito, debito = g.get("credito"), g.get("debito")
        valor = para_decimal(credito) if credito else -abs(para_decimal(debito))
    else:
        valor = para_decimal(g["valor"], g.get("dc"))
    saldo = para_decimal(g["saldo"], g.get("saldo_dc")) if g.get("saldo") else None
    return {"linha": n, "pagina": pagina, "data": ler_data(g["data"], fmt.get("formato_data", "%d/%m/%Y"), ano),
            "descricao": " ".join(g.get("descricao", "").split()), "ref": (g.get("ref") or "").strip(),
            "valor": valor, "saldo": saldo, "tipo": "movimento"}


def ler_texto(caminho: Path, fmt: dict, ano: int | None) -> tuple[list[dict], dict]:
    bruto = caminho.read_bytes()
    try:
        texto = bruto.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = bruto.decode("cp1252")
    padrao = re.compile(fmt["linha"])
    ignorar = [re.compile(p) for p in fmt.get("ignorar", [])]
    inicial = re.compile(fmt["saldo_inicial"]) if fmt.get("saldo_inicial") else None
    final = re.compile(fmt["saldo_final"]) if fmt.get("saldo_final") else None
    dia = re.compile(fmt["saldo_dia"]) if fmt.get("saldo_dia") else None
    linhas: list[dict] = []
    extras = {"saldo_inicial": None, "saldo_final": None, "ignoradas": 0, "desconhecidas": [], "marcadores": []}
    pagina = 1
    for n, bruta in enumerate(re.split(r"\r?\n", texto), start=1):
        pagina += bruta.count("\f")
        linha = bruta.replace("\f", "").strip()
        if not linha:
            continue
        if any(p.search(linha) for p in ignorar):
            extras["ignoradas"] += 1
            continue
        if inicial and (m := inicial.search(linha)):
            extras["saldo_inicial"] = para_decimal(m["valor"], m.groupdict().get("dc"))
            continue
        if final and (m := final.search(linha)):
            extras["saldo_final"] = para_decimal(m["valor"], m.groupdict().get("dc"))
            continue
        if dia and (m := dia.search(linha)):
            extras["marcadores"].append({"apos": len(linhas), "saldo": para_decimal(m["valor"], m.groupdict().get("dc")), "linha": n})
            continue
        if m := padrao.search(linha):
            linhas.append(nova_linha(m, fmt, n, pagina, ano))
            continue
        if (m := VALOR_SOLTO.match(linha)) and linhas and linhas[-1].get("sem_valor"):
            linhas[-1]["valor"] = para_decimal(m["valor"], m.groupdict().get("dc"))
            if m["saldo"]:
                linhas[-1]["saldo"] = para_decimal(m["saldo"], m["saldo_dc"])
            del linhas[-1]["sem_valor"]
            continue
        if fmt.get("linha_sem_valor") and (m := re.search(fmt["linha_sem_valor"], linha)):
            linhas.append({"linha": n, "pagina": pagina, "data": ler_data(m["data"], fmt.get("formato_data", "%d/%m/%Y"), ano),
                           "descricao": " ".join(m["descricao"].split()), "ref": "", "valor": Decimal("0"), "saldo": None,
                           "tipo": "movimento", "sem_valor": True})
            continue
        if fmt.get("continuacao") and linhas and not re.search(r"\d,\d{2}\b", linha):
            linhas[-1]["descricao"] += " " + " ".join(linha.split())
            continue
        extras["desconhecidas"].append((n, linha[:100]))
    if fmt.get("ordem") == "decrescente":
        linhas.reverse()
    return linhas, extras


def ler_csv(caminho: Path, fmt: dict, ano: int | None) -> tuple[list[dict], dict]:
    bruto = caminho.read_bytes()
    try:
        texto = bruto.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = bruto.decode("cp1252")
    c = fmt["colunas"]
    linhas: list[dict] = []
    extras = {"saldo_inicial": None, "saldo_final": None, "ignoradas": 0, "desconhecidas": [], "marcadores": []}
    leitor = csv.DictReader(texto.splitlines(), delimiter=fmt.get("delimitador", ";"))
    for n, reg in enumerate(leitor, start=2):
        credito, debito = (reg.get(c["credito"]) if c.get("credito") else None), (reg.get(c["debito"]) if c.get("debito") else None)
        if c.get("valor"):
            bruto_v = reg.get(c["valor"], "")
            valor = para_decimal(bruto_v, reg.get(c["dc"]) if c.get("dc") else None) if bruto_v.strip() else None
        elif (credito or "").strip():
            valor = para_decimal(credito)
        elif (debito or "").strip():
            valor = -abs(para_decimal(debito))
        else:
            valor = None
        if valor is None:
            extras["desconhecidas"].append((n, "linha sem valor"))
            continue
        saldo_bruto = reg.get(c["saldo"], "") if c.get("saldo") else ""
        linhas.append({"linha": n, "pagina": 1, "data": ler_data(reg[c["data"]], fmt.get("formato_data", "%d/%m/%Y"), ano),
                       "descricao": " ".join((reg.get(c["descricao"]) or "").split()), "ref": (reg.get(c["ref"]) or "") if c.get("ref") else "",
                       "valor": valor, "saldo": para_decimal(saldo_bruto) if saldo_bruto.strip() else None, "tipo": "movimento"})
    if fmt.get("ordem") == "decrescente":
        linhas.reverse()
    return linhas, extras


def hipotese(dif: Decimal, linha: dict, indice: int, total: int) -> str:
    if abs(dif) == 2 * abs(linha["valor"]) and linha["valor"] != 0:
        return "a diferença é o dobro do valor desta linha: sinal D/C invertido"
    if indice == 0:
        return "só na primeira linha: confira o saldo inicial (pode vir de período anterior)"
    return f"falta um movimento de {br(abs(dif))} antes desta linha, ou um valor partido; procure valor sem descrição por perto"


def provar(linhas: list[dict], extras: dict) -> dict:
    """Confere linha a linha contra o último saldo conhecido; cada quebra é contada uma vez."""
    faltou_valor = [l for l in linhas if l.get("sem_valor")]
    acumulado = extras["saldo_inicial"]
    referencia = extras["saldo_inicial"]
    quebras = []
    for i, l in enumerate(linhas):
        if acumulado is not None:
            acumulado += l["valor"]
        if referencia is not None:
            referencia += l["valor"]
        l["calculado"] = acumulado
        if l["saldo"] is None:
            l["dif"] = None
            continue
        if referencia is None:
            l["dif"], acumulado, referencia = None, l["saldo"], l["saldo"]
            l["calculado"] = acumulado
            continue
        dif = l["saldo"] - referencia
        l["dif"] = dif
        if dif != 0:
            quebras.append({"linha": l["linha"], "pagina": l["pagina"], "dif": dif, "hipotese": hipotese(dif, l, i, len(linhas))})
        referencia = l["saldo"]
    for q1, q2 in zip(quebras, quebras[1:]):
        if q1["dif"] == -q2["dif"] and q2["linha"] - q1["linha"] <= 3:
            texto = "duas quebras opostas em linhas vizinhas: o saldo impresso da primeira destoa; confira no original se é erro de impressão ou movimento partido"
            q1["hipotese"], q2["hipotese"] = texto, texto
    marcadores_ruins = []
    for mk in extras["marcadores"]:
        if extras["saldo_inicial"] is not None:
            calc = extras["saldo_inicial"] + sum((l["valor"] for l in linhas[: mk["apos"]]), Decimal("0"))
            if calc != mk["saldo"]:
                marcadores_ruins.append({"linha": mk["linha"], "dif": mk["saldo"] - calc})
    soma = sum((l["valor"] for l in linhas), Decimal("0"))
    fecha = None
    if extras["saldo_inicial"] is not None and extras["saldo_final"] is not None:
        fecha = extras["saldo_inicial"] + soma - extras["saldo_final"]
    return {"quebras": quebras, "soma": soma, "fecha": fecha, "marcadores_ruins": marcadores_ruins, "sem_valor": faltou_valor}


def gravar(saida: Path, linhas: list[dict], extras: dict, r: dict) -> None:
    try:
        arq = open(saida, "x", encoding="utf-8-sig", newline="")
    except FileExistsError:
        falha(f"{saida} já existe; escolha outro nome (este programa nunca sobrescreve)")
    with arq:
        w = csv.writer(arq, delimiter=";")
        w.writerow(["linha_origem", "pagina", "data", "descricao", "referencia", "valor", "saldo_impresso", "saldo_calculado", "diferenca", "tipo"])
        if extras["saldo_inicial"] is not None:
            w.writerow(["", "", "", "SALDO INICIAL", "", "", br(extras["saldo_inicial"]), br(extras["saldo_inicial"]), "", "saldo_inicial"])
        for l in linhas:
            w.writerow([l["linha"], l["pagina"], l["data"], l["descricao"], l["ref"], br(l["valor"]), br(l["saldo"]), br(l["calculado"]), br(l["dif"]), l["tipo"]])
        if extras["saldo_final"] is not None:
            w.writerow(["", "", "", "SALDO FINAL", "", "", br(extras["saldo_final"]), "", "", "saldo_final"])


def gravar_xlsx(saida: Path, linhas: list[dict], extras: dict) -> None:
    """Planilha mínima: número como número, data como data, documento como texto. Texto nunca vira fórmula."""
    def texto(col: str, n: int, v: str, s: int = 0) -> str:
        return f'<c r="{col}{n}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{escape(v)}</t></is></c>' if v else ""

    def numero(col: str, n: int, v, s: int = 2) -> str:
        return f'<c r="{col}{n}" s="{s}"><v>{v}</v></c>' if v is not None else ""

    titulos = ["Linha origem", "Página", "Data", "Descrição", "Referência", "Valor", "Saldo impresso", "Saldo calculado", "Diferença", "Tipo"]
    colunas = "ABCDEFGHIJ"
    corpo = ['<row r="1">' + "".join(texto(c, 1, x, 3) for c, x in zip(colunas, titulos)) + "</row>"]
    n = 2
    if extras["saldo_inicial"] is not None:
        corpo.append(f'<row r="{n}">' + texto("D", n, "SALDO INICIAL") + numero("G", n, extras["saldo_inicial"]) + numero("H", n, extras["saldo_inicial"]) + texto("J", n, "saldo_inicial") + "</row>")
        n += 1
    for l in linhas:
        serial = (date.fromisoformat(l["data"]) - date(1899, 12, 30)).days
        corpo.append(f'<row r="{n}">' + numero("A", n, l["linha"], 0) + numero("B", n, l["pagina"], 0) + numero("C", n, serial, 1) + texto("D", n, l["descricao"]) + texto("E", n, l["ref"])
                     + numero("F", n, l["valor"]) + numero("G", n, l["saldo"]) + numero("H", n, l["calculado"]) + numero("I", n, l["dif"]) + texto("J", n, l["tipo"]) + "</row>")
        n += 1
    if extras["saldo_final"] is not None:
        corpo.append(f'<row r="{n}">' + texto("D", n, "SALDO FINAL") + numero("G", n, extras["saldo_final"]) + texto("J", n, "saldo_final") + "</row>")
    folha = ('<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0">'
             '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><sheetData>' + "".join(corpo) + f'</sheetData><autoFilter ref="A1:J{n}"/></worksheet>')
    estilos = ('<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
               '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
               '<cellXfs count="4"><xf/><xf numFmtId="14" applyNumberFormat="1"/><xf numFmtId="4" applyNumberFormat="1"/><xf fontId="1" applyFont="1"/></cellXfs></styleSheet>')
    partes = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        "xl/workbook.xml": '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Extrato" sheetId="1" r:id="rId1"/></sheets></workbook>',
        "xl/_rels/workbook.xml.rels": '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
        "xl/styles.xml": estilos,
        "xl/worksheets/sheet1.xml": folha,
    }
    try:
        arq = open(saida, "xb")
    except FileExistsError:
        falha(f"{saida} já existe; escolha outro nome (este programa nunca sobrescreve)")
    with arq, zipfile.ZipFile(arq, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, conteudo in partes.items():
            z.writestr(nome, conteudo)


def relatorio(linhas: list[dict], extras: dict, r: dict) -> int:
    creditos = sum((l["valor"] for l in linhas if l["valor"] > 0), Decimal("0"))
    debitos = sum((l["valor"] for l in linhas if l["valor"] < 0), Decimal("0"))
    print(f"movimentos: {len(linhas)}; créditos: {br(creditos)}; débitos: {br(debitos)}; soma: {br(r['soma'])}")
    print(f"saldo inicial: {br(extras['saldo_inicial']) or 'não achado'}; saldo final: {br(extras['saldo_final']) or 'não achado'}")
    if linhas:
        print(f"período: {linhas[0]['data']} a {linhas[-1]['data']}")
    print(f"linhas de ruído ignoradas: {extras['ignoradas']}; não reconhecidas: {len(extras['desconhecidas'])}")
    for n, t in extras["desconhecidas"][:15]:
        print(f"  não reconhecida, linha {n}: {t}")
    for l in r["sem_valor"]:
        print(f"  MOVIMENTO SEM VALOR, linha {l['linha']}: {l['descricao'][:60]}")
    ok = not r["quebras"] and not r["sem_valor"] and not r["marcadores_ruins"] and r["fecha"] in (None, Decimal("0")) and not extras["desconhecidas"]
    if r["fecha"] is None:
        print("PROVA INCOMPLETA: falta saldo inicial ou final para a equação de fechamento")
        ok = False
    elif r["fecha"] != 0:
        print(f"NÃO FECHA: saldo inicial + movimentos − saldo final = {br(r['fecha'])}")
    if r["quebras"]:
        print(f"QUEBRAS NO SALDO CORRIDO: {len(r['quebras'])}")
        for q in r["quebras"][:15]:
            print(f"  linha {q['linha']} (página {q['pagina']}): diferença {br(q['dif'])}; {q['hipotese']}")
    for m in r["marcadores_ruins"][:15]:
        print(f"  saldo do dia, linha {m['linha']}: diferença {br(m['dif'])}")
    print("RESULTADO: " + ("SALDO BATE" if ok else "NÃO ENTREGUE COMO BOM"))
    return 0 if ok else 2


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--formato", required=True, type=Path)
    ap.add_argument("--entrada", required=True, type=Path)
    ap.add_argument("--saida", required=True, type=Path)
    ap.add_argument("--xlsx", type=Path)
    ap.add_argument("--ano", type=int)
    a = ap.parse_args()
    fmt = json.loads(a.formato.read_text(encoding="utf-8"))
    leitor = ler_csv if fmt.get("tipo") == "csv" else ler_texto
    try:
        linhas, extras = leitor(a.entrada, fmt, a.ano)
    except ValueError as e:
        falha(str(e))
    r = provar(linhas, extras)
    gravar(a.saida, linhas, extras, r)
    if a.xlsx:
        gravar_xlsx(a.xlsx, linhas, extras)
    sys.exit(relatorio(linhas, extras, r))


if __name__ == "__main__":
    main()
