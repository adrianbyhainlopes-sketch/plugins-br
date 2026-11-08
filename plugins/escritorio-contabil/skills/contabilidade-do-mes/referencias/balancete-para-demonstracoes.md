# Balancete para demonstrações

Mecânica do Excel: use a skill de planilha que houver. O método abaixo vale para qualquer ferramenta.

## 1. Preparar o balancete
- Remova linhas de subtotal e de grupo antes de classificar. É o erro mais comum.
- O código hierárquico do plano de contas, se houver, é a regra de prioridade zero.
- Saldo único com sinal: débito menos crédito, ou coluna única com sinal, ou sufixo D/C.
- **Prova:** a soma dá 0. Se não der, é balancete antes do encerramento, e a diferença é o resultado do período.

## 2. Aba de mapeamento
Número da conta; conta; saldo atual; saldo anterior; categoria (ativo circulante e não circulante, PL, passivo circulante e não circulante, receita, despesa); subcategoria (a chave do `SOMASES`); nota.

Regras em ordem de prioridade; a primeira que casar vence:
1. Natureza no nome: "a pagar" ou "credor" é passivo; "a receber" ou "devedor" é ativo; adiantamento de cliente é passivo; adiantamento a fornecedor é ativo.
2. Nome exato conhecido.
3. Palavras-chave por grupo.
4. Nome de pessoa ou empresa (conta corrente): saldo devedor é ativo, credor é passivo.
5. Grupo do sistema de origem. Grupo "empréstimos" com saldo devedor é empréstimo concedido.

Parte das contas sempre pede julgamento: mostre a lista "a confirmar" e não classifique por palpite.

## 3. Fórmulas
- Multiplicador de sinal: +1 para ativos e despesas; −1 para PL, passivos e receitas. Valor apresentado negativo é conta redutora válida ou classificação errada: confira.
- Cada célula das demonstrações é um `SOMASES` sobre a aba de mapeamento, sem número digitado. Excel em português usa `;`.
- Linha de checagem no rodapé: ativo − (PL + passivo) = 0. Antes do encerramento, PL = contas de PL + resultado do ano.

## 4. DFC indireta só do mapeamento
Lucro antes do imposto + depreciação + despesa financeira − receita financeira ± ganho ou perda na venda de bens; capital de giro = atual − anterior por grupo, com sinal invertido nos ativos; investimentos = variação do imobilizado bruto e dos investimentos; financiamentos = variação de empréstimos, juros pagos. **O caixa final tem de bater com o caixa do BP.**

## 5. Ajustes e reclassificações de fim de período
Provisões, diferimentos, depreciação, perda estimada com clientes, estoque obsoleto, tributos. Dívida que vence em 12 meses passa para o curto prazo; contas redutoras ficam líquidas na apresentação.

## 6. Quadro de movimentação do imobilizado
Saldo inicial, adições, baixas e saldo final; o mesmo para a depreciação; líquido atual e anterior.

## 7. Comparativo
Valor; variação em valor e em %; conta zerada no ano com saldo no anterior aparece. A revisão final pode usar a skill confere-numeros.
