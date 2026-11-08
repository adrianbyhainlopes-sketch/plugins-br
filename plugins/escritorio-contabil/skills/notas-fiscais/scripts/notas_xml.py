"""Lote de XML de NF-e, NFC-e, CT-e e NFS-e nacional: planilhas por nota e por item, totais por CFOP e CST, e conferência.

Uso:
    python -I notas_xml.py --entrada pasta_ou_arquivo --saida pasta_nova_de_saida

NFS-e de leiaute municipal (fora do padrão nacional) é contada e listada à parte: ver referencias/mapas-xml/nfse.md.
Só lê as entradas. Só grava dentro de --saida, que não pode existir. Só biblioteca padrão.
Fechamento: arquivos lidos = notas + eventos + duplicadas + municipais à parte + não reconhecidos + com erro.
Código de saída: 0 sem alerta; 2 com alerta; 1 erro de uso.
"""
from __future__ import annotations

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

ZERO = Decimal("0")


def br(v: Decimal, casas: int = 2) -> str:
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def local(e: ET.Element) -> str:
    return e.tag.rsplit("}", 1)[-1]


def achar(e: ET.Element | None, *caminho: str) -> ET.Element | None:
    atual = e
    for nome in caminho:
        if atual is None:
            return None
        atual = next((f for f in atual if local(f) == nome), None)
    return atual


def txt(e: ET.Element | None, *caminho: str) -> str:
    alvo = achar(e, *caminho)
    return (alvo.text or "").strip() if alvo is not None else ""


def dec(texto: str) -> Decimal:
    try:
        return Decimal(texto) if texto else ZERO
    except InvalidOperation:
        return ZERO


def primeiro(e: ET.Element | None, nome: str) -> ET.Element | None:
    if e is None:
        return None
    return next((f for f in e.iter() if local(f) == nome), None)


def doc_id(e: ET.Element | None) -> str:
    return txt(e, "CNPJ") or txt(e, "CPF")


def dv_chave_ok(chave: str) -> bool | None:
    """Módulo 11 sobre as 43 primeiras posições (MOC, campo cDV). Letra na chave: não conferido."""
    if len(chave) != 44:
        return False
    if not chave.isdigit():
        return None
    pesos, soma, p = chave[:43][::-1], 0, 2
    for c in pesos:
        soma += int(c) * p
        p = 2 if p == 9 else p + 1
    resto = soma % 11
    return int(chave[43]) == (0 if resto < 2 else 11 - resto)


