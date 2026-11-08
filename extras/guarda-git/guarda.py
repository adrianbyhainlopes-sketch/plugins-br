#!/usr/bin/env python3
"""Guarda opcional de git e de comandos destrutivos (hook PreToolUse do Claude Code).

Lê do stdin o JSON do hook, olha o comando das ferramentas Bash e PowerShell e
sai com um destes dois códigos, e nenhum outro:
  0  deixa seguir (sem saída nenhuma: a decisão volta ao fluxo normal de permissões);
  2  bloqueia, com o motivo no stderr.

O código 1 não bloqueia no Claude Code. Por isso toda falha aqui dentro vira
código 2 de propósito, e o processo termina com os._exit para que nem o
encerramento do interpretador consiga trocar o código.

Decisões para entrada estranha:
  JSON quebrado, stdin vazio, não é objeto ........ bloqueia
  tool_name ausente ou que não é texto ............ bloqueia
  Bash ou PowerShell sem tool_input.command texto . bloqueia
  command vazio ou só com espaços ................. passa (nada a executar)
  outra ferramenta qualquer ....................... passa (fora do escopo)
  erro interno, aninhamento demais ................ bloqueia

O método é ler o comando como o shell leria: separa em comandos simples e só
olha a palavra na posição de comando. Texto entre aspas é dado, então um echo
ou uma mensagem de commit que cita um comando perigoso passa. Já $(...), crase,
bash -c, powershell -Command, cmd /c, eval e Invoke-Expression com texto literal
são abertos e lidos.

É rede de segurança contra engano, não sandbox: o README lista o que escapa.
Só biblioteca padrão; roda com python -I.
"""
import base64
import json
import os
import re
import sys

PASSA = 0
BLOQUEIA = 2

BASH = "bash"
PS = "powershell"
CMD = "cmd"
FERRAMENTAS = {"Bash": BASH, "PowerShell": PS}

PROFUNDIDADE_MAXIMA = 12

# O PowerShell aceita aspas curvas como aspas e traços tipográficos como hífen.
TRACOS = "".join(map(chr, (0x2013, 0x2014, 0x2015)))
ASPAS_CURVAS = str.maketrans({
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"',
})

RESERVADAS = {
    "if", "then", "elif", "elseif", "else", "while", "until", "do", "done", "fi",
    "for", "foreach", "case", "esac", "select", "switch", "try", "catch", "finally",
    "!", "{", "}", "time", "coproc",
}

# Programas que só repassam o comando seguinte, e quais opções deles recebem valor.
EMBRULHOS = {
    "sudo": {"-u", "-g", "-h", "-p", "-C", "-r", "-t", "-T", "-U", "-D", "-R", "--user", "--group"},
    "doas": {"-u", "-C"},
    "env": {"-u", "-C", "--unset", "--chdir"},
    "command": set(),
    "builtin": set(),
    "exec": {"-a"},
    "nohup": set(),
    "setsid": set(),
    "stdbuf": {"-i", "-o", "-e"},
    "nice": {"-n", "--adjustment"},
    "ionice": {"-c", "-n"},
    "timeout": {"-k", "-s", "--kill-after", "--signal"},
    "xargs": {"-I", "-n", "-P", "-L", "-s", "-d", "-E", "-a"},
    "winpty": set(),
    "busybox": set(),
    "wsl": {"-d", "-u", "--distribution", "--user", "--cd"},
    "npx": {"-p", "--package", "-c", "--call"},
    "bunx": set(),
}

SHELLS_POSIX = {"bash", "sh", "zsh", "dash", "ksh", "ash"}
SHELLS_PS = {"powershell", "pwsh"}
AVALIADORES_PS = {"iex", "invoke-expression"}
BAIXADORES = {"curl", "wget", "iwr", "irm", "invoke-webrequest", "invoke-restmethod"}
EMISSORES = {"echo", "printf", "write-output", "write"}

FAMILIA_APAGAR = {"rm", "ri", "remove-item", "del", "erase", "rd", "rmdir"}
LISTADORES = {"get-childitem", "gci", "ls", "dir"}
CLIENTES_SQL = {"psql", "mysql", "mariadb", "sqlite3", "sqlcmd", "osql", "isql", "pgcli", "mycli", "litecli", "duckdb"}
INDIRETOS_SQL = {"docker", "docker-compose", "podman", "kubectl", "ssh"}
DISCO_SEMPRE = {"format-volume", "clear-disk", "diskpart"}

