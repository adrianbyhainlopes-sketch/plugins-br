# Hooks, permissões e settings

Conferido na documentação oficial do Claude Code em 08/11/2026 (fontes no fim). Reconfira antes de confiar: muda entre versões.

## Regra de ouro
Todo modo de falha de um hook termina em "a ferramenta segue". Hook que rodou e permitiu é indistinguível de hook nunca ligado. **Primeiro teste de qualquer guarda:** mande pela entrada padrão um JSON de exemplo de uma ação proibida e veja se ela nega.

## Códigos de saída
| Saída | Efeito |
|---|---|
| 0 | segue; o JSON impresso é aplicado |
| 2 | bloqueia, nos eventos que podem bloquear (`PreToolUse` bloqueia a ferramenta; `UserPromptSubmit`, o pedido; `Stop` impede de parar; em `PostToolUse` a ferramenta já rodou) |
| outro, inclusive 1 | erro não bloqueante: a ação vai em frente |

Guarda sem código 2 e sem negação no JSON é só um log. Em `PreToolUse`, `permissionDecision` fica dentro de `hookSpecificOutput`; no nível de cima é ignorado sem aviso.

Entrada: JSON pela entrada padrão, com `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `tool_name` e `tool_input` (o comando está em `tool_input.command`).

## Não dispara
1. `/hooks` mostra o hook no evento certo, com a origem. Se não mostra, não carregou: mora fora da chave `hooks`, JSON inválido, ou `matcher` é lista em vez de texto.
2. **Matcher diferencia maiúscula:** `Bash`, `Edit`, `Write`, `Read`. `bash` não pega nada.
3. Só letras, dígitos, `_`, `-`, espaço, `,` e `|`: lista exata. Qualquer outro caractere: expressão regular sem âncora, e `Edit.*` pega também `NotebookEdit`.
4. **`Bash` não cobre `PowerShell`.** Use `Bash|PowerShell`.
5. Script ausente no caminho configurado é a causa mais comum de guarda que nunca guardou: use caminho absoluto ou `${CLAUDE_PROJECT_DIR}`.
6. Mudança em settings entra sozinha em segundos; se não entrar, reinicie a sessão.
7. `claude --debug` ou `/debug` mostram o evento, os matchers e a saída.

## Erro e saída ignorada
- Teste manual (Bash): `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./meu-hook.sh; echo $?`
- `jq` não existe: use Python ou Node.
- Perfil do shell que imprime algo antes do JSON faz o Claude Code ler como texto puro; o debug acusa `Hook output does not start with {`.
- Windows: o campo `shell` aceita `bash` ou `powershell`; o padrão é `bash`, ou `powershell` quando o Git Bash não está instalado. Falta do Git Bash pode bloquear a ferramenta quando o hook falha (`referencias/windows.md`).

## `Stop`
Dispara em todo fim de resposta, não só no fim da tarefa. Interrupção do usuário não dispara. Depois de oito bloqueios seguidos, o Claude Code passa por cima. Saia cedo se `stop_hook_active` vier `true`, ou o laço fica girando.

## O que a leitura não vê
Se o hook disparou: faça-o gravar uma linha a cada chamada. Matcher `Write|Edit` não vê `> arquivo`, `sed -i` ou `cp` pelo shell: para isso, confira depois (`git status --porcelain`). Guarda de caminho: resolva o caminho real dos dois lados, ou symlink e junção do Windows escapam. Catch silencioso: falhar aberto precisa ser decisão.

## Permissões e settings
- Ordem: `deny`, depois `ask`, depois `allow`. O primeiro que casa decide; especificidade não muda a ordem.
- Precedência de settings, do mais forte: gerenciado, linha de comando, `.claude/settings.local.json`, `.claude/settings.json`, `~/.claude/settings.json`. Listas se somam entre os arquivos. `/status` mostra as fontes, `/permissions` as regras e `claude doctor` o que foi rejeitado.
- **`.claudeignore` não tem efeito.** Quem tem um deve passar as linhas para regras `Read` em `deny`: `Read(./.env)`, `Read(./secrets/**)`.
- Regra de `Read` barra as ferramentas de arquivo do Claude. Regra de `Bash` casa com o texto do comando e não é fronteira de segurança: `Bash(rm *)` não barra `/bin/rm`. Garantia pede hook ou sandbox.
- `PowerShell(Remove-Item *)` é regra própria; aliases comuns são reconhecidos.
- Padrões de caminho seguem a sintaxe do gitignore: `Read(.env)` casa em qualquer profundidade; `*` um nível, `**` vários.

## Guarda contra comandos destrutivos
Regras em `comandos-destrutivos.md`. Se o usuário quiser um hook: `PreToolUse`, matcher `Bash|PowerShell`, código 2 ou negação em JSON, testado com ação proibida e com ação permitida, instalado só com o sim e pela skill de configuração. Este plugin não traz nenhum.

Duas guardas no mesmo evento rodam em paralelo; uma só por evento, ramificando dentro do script, é mais fácil de depurar. Hook caro em matcher `*` custa em toda chamada.

## Fontes (lidas em 08/11/2026)
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/hooks-guide
- https://code.claude.com/docs/en/debug-your-config
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/permissions