def ler_nfe(raiz: ET.Element, arq: str) -> dict:
    inf = primeiro(raiz, "infNFe")
    ide, emit, dest, total = achar(inf, "ide"), achar(inf, "emit"), achar(inf, "dest"), achar(inf, "total")
    t = achar(total, "ICMSTot")
    iss = achar(total, "ISSQNtot")
    chave = (inf.get("Id") or "").removeprefix("NFe")
    prot = primeiro(raiz, "infProt")
    nota = {"arquivo": arq, "tipo": "NFC-e" if txt(ide, "mod") == "65" else "NF-e", "chave": chave, "serie": txt(ide, "serie"), "numero": txt(ide, "nNF"),
            "emissao": txt(ide, "dhEmi")[:10] or txt(ide, "dEmi"), "operacao": {"0": "entrada", "1": "saída"}.get(txt(ide, "tpNF"), txt(ide, "tpNF")),
            "emitente": doc_id(emit), "emitente_nome": txt(emit, "xNome"), "destinatario": doc_id(dest), "crt": txt(emit, "CRT"),
            "valor_nota": dec(txt(t, "vNF")), "cstat": txt(prot, "cStat"), "protocolo": txt(prot, "nProt"), "alertas": []}
    itens, soma_prod, soma_icms = [], ZERO, ZERO
    for det in (f for f in inf if local(f) == "det"):
        prod, imp = achar(det, "prod"), achar(det, "imposto")
        grupo = next(iter(achar(imp, "ICMS") or []), None) if achar(imp, "ICMS") is not None else None
        v_prod, v_icms = dec(txt(prod, "vProd")), dec(txt(grupo, "vICMS"))
        q, un = dec(txt(prod, "qCom")), dec(txt(prod, "vUnCom"))
        if q and un and abs(q * un - v_prod) > Decimal("0.01"):
            nota["alertas"].append(f"item {det.get('nItem')}: quantidade × unitário = {br(q * un)} e vProd = {br(v_prod)}")
        if txt(prod, "indTot") != "0":
            soma_prod += v_prod
        soma_icms += v_icms
        itens.append({"chave": chave, "item": det.get("nItem") or "", "codigo": txt(prod, "cProd"), "descricao": txt(prod, "xProd"), "ncm": txt(prod, "NCM"),
                      "cfop": txt(prod, "CFOP"), "cst_ou_csosn": txt(grupo, "CST") or txt(grupo, "CSOSN"), "aliq_icms": txt(grupo, "pICMS"),
                      "valor_produto": v_prod, "base_icms": dec(txt(grupo, "vBC")), "valor_icms": v_icms})
    if soma_prod != dec(txt(t, "vProd")):
        nota["alertas"].append(f"soma dos itens {br(soma_prod)} difere de vProd {br(dec(txt(t, 'vProd')))}")
    if soma_icms != dec(txt(t, "vICMS")):
        nota["alertas"].append(f"soma do ICMS dos itens {br(soma_icms)} difere de vICMS {br(dec(txt(t, 'vICMS')))}")
    if any(txt(d, "prod", "veicProd", "tpOp") == "2" for d in inf if local(d) == "det"):
        nota["alertas"].append("faturamento direto de veículo: identidade do total não conferida (exceção do MOC)")
    else:
        g = lambda n: dec(txt(t, n))
        calculado = g("vProd") - g("vDesc") - g("vICMSDeson") + g("vST") + g("vFCPST") + g("vFrete") + g("vSeg") + g("vOutro") + g("vII") + g("vIPI") + g("vIPIDevol") + dec(txt(iss, "vServ"))
        if calculado != g("vNF"):
            nota["alertas"].append(f"total calculado {br(calculado)} difere de vNF {br(g('vNF'))} (regra W16 do MOC)")
    return {"nota": nota, "itens": itens}


def ler_cte(raiz: ET.Element, arq: str) -> dict:
    inf = primeiro(raiz, "infCte")
    ide, emit = achar(inf, "ide"), achar(inf, "emit")
    prest = achar(inf, "vPrest")
    chave = (inf.get("Id") or "").removeprefix("CTe")
    prot = primeiro(raiz, "infProt")
    total = dec(txt(prest, "vTPrest"))
    nota = {"arquivo": arq, "tipo": "CT-e", "chave": chave, "serie": txt(ide, "serie"), "numero": txt(ide, "nCT"), "emissao": txt(ide, "dhEmi")[:10], "operacao": "",
            "emitente": doc_id(emit), "emitente_nome": txt(emit, "xNome"), "destinatario": doc_id(achar(inf, "dest")), "crt": "",
            "valor_nota": total, "cstat": txt(prot, "cStat"), "protocolo": txt(prot, "nProt"), "alertas": []}
    comps = [dec(txt(c, "vComp")) for c in (prest if prest is not None else []) if local(c) == "Comp"]
    if comps and sum(comps, ZERO) != total:
        nota["alertas"].append(f"soma dos componentes {br(sum(comps, ZERO))} difere de vTPrest {br(total)}")
    grupo = next(iter(achar(inf, "imp", "ICMS") or []), None) if achar(inf, "imp", "ICMS") is not None else None
    item = {"chave": chave, "item": "1", "codigo": "", "descricao": txt(ide, "natOp"), "ncm": "", "cfop": txt(ide, "CFOP"), "cst_ou_csosn": txt(grupo, "CST"),
            "aliq_icms": txt(grupo, "pICMS"), "valor_produto": total, "base_icms": dec(txt(grupo, "vBC")), "valor_icms": dec(txt(grupo, "vICMS"))}
    return {"nota": nota, "itens": [item]}