GIT_GLOBAIS_COM_VALOR = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env"}

ATRIBUICAO = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\+?=")
ATRIBUICAO_PS = re.compile(r"^\$[\w:.\[\]]+=(.+)$")
HERE_STRING = re.compile(r"@(['\"])[ \t]*\r?\n")
UNIDADE = re.compile(r"^[a-z]:[\\/]?$", re.I)
SQL_DESTRUTIVO = re.compile(
    r"\bdrop\s+(table|database|schema|view|materialized\s+view|index|sequence|function"
    r"|procedure|role|user|type|extension|trigger|policy|owned|column)\b"
    r"|\btruncate\s+(table\s+|only\s+)?[\w\"`\[]",
    re.I,
)
SQL_APAGA = re.compile(r"\bdelete\s+from\b", re.I)
SQL_ALTERA = re.compile(r"\bupdate\s+\S+\s+set\b", re.I)
SQL_WHERE = re.compile(r"\bwhere\b", re.I)


class Bloqueio(Exception):
    """Levantada com o motivo quando um comando deve ser barrado."""


class Comando:
    """Um comando simples: palavras, textos que recebe na entrada e o estágio anterior do pipe."""

    __slots__ = ("argv", "entrada", "anterior")

    def __init__(self, anterior=None):
        self.argv = []
        self.entrada = []
        self.anterior = anterior


