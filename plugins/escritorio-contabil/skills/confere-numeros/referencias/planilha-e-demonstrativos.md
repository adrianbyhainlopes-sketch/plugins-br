# Planilha, demonstrativos e revisão forense

## 1. Fórmulas, em todo escopo
Erros (`#REF!`, `#VALOR!`, `#N/D`, `#DIV/0!`, `#NOME?`); número fixo dentro de fórmula (`=A1*1,05`: o 1,05 deveria ser célula); fórmula fora do padrão dos vizinhos; intervalo que perde a primeira ou a última linha; valor colado por cima de fórmula; referência circular; vínculo entre abas quebrado; escala misturada (mil e milhão, % como número inteiro); linhas e abas ocultas.

Número fixo colado por cima é a principal fonte de erro silencioso. Erro de sinal em saída de caixa é muito comum. Cálculo feito por macro não é auditável pela fórmula: diga que não foi coberto.

## 2. Modelo inteiro
Separação entre entrada e cálculo; convenção de cores aplicada com consistência; ordem das abas (premissas, DRE, balanço, fluxo de caixa); cabeçalhos de data e unidade iguais em todas as abas. Referência circular intencional exige chave de iteração que funcione; acidental, mostre como quebrar.

Relatório de planilha: `# | Aba | Célula | Gravidade | Categoria | Problema | Correção sugerida`, gravidade Crítico (resultado errado), Atenção (risco: número fixo, fórmula inconsistente), Info (estilo). No modelo inteiro, uma linha de resumo antes. Nada é alterado sem pedido.

## 3. Amarrações dos três demonstrativos
- Ativo = passivo + PL em todo período. Se não fecha, meça a diferença por período e ache onde quebra antes de tudo.
- Lucros acumulados anterior + lucro − dividendos = atual.
- Caixa final do fluxo = caixa do balanço.
- Operacional + investimento + financiamento = variação do caixa.
- Depreciação igual no fluxo e na DRE.
- Aquisição de imobilizado do fluxo bate com a movimentação do imobilizado.
- Sinais das variações de capital de giro coerentes com o balanço.
- Imposto próximo de lucro antes do imposto × alíquota, com a alíquota da linha do arquivo de dados ou do documento.

## 4. Revisão forense, nesta ordem
1. Ativo = PL + passivo. Causas típicas de diferença: imposto contado duas vezes; `ABS()` em conta redutora; coluna anterior puxando o bruto em vez do líquido; contas que só têm saldo anterior fora do mapeamento; multiplicador de sinal esquecido.
2. O lucro do período chega ao PL.
3. Caixa final da DFC = caixa do BP.
4. Total de cada nota = valor da linha correspondente na demonstração.
5. Negativo onde não devia: passivo negativo é erro de sinal; ativo negativo fora de redutora é classificação errada; receita negativa pede conferência; notação científica é resíduo de arredondamento.
6. Célula com número digitado em vez de fórmula.
7. Soma do balancete = 0, ou = resultado antes do encerramento. Se não, entrou subtotal ou faltou conta.
8. Comparativo completo: conta zerada no ano com saldo no anterior tem de aparecer.

Saída: `# | severidade (crítica, alta, média) | aba | célula | achado | correção sugerida`.

Sinais de alerta, sempre rotulados como indício sem valor de prova e sem limiar fixo: liquidez corrente baixa; dívida alta contra o PL; recebíveis crescendo muito mais rápido que a receita; prazo de estoque subindo com receita parada; caixa operacional negativo com lucro positivo; outras receitas ou despesas grandes sem abertura; um cliente concentrando grande parte da receita.

## 5. Revisar uma apuração
Identidades aritméticas (base = receita − deduções previstas); faixas e alíquotas contra as linhas vigentes do arquivo de dados, citando o id; documentos esperados que não apareceram; coerência entre partes do cálculo. Comparar regimes ou anexos só quando pedirem, e sempre como conta, não como recomendação tributária. Diga quem decide.
