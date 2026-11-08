"""OFX para planilha e planilha para OFX, com o saldo como prova.

Uso:
    python -I ofx.py ler --entrada arquivo.ofx --saida tabela.csv [--saldo-inicial 1000,00]
    python -I ofx.py gerar --entrada tabela.csv --saida arquivo.ofx --banco 000 --conta 0000 [--tipo CHECKING] [--aceitar-diferenca]

"gerar" lê o CSV do extrato.py e recusa arquivo com diferença de saldo, salvo com --aceitar-diferenca.
Só lê a entrada. Só grava o arquivo de --saida, que não pode existir. Só biblioteca padrão.
Código de saída: 0 ok; 2 prova não fecha; 1 erro de uso.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


def falha(msg: str) -> None:
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def br(v: Decimal) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def dec_ofx(t: str) -> tuple[Decimal, bool]:
    """Devolve o valor e se veio fora do padrão (vírgula decimal)."""
    s = t.strip()
    fora = "," in s
    if fora:
        s = s.replace(".", "").replace(",", ".")
    try:
        return Decimal(s), fora
    except InvalidOperation:
        raise ValueError(f"valor ilegível no OFX: {t!r}")


def dec_br(t: str) -> Decimal:
    s = t.strip().replace(".", "").replace(",", ".")
    return Decimal(s)


def decodificar(bruto: bytes) -> str:
    cabeca = bruto[:400].decode("ascii", errors="ignore").upper()
    if "CHARSET:1252" in cabeca or "ENCODING:USASCII" in cabeca:
        return bruto.decode("cp1252", errors="replace")
    try:
        return bruto.decode("utf-8-sig")
    except UnicodeDecodeError:
        return bruto.decode("cp1252", errors="replace")


def tag(bloco: str, nome: str) -> str:
    m = re.search(rf"<{nome}>([^<\r\n]*)", bloco, re.I)
    return m.group(1).strip() if m else ""


def data_ofx(t: str) -> str:
    d = t[:8]
    return f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 and d.isdigit() else ""


def ler(a) -> int:
    texto = decodificar(a.entrada.read_bytes())
    blocos = re.findall(r"<STMTTRN>(.*?)</STMTTRN>", texto, re.I | re.S)
    if not blocos:
        falha("nenhum <STMTTRN> encontrado: não é extrato OFX de conta")
    linhas, fora, repetidos, vistos, sinal_estranho = [], 0, [], set(), 0
    for n, b in enumerate(blocos, start=1):
        valor, f = dec_ofx(tag(b, "TRNAMT"))
        fora += f
        tipo = tag(b, "TRNTYPE").upper()
        fitid = tag(b, "FITID")
        if fitid in vistos:
            repetidos.append(fitid)
        vistos.add(fitid)
        if (tipo == "CREDIT" and valor < 0) or (tipo == "DEBIT" and valor > 0):
            sinal_estranho += 1
        linhas.append([n, data_ofx(tag(b, "DTPOSTED")), tag(b, "MEMO") or tag(b, "NAME"), tag(b, "CHECKNUM"), valor, tipo, fitid])
    soma = sum((l[4] for l in linhas), Decimal("0"))
    try:
        arq = open(a.saida, "x", encoding="utf-8-sig", newline="")
    except FileExistsError:
        falha(f"{a.saida} já existe; este programa nunca sobrescreve")
    with arq:
        w = csv.writer(arq, delimiter=";")
        w.writerow(["ordem", "data", "descricao", "referencia", "valor", "tipo_ofx", "fitid"])
        for l in linhas:
            w.writerow([*l[:4], br(l[4]), *l[5:]])
    print(f"movimentos: {len(linhas)}; soma: {br(soma)}; período no arquivo: {data_ofx(tag(texto, 'DTSTART'))} a {data_ofx(tag(texto, 'DTEND'))}")
    print(f"conta: {'presente' if tag(texto, 'ACCTID') else 'ausente'} (não repetida aqui); moeda: {tag(texto, 'CURDEF')}")
    if fora:
        print(f"AVISO: {fora} valor(es) com vírgula decimal, fora da especificação; convertidos")
    if sinal_estranho:
        print(f"AVISO: {sinal_estranho} movimento(s) com TRNTYPE que contraria o sinal; vale o sinal de TRNAMT")
    if repetidos:
        print(f"AVISO: FITID repetido em {len(repetidos)} movimento(s): pode ser arquivo importado duas vezes")
    saldo = tag(texto, "BALAMT")
    if not saldo:
        print("PROVA INCOMPLETA: arquivo sem LEDGERBAL")
        return 2
    final, _ = dec_ofx(saldo)
    print(f"saldo final informado: {br(final)} em {data_ofx(tag(texto, 'DTASOF'))}")
    if a.saldo_inicial is None:
        print(f"PROVA INCOMPLETA: informe --saldo-inicial; o saldo inicial deveria ser {br(final - soma)}")
        return 2
    inicial = dec_br(a.saldo_inicial)
    dif = inicial + soma - final
    print(("RESULTADO: SALDO BATE" if dif == 0 else f"NÃO FECHA: saldo inicial + movimentos − saldo final = {br(dif)}"))
    return 0 if dif == 0 else 2


def limpar(t: str) -> str:
    return re.sub(r"[<>&\r\n]", " ", t).strip()[:255]


def gerar(a) -> int:
    with open(a.entrada, encoding="utf-8-sig", newline="") as f:
        regs = list(csv.DictReader(f, delimiter=";"))
    movs = [r for r in regs if r.get("tipo") == "movimento"]
    if not movs:
        falha("o CSV não traz linhas de movimento do extrato.py")
    com_dif = [r for r in movs if r.get("diferenca") not in ("", "0,00", None)]
    if com_dif and not a.aceitar_diferenca:
        print(f"RECUSADO: {len(com_dif)} linha(s) com diferença de saldo; corrija o formato do banco antes de gerar o OFX")
        return 2
    finais = [r for r in regs if r.get("tipo") == "saldo_final"]
    datas = sorted(r["data"] for r in movs)
    compacto = lambda d: d.replace("-", "")
    corpo, soma = [], Decimal("0")
    for n, r in enumerate(movs, start=1):
        valor = dec_br(r["valor"])
        soma += valor
        chave = f"{r['data']}|{r['valor']}|{r['descricao']}|{n}"
        fitid = hashlib.sha1(chave.encode("utf-8")).hexdigest()[:20]
        ref = limpar(r.get("referencia", ""))
        corpo.append("<STMTTRN>\n<TRNTYPE>" + ("CREDIT" if valor >= 0 else "DEBIT") + f"\n<DTPOSTED>{compacto(r['data'])}\n<TRNAMT>{valor:.2f}\n<FITID>{fitid}\n"
                     + (f"<CHECKNUM>{ref}\n" if ref else "") + f"<MEMO>{limpar(r['descricao'])}\n</STMTTRN>")
    saldo = f"<LEDGERBAL>\n<BALAMT>{dec_br(finais[0]['saldo_impresso']):.2f}\n<DTASOF>{compacto(datas[-1])}\n</LEDGERBAL>\n" if finais else ""
    cabecalho = "OFXHEADER:100\nDATA:OFXSGML\nVERSION:102\nSECURITY:NONE\nENCODING:USASCII\nCHARSET:1252\nCOMPRESSION:NONE\nOLDFILEUID:NONE\nNEWFILEUID:NONE\n\n"
    texto = (cabecalho + "<OFX>\n<SIGNONMSGSRSV1>\n<SONRS>\n<STATUS>\n<CODE>0\n<SEVERITY>INFO\n</STATUS>\n"
             f"<DTSERVER>{compacto(datas[-1])}\n<LANGUAGE>POR\n</SONRS>\n</SIGNONMSGSRSV1>\n<BANKMSGSRSV1>\n<STMTTRNRS>\n<TRNUID>1\n<STATUS>\n<CODE>0\n<SEVERITY>INFO\n</STATUS>\n"
             f"<STMTRS>\n<CURDEF>BRL\n<BANKACCTFROM>\n<BANKID>{a.banco}\n<ACCTID>{a.conta}\n<ACCTTYPE>{a.tipo}\n</BANKACCTFROM>\n<BANKTRANLIST>\n"
             f"<DTSTART>{compacto(datas[0])}\n<DTEND>{compacto(datas[-1])}\n" + "\n".join(corpo) + "\n</BANKTRANLIST>\n" + saldo
             + "</STMTRS>\n</STMTTRNRS>\n</BANKMSGSRSV1>\n</OFX>\n")
    try:
        arq = open(a.saida, "x", encoding="cp1252", errors="replace", newline="")
    except FileExistsError:
        falha(f"{a.saida} já existe; este programa nunca sobrescreve")
    with arq:
        arq.write(texto)
    print(f"movimentos: {len(movs)}; soma: {br(soma)}; arquivo gravado: {a.saida}")
    if com_dif:
        print(f"AVISO: gerado com {len(com_dif)} linha(s) com diferença, por pedido explícito")
    print("Confira importando num ambiente de teste do sistema contábil; o cabeçalho segue o padrão SGML 1.0x.")
    return 0


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("ler")
    p1.add_argument("--entrada", required=True, type=Path)
    p1.add_argument("--saida", required=True, type=Path)
    p1.add_argument("--saldo-inicial", dest="saldo_inicial")
    p2 = sub.add_parser("gerar")
    p2.add_argument("--entrada", required=True, type=Path)
    p2.add_argument("--saida", required=True, type=Path)
    p2.add_argument("--banco", required=True)
    p2.add_argument("--conta", required=True)
    p2.add_argument("--tipo", default="CHECKING")
    p2.add_argument("--aceitar-diferenca", action="store_true")
    a = ap.parse_args()
    try:
        sys.exit(ler(a) if a.cmd == "ler" else gerar(a))
    except ValueError as e:
        falha(str(e))


if __name__ == "__main__":
    main()
