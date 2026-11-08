# /compact sob medida e regras esquecidas

## O que sobrevive à compactação (Claude Code, conferido em 08/11/2026)
| Volta do disco | Volta só quando o arquivo é tocado | Vira resumo |
|---|---|---|
| CLAUDE.md da raiz, regras sem `paths`, memória automática, plano do modo plano | regras com `paths`, CLAUDE.md de pasta | o que foi dito só na conversa, o contexto acrescentado por hooks |

Skills já invocadas voltam com limite (5 mil tokens por skill, 25 mil no total; as mais antigas saem primeiro) e até cinco arquivos recentes são relidos. Instrução que não pode se perder vai para um arquivo. Fonte: https://code.claude.com/docs/en/context-window

## Preparar o /compact (só no Claude Code)
Monte uma única linha, com campos separados por ` | `:

`/compact meta: <uma frase> | próximo: <verbo + alvo: editar caminho, rodar comando, inspecionar, perguntar, esperar agente> | arquivos: <o mínimo, plano primeiro> | decisões: <com motivo; restrições do usuário entre aspas; bloqueios> | estado: <sem commit; testes passando, falhando ou desconhecidos; comando mais curto para verificar; o que está pela metade; agentes em andamento>`

- Varra a conversa recente. Decisão só conta com aceite do usuário. Sem evidência, o campo some.
- Literais ficam literais. Corte conversa e becos sem saída, menos os que sustentam um bloqueio.
- **Armadilha:** o comando precisa ser uma linha física. Quebra de linha logo depois de `/compact` faz ele rodar sem as instruções; citação com `>` também atrapalha.
- Entregue a linha para o usuário colar: quem roda é ele. Depois de compactar, releia os arquivos listados e siga do próximo passo.

## Regras esquecidas
Funciona sem ferramenta: está tudo na conversa.

1. **Colete, do começo ao fim:** instruções (idioma, grafia, tom, tamanho, formato, o que evitar, como tratar) e decisões travadas (público, ferramenta, nome, número, prazo). Vale mesmo dita uma vez, sem "sempre". Só o que o usuário disse ou aceitou.
2. **Fica de fora:** pedido pontual já cumprido; instruções de sistema, de Projeto e CLAUDE.md (são recarregados, não desbotam); segredo (nem em parte); dado pessoal (escreva a regra pelo efeito).
3. **Regra que mudou:** só a última, com "(antes: X)". Pista depois do pedido: confira primeiro e varra tudo mesmo assim.
4. **Refaça a resposta** (a última antes do pedido ou a que a pista apontar). Se ela enviou, apagou, publicou ou pagou algo, nunca repita a ação: mostre a versão corrigida como rascunho e pergunte. Confira regra por regra nas palavras reais. Não quebrou nenhuma: uma linha dizendo isso. Quebrou: reescreva do zero, mesma substância, a corrigida primeiro, sem desculpa.
5. **Bloco "Regras deste chat":** num bloco de código, regras numeradas, até 10, cada uma com cerca de 15 palavras e começando por verbo, no idioma em que foram ditas. Passou de 10: fique com as quebradas, funda as afins, nunca corte a da pista.
6. Daí em diante, siga o bloco sem mencioná-lo. Conversa compactada: avise numa linha que pode faltar coisa. Nenhuma regra encontrada: peça a regra em uma linha.

## Código-palavra (alarme barato)
Se o usuário quiser: uma frase fixa no início de toda resposta. Quando some, a conversa começou a perder instruções antigas, e quem confere é o usuário, não o Claude julgando a si mesmo. Ao ligar, a resposta já começa com ela e diz em poucas linhas para que serve e como desligar. Frase que o Claude diria por hábito ("Ok"): avise e sugira uma incomum, respeitando a escolha. É alarme, não garantia, e vale só nesta conversa, salvo se a passagem a religar.