class Leitor:
    """Separa o texto em comandos simples, seguindo as regras de aspas de cada shell."""

    def __init__(self, texto, dialeto):
        self.t = texto
        self.n = len(texto)
        self.i = 0
        self.d = dialeto
        self.esc = {BASH: "\\", PS: "`", CMD: "^"}[dialeto]
        self.comandos = []
        self.pendentes = []

    def ler(self, fecho=None):
        """Lê até o fecho sem aspas (ou até o fim) e guarda os comandos encontrados."""
        t, d = self.t, self.d
        atual = Comando()
        palavra = None
        destino = "argv"

        def fecha_palavra():
            nonlocal palavra, destino
            if palavra is None:
                return
            if d == PS and palavra[:1] in TRACOS:
                palavra = "-" + palavra[1:]
            if destino == "argv":
                atual.argv.append(palavra)
            elif destino == "entrada":
                atual.entrada.append(palavra)
            palavra, destino = None, "argv"

        def fecha_comando(ligado=False):
            nonlocal atual, destino
            fecha_palavra()
            destino = "argv"
            if atual.argv or atual.entrada:
                self.comandos.append(atual)
                atual = Comando(atual if ligado else None)
            else:
                atual = Comando()

        while self.i < self.n:
            c = t[self.i]
            prox = t[self.i + 1] if self.i + 1 < self.n else ""

            if fecho and c == fecho:
                fecha_comando()
                self.i += 1
                return
            if c == "\n":
                fecha_comando()
                self.i += 1
                self._ler_heredocs()
                continue
            if c in " \t\r":
                fecha_palavra()
                self.i += 1
                continue
            if d == PS and palavra is None and t.startswith("<#", self.i):
                fim = t.find("#>", self.i + 2)
                self.i = self.n if fim < 0 else fim + 2
                continue
            if c == "#" and palavra is None and d != CMD:
                fim = t.find("\n", self.i)
                self.i = self.n if fim < 0 else fim
                continue
            if c == self.esc:
                if prox == "\r" and t[self.i + 2:self.i + 3] == "\n":
                    self.i += 3
                elif prox == "\n":
                    self.i += 2
                else:
                    palavra = (palavra or "") + prox
                    self.i += 2
                continue
            if c == "'" and d != CMD:
                palavra = (palavra or "") + self._aspas_simples()
                continue
            if c == '"':
                palavra = (palavra or "") + self._aspas_duplas()
                continue
            if d == BASH and c == "$" and prox == "'":
                self.i += 1
                palavra = (palavra or "") + self._ansi()
                continue
            if d == BASH and c == "$" and prox == '"':
                self.i += 1
                continue
            if d == PS and c == "@" and HERE_STRING.match(t, self.i):
                palavra = (palavra or "") + self._here_string()
                continue
            if d == PS and c == "$" and prox == "{":
                fim = t.find("}", self.i)
                fim = self.n - 1 if fim < 0 else fim
                palavra = (palavra or "") + t[self.i:fim + 1]
                self.i = fim + 1
                continue
            if d == BASH and c == "`":
                self._crase()
                palavra = (palavra or "") + "$()"
                continue
            if d == BASH and c == "(" and re.match(r"\(\s*\)", t[self.i:self.i + 40]):
                # Definição de função: o corpo vem depois e é lido como comando.
                self.i = t.index(")", self.i) + 1
                palavra = None
                atual = Comando()
                continue
            if c == "(" or (c == "{" and d == PS):
                self.i += 1
                self.ler(")" if c == "(" else "}")
                if palavra is not None or atual.argv:
                    palavra = (palavra or "") + "$()"
                continue
            if c == ")" or (c == "}" and d == PS):
                fecha_comando()
                self.i += 1
                continue
            if c == ";" and d != CMD:
                fecha_comando()
                self.i += 1
                continue
            if c == "|":
                if prox == "|":
                    fecha_comando()
                    self.i += 2
                else:
                    self.i += 2 if d == BASH and prox == "&" else 1
                    fecha_comando(ligado=True)
                continue
            if c == "&":
                if d == BASH and prox == ">":
                    fecha_palavra()
                    self.i += 2
                    if self.i < self.n and t[self.i] == ">":
                        self.i += 1
                    destino = "pular"
                    continue
                fecha_comando()
                self.i += 2 if prox == "&" else 1
                continue
            if c in "<>":
                if d == BASH and prox == "(":
                    self.i += 1  # substituição de processo: o parêntese é lido em seguida
                    continue
                if d == BASH and t.startswith("<<<", self.i):
                    fecha_palavra()
                    self.i += 3
                    destino = "entrada"
                    continue
                if d == BASH and prox == "<":
                    fecha_palavra()
                    self.i += 2
                    self._registrar_heredoc(atual)
                    continue
                if palavra is not None and (palavra.isdigit() or palavra == "*"):
                    palavra = None
                else:
                    fecha_palavra()
                self.i += 1
                while self.i < self.n and t[self.i] in ">&|":
                    self.i += 1
                destino = "pular"
                continue

            palavra = (palavra or "") + c
            self.i += 1

        fecha_comando()

    def ler_tudo(self):
        self.ler()
        return self.comandos

    def _aspas_simples(self):
        t = self.t
        self.i += 1
        saida = []
        while self.i < self.n:
            c = t[self.i]
            if c == "'":
                if self.d == PS and t[self.i + 1:self.i + 2] == "'":
                    saida.append("'")
                    self.i += 2
                    continue
                self.i += 1
                break
            saida.append(c)
            self.i += 1
        return "".join(saida)

    def _ansi(self):
        t = self.t
        self.i += 1
        saida = []
        while self.i < self.n and t[self.i] != "'":
            if t[self.i] == "\\" and self.i + 1 < self.n:
                saida.append(t[self.i + 1])
                self.i += 2
                continue
            saida.append(t[self.i])
            self.i += 1
        self.i += 1
        return "".join(saida)

    def _aspas_duplas(self):
        t, d = self.t, self.d
        self.i += 1
        saida = []
        while self.i < self.n:
            c = t[self.i]
            prox = t[self.i + 1] if self.i + 1 < self.n else ""
            if c == '"':
                if d == PS and prox == '"':
                    saida.append('"')
                    self.i += 2
                    continue
                self.i += 1
                break
            if d == BASH and c == "\\" and prox:
                if prox == "\n":
                    self.i += 2
                elif prox in '"\\$`':
                    saida.append(prox)
                    self.i += 2
                else:
                    saida.append(c)
                    self.i += 1
                continue
            if d == PS and c == "`" and prox:
                saida.append(prox)
                self.i += 2
                continue
            if d in (BASH, PS) and c == "$" and prox == "(":
                self.i += 2
                self.ler(")")
                saida.append("$()")
                continue
            if d == BASH and c == "`":
                self._crase()
                saida.append("$()")
                continue
            saida.append(c)
            self.i += 1
        return "".join(saida)

    def _crase(self):
        """Substituição com crase do Bash: extrai o miolo e lê como comando."""
        t = self.t
        self.i += 1
        miolo = []
        while self.i < self.n and t[self.i] != "`":
            if t[self.i] == "\\" and self.i + 1 < self.n and t[self.i + 1] in "`\\$":
                miolo.append(t[self.i + 1])
                self.i += 2
                continue
            miolo.append(t[self.i])
            self.i += 1
        self.i += 1
        self.comandos.extend(Leitor("".join(miolo), self.d).ler_tudo())

    def _here_string(self):
        t = self.t
        m = HERE_STRING.match(t, self.i)
        aspa = m.group(1)
        inicio = m.end()
        fim = re.compile(r"\n" + aspa + "@").search(t, inicio - 1)
        if fim is None:
            corpo, self.i = t[inicio:], self.n
        else:
            corpo, self.i = t[inicio:max(inicio, fim.start())], fim.end()
        if aspa == '"':
            self._varrer_expansoes(corpo)
        return corpo

    def _registrar_heredoc(self, comando):
        t = self.t
        tira_tabs = self.i < self.n and t[self.i] == "-"
        if tira_tabs:
            self.i += 1
        while self.i < self.n and t[self.i] in " \t":
            self.i += 1
        delimitador = []
        literal = False
        while self.i < self.n and t[self.i] not in " \t\r\n;|&<>()":
            c = t[self.i]
            if c in "'\"":
                literal = True
                fim = t.find(c, self.i + 1)
                fim = self.n if fim < 0 else fim
                delimitador.append(t[self.i + 1:fim])
                self.i = fim + 1
                continue
            if c == "\\" and self.i + 1 < self.n:
                literal = True
                delimitador.append(t[self.i + 1])
                self.i += 2
                continue
            delimitador.append(c)
            self.i += 1
        self.pendentes.append((comando, "".join(delimitador), tira_tabs, literal))

    def _ler_heredocs(self):
        t = self.t
        for comando, delimitador, tira_tabs, literal in self.pendentes:
            linhas = []
            while self.i < self.n:
                fim = t.find("\n", self.i)
                fim = self.n if fim < 0 else fim
                linha = t[self.i:fim]
                self.i = min(fim + 1, self.n)
                comparada = linha.lstrip("\t") if tira_tabs else linha
                if comparada.rstrip("\r") == delimitador:
                    break
                linhas.append(linha)
            corpo = "\n".join(linhas)
            comando.entrada.append(corpo)
            if not literal:
                self._varrer_expansoes(corpo)
        self.pendentes = []

    def _varrer_expansoes(self, corpo):
        """Texto expansível: só o que está em $(...) ou crase executa."""
        sub = Leitor(corpo, self.d)
        while sub.i < sub.n:
            if corpo.startswith("$(", sub.i):
                sub.i += 2
                sub.ler(")")
            elif sub.d == BASH and corpo[sub.i] == "`":
                sub._crase()
            elif corpo[sub.i] == sub.esc:
                sub.i += 2
            else:
                sub.i += 1
        self.comandos.extend(sub.comandos)


