# Camadas de memória: onde cada fato mora

Conferido na documentação oficial em 08/11/2026 (fontes no fim). Plataforma muda: na dúvida, confira de novo.

Dois princípios:
1. Custo de carga e apodrecimento andam em sentidos opostos. O que carrega sempre precisa ser pouco e durável; o resto fica atrás de um ponteiro.
2. Afirmação com fiscal (teste, hook, CI) continua verdadeira; afirmação só com autor apodrece. Regra escrita é conselho; bloqueio é muro.

## Onde guardar: pare no primeiro sim (Claude Code)
1. Dá para descobrir no código ou no git? Não guarde.
2. Um colega ou um clone novo precisaria? Vai para o repositório (CLAUDE.md do projeto, regra, registro de decisão).
3. Só vale ao tocar certos arquivos? Regra com `paths:` ou CLAUDE.md de pasta.
4. Vale em todo repositório? Global, uma linha.
5. É sobre o usuário, as correções dele ou estado fora do repositório? Arquivo de memória mais uma linha no índice.

Tem de valer sempre, sem depender da boa vontade do modelo? Nenhuma dessas: vai para `permissions.deny` ou hook (skill instrucoes).

## Claude Code
| Camada | Onde | Quando carrega | O que guarda |
|---|---|---|---|
| Global | `~/.claude/CLAUDE.md` | toda sessão | preferência que valeria num repositório novo; nada de projeto, caminho ou tarefa |
| Projeto | `./CLAUDE.md` ou `./.claude/CLAUDE.md` | toda sessão | regra que proíbe, exige ou desambigua; ponteiros |
| Local | `./CLAUDE.local.md` (fora do git) | toda sessão | preferência pessoal neste projeto |
| Regra sem `paths` | `.claude/rules/*.md` | toda sessão | tema separado, mesma prioridade do projeto |
| Regra com `paths` | `.claude/rules/*.md` | ao ler, gravar ou editar arquivo do padrão | restrição de uma área |
| CLAUDE.md de pasta | subpasta | ao ler, gravar ou editar arquivo daquela pasta | invariante local ("gerado, não editar") |
| Memória automática | `~/.claude/projects/<projeto>/memory/` | índice `MEMORY.md`: primeiras 200 linhas ou 25 KB, o que vier primeiro; arquivos de tema sob demanda | tipos `user`, `feedback`, `project`, `reference` |
| Bloqueio | `permissions.deny`, hook, CI | sempre, fora do modelo | o que não pode acontecer |

O que costuma enganar:
- Todos os CLAUDE.md achados são somados; nenhum sobrepõe outro. Se dois se contradizem, o modelo pode seguir qualquer um.
- A memória automática é por repositório: worktrees e subpastas do mesmo repositório dividem o mesmo diretório; fora de git, vale a raiz do projeto. É da máquina: não vai para outro computador nem para a nuvem.
- Ela fica fora da limpeza de transcrições: só sai se alguém apagar.
- O que passa de 200 linhas ou 25 KB no `MEMORY.md` não carrega no início da sessão.
- Subagentes não recebem a memória automática da conversa principal.
- Restrição numa regra com `paths` só entra quando o arquivo é tocado. Se ela muda o plano, precisa de uma linha na raiz.
- Depois de `/compact`, CLAUDE.md da raiz, regras sem `paths` e memória automática voltam do disco; regra com `paths` e CLAUDE.md de pasta voltam só quando o arquivo é tocado de novo; o que foi dito só na conversa vira resumo.

Memória de maior valor por custo: a **roteadora** ("antes de pesquisar X, leia `docs/X.md`; acrescente lá"). Quase não ocupa e evita refazer uma investigação.

Fica de fora: tarefa em andamento (lista de tarefas), estado da sessão (skill continuidade), notas de conhecimento (skill cofre).

## Chat (claude.ai)
| Camada | Onde | Vale para | O que guarda |
|---|---|---|---|
| Memória da conta | gerada nas conversas; ver em Configurações, Your Claude, Your memory, Manage | conversas fora de Projeto e, se ligado, dentro dos Projetos | quem é a pessoa, preferências gerais |
| Memória do Projeto | cada Projeto tem a sua | só aquele Projeto (usa também a da conta, não a de outros Projetos); "Use account memory" desligado isola | o que se aprende naquele Projeto |
| Instruções do Projeto | "Set project instructions" | todas as conversas do Projeto | regras de comportamento |
| Arquivos do Projeto | base de conhecimento | todas as conversas do Projeto | material, tabelas, RUMO, passagens |

O que costuma enganar:
- Pedir no chat para lembrar, mudar ou esquecer vale a partir da próxima conversa.
- Uma conversa de um Projeto não enxerga outra, salvo pelo que foi para os arquivos do Projeto.
- Nome e descrição do Projeto não chegam ao Claude.
- Conversa anônima não vai para memória nem para busca.
- Apagar uma conversa não apaga as memórias que vieram dela: é item a item.
- Por padrão a memória não guarda temas sensíveis; números de documento de governo, de conta financeira e situação migratória nunca são guardados.

### Onde guardar no chat: pare no primeiro sim
1. É regra de como trabalhar neste Projeto? Instruções do Projeto.
2. É material que as conversas do Projeto vão consultar? Arquivo do Projeto.
3. Vale em qualquer assunto, em qualquer conversa? Memória da conta.
4. Vale só para o resto desta conversa? Não guarde.

A skill não grava nessas camadas: entrega o texto e diz onde colar.

## Cowork
Lê e escreve arquivos na pasta aberta e carrega as skills e os plugins ligados na conta, sem ler o `~/.claude` da máquina. O que ele guarda entre sessões não foi conferido: trate o arquivo na pasta como a memória.

## A ponte entre superfícies
Nada se sincroniza sozinho: memória do chat, memória do Claude Code e cofre são lugares separados. Fato que precisa valer em mais de um tem **um dono**, e nos outros fica uma linha apontando para ele. Quando não houver como apontar (chat não lê o disco), entregue a linha para colar e registre qual é o dono.

## Fontes (lidas em 08/11/2026)
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/context-window
- https://code.claude.com/docs/en/claude-directory
- https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context
- https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- https://claude.com/docs/cowork/overview
