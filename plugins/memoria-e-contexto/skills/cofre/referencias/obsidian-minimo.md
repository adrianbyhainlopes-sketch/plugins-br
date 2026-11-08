# Obsidian mínimo (só o não óbvio)

Conferido em obsidian.md/help em 08/11/2026.

## Forma de link
| | Markdown relativo | Wikilink |
|---|---|---|
| Exemplo | `[Beta](notas/Beta%20dois.md)` | `[[Beta dois]]` |
| Abre no GitHub e no VS Code | sim | não |
| Espaço no nome | vira `%20` | fica como está |
| Nomes repetidos | sem problema | ambíguo |
| No Obsidian | funciona | padrão do app |

A regra de cada cofre está no arquivo pessoal: `forma-de-link: relativo` ou `forma-de-link: wikilink`. Vale `relativo` se o cofre for aberto fora do Obsidian em algum momento; `wikilink` se for só nele, e com nomes de arquivo únicos. Não converta o cofre inteiro por conta: é mudança estrutural, com plano e sim.

Para usar Markdown no app: Configurações, Arquivos e links, desligar "Use [[Wikilinks]]". "Atualizar links internos automaticamente" faz o Obsidian corrigir os links ao renomear pelo app; renomear por fora não corrige nada.

## Ao escrever
- Índice por pasta onde alguém possa entrar: `[título](caminho): quando ler`. Linha só com caminho não ajuda. Nunca sobrescreva índice existente.
- Todo documento termina com "Relacionado:" (o que usa, contradiz ou substitui).
- Propriedades em YAML no topo: `tags` e `aliases` são nativas, lista com um item por linha começando com `- `, cada nome uma vez só. **Link interno em propriedade vai entre aspas.**
- Nomes distintos, com prefixo de data onde repetiria. Antes de criar, confira se existe: criar às cegas gera `data 1.md` e esconde a nota de outra sessão.
- Em cofre sem convenção: nome em minúsculas sem acento, se ele for lido por script ou no GitHub.

## Nota diária
Confira se o arquivo do dia existe antes de criar. Sessão que vira a meia-noite usa a data de início. Log: `hora: título`, objetivo, feito (com links), resultado (feito, parcial ou bloqueado, e por quê), aberto.

## Sincronização
- Conflito no Obsidian Sync: por padrão ele funde, o que pode gerar texto duplicado; com "Create conflict file", cria `nome (Conflicted copy dispositivo AAAAMMDDHHMM).md`.
- Dois sincronizadores no mesmo cofre (Obsidian Sync mais outro serviço) é causa conhecida de problema: um só.
- Pasta na nuvem cria cópia com `(1)` no nome. Liste as cópias; compare; nunca apague. Quem escolhe é o usuário.
- Não versione `workspace.json`, cache nem `data.json` de plugin.

## Um cofre ou vários
Um cofre é um espaço de links. Separe só quando as árvores não se ligam, precisam de privacidade diferente ou uma é enorme. Pastas e tags resolvem a maioria das "áreas da vida".

## Linha de comando oficial
Existe, a partir do instalador 1.12.7, ligada em Configurações, Geral. Precisa do app aberto (o primeiro comando o abre). No Windows, o programa é `Obsidian.com`, e o caminho novo só vale em terminal aberto depois. Com o app fechado, leia os arquivos direto.
