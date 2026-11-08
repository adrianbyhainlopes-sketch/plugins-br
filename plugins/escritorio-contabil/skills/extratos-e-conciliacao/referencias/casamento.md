# Casamento linha a linha

Casa duas listas (extrato com razão, depósitos com faturas) sem chute. Vale para qualquer conciliação desta skill.

## Antes de casar
Defina as colunas de cada lado, o sinal (um lado pode trazer saída como negativa e o outro como positiva) e a janela de data combinada. Sem combinar, a janela é a data exata.

## Ordem de tentativa
Cada linha casa uma vez só. Em cada passo, só se casa quando há **uma** combinação possível.

| Passo | Critério | Grau |
|---|---|---|
| 1 | referência ou documento igual nos dois lados | casado |
| 2 | valor exato + data exata + descrição com elemento comum | casado |
| 3 | valor exato + data na janela + descrição com elemento comum | casado, com a diferença de dias dita |
| 4 | valor exato + data na janela, sem elemento comum | olhada, com o motivo |
| 5 | 1 para N: uma linha cobre várias do outro lado | olhada, com **todas** as combinações |
| 6 | N para 1: várias linhas somam uma do outro lado | olhada, com todas as combinações |

## Regras
- **Nunca o primeiro com o mesmo valor.** Dois lançamentos iguais na mesma janela são lista de candidatos; não se escolhe.
- Valor próximo não força casamento. Tolerância de valor só se combinada, com o motivo, e a diferença vai para coluna própria.
- Combinações somando um valor: procure só entre linhas do mesmo cliente ou contraparte e diga quantas combinações existem; uma só é provável, e pede confirmação; várias ou nenhuma, liste sem escolher.
- Transação legítima repetida não é duplicidade. Duplicidade só comprovada, com os dois ids.
- Com código, use aritmética decimal e centavos inteiros.

## Saída
Três grupos: casados (com o passo usado), olhada (motivo e melhor palpite, sem escolher entre candidatos) e sem par (por lado, com idade). Fechamento por lado: linhas = casadas + olhada + sem par. A soma de cada grupo é dita, e a diferença entre os lados é explicada pelos itens listados.
