# Guarda de git e de comandos destrutivos

Hook opcional do Claude Code (`PreToolUse`). Antes de cada comando das ferramentas Bash e PowerShell, lê o comando como o shell leria e barra o que apaga, sobrescreve ou reescreve sem desfazer. No Windows a ferramenta PowerShell não passa por guardas escritas só para Bash; esta cobre as duas.

**Só se liga com o sim de quem usa.** Nada aqui se instala sozinho.

É rede de segurança contra engano, não sandbox. Quem quiser passar por cima consegue.

## O que bloqueia

| Área | Comandos |
|---|---|
| git, remoto | `push` com `--force`, `-f`, `--force-with-lease`, `--force-if-includes`, `--mirror`, `--delete`, `--prune`, refspec `+nome` ou `:nome` |
| git, local | `reset --hard` e `--merge`, `clean -f`, `checkout` com caminho, `.` ou `-f`, `restore` na árvore de trabalho, `switch` forçado, `branch -D`, `stash drop` e `clear`, `filter-repo`, `filter-branch` |
| Apagar | `rm` recursivo, `Remove-Item -Recurse` e os apelidos `ri`, `rm`, `del`, `erase`, `rd`, `rmdir`, parâmetro abreviado incluso, `del /s`, `rd /s`, `rimraf`, `find -delete`, o mesmo `rm` dentro de `find -exec` ou `xargs`, listagem recursiva canalizada para remoção |
| Disco | `format X:`, `Format-Volume`, `Clear-Disk`, `diskpart`, `mkfs` |
| SQL em linha de comando | `DROP`, `TRUNCATE`, `DELETE` ou `UPDATE` sem `WHERE`, nos clientes `psql`, `mysql`, `mariadb`, `sqlite3`, `sqlcmd` e parecidos |
| Ferramentas | `supabase db reset`, `db push`, `migration repair`; `vercel --prod`, `promote`, `rollback`, `env rm`, `env pull`; `docker system prune`, `volume rm`, `compose down -v` |
| Processos | `pkill`, `killall`, `taskkill /IM`, `Stop-Process -Name`, `Get-Process` canalizado para `Stop-Process` |
| Baixar e executar | `curl` ou `wget` em `sh`, `iwr` ou `irm` em `iex` |

Ela enxerga através de `&&`, `;`, `|`, nova linha, `git -C caminho`, variável de ambiente na frente, `sudo`, `env`, maiúsculas, aspas picando o nome, caminho completo do executável, `$(...)`, crase, `bash -c`, `powershell -Command` e `-EncodedCommand`, `cmd /c`, `eval` e `Invoke-Expression` com texto literal.

## Decisões

- **`--force-with-lease` bloqueia.** Ele só protege contra commit alheio que você ainda não viu; o histórico do remoto continua sendo reescrito.
- **Recursivo sem força também bloqueia.** Sem terminal, não há quem responda à confirmação: `rm -r` e `Remove-Item -Recurse` apagam do mesmo jeito.
- **`git push` normal passa**, assim como `git checkout arquivo` (sem `--`, não dá para distinguir de branch).
- **Modo de ensaio passa:** `git push -n`, `git clean -n`, `Remove-Item -WhatIf`.
- **Bloquear não pergunta.** Se for isso mesmo, a pessoa roda o comando no próprio terminal.

| Entrada | O que faz |
|---|---|
| JSON quebrado, stdin vazio, JSON que não é objeto | bloqueia |
| Falta `tool_name` | bloqueia |
| Bash ou PowerShell sem `tool_input.command` em texto | bloqueia |
| `command` vazio ou só com espaços | passa |
| Outra ferramenta | passa, fora do escopo |
| Erro interno ou aninhamento acima do limite | bloqueia |

Ela só sai com código 0 ou 2. O código 1 deixaria o comando passar.

## O que ela não pega

- Comando dentro de script (`./limpa.sh`, `.\limpa.ps1`, `psql -f limpa.sql`, `psql < limpa.sql`).
- Outra linguagem apagando (`python -c`, `node -e`, `[IO.Directory]::Delete`).
- Texto montado em variável: `$c = "git push --force"; Invoke-Expression $c`, `git push $flag`, `& $g push`, parâmetros por splatting.
- Alias já configurado (`git fp`, `Set-Alias`) e `Start-Process` com argumentos.
- Comando remoto (`ssh servidor '...'`).
- Lote sem recursão (`rm *.txt`, `Remove-Item *`) e o que depende de contexto, como `rebase` ou `commit --amend` em branch publicada.
- Outras ferramentas que executam comandos, como a Monitor e servidores MCP. Só Bash e PowerShell chegam aqui.
- Um mod instalado que aprove a chamada pode passar por cima do bloqueio, conforme a documentação de permissões.

## Como ligar

Precisa de Python 3 no PATH e do Claude Code 2.1.295 ou mais novo (por causa do `onFailure`). Peça ao Claude Code, pela skill `update-config`, para acrescentar este bloco ao `settings.json`, trocando o caminho pelo real:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "python -I \"C:/Users/SeuNome/Meus Projetos/guarda-git/guarda.py\"",
            "timeout": 10,
            "onFailure": "block"
          }
        ]
      }
    ]
  }
}
```

- O matcher precisa ter os dois nomes. Só `Bash` deixa o PowerShell de fora.
- O caminho fica entre aspas por causa do espaço. Use `/` no lugar de `\`, que funciona tanto no Git Bash quanto no PowerShell.
- `-I` isola o Python de variáveis e de módulos da pasta atual.
- `onFailure: block` faz a falha do hook bloquear. Sem ele, caminho errado, Python ausente ou tempo esgotado deixam tudo passar sem aviso.

Com `onFailure: block`, se o Python ou o arquivo sumirem, **todo comando de shell fica bloqueado** até o bloco ser corrigido. Confira logo depois de ligar, com comandos que não fazem estrago se a guarda falhar: `git status` passa e `rm -r pasta-que-nao-existe` é barrado.

## Como desligar

Tire o bloco do `settings.json`, pela skill `update-config` ou à mão num editor de texto. Editar o arquivo à mão funciona mesmo com todos os comandos de shell bloqueados.

## Testes

```bash
python -I teste_guarda.py
```

Cada caso sobe a guarda com JSON sintético pelo stdin. Nenhum comando é executado. Os casos de `LIMITES` registram o que escapa de propósito.
