# Comandos destrutivos em camadas

Comando que apaga, sobrescreve ou publica não se desfaz com "desfazer". Checkpoint e /rewind do Claude Code voltam arquivos editados pela sessão, não o efeito de um comando (migração aplicada, `rm`, push). Por isso: o que destrói pede o sim do usuário, e o que só arruma a árvore nunca usa comando destrutivo.

## Camada 1: nunca, nem para arrumar
Usados para "limpar" ou "voltar", apagam trabalho que não é seu (inclusive o não commitado do usuário).
| Em vez de | Faça |
|---|---|
| `git reset --hard`, `git checkout -- arquivo`, `git checkout .`, `git restore .`, `git clean -f` | desfaça a própria edição editando de volta; experimente num `git worktree` separado; restaure de uma cópia que você mesmo fez antes |
| `git stash` para "limpar" a árvore antes de testar | worktree separado na base certa |
| `pkill`, `taskkill /IM nome.exe`, `Stop-Process -Name` | pare só o processo que você iniciou, pelo PID guardado (`Start-Process -PassThru`) |
| `rm -rf` ou `Remove-Item -Recurse -Force` em pasta que você não criou | apague só a pasta temporária de nome único que você criou, conferindo o caminho antes |

## Camada 2: só com o sim do usuário, dito o alvo
Diga o comando, o alvo exato (branch, banco, projeto, pasta) e o que se perde. Espere o sim para este comando, não para "comandos parecidos".
- git: `push` (qualquer forma), `push --force` e `--force-with-lease`, `branch -D`, `rebase` em branch publicada, `commit --amend` em commit publicado, `reset` de qualquer tipo, `filter-repo`.
- Banco e Supabase: `supabase db reset`, `supabase db push`, `migration repair`, `DROP`, `TRUNCATE`, `DELETE` ou `UPDATE` sem `WHERE` conferido, qualquer comando contra banco de produção. Nunca aponte a sessão para produção para "ver se funciona".
- Vercel: `vercel --prod`, `vercel promote`, `vercel rollback`, `vercel env rm`, `vercel env pull` (grava valores reais num arquivo local).
- Docker: `docker system prune`, `docker volume rm`, `docker compose down -v` (o `-v` apaga os dados).
- Arquivos: mover ou apagar em lote, sobrescrever planilha ou pasta de cliente, renomear em massa. Rode primeiro em modo de ensaio e mostre a lista.
- Publicar: criar issue, comentar em PR, postar, enviar e-mail ou mensagem, ativar workflow ou webhook.

## Camada 3: ler antes de rodar
- Comando montado com variável: imprima o comando final e confira o caminho antes (variável vazia transforma `Remove-Item "$pasta\*"` em apagar outra coisa).
- PowerShell 5.1: `-Recurse` e `-Force` juntos não pedem confirmação; `-WhatIf` mostra o que faria sem fazer.
- Bash e PowerShell são ferramentas diferentes no Claude Code: uma regra ou guarda escrita para uma não vale para a outra.
- Script baixado ou colado: leia inteiro antes de rodar; nunca `curl ... | sh` nem `iwr ... | iex`.

## Se algo destrutivo já rodou
Pare, diga o que rodou e o alvo, e não tente "consertar" com outro comando destrutivo. Procure o que ainda dá para recuperar (`git reflog`, lixeira, backup, histórico de deploy) e proponha.