def nome_base(palavra):
    """Nome do programa sem pasta, sem extensão e em minúsculas."""
    nome = palavra.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1].lower()
    for extensao in (".exe", ".cmd", ".bat", ".com"):
        if nome.endswith(extensao):
            return nome[: -len(extensao)]
    return nome


def _pular_opcoes(palavras, com_valor):
    i = 0
    while i < len(palavras) and palavras[i].startswith("-") and palavras[i] != "-":
        if palavras[i] == "--":
            i += 1
            break
        i += 2 if palavras[i] in com_valor else 1
    return palavras[i:]


def desembrulhar(argv):
    """Tira atribuições, palavras reservadas e programas que só repassam o comando."""
    v = list(argv)
    while v:
        nome = nome_base(v[0])
        if nome in RESERVADAS or ATRIBUICAO.match(v[0]):
            v = v[1:]
            continue
        if v[0].startswith("$"):
            if len(v) > 1 and v[1] in ("=", "+=", "-="):
                v = v[2:]
                continue
            m = ATRIBUICAO_PS.match(v[0])
            if m:
                v = [m.group(1)] + v[1:]
                continue
        if nome == "command" and any(a in ("-v", "-V") for a in v[1:2]):
            return []
        if nome in ("npm", "pnpm", "yarn") and v[1:2] in (["dlx"], ["exec"]):
            v = _pular_opcoes(v[2:], set())
            continue
        if nome in EMBRULHOS:
            resto = _pular_opcoes(v[1:], EMBRULHOS[nome])
            v = resto[1:] if nome == "timeout" else resto
            continue
        return v
    return []


