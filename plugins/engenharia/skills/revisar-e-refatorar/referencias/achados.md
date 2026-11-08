<!-- cópia gerada de compartilhado/achados.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Escala de achados

Uma escala só para toda revisão (tela, código, segurança), para que relatórios de skills diferentes possam ser juntados.

## Gravidade
| Gravidade | Quando |
|---|---|
| Crítico | impede a tarefa principal, perde ou expõe dado, ou deixa alguém sem acesso nenhum (por exemplo, nada alcançável pelo teclado) |
| Alto | quebra um estado ou um fluxo, induz a erro, ou falha critério de acessibilidade nível A, ou AA no caminho principal |
| Médio | atrapalha mas tem contorno: falha AA fora do caminho principal, deriva que encarece a próxima mudança, inconsistência visível |
| Baixo | acabamento, AAA, boa prática, ruído contado |

- Sobe um degrau quando está no caminho principal (a ação mais provável da tela) ou se repete pela página.
- Ordem no relatório: gravidade, depois impacto dividido por esforço (o que corrige mais com menos vem antes).

## Confiança
Cada achado diz quanto se sabe:
- **Confirmado:** medido, reproduzido ou lido no código, com a evidência citada.
- **Provável:** o sinal está lá, mas falta um passo para provar (por exemplo, visto na captura, não no código).
- **Precisa de verificação:** hipótese que vale checar; não entra na contagem de falhas.

## Não verificado (à parte)
O que dependia de algo que não houve (navegador, dispositivo real, leitor de tela, dado de produção) vai para uma lista separada, com o motivo. Nunca vira "passou".

## Teto
- No máximo 10 achados por revisão. Se houver mais, os 10 de maior gravidade e uma linha com a contagem do resto.
- Juntando várias revisões: uma tabela só, todo Crítico e Alto mantidos, o resto até 15 linhas; um defeito aparece uma vez, na revisão dona do assunto.
- "Nada a corrigir" é veredito válido.

## Formato do achado
Uma linha que afirma o problema (não pergunta), onde está (arquivo:linha, rota e seletor, ou região da captura), a evidência, a consequência para quem usa e a menor correção.
