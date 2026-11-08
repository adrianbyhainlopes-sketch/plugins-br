# Fórmulas gerenciais de pequeno negócio

Toda conta segue `evidencia-numerica.md`: só números do usuário, desconhecido fica desconhecido, conta mostrada. Imposto sobre a receita, encargo ou limite vem do arquivo de regras fiscais, pela data do fato; sem linha vigente, o valor é desconhecido e o resultado é parcial.

## 1. Margem de contribuição
- Receita líquida = vendas − descontos − devoluções.
- Custos variáveis = tudo que sobe e desce com cada venda: custo do produto ou do serviço prestado, embalagem, frete pago, taxa da maquininha ou do marketplace, comissão, **imposto sobre a receita** (no Simples, pela alíquota efetiva; em outro regime, pelas alíquotas dele).
- Margem de contribuição (em R$) = receita líquida − custos variáveis.
- Margem de contribuição (em %) = margem em R$ ÷ receita líquida (denominador nomeado; só se for positivo).
- Por unidade: preço líquido − custos variáveis por unidade.
- Antes e depois de anúncio: a margem depois de anúncio = margem antes − anúncio alocado àquele produto ou canal.
- Custo fixo e retirada do dono ficam **fora** da margem de contribuição; aparecem uma vez, no total.
- Custo compartilhado só é rateado com regra dada pelo usuário; sem regra, fica num total à parte, e o rótulo não diz "depois de todos os custos".
- Cortar um produto não corta o custo fixo rateado a ele: separe a contribuição perdida dos custos que de fato param.

## 2. Ponto de equilíbrio
- Em receita: custos fixos do período ÷ margem de contribuição em %.
- Em unidades: custos fixos ÷ margem de contribuição por unidade.
- Com retirada do dono: some a retirada aos fixos e diga que somou.
- Com vários produtos: use a margem média ponderada pelo mix **atual** e diga que o ponto muda se o mix mudar.
- Margem de contribuição zero ou negativa: não há ponto de equilíbrio; diga isso em vez de dividir.

## 3. Preço
- Preço que cobre custo e meta: preço = (custo variável unitário em R$ + parcela do fixo por unidade, se o usuário quiser) ÷ (1 − soma dos percentuais sobre o preço: imposto sobre a receita, taxa de cartão, comissão, margem desejada).
- Se a soma dos percentuais chega a 100% ou passa, o preço não existe: diga qual percentual precisa cair.
- Markup (multiplicador) = 1 ÷ (1 − soma dos percentuais). Mostre o markup e o preço; não chame margem de markup nem o contrário.
- Desconto: com margem de contribuição m e desconto d (ambos sobre o preço), as vendas precisam crescer m ÷ (m − d) vezes para manter a mesma contribuição total. Se d ≥ m, nenhum volume compensa. A fórmula supõe custos variáveis fixos em R$ por unidade; a parte que é percentual do preço (imposto sobre a receita, taxa de cartão) cai junto com o preço, e então a conta se refaz linha a linha.
- Preço de concorrente ou "de mercado" só entra se o usuário der, como referência dele.

## 4. Caixa projetado
- Por semana ou por mês: saldo inicial + recebimentos previstos − pagamentos previstos = saldo final, que vira o inicial do período seguinte.
- Recebimento entra na data em que o dinheiro cai, não na data da venda: venda no cartão de crédito, boleto e venda a prazo entram pelo prazo que o usuário der.
- Separe o certo (contratado, já vendido) do provável (previsto) e mostre o saldo nos dois cenários.
- Marque o primeiro período com saldo negativo e o tamanho do buraco.

## 5. Capital de giro e ciclo de caixa
- Prazo médio de recebimento (PMR) = contas a receber ÷ vendas a prazo do período × dias do período.
- Prazo médio de estoque (PME) = estoque médio ÷ custo das vendas do período × dias do período.
- Prazo médio de pagamento (PMP) = contas a pagar a fornecedores ÷ compras a prazo do período × dias do período.
- Ciclo de caixa = PMR + PME − PMP (em dias). Positivo: o negócio financia o cliente por esse tempo.
- Necessidade de capital de giro, aproximada = custo de um dia de operação × ciclo de caixa. Diga que é aproximação.
- Serviço sem estoque: PME = 0.

## 6. Quanto pagar por cliente (payback)
- **Teto por cliente** = margem de contribuição por venda (em R$) × vendas por cliente dentro da janela de retorno. Assinatura: preço mensal × margem de contribuição em % × meses da janela. Janela padrão de 12 meses, dita como suposição; janela menor aperta todos os tetos.
- Com saída mensal de clientes c (só se o usuário der): teto = preço × margem × (1 − (1 − c)^w) ÷ c, com w os meses da janela. Valor do cliente na vida toda só se pedido, com horizonte de até 36 meses.
- **Cadeia descendente**, só com as taxas do usuário: teto por cliente → por contato que vira cliente (× taxa de contato que vira cliente) → por clique ou mensagem (× taxa de clique que vira contato) → por pessoa alcançada (× taxa de alcance que vira clique). Taxa observada sempre substitui a suposta; depois do teste, refaça a cadeia inteira.
- Taxa que o usuário não tem: dê a fórmula e o teste que a mediria, nunca uma taxa "típica".
- **Com valor cotado** (impulsionamento, parceria): clientes necessários = valor ÷ teto por cliente (exato e arredondado para cima); clientes esperados = alcance × taxas da cadeia; quanto do valor volta na janela, em %, e quanto falta; quantas vezes a taxa combinada teria de ser maior.
- **Veredito:** Vai (paga com taxas observadas); Teste pequeno antes (só paga com taxas supostas, ou valor desconhecido); Agora não (não paga com taxas observadas, estoura o caixa ou falta pré-requisito).
- Crédito de anúncio, cupom e mês grátis: valor de face não é custo. Depende de se aqueles meses seriam pagos. Sem a informação, os dois cenários e o fato que decide.
- Limite mensal de caixa é separado do orçamento total da campanha.
- **Teste pequeno com limiar declarado antes:** "com R$ V em N dias, o teste passa se trouxer ao menos k clientes (ou contatos)". k sai da conta acima, proporcional ao valor do teste (k = V ÷ teto por cliente, arredondado para cima; em contatos, dividido pela taxa de contato que vira cliente, se o usuário tiver). Fixe V, N e k antes de rodar e compare depois; é decisão de negócio, não prova estatística.

## 7. Índices
Tabela: índice | numerador | denominador | atual | anterior | variação. Explicação obrigatória quando a variação passa do limite que o usuário escolher (padrão: 25%, dito como padrão ajustável).
- Margem bruta = (receita líquida − custo das vendas) ÷ receita líquida.
- Margem líquida = resultado do período ÷ receita líquida.
- Liquidez corrente = ativo circulante ÷ passivo circulante.
- Despesa sobre receita = despesa ÷ receita líquida, por grupo.
- Ticket médio = receita líquida ÷ número de vendas (diga se "venda" é pedido ou item).

## 8. Custo total de um empregado
Custo mensal = salário bruto + encargos do empregador + provisões (13º, férias e o adicional de férias, se o regime pedir) + benefícios pagos pela empresa. Os percentuais de encargo dependem do regime tributário e vêm do arquivo de regras fiscais; sem linha vigente, a parte dos encargos fica desconhecida e o resultado é parcial. Compare com a receita que a contratação precisa trazer: custo mensal ÷ margem de contribuição em %.