def curtas(args, com_valor=""):
    """Letras das opções curtas agrupadas, parando na que recebe valor."""
    letras = set()
    for a in args:
        if a.startswith("-") and not a.startswith("--") and len(a) > 1:
            for letra in a[1:]:
                letras.add(letra)
                if letra in com_valor:
                    break
    return letras


def longa(args, nome, minimo):
    """Git aceita opção longa abreviada: casa qualquer prefixo a partir do mínimo."""
    for a in args:
        if a.startswith("--"):
            chave = a.split("=", 1)[0].lower()
            if len(chave) >= minimo and nome.startswith(chave):
                return True
    return False


def regra_git(args, prof):
    i = 0
    configs = []
    while i < len(args) and args[i].startswith("-"):
        if args[i] in GIT_GLOBAIS_COM_VALOR:
            if args[i] == "-c" and i + 1 < len(args):
                configs.append(args[i + 1])
            i += 2
        else:
            i += 1
    if i >= len(args):
        return
    sub = args[i].lower()
    resto = args[i + 1:]
    if resto[:1] in (["--help"], ["-h"]):
        return

    for config in configs:
        chave, _, valor = config.partition("=")
        if chave.lower() == "alias." + sub and valor:
            analisar(valor[1:] if valor.startswith("!") else "git " + valor, BASH, prof + 1)

    if "--" in resto:
        corte = resto.index("--")
        antes, depois = resto[:corte], resto[corte + 1:]
    else:
        antes, depois = resto, []
    pos = [a for a in antes if not a.startswith("-")]

    if sub == "push":
        c = curtas(antes, "o")
        if "n" in c or longa(antes, "--dry-run", 4):
            return
        if "f" in c or "F" in c or longa(antes, "--force", 3) or longa(antes, "--force-with-lease", 8) or longa(antes, "--force-if-includes", 8):
            raise Bloqueio("git push com força reescreve o histórico do remoto (--force-with-lease também)")
        if longa(antes, "--mirror", 4):
            raise Bloqueio("git push --mirror sobrescreve e apaga referências no remoto")
        if "d" in c or longa(antes, "--delete", 3) or longa(antes, "--prune", 5):
            raise Bloqueio("git push apagando branch ou tag no remoto")
        for ref in pos[1:] + depois:
            if ref.startswith("+"):
                raise Bloqueio("git push com refspec + força a atualização no remoto")
            if ref.startswith(":") and len(ref) > 1:
                raise Bloqueio("git push com refspec :nome apaga a referência no remoto")
    elif sub == "reset":
        if longa(antes, "--hard", 3) or longa(antes, "--merge", 4):
            raise Bloqueio("git reset --hard descarta trabalho não commitado")
    elif sub == "clean":
        c = curtas(antes, "e")
        if "n" in c or longa(antes, "--dry-run", 4):
            return
        if "f" in c or "F" in c or longa(antes, "--force", 3):
            raise Bloqueio("git clean -f apaga arquivos não rastreados, sem volta")
        if any(cfg.lower().replace(" ", "").startswith("clean.requireforce=false") for cfg in configs):
            raise Bloqueio("git clean com clean.requireForce desligado apaga arquivos não rastreados")
    elif sub == "checkout":
        c = curtas(antes, "bB")
        if "f" in c or "F" in c or longa(antes, "--force", 3):
            raise Bloqueio("git checkout -f descarta alterações locais")
        if "b" in c or "B" in c:
            return
        parece_caminho = any(
            a in (".", "..") or a.startswith(("./", ".\\", "../", "..\\", ":/")) or "*" in a
            for a in pos
        )
        if depois or parece_caminho or longa(antes, "--pathspec-from-file", 6):
            raise Bloqueio("git checkout com caminho descarta alterações não commitadas")
    elif sub == "restore":
        c = curtas(antes, "sU")
        so_indice = ("S" in c or longa(antes, "--staged", 4)) and not ("W" in c or longa(antes, "--worktree", 3))
        if not so_indice and (pos or depois or longa(antes, "--pathspec-from-file", 6)):
            raise Bloqueio("git restore descarta alterações não commitadas")
    elif sub == "switch":
        c = curtas(antes, "cC")
        if "f" in c or longa(antes, "--force", 3) or longa(antes, "--discard-changes", 4):
            raise Bloqueio("git switch forçado descarta alterações locais")
    elif sub == "branch":
        c = curtas(antes)
        apaga = "d" in c or longa(antes, "--delete", 3)
        forca = "f" in c or longa(antes, "--force", 3)
        if "D" in c or (apaga and forca):
            raise Bloqueio("git branch -D apaga a branch mesmo sem merge")
    elif sub == "stash":
        if pos[:1] in (["drop"], ["clear"]):
            raise Bloqueio("git stash drop ou clear apaga trabalho guardado")
    elif sub in ("filter-repo", "filter-branch"):
        raise Bloqueio("git " + sub + " reescreve o histórico inteiro")


