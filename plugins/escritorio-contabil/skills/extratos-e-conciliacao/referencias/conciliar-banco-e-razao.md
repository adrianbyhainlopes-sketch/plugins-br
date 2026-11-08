# Conciliar banco e razão

## Demonstrativo em duas metades
Os dois ajustados têm de ser iguais; diferença 0,00.

| Metade | Conta |
|---|---|
| A. Banco | saldo do extrato + depósitos em trânsito − pagamentos não compensados ± erros do banco = banco ajustado |
| B. Razão | saldo do razão + créditos do banco não lançados − débitos do banco não lançados ± erros do razão = razão ajustado |

Os itens da metade do banco não pedem lançamento; os da metade do razão pedem. Marque "CONCILIADO" ou "DIFERENÇA" com o valor.

Se vier só um arquivo, pergunte qual fonte ele é. Confirme o mapeamento de colunas quando ambíguo. Use a conciliação do mês anterior para comparar o saldo de abertura. Título: entidade, "CONCILIAÇÃO BANCÁRIA", período e banco.

## Três categorias de item
1. **Temporal:** some sozinho no ciclo normal e não pede lançamento (transferência que compensa no dia seguinte, depósito em trânsito).
2. **Pede ajuste:** tarifa, juros, valor ou conta errados, duplicidade, lançamento faltando. Prepare a proposta de lançamento de correção.
3. **Pede investigação:** sem causa, contestado, velho ou recorrente. Documente e escale.

## Idade e tolerância (padrão; o escritório ajusta)
Idade: 0 a 30 dias, acompanhar; 31 a 60, investigar; 61 a 90, escalar; acima de 90, gerência e possível baixa. Tolerância: zero para banco, clientes, fornecedores e grupo; centavos só em recálculo de imposto, com o motivo.

Relatório de pendências: número, descrição, valor, data de origem, idade, categoria, status, responsável. Compare a quantidade e o total com o período anterior: item que aparece todo mês aponta problema de processo.

## Rastro da divergência
Busque o lançamento (id, data, origem, lote, preparador) e a transação (id, datas, contraparte, origem). Alinhe os atributos: data, mapeamento de conta, sinal, valor. O atributo que difere costuma ser a causa.

Frase de causa: "<lado> <fez o quê> porque <motivo>", com a consequência. Saída por divergência: chave; causa; dono (operação, cadastro, contabilidade ou sistema de origem); data prevista de resolução ou nula; ação (acompanhar, ajustar, abrir chamado, suprimir). Esta etapa só diagnostica.

## Razão e auxiliar
Saldo do razão e relatório do auxiliar (clientes, fornecedores, imobilizado, estoque) na mesma data. Controle de soma: soma dos saldos individuais = saldo da conta coletiva. Causas típicas: lançamento manual direto na conta de controle; movimento do auxiliar não integrado; lote em outro momento; reclassificação só no razão.

## Conta de imposto
- Imposto calculado = conta a recolher = valor declarado (amarração tripla).
- Movimentação: saldo inicial + débitos do período − créditos − pagamento do período anterior = saldo final = valor a pagar, comparado ao razão.
- Razoabilidade: base × alíquota da linha vigente do arquivo de dados, com tolerância de centavos, citando o id.

Regra de quem concilia: quem concilia não lança naquela conta. Preparador, revisor e data em todo papel de trabalho.
