# Lançamentos

## Campos
Data, conta débito, conta crédito, valor com centavos, histórico (o quê, quem, para quê e de que período), número do documento, competência, preparador e data, aprovação conforme a alçada, indicador de estorno e data do estorno.

## Fluxo
Identifique o fato; escolha as contas; apure o valor (líquido ou bruto); trate o imposto (pela linha do arquivo de dados ou pelo documento); redija; cheque; aprove pela alçada.

## Checagens antes de liberar
1. Débito = crédito, sem tolerância.
2. Conta existe no plano.
3. Documento presente e único.
4. Data no exercício aberto.
5. Valor negativo não entra: corrige-se por estorno.
6. Conta ligada a imposto exige alíquota válida, com id ou documento.

## Modelos
Lançamento simples e composto, com linha de soma e a marca "débito = crédito".

| Tipo | Partida | Cuidado |
|---|---|---|
| Serviço ou compra recebidos sem nota | débito despesa; crédito provisão | base: pedido, contrato, recorrente; estorne no mês seguinte; compare real com provisionado |
| Depreciação | débito despesa; crédito depreciação acumulada | adições e baixas; contábil não é fiscal |
| Despesa antecipada | débito despesa; crédito antecipada | cronograma com início, fim e valor mensal |
| Folha | salário, encargos, férias e 13º por competência | a parte do empregado é descontada do líquido |
| Receita | reconhecer com conta a receber; diferir adiantamento | CPC 47 pede obrigação de desempenho: registre o critério |

## Exemplos brasileiros, com a alíquota do documento
- **Venda com imposto na nota:** débito clientes; crédito receita; débito imposto sobre vendas; crédito imposto a recolher.
- **Serviço prestado com ISS retido pelo tomador:** o valor recebido é o líquido; a retenção é conta própria, não despesa de quem recebeu sem conferir.
- **Compra de mercadoria com crédito de imposto (regime que permite):** o imposto recuperável não vai ao custo.
- **Pagamento de imposto apurado:** débito imposto a recolher; crédito banco.
- **Optante pelo Simples:** o DAS, como regra, vira despesa ou dedução do mês, sem crédito destacado na venda; o critério do escritório manda.
Sempre com a conta do plano real e o valor do documento.

## Checklist do revisor
Débito = crédito; período correto e aberto; contas existem e fazem sentido; a conta bate com o suporte; histórico suficiente para auditoria; centro de custo, se houver; coerente com os períodos anteriores e a política; estorno configurado; suporte anexado; dentro da alçada; não duplica outro lançamento; valor grande ou estranho justificado.

## Erros comuns
Desbalanceado; período errado; sinal trocado; duplicado; conta de código parecido; provisão sem estorno, que conta duas vezes; provisão velha não atualizada; valor redondo demais, sinal de estimativa sem cálculo; capitalizar ou despesar errado; erro de corte.

## Exportação
Leiaute de importação depende do sistema contábil do escritório: pegue o exemplo real na camada pessoal. Sem exemplo, entregue a tabela e diga que o leiaute falta.
