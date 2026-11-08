# Formato de memória

## Arquivo de memória
Um fato por arquivo. Se a pasta já tem um formato, siga o dela; este é o padrão:

```markdown
---
name: nome-curto-em-minusculas
description: uma linha que decide se vale abrir
type: user | feedback | project | reference
---

O fato, no presente, em até três frases.

**Por quê:** o motivo ou o incidente.
**Como aplicar:** quando vale e o que fazer.
```

- `user`: quem é, papel, nível. `feedback`: correção ou confirmação de abordagem. `project`: quem faz o quê, por quê, até quando. `reference`: onde olhar fora do projeto, não o conteúdo.
- `feedback` e `project` sempre com **Por quê** e **Como aplicar**: sem o motivo, a regra é aplicada rígida demais ou não é aplicada.
- Só datas absolutas. Estado leva "em AAAA-MM-DD" e o comando ou caminho que reconfere.
- Fato atemporal ("o limite da API é 100 por minuto"), não diário ("hoje descobrimos").
- Atualize antes de criar. Filtro de quantidade: se uma sessão pede mais de cinco memórias novas, provavelmente é log, não memória.
- Retratação à vista: corrija no topo, diga por quê, e risque o antigo (`~~assim~~`) enquanto ele puder confundir.
- **Uma direção atual só.** Ao mudar o rumo, o antigo vira história datada na mesma edição.

## Índice (`MEMORY.md`)
Uma linha por memória, em ordem de uso: `- [Título](arquivo.md): o que é e quando importa`.
- Só as primeiras 200 linhas ou 25 KB carregam, o que vier primeiro (documentação do Claude Code, 08/11/2026). O índice é para caber com folga: linha de cerca de 150 caracteres é prática das fontes, não limite.
- O detalhe mora no arquivo. Linha que repete a conclusão inteira é o caminho para o índice de 10 KB.
- Nada volátil no índice (versão, "estado atual em", contagem): isso envelhece onde todo mundo lê.
- Arquivo e linha mudam juntos. Memória sem linha não existe para a próxima sessão.

## Correção do Claude: Gatilho e Checagem
Quando o usuário corrige algo que se repetiria. Não registrar: estilo menor, digitação, mudança de ideia dele.

```markdown
## [0003] 2026-11-08: inventou o método X da biblioteca Y
Categoria: alucinação | exagero | confusão | acréscimo não pedido | suposição errada
Gatilho: a situação, não as palavras ("pediu algo rápido que cabia numa linha")
Falha: uma a três frases, honestas.
Correção: o que devia ter feito.
Checagem: imperativo que se confere num rascunho ("se o pedido diz rápido e cabe em 5 linhas, sem CLI, log nem tipos")
```

"Ser mais cuidadoso" não é checagem. Não invente gatilho que a conversa não mostra: se não ficou claro o que deu errado, pergunte. Numeração estável, para "ver #7" não quebrar. Reconheça em prosa e confirme em uma frase.

Para decidir onde a correção mora, suba a escada e pare no primeiro degrau que serve: mudança que torna o erro impossível; teste ou hook; regra em CLAUDE.md ou Instruções de Projeto; memória de `feedback`; nada (skill instrucoes).

Consulte os gatilhos antes de tarefa não trivial, antes de afirmar que uma API existe e antes de acrescentar algo não pedido. Leve: leia os títulos, aplique só as checagens que casam, e sem narrar. Ausência de registro não prova que o plano é seguro.

## Decisão
Mesmo formato do arquivo de rumo. Livro datado ou um arquivo por decisão, conforme o projeto já faça.

```markdown
## D-012 2026-11-08: título curto, no presente
Contexto: por que foi preciso decidir.
Decisão: "vamos usar X".
Alternativas rejeitadas: Y, porque...; Z, porque...
Consequências: o que fica melhor, o que fica pior.
Estado: proposta | aceita | superada
substitui: D-007 ou nada
superada_por: (preenchido quando for o caso)
```

- Pergunte só o que falta. Insista de leve nas alternativas: é a seção mais valiosa e a mais pulada, e o rejeitado que não foi escrito volta a ser proposto.
- Reversão: a antiga vira `superada` com o link, a nova leva `substitui`. Nada se apaga.
- Ainda é ideia? Guarde como ideia e ofereça o registro quando a decisão vier.
- Questões fechadas, quando não pedem registro próprio: uma linha por opção rejeitada ou hipótese morta, com veredito, data e onde está a evidência.
- Decisão que afeta o rumo geral: `contrato-rumo.md` (proposta, nunca escrita direta).

## Perfil
Seções: papel e foco; pontos fortes e o que está aprendendo; estilo de trabalho (perguntar ou fazer, ritmo, profundidade); comunicação (idioma, tamanho, formato); interesses atuais com data.
- Abaixo de 2 KB, porque é lido em toda sessão. Sem julgamento. Remende seções em vez de regerar.
- Mostre e valide antes de gravar. Nunca colha dado em silêncio (nomes e e-mails do git, agenda, caixa de correio).

## Glossário
- Decodifique antes de agir: glossário, depois memória, depois pergunte ("Não sei o que é X ainda. Me diz que eu guardo.").
- Tabela curta, com o contexto de cada sigla e os apelidos. Promova o que se usa toda hora; rebaixe o que parou.
- Só termos de trabalho. Nada de fichas de pessoas com trivialidades, muito menos de clientes.
- O conteúdo mora em arquivo pessoal do usuário (apontado nas instruções), não dentro do plugin.
