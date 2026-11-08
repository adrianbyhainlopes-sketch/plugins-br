# Recebimentos e repasses

## Faturas pagas
**Paga, só com os três:** valor exatamente igual; descrição com o número da fatura ou o nome do cliente (ou abreviação clara); data do depósito igual ou posterior à da fatura.

**Precisa de olhada,** com motivo e melhor palpite:
- valor bate sem nome nem número (um candidato: "provavelmente paga, confirme"; vários: liste todos);
- nome bate e valor não (pagamento a menor ou a maior: mostre a diferença);
- valor agrupado (um depósito pode cobrir várias faturas do mesmo cliente: mostre todas as combinações, ver `casamento.md`);
- repasse de maquininha ou intermediador (lote de pagamentos menos tarifa: confira o relatório do intermediador);
- depósito antes da data da fatura (adiantamento: não marque paga);
- possível pagamento em dobro.

**Em aberto:** faturas sem depósito plausível, as mais atrasadas primeiro, com dias de atraso se houver vencimento.

**Separados:** estornos, tarifas e juros, transferências entre contas do próprio dono, entradas que não são de cliente (empréstimo, aporte). Liste curto, para mostrar que foram vistos.

**Fechamento:** faturas = pagas + em aberto + olhada; depósitos = casados + olhada + separados. Some ao centavo.

Saída: PAGAS, EM ABERTO, PRECISA DE OLHADA (cada uma com quantidade e total), SEPARADOS, Resumo e um próximo passo útil. Só relata: não muda sistema, não marca fatura paga, não contata cliente.

## Repasse de maquininha e marketplace
1. **Identifique:** vendedor, canal, período, moeda, versão do relatório e o que cada linha representa. Diga se o agrupamento é pela data da transação ou da venda original; devolução tardia pertence à venda antiga.
2. **Mapeie campos em categorias:** mercadoria, desconto, devolução, frete, imposto, taxa e crédito de taxa, antecipação, chargeback, anúncio. Pergunte se a "venda líquida" já desconta a devolução e se o repasse já desconta as taxas. Cada valor vai para uma categoria só.
3. **Junte** pelos ids de pedido, linha e devolução. Não multiplique frete ou taxa do pedido pelos itens. Importação repetida não é compra repetida.
4. **Separe** cancelamento, reembolso, devolução física. Crédito de taxa fica separado da taxa.
5. **Mostre como cada relatório fecha:** incluídos + excluídos + em aberto = total original. Não force. Causas típicas: tempo, retenção, impostos, frete, ajustes, cobertura incompleta.

Saída: ponte compacta de vendas para devoluções, despesas de venda, itens de tempo e repasse esperado, comparado com o recebido, com os ids ao lado. Armadilha: devolução que o relatório líquido já descontou não pode ser subtraída de novo. Repasse não é receita.

Taxa de maquininha e prazo de recebimento: só os do relatório ou do contrato do usuário.
