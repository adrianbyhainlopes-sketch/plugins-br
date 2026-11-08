"""Build dos plugins: bloco da casa, cópias de compartilhado/, créditos e checagens.

Uso, a partir da raiz do repositório:
    python -I ferramentas/montar.py              monta e confere
    python -I ferramentas/montar.py --conferir   só confere; falha se algo estiver desatualizado
    python -I ferramentas/montar.py --zip        monta, confere e gera dist/<plugin>-<versão>.zip

Só biblioteca padrão. Lê e escreve apenas dentro do repositório. Não usa rede.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import tomllib
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLUGINS = RAIZ / "plugins"
COMPARTILHADO = RAIZ / "compartilhado"
CREDITOS = RAIZ / "creditos"
TERMOS_PROIBIDOS = RAIZ / "pessoal" / "infra" / "publicacao-termos-proibidos.txt"
MARKETPLACE = RAIZ / ".claude-plugin" / "marketplace.json"
DIST = RAIZ / "dist"

CASA_INI = "<!-- casa:inicio (gerado de compartilhado/casa.md pelo ferramentas/montar.py; não edite aqui) -->"
CASA_FIM = "<!-- casa:fim -->"
CASA_RE = re.compile(r"<!-- casa:inicio.*?-->.*?<!-- casa:fim -->", re.S)
CRED_INI = "<!-- creditos:inicio (gerado de creditos/*.csv pelo ferramentas/montar.py) -->"
CRED_FIM = "<!-- creditos:fim -->"
CRED_RE = re.compile(r"<!-- creditos:inicio.*?-->.*?<!-- creditos:fim -->", re.S)
CABECALHO_COPIA = "<!-- cópia gerada de compartilhado/{nome} pelo ferramentas/montar.py; edite a fonte, não esta cópia -->\n\n"

TRACOS = {"‒": "traço numérico", "–": "meia-risca", "—": "travessão", "―": "barra horizontal"}
NOME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PALAVRAS_RESERVADAS = ("anthropic", "claude")
PREFIXOS_RESERVADOS = ("claude-", "anthropic-", "anthropics-", "cc-plugin-")
CAMPOS_SKILL = {"name", "description"}
LIMITE_DESCRICAO = 1024
LINHAS_AVISO, LINHAS_MAX = 300, 500
USOS_VALIDOS = {"adaptado", "ideia", "do zero"}
# Agentes (conferido em code.claude.com/docs/en/sub-agents, 08/11/2026; fase4/conferencias.md, item 30).
PLUGINS_COM_AGENTES = {"engenharia", "seguranca-infra"}
CAMPOS_AGENTE = {
    "name", "description", "tools", "disallowedTools", "model", "maxTurns", "autoCompactWindow",
    "skills", "memory", "background", "omitClaudeMd", "effort", "isolation", "color", "experimental",
}
CAMPOS_AGENTE_IGNORADOS_EM_PLUGIN = {"hooks", "mcpServers", "permissionMode", "initialPrompt"}
MODELOS_AGENTE = {"sonnet", "opus", "haiku", "fable", "inherit"}
# A arquitetura pede agentes só de leitura: nada que escreva arquivo ou rode shell.
FERRAMENTAS_DE_ESCRITA = {"Write", "Edit", "NotebookEdit", "Bash", "PowerShell"}
EXTENSOES_TEXTO = {".md", ".json", ".toml", ".csv", ".txt"}


class Relatorio:
    def __init__(self) -> None:
        self.erros: list[str] = []
        self.avisos: list[str] = []
        self.mudancas: list[str] = []

    def erro(self, msg: str) -> None:
        self.erros.append(msg)

    def aviso(self, msg: str) -> None:
        self.avisos.append(msg)


def rel(p: Path) -> str:
    return p.relative_to(RAIZ).as_posix()


def ler(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def gravar_se_mudou(p: Path, conteudo: str, conferir: bool, r: Relatorio) -> None:
    atual = ler(p) if p.exists() else None
    if atual == conteudo:
        return
    if conferir:
        r.erro(f"{rel(p)}: desatualizado (rode o build sem --conferir)")
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(conteudo, encoding="utf-8", newline="\n")
    r.mudancas.append(rel(p))


# ---------- créditos ----------

def carregar_creditos(r: Relatorio) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    with open(CREDITOS / "fontes.csv", encoding="utf-8", newline="") as f:
        fontes = {linha["id"]: linha for linha in csv.DictReader(f)}
    with open(CREDITOS / "uso.csv", encoding="utf-8", newline="") as f:
        usos = list(csv.DictReader(f))
    for n, u in enumerate(usos, start=2):
        if u["uso"] not in USOS_VALIDOS:
            r.erro(f"creditos/uso.csv:{n}: uso '{u['uso']}' inválido (use {sorted(USOS_VALIDOS)})")
        if u["fonte"] and u["fonte"] not in fontes:
            r.erro(f"creditos/uso.csv:{n}: fonte '{u['fonte']}' não está em fontes.csv")
        if u["uso"] != "do zero" and not u["fonte"]:
            r.erro(f"creditos/uso.csv:{n}: uso '{u['uso']}' sem fonte")
        if u["plugin"] == "compartilhado" and not ((COMPARTILHADO / f"{u['skill']}.md").exists() or (COMPARTILHADO / u["skill"]).is_file()):
            r.erro(f"creditos/uso.csv:{n}: compartilhado/{u['skill']}.md não existe")
    for i in sorted(set(fontes) - {u["fonte"] for u in usos}):
        r.aviso(f"creditos/fontes.csv: fonte '{i}' não é usada por nenhuma skill")
    return fontes, usos


def nome_fonte(f: dict[str, str]) -> str:
    repo = f["repositorio"].removeprefix("https://github.com/")
    if f["subpasta"]:
        repo += f"/{f['subpasta']}"
    return f"{repo} ({f['licenca']})"


def bloco_creditos(plugin: str, skill: str, fontes: dict, usos: list) -> str:
    itens = [u for u in usos if u["plugin"] == plugin and u["skill"] == skill]
    nomes: list[str] = []
    for u in itens:
        if u["fonte"]:
            n = nome_fonte(fontes[u["fonte"]])
            if n not in nomes:
                nomes.append(n)
    partes = []
    if nomes:
        partes.append("Adaptado de " + "; ".join(nomes) + ".")
    if any(u["uso"] == "do zero" for u in itens):
        partes.append("Partes escritas do zero.")
    if any(u["fonte"] and fontes[u["fonte"]]["licenca"].startswith("Apache") for u in itens):
        partes.append("Mudanças em relação às fontes: traduzido, condensado e corrigido; nenhum script copiado.")
    partes.append("Versões e licenças: CREDITS.md do repositório.")
    return "<!-- " + " ".join(partes) + " -->"


def gerar_credits_md(fontes: dict, usos: list) -> str:
    out = [
        "# Créditos",
        "",
        "Gerado pelo `ferramentas/montar.py` a partir de `creditos/fontes.csv` e `creditos/uso.csv`. Não edite à mão.",
        "",
        "Licença deste projeto: Apache-2.0. As fontes abaixo são de terceiros, cada uma com a sua licença. Os textos adaptados foram traduzidos, condensados e corrigidos; nenhum script, hook ou instalador das fontes foi copiado.",
        "",
    ]
    grupos: dict[tuple[str, str], list] = {}
    for u in usos:
        grupos.setdefault((u["plugin"], u["skill"]), []).append(u)
    plugins = sorted({p for p, _ in grupos}, key=lambda p: (p != "compartilhado", p))
    for p in plugins:
        out += [f"## {'Peças comuns (compartilhado/)' if p == 'compartilhado' else 'Plugin ' + p}", ""]
        for (pp, s), itens in grupos.items():
            if pp != p:
                continue
            out += [f"### {s}", "", "| fonte | repositório | versão (sha) | licença | uso | mudanças |", "|---|---|---|---|---|---|"]
            for u in itens:
                if u["fonte"]:
                    f = fontes[u["fonte"]]
                    repo = f["repositorio"] + (f" (`{f['subpasta']}`)" if f["subpasta"] else "")
                    out.append(f"| {u['fonte']} | {repo} | {f['sha']} | {f['licenca']} | {u['uso']} | {u['mudancas']} |")
                else:
                    out.append(f"| (nenhuma) | | | | {u['uso']} | {u['mudancas']} |")
            out.append("")
    cadeias = [(i, f["cadeia"]) for i, f in fontes.items() if f["cadeia"]]
    if cadeias:
        out += ["## Cadeias de crédito e restrições", ""]
        out += [f"- **{i}:** {c}" for i, c in cadeias]
        out.append("")
    return "\n".join(out)


# ---------- skills ----------

def frontmatter(texto: str, caminho: str, r: Relatorio) -> dict[str, str]:
    linhas = texto.split("\n")
    if not linhas or linhas[0].strip() != "---":
        r.erro(f"{caminho}: frontmatter ausente (a linha 1 tem de ser ---)")
        return {}
    try:
        fim = linhas.index("---", 1)
    except ValueError:
        r.erro(f"{caminho}: frontmatter sem o --- de fechamento")
        return {}
    campos: dict[str, str] = {}
    for n, linha in enumerate(linhas[1:fim], start=2):
        if not linha.strip():
            continue
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", linha)
        if not m:
            r.erro(f"{caminho}:{n}: linha de frontmatter inválida (um campo por linha, sem quebra)")
            continue
        chave, valor = m.group(1), m.group(2).strip()
        if chave in campos:
            r.erro(f"{caminho}:{n}: campo '{chave}' repetido")
        if valor.startswith('"'):
            if len(valor) < 2 or not valor.endswith('"'):
                r.erro(f"{caminho}:{n}: aspas sem fechamento")
                continue
            miolo = valor[1:-1]
            if re.search(r'(?<!\\)"', miolo):
                r.erro(f"{caminho}:{n}: aspas duplas dentro do valor; use aspas simples")
            valor = miolo.replace('\\"', '"')
        elif ": " in valor or " #" in valor:
            r.erro(f"{caminho}:{n}: valor com ': ' ou ' #' precisa de aspas duplas")
        campos[chave] = valor
    return campos


def conferir_skill(dir_skill: Path, texto: str, r: Relatorio) -> None:
    caminho = rel(dir_skill / "SKILL.md")
    campos = frontmatter(texto, caminho, r)
    extras = set(campos) - CAMPOS_SKILL
    if extras:
        r.erro(f"{caminho}: campos que o chat recusa: {sorted(extras)} (só name e description)")
    nome = campos.get("name", "")
    if nome != dir_skill.name:
        r.erro(f"{caminho}: name '{nome}' diferente da pasta '{dir_skill.name}'")
    if not NOME_RE.match(nome) or len(nome) > 64:
        r.erro(f"{caminho}: name inválido (minúsculas, números e hífen, até 64)")
    if any(p in nome for p in PALAVRAS_RESERVADAS):
        r.erro(f"{caminho}: name contém palavra reservada")
    desc = campos.get("description", "")
    if not desc:
        r.erro(f"{caminho}: description vazia")
    elif len(desc) > LIMITE_DESCRICAO:
        r.erro(f"{caminho}: description com {len(desc)} caracteres (máximo {LIMITE_DESCRICAO})")
    if "<" in desc or ">" in desc:
        r.erro(f"{caminho}: description com < ou >")
    n_linhas = texto.count("\n") + 1
    if n_linhas > LINHAS_MAX:
        r.erro(f"{caminho}: {n_linhas} linhas (máximo {LINHAS_MAX})")
    elif n_linhas > LINHAS_AVISO:
        r.aviso(f"{caminho}: {n_linhas} linhas (alvo até {LINHAS_AVISO})")
    sem_blocos = CRED_RE.sub("", CASA_RE.sub("", texto))
    citadas = set(re.findall(r"referencias/([A-Za-z0-9_./-]+\.md)", sem_blocos))
    pasta = dir_skill / "referencias"
    existentes = {p.relative_to(pasta).as_posix() for p in pasta.rglob("*.md")} if pasta.exists() else set()
    for c in sorted(citadas - existentes):
        r.erro(f"{caminho}: cita referencias/{c}, que não existe")
    for o in sorted(existentes - citadas):
        r.aviso(f"{caminho}: referencias/{o} existe mas não é citada no SKILL.md")


def conferir_agentes(dir_plugin: Path, usos: list[dict[str, str]], r: Relatorio) -> int:
    """Confere plugins/<plugin>/agents/*.md: só nos plugins permitidos, campos válidos, só leitura, créditos."""
    pasta = dir_plugin / "agents"
    if not pasta.exists():
        return 0
    arquivos = sorted(p for p in pasta.rglob("*") if p.is_file())
    if dir_plugin.name not in PLUGINS_COM_AGENTES:
        r.erro(f"{rel(pasta)}: agentes só em {sorted(PLUGINS_COM_AGENTES)} (passagem da fase 4)")
        return 0
    nomes: dict[str, str] = {}
    for arq in arquivos:
        caminho = rel(arq)
        if arq.suffix != ".md":
            r.erro(f"{caminho}: em agents/ só arquivos .md")
            continue
        texto = ler(arq)
        campos = frontmatter(texto, caminho, r)
        if not campos:
            continue
        ignorados = set(campos) & CAMPOS_AGENTE_IGNORADOS_EM_PLUGIN
        if ignorados:
            r.erro(f"{caminho}: campos que o Claude Code ignora em agente de plugin: {sorted(ignorados)}")
        desconhecidos = set(campos) - CAMPOS_AGENTE - CAMPOS_AGENTE_IGNORADOS_EM_PLUGIN
        if desconhecidos:
            r.erro(f"{caminho}: campos desconhecidos (seriam ignorados em silêncio): {sorted(desconhecidos)}")
        nome = campos.get("name", "")
        if not nome:
            r.erro(f"{caminho}: falta 'name'")
        else:
            if not NOME_RE.match(nome) or len(nome) > 64:
                r.erro(f"{caminho}: name '{nome}' inválido (minúsculas, números e hífen, até 64)")
            if nome != arq.stem:
                r.erro(f"{caminho}: name '{nome}' diferente do nome do arquivo")
            if nome in nomes:
                r.erro(f"{caminho}: name '{nome}' repetido (também em {nomes[nome]})")
            nomes[nome] = caminho
        desc = campos.get("description", "")
        if not desc:
            r.erro(f"{caminho}: description vazia")
        elif len(desc) > LIMITE_DESCRICAO:
            r.erro(f"{caminho}: description com {len(desc)} caracteres (máximo {LIMITE_DESCRICAO})")
        ferramentas = {t.strip() for t in campos.get("tools", "").split(",") if t.strip()}
        if not ferramentas:
            r.erro(f"{caminho}: falta 'tools' (sem a lista, o agente herda todas as ferramentas, inclusive as de escrita)")
        escrita = ferramentas & FERRAMENTAS_DE_ESCRITA
        if escrita:
            r.erro(f"{caminho}: ferramentas de escrita ou shell {sorted(escrita)} (os agentes do projeto são só de leitura)")
        modelo = campos.get("model")
        if modelo is not None and modelo not in MODELOS_AGENTE and not modelo.startswith("claude-"):
            r.erro(f"{caminho}: model '{modelo}' inválido (use {sorted(MODELOS_AGENTE)} ou um ID completo)")
        partes = texto.split("\n---", 1)
        if len(partes) < 2 or not partes[1].strip("-\n "):
            r.erro(f"{caminho}: agente sem corpo (instruções) depois do frontmatter")
        if nome and not any(u["plugin"] == dir_plugin.name and u["skill"] == f"agents/{nome}" for u in usos):
            r.erro(f"creditos/uso.csv: nenhuma linha para {dir_plugin.name}/agents/{nome}")
    return len(nomes)


def injetar(texto: str, padrao: re.Pattern, ini: str, fim: str, bloco: str, caminho: str, r: Relatorio) -> str | None:
    if not padrao.search(texto):
        r.erro(f"{caminho}: marcadores {ini.split(' ')[1]} ausentes")
        return None
    novo_bloco = f"{ini}\n{bloco.rstrip()}\n{fim}"
    return padrao.sub(lambda _m: novo_bloco, texto, count=1)


# ---------- plugins e marketplace ----------

def conferir_plugin(dir_plugin: Path, r: Relatorio) -> dict | None:
    pj = dir_plugin / ".claude-plugin" / "plugin.json"
    if not pj.exists():
        r.erro(f"{rel(dir_plugin)}: falta .claude-plugin/plugin.json")
        return None
    try:
        dados = json.loads(ler(pj))
    except json.JSONDecodeError as e:
        r.erro(f"{rel(pj)}: JSON inválido ({e})")
        return None
    nome = dados.get("name", "")
    if nome != dir_plugin.name:
        r.erro(f"{rel(pj)}: name '{nome}' diferente da pasta")
    if not NOME_RE.match(nome) or nome.startswith(PREFIXOS_RESERVADOS) or nome in {"claude", "anthropic", "claude-code"}:
        r.erro(f"{rel(pj)}: name inválido ou reservado")
    for campo in ("version", "description", "license"):
        if not dados.get(campo):
            r.aviso(f"{rel(pj)}: falta '{campo}'")
    if not (dados.get("author") or {}).get("name"):
        r.aviso(f"{rel(pj)}: falta author.name")
    if (dir_plugin / "bin").exists():
        r.erro(f"{rel(dir_plugin)}: pasta bin/ impede a instalação no claude.ai e no Cowork")
    for proibida, motivo in (("hooks", "nenhum hook ativo (R-020); hook opcional mora em extras/"), ("commands", "nenhum comando (o chat transforma comando em skill)")):
        if (dir_plugin / proibida).exists():
            r.erro(f"{rel(dir_plugin)}: pasta {proibida}/ proibida: {motivo}")
    if (dir_plugin / "CLAUDE.md").exists():
        r.aviso(f"{rel(dir_plugin)}: CLAUDE.md na raiz do plugin não é carregado")
    if not (dir_plugin / "skills").is_dir():
        r.erro(f"{rel(dir_plugin)}: falta a pasta skills/")
        return None
    return dados


def conferir_marketplace(plugins: dict[str, dict], r: Relatorio) -> None:
    if not MARKETPLACE.exists():
        r.erro(".claude-plugin/marketplace.json não existe")
        return
    dados = json.loads(ler(MARKETPLACE))
    entradas = {p.get("name"): p for p in dados.get("plugins", [])}
    for nome in plugins:
        e = entradas.get(nome)
        if not e:
            r.erro(f"marketplace.json: falta o plugin '{nome}'")
        elif e.get("source") != f"./plugins/{nome}":
            r.erro(f"marketplace.json: source de '{nome}' deveria ser ./plugins/{nome}")
    for nome in set(entradas) - set(plugins):
        r.erro(f"marketplace.json: '{nome}' não existe em plugins/")


# ---------- textos públicos ----------

def carregar_termos(r: Relatorio) -> list[str]:
    if not TERMOS_PROIBIDOS.exists():
        r.aviso("pessoal/infra/publicacao-termos-proibidos.txt não existe: termos internos não conferidos")
        return []
    termos = []
    for linha in ler(TERMOS_PROIBIDOS).splitlines():
        t = linha.strip()
        if t and not t.startswith("#"):
            termos.append(t)
    return termos


def arquivos_publicos() -> list[Path]:
    lista = []
    for base in (PLUGINS, COMPARTILHADO, CREDITOS, RAIZ / ".claude-plugin"):
        lista += [p for p in base.rglob("*") if p.is_file() and p.suffix in EXTENSOES_TEXTO]
    if (RAIZ / "CREDITS.md").exists():
        lista.append(RAIZ / "CREDITS.md")
    return sorted(lista)


def conferir_textos(r: Relatorio) -> None:
    termos = carregar_termos(r)
    # Sensível a maiúsculas: os termos são nomes próprios, e alguns também são palavras comuns em minúscula.
    padroes = [(t, re.compile(rf"(?<!\w){re.escape(t)}(?!\w)")) for t in termos]
    for p in arquivos_publicos():
        for n, linha in enumerate(ler(p).splitlines(), start=1):
            for ch, nome in TRACOS.items():
                if ch in linha:
                    r.erro(f"{rel(p)}:{n}: {nome} no texto")
            for t, padrao in padroes:
                if padrao.search(linha):
                    r.erro(f"{rel(p)}:{n}: termo interno '{t}' em arquivo público")


# ---------- pacote ----------

def empacotar(plugins: dict[str, dict], r: Relatorio) -> None:
    DIST.mkdir(exist_ok=True)
    for nome, dados in plugins.items():
        destino = DIST / f"{nome}-{dados.get('version', '0')}.zip"
        base = PLUGINS / nome
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
            for p in sorted(base.rglob("*")):
                if p.is_file() and "__pycache__" not in p.parts:
                    z.write(p, f"{nome}/{p.relative_to(base).as_posix()}")
        r.mudancas.append(rel(destino))


# ---------- principal ----------

def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    conferir = "--conferir" in argv
    r = Relatorio()
    fontes, usos = carregar_creditos(r)
    casa = ler(COMPARTILHADO / "casa.md")
    copias = tomllib.loads(ler(RAIZ / "ferramentas" / "copias.toml")).get("copias", {})
    plugins: dict[str, dict] = {}
    vistas: set[str] = set()
    n_agentes = 0

    for dir_plugin in sorted(p for p in PLUGINS.iterdir() if p.is_dir()):
        dados = conferir_plugin(dir_plugin, r)
        if dados is None:
            continue
        plugins[dir_plugin.name] = dados
        for dir_skill in sorted(p for p in (dir_plugin / "skills").iterdir() if p.is_dir()):
            chave = f"{dir_plugin.name}/{dir_skill.name}"
            vistas.add(chave)
            arq = dir_skill / "SKILL.md"
            if not arq.exists():
                r.erro(f"{rel(dir_skill)}: falta SKILL.md")
                continue
            texto = ler(arq)
            novo = injetar(texto, CASA_RE, CASA_INI, CASA_FIM, casa, rel(arq), r)
            if novo is not None:
                cred = bloco_creditos(dir_plugin.name, dir_skill.name, fontes, usos)
                novo = injetar(novo, CRED_RE, CRED_INI, CRED_FIM, cred, rel(arq), r)
            if novo is not None:
                gravar_se_mudou(arq, novo, conferir, r)
                texto = novo
            esperadas = copias.get(chave)
            if esperadas is None:
                r.aviso(f"ferramentas/copias.toml: falta a entrada \"{chave}\"")
                esperadas = []
            for nome in esperadas:
                fonte = COMPARTILHADO / nome
                if not fonte.exists():
                    r.erro(f"ferramentas/copias.toml: compartilhado/{nome} não existe")
                    continue
                # CSV não leva cabeçalho de comentário (quebraria a leitura da tabela); a conferência de cópia vale igual.
                cabecalho = "" if fonte.suffix == ".csv" else CABECALHO_COPIA.format(nome=nome)
                gravar_se_mudou(dir_skill / "referencias" / nome, cabecalho + ler(fonte), conferir, r)
            pasta = dir_skill / "referencias"
            if pasta.exists():
                for p in pasta.rglob("*.md"):
                    if ler(p).startswith("<!-- cópia gerada de compartilhado/") and p.relative_to(pasta).as_posix() not in esperadas:
                        r.erro(f"{rel(p)}: cópia gerada que não está no copias.toml (apague ou liste)")
            if not any(u["plugin"] == dir_plugin.name and u["skill"] == dir_skill.name for u in usos):
                r.erro(f"creditos/uso.csv: nenhuma linha para {chave}")
            conferir_skill(dir_skill, texto, r)
        n_agentes += conferir_agentes(dir_plugin, usos, r)

    for chave in copias:
        if chave not in vistas:
            r.erro(f"ferramentas/copias.toml: \"{chave}\" não existe em plugins/")
    conferir_marketplace(plugins, r)
    gravar_se_mudou(RAIZ / "CREDITS.md", gerar_credits_md(fontes, usos), conferir, r)
    conferir_textos(r)
    if "--zip" in argv and not r.erros:
        empacotar(plugins, r)

    for titulo, itens in (("Gravado", r.mudancas), ("Avisos", r.avisos), ("Erros", r.erros)):
        if itens:
            print(f"{titulo} ({len(itens)}):")
            for i in itens:
                print(f"  {i}")
    n_skills = len(vistas)
    estado = "FALHOU" if r.erros else "ok"
    print(f"Resultado: {estado}. {len(plugins)} plugin(s), {n_skills} skill(s), {n_agentes} agente(s), {len(r.erros)} erro(s), {len(r.avisos)} aviso(s).")
    return 1 if r.erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