def tem_recursao(args, nome, agrupadas=True):
    for a in args:
        if a == "--":
            return False
        b = a.lower()
        if b == "/s" and nome != "rm":
            return True
        if a.startswith("--"):
            if len(b) >= 3 and "--recursive".startswith(b.split("=", 1)[0]):
                return True
            continue
        if a.startswith("-") and len(a) > 1:
            chave, _, valor = b[1:].partition(":")
            if chave and "recurse".startswith(chave):
                if valor in ("$false", "0"):
                    continue
                return True
            if agrupadas and set(b[1:]) <= set("fridv") and "r" in b[1:]:
                return True
    return False


def tem_whatif(args):
    for a in args:
        chave, _, valor = a.lower().lstrip("-").partition(":")
        if a.startswith("-") and len(chave) >= 2 and "whatif".startswith(chave) and valor != "$false":
            return True
    return False


def regra_apagar(comando, nome, args, dialeto):
    if tem_whatif(args):
        return
    if tem_recursao(args, nome):
        raise Bloqueio("apagar pasta inteira (" + nome + " recursivo) não tem desfazer")
    anterior = comando.anterior
    if dialeto == PS and anterior is not None and anterior.argv:
        if nome_base(anterior.argv[0]) in LISTADORES and tem_recursao(anterior.argv[1:], "rm", agrupadas=False):
            raise Bloqueio("listagem recursiva canalizada para remoção apaga a árvore inteira")


def regra_find(args, dialeto, prof):
    for j, a in enumerate(args):
        b = a.lower()
        if b == "-delete":
            raise Bloqueio("find -delete apaga em lote")
        if b in ("-exec", "-execdir", "-ok", "-okdir"):
            sub = []
            for parte in args[j + 1:]:
                if parte in (";", "+"):
                    break
                sub.append(parte)
            verificar(Comando(), dialeto, prof, sub)


def regra_sql(textos):
    for texto in textos:
        if SQL_DESTRUTIVO.search(texto):
            raise Bloqueio("SQL com DROP ou TRUNCATE apaga dados")
        for instrucao in texto.split(";"):
            if (SQL_APAGA.search(instrucao) or SQL_ALTERA.search(instrucao)) and not SQL_WHERE.search(instrucao):
                raise Bloqueio("SQL com DELETE ou UPDATE sem WHERE altera a tabela inteira")


def regra_processos(comando, nome, args, dialeto):
    if nome in ("pkill", "killall"):
        raise Bloqueio(nome + " derruba processos pelo nome, inclusive os que não são desta sessão")
    if nome == "taskkill" and any(a.lower() in ("/im", "-im") for a in args):
        raise Bloqueio("taskkill /IM derruba processos pelo nome, inclusive os que não são desta sessão")
    if nome in ("stop-process", "spps") or (nome == "kill" and dialeto == PS):
        for a in args:
            chave = a.lower().lstrip("-").partition(":")[0]
            if a.startswith("-") and chave and "name".startswith(chave):
                raise Bloqueio("Stop-Process -Name derruba processos pelo nome, inclusive os que não são desta sessão")
        anterior = comando.anterior
        if anterior is not None and anterior.argv and nome_base(anterior.argv[0]) in ("get-process", "gps", "ps"):
            raise Bloqueio("Get-Process canalizado para Stop-Process derruba processos pelo nome")


def regra_disco(nome, args):
    if nome in DISCO_SEMPRE or nome == "mkfs" or nome.startswith("mkfs."):
        raise Bloqueio(nome + " formata ou apaga um disco")
    if nome == "format" and any(UNIDADE.match(a) for a in args):
        raise Bloqueio("format apaga a unidade inteira")