def ler_nfse(raiz: ET.Element, arq: str) -> dict:
    inf = primeiro(raiz, "infNFSe")
    dps = achar(inf, "DPS", "infDPS")
    val_nota, val_dps = achar(inf, "valores"), achar(dps, "valores")
    serv = achar(dps, "serv", "cServ")
    v_serv = dec(txt(val_dps, "vServPrest", "vServ"))
    cond, incond = dec(txt(val_dps, "vDescCondIncond", "vDescCond")), dec(txt(val_dps, "vDescCondIncond", "vDescIncond"))
    ret, liq = dec(txt(val_nota, "vTotalRet")), dec(txt(val_nota, "vLiq"))
    chave = (inf.get("Id") or "").removeprefix("NFS")
    nota = {"arquivo": arq, "tipo": "NFS-e", "chave": chave, "serie": txt(dps, "serie"), "numero": txt(inf, "nNFSe"), "emissao": txt(dps, "dhEmi")[:10],
            "operacao": "serviço", "emitente": doc_id(achar(inf, "emit")), "emitente_nome": txt(inf, "emit", "xNome"), "destinatario": doc_id(achar(dps, "toma")), "crt": "",
            "valor_nota": v_serv, "cstat": txt(inf, "cStat"), "protocolo": txt(inf, "cStat"), "alertas": []}
    if v_serv - cond - incond - ret != liq:
        nota["alertas"].append(f"valor líquido {br(liq)} difere de serviço − descontos − retidos = {br(v_serv - cond - incond - ret)}")
    trib = achar(val_dps, "trib", "tribMun")
    item = {"chave": chave, "item": "1", "codigo": txt(serv, "cTribNac"), "descricao": txt(serv, "xDescServ"), "ncm": "", "cfop": "serviço " + txt(serv, "cTribNac"),
            "cst_ou_csosn": "ISS retido" if txt(trib, "tpRetISSQN") in ("2", "3") else "ISS não retido", "aliq_icms": txt(val_nota, "pAliqAplic") or txt(trib, "pAliq"),
            "valor_produto": v_serv, "base_icms": dec(txt(val_nota, "vBC")), "valor_icms": dec(txt(val_nota, "vISSQN"))}
    return {"nota": nota, "itens": [item]}


def classificar(raiz: ET.Element) -> str:
    nomes = {local(e) for e in raiz.iter()}
    if "infNFe" in nomes:
        return "nfe"
    if "infCte" in nomes:
        return "cte"
    if "infEvento" in nomes or "retEvento" in nomes:
        return "evento"
    if "infNFSe" in nomes:
        return "nfse"
    if nomes & {"InfNfse", "CompNfse"}:
        return "municipal"
    return "desconhecido"