def regra_ferramentas(nome, args):
    posicionais = [a.lower() for a in args if not a.startswith("-")]
    pares = list(zip(posicionais, posicionais[1:]))
    if nome == "supabase" and ({("db", "reset"), ("db", "push"), ("migration", "repair")} & set(pares)):
        raise Bloqueio("supabase db reset, db push e migration repair mexem no banco")
    if nome in ("vercel", "vc"):
        if any(a.split("=", 1)[0].lower() in ("--prod", "--production") for a in args):
            raise Bloqueio("vercel --prod publica em produção")
        if posicionais[:1] in (["promote"], ["rollback"]):
            raise Bloqueio("vercel promote e rollback mudam o que está em produção")
        if ("env", "rm") in pares or ("env", "remove") in pares or ("env", "pull") in pares:
            raise Bloqueio("vercel env rm apaga variável e env pull grava valores reais em arquivo")
    if nome in ("docker", "docker-compose", "podman"):
        minusculos = [a.lower() for a in args]
        if ("system", "prune") in pares or ("volume", "rm") in pares or ("volume", "prune") in pares:
            raise Bloqueio("limpeza de volumes e imagens do Docker apaga dados")
        if "down" in posicionais and ("-v" in minusculos or "--volumes" in minusculos):
            raise Bloqueio("docker compose down -v apaga os dados dos volumes")


def textos_internos(nome, args):
    """Devolve (texto, dialeto) de quem executa texto: bash -c, cmd /c, eval e parentes."""
    if nome in SHELLS_POSIX:
        j = 0
        while j < len(args):
            a = args[j]
            if a in ("-o", "-O", "+o", "+O"):
                j += 2
                continue
            if not a.startswith(("-", "+")) or a == "--":
                break
            if not a.startswith("--") and "c" in a[1:]:
                return [(args[j + 1], BASH)] if j + 1 < len(args) else []
            j += 1
        return []
    if nome in SHELLS_PS:
        return _textos_powershell(nome, args)
    if nome == "cmd":
        for j, a in enumerate(args):
            m = re.match(r"/[ck](.*)$", a, re.I | re.S)
            if m:
                partes = ([m.group(1)] if m.group(1) else []) + args[j + 1:]
                if len(partes) > 1:
                    partes = ['"' + p + '"' if " " in p else p for p in partes]
                return [(" ".join(partes), CMD)]
        return []
    if nome == "eval":
        return [(" ".join(args), BASH)]
    if nome in AVALIADORES_PS:
        return [(" ".join(a for a in args if not a.startswith("-")), PS)]
    return []


def _textos_powershell(nome, args):
    com_valor = ("executionpolicy", "windowstyle", "inputformat", "outputformat", "psconsolefile",
                 "version", "configurationname", "workingdirectory", "custompipename", "settingsfile")
    j = 0
    while j < len(args):
        a = args[j]
        if a[:1] not in ("-", "/") or a == "-":
            return [(" ".join(args[j:]), PS)] if nome == "powershell" else []
        chave = a.lstrip("-/").split(":", 1)[0].lower()
        if chave and "command".startswith(chave):
            return [(" ".join(args[j + 1:]), PS)]
        if chave in ("e", "ec") or (len(chave) >= 2 and "encodedcommand".startswith(chave)):
            try:
                return [(base64.b64decode(args[j + 1], validate=True).decode("utf-16-le"), PS)]
            except (ValueError, IndexError):
                raise Bloqueio("comando codificado em base64 que a guarda não consegue ler")
        if chave and "file".startswith(chave):
            return []
        if chave and (chave in ("ep", "ex", "wd") or any(v.startswith(chave) for v in com_valor)):
            j += 2
            continue
        j += 1
    return []


def entrada_canalizada(comando):
    """Textos que chegam pela entrada: heredoc, here-string ou echo no pipe."""
    textos = list(comando.entrada)
    anterior = comando.anterior
    if anterior is not None and anterior.argv:
        nome = nome_base(anterior.argv[0])
        if nome in EMISSORES:
            palavras = [a for a in anterior.argv[1:] if not a.startswith("-")]
            if nome == "printf":
                palavras = palavras[1:]
            textos.append(" ".join(palavras))
        elif len(anterior.argv) == 1:
            textos.append(anterior.argv[0])
    return textos


def verificar(comando, dialeto, prof, argv=None):
    v = desembrulhar(comando.argv if argv is None else argv)
    if not v:
        return
    nome = nome_base(v[0])
    args = v[1:]
    entrada = entrada_canalizada(comando)

    executa_texto = nome in SHELLS_POSIX or nome in SHELLS_PS or nome in AVALIADORES_PS or nome == "cmd"
    if executa_texto and comando.anterior is not None:
        origem = desembrulhar(comando.anterior.argv)
        if origem and nome_base(origem[0]) in BAIXADORES:
            raise Bloqueio("baixar e executar direto, sem ler o script antes")

    for texto, dialeto_interno in textos_internos(nome, args):
        analisar(texto, dialeto_interno, prof + 1)
    if executa_texto:
        dialeto_entrada = BASH if nome in SHELLS_POSIX else (CMD if nome == "cmd" else PS)
        for texto in entrada:
            analisar(texto, dialeto_entrada, prof + 1)

    if nome == "git":
        regra_git(args, prof)
    elif nome in FAMILIA_APAGAR:
        regra_apagar(comando, nome, args, dialeto)
    elif nome == "rimraf":
        raise Bloqueio("rimraf apaga pasta inteira")
    elif nome == "find":
        regra_find(args, dialeto, prof)
    elif nome in CLIENTES_SQL:
        regra_sql(args + entrada)

    if nome in INDIRETOS_SQL:
        for j, a in enumerate(args):
            if nome_base(a) in CLIENTES_SQL:
                regra_sql(args[j + 1:] + entrada)
                break

    regra_processos(comando, nome, args, dialeto)
    regra_disco(nome, args)
    regra_ferramentas(nome, args)


def analisar(texto, dialeto, prof=0):
    """Levanta Bloqueio se algum comando do texto for perigoso."""
    if prof > PROFUNDIDADE_MAXIMA:
        raise Bloqueio("comando aninhado demais para a guarda ler")
    if dialeto == PS:
        texto = texto.translate(ASPAS_CURVAS)
    comandos = Leitor(texto, dialeto).ler_tudo()
    nomes = set()
    for comando in comandos:
        verificar(comando, dialeto, prof)
        v = desembrulhar(comando.argv)
        if v:
            nomes.add(nome_base(v[0]))
    if nomes & AVALIADORES_PS and (nomes & BAIXADORES or "downloadstring" in texto.lower()):
        raise Bloqueio("baixar e executar direto, sem ler o script antes")


def recusa_entrada(motivo):
    return BLOQUEIA, (
        "guarda-git bloqueou por segurança: " + motivo + ".\n"
        "Sem entender a entrada, a guarda não deixa passar. "
        "Se isso se repetir, confira a instalação ou tire o bloco dela do settings.json.\n"
    )


def decidir(cru):
    """Recebe os bytes do stdin e devolve (código de saída, mensagem para o stderr)."""
    try:
        dados = json.loads(cru.decode("utf-8-sig"))
    except ValueError:
        return recusa_entrada("o JSON recebido no stdin está quebrado ou vazio")
    if not isinstance(dados, dict):
        return recusa_entrada("o JSON recebido não é um objeto")
    ferramenta = dados.get("tool_name")
    if not isinstance(ferramenta, str):
        return recusa_entrada("falta o campo tool_name")
    if ferramenta not in FERRAMENTAS:
        return PASSA, ""
    entrada = dados.get("tool_input")
    if not isinstance(entrada, dict) or not isinstance(entrada.get("command"), str):
        return recusa_entrada("falta o campo tool_input.command")
    comando = entrada["command"]
    if not comando.strip():
        return PASSA, ""
    try:
        analisar(comando, FERRAMENTAS[ferramenta])
    except Bloqueio as bloqueio:
        return BLOQUEIA, (
            "guarda-git bloqueou este comando: " + str(bloqueio) + ".\n"
            "Comando: " + comando[:300] + "\n"
            "Não procure outro caminho para o mesmo efeito. Diga à pessoa o comando, o alvo "
            "e o que se perde; se ela quiser seguir, ela mesma roda no terminal dela.\n"
        )
    return PASSA, ""


def principal():
    codigo = BLOQUEIA
    mensagem = "guarda-git bloqueou por segurança: erro interno da guarda.\n"
    try:
        codigo, mensagem = decidir(sys.stdin.buffer.read())
    except BaseException as erro:
        codigo = BLOQUEIA
        mensagem = "guarda-git bloqueou por segurança: erro interno da guarda (" + type(erro).__name__ + ").\n"
    try:
        if mensagem:
            sys.stderr.buffer.write(mensagem.encode("utf-8", "replace"))
            sys.stderr.buffer.flush()
    except BaseException:
        pass
    os._exit(codigo)


if __name__ == "__main__":
    principal()