def gravar(caminho: Path, campos: list[str], linhas: list[dict]) -> None:
    with open(caminho, "x", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for l in linhas:
            w.writerow({k: br(v) if isinstance(v, Decimal) else v for k, v in l.items()})


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--entrada", required=True, type=Path)
    ap.add_argument("--saida", required=True, type=Path)
    a = ap.parse_args()
    arquivos = sorted(p for p in a.entrada.rglob("*") if p.suffix.lower() == ".xml") if a.entrada.is_dir() else [a.entrada]
    if not arquivos:
        print("ERRO: nenhum .xml na entrada", file=sys.stderr)
        sys.exit(1)
    try:
        a.saida.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(f"ERRO: {a.saida} já existe; este programa nunca sobrescreve", file=sys.stderr)
        sys.exit(1)
    notas, itens, eventos, nfse, desconhecidos, erros, duplicadas, vistas = [], [], [], [], [], [], [], {}
    for p in arquivos:
        rotulo = str(p.relative_to(a.entrada)) if a.entrada.is_dir() else p.name
        bruto = p.read_bytes()
        if b"<!DOCTYPE" in bruto[:2048].upper():
            erros.append((rotulo, "DOCTYPE recusado"))
            continue
        try:
            raiz = ET.fromstring(bruto)
        except ET.ParseError as e:
            erros.append((rotulo, f"XML inválido: {e}"))
            continue
        tipo = classificar(raiz)
        if tipo == "evento":
            eventos.append({"arquivo": rotulo, "chave": txt(primeiro(raiz, "infEvento"), "chNFe"), "evento": txt(primeiro(raiz, "detEvento"), "descEvento") or txt(primeiro(raiz, "infEvento"), "tpEvento")})
            continue
        if tipo == "municipal":
            nfse.append(rotulo)
            continue
        if tipo == "desconhecido":
            desconhecidos.append(rotulo)
            continue
        lido = {"nfe": ler_nfe, "cte": ler_cte, "nfse": ler_nfse}[tipo](raiz, rotulo)
        nota = lido["nota"]
        if nota["chave"] in vistas:
            duplicadas.append((rotulo, vistas[nota["chave"]]))
            continue
        vistas[nota["chave"]] = rotulo
        dv = dv_chave_ok(nota["chave"]) if tipo != "nfse" else True
        if dv is False:
            nota["alertas"].append("chave de acesso com dígito verificador errado ou tamanho diferente de 44")
        elif dv is None:
            nota["alertas"].append("chave com letras: dígito verificador não conferido")
        if tipo == "nfse":
            if nota["cstat"] not in ("100", "102", "103", "107"):
                nota["alertas"].append(f"situação {nota['cstat']} fora do leiaute nacional: confira")
        elif not nota["protocolo"]:
            nota["alertas"].append("sem protocolo de autorização no arquivo")
        elif nota["cstat"] != "100":
            nota["alertas"].append(f"situação {nota['cstat']} no protocolo: confira se foi autorizada")
        notas.append(nota)
        itens += lido["itens"]
    canceladas = {e["chave"] for e in eventos if "cancel" in e["evento"].lower()}
    for n in notas:
        n["cancelada"] = "sim" if n["chave"] in canceladas else ""
        n["alertas_txt"] = " | ".join(n["alertas"])
    validas = {n["chave"] for n in notas if not n["cancelada"]}
    resumo: dict[tuple, dict] = defaultdict(lambda: {"itens": 0, "valor_produto": ZERO, "base_icms": ZERO, "valor_icms": ZERO})
    operacao = {n["chave"]: n["operacao"] for n in notas}
    for i in itens:
        if i["chave"] in validas:
            r = resumo[(operacao[i["chave"]], i["cfop"], i["cst_ou_csosn"], i["aliq_icms"])]
            r["itens"] += 1
            for campo in ("valor_produto", "base_icms", "valor_icms"):
                r[campo] += i[campo]
    gravar(a.saida / "notas.csv", ["arquivo", "tipo", "chave", "serie", "numero", "emissao", "operacao", "emitente", "emitente_nome", "destinatario", "crt", "valor_nota", "cstat", "protocolo", "cancelada", "alertas_txt"], notas)
    gravar(a.saida / "itens.csv", ["chave", "item", "codigo", "descricao", "ncm", "cfop", "cst_ou_csosn", "aliq_icms", "valor_produto", "base_icms", "valor_icms"], itens)
    linhas_resumo = [{"operacao": k[0], "cfop": k[1], "cst_ou_csosn": k[2], "aliq_icms": k[3], **v} for k, v in sorted(resumo.items())]
    gravar(a.saida / "resumo-cfop-cst.csv", ["operacao", "cfop", "cst_ou_csosn", "aliq_icms", "itens", "valor_produto", "base_icms", "valor_icms"], linhas_resumo)
    total = sum((n["valor_nota"] for n in notas if not n["cancelada"]), ZERO)
    fecha = len(notas) + len(eventos) + len(duplicadas) + len(nfse) + len(desconhecidos) + len(erros)
    print(f"arquivos lidos: {len(arquivos)}; notas: {len(notas)}; canceladas por evento no lote: {len(canceladas & set(vistas))}; eventos: {len(eventos)}; duplicadas: {len(duplicadas)}; municipais à parte: {len(nfse)}; não reconhecidos: {len(desconhecidos)}; com erro: {len(erros)}")
    print(f"fechamento: {fecha} de {len(arquivos)} arquivos em um grupo só" + ("" if fecha == len(arquivos) else " (NÃO FECHA)"))
    print(f"valor total das notas válidas: {br(total)}; soma por CFOP confere com itens: {sum(r['valor_produto'] for r in resumo.values()) == sum(i['valor_produto'] for i in itens if i['chave'] in validas)}")
    com_alerta = [n for n in notas if n["alertas"]]
    for n in com_alerta[:25]:
        print(f"ALERTA {n['arquivo']}: {n['alertas_txt']}")
    for rot, orig in duplicadas[:10]:
        print(f"DUPLICADA {rot}: mesma chave de {orig}")
    for rot, motivo in erros[:10]:
        print(f"ERRO DE LEITURA {rot}: {motivo}")
    for rot in nfse[:10]:
        print(f"MUNICIPAL À PARTE {rot}: leiaute a mapear")
    for rot in desconhecidos[:10]:
        print(f"NÃO RECONHECIDO {rot}")
    sys.exit(2 if com_alerta or duplicadas or erros or nfse or desconhecidos or fecha != len(arquivos) else 0)


if __name__ == "__main__":
    main()
