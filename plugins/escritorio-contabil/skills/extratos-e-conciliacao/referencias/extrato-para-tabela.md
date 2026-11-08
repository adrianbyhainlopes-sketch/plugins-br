# Extrato para tabela

## Fluxo
1. **Veja o que é o arquivo.** PDF com texto: `pdftotext -enc UTF-8 -table arquivo.pdf extrato.txt` no `pdftotext` 4.00 que vem com o Git for Windows (no modo `-layout` dele, as colunas podem sair deslocadas de linha); no do Poppler, `-layout`. Olhe 5 linhas: data, descrição e valor têm de estar na mesma linha; se não estiverem, troque o modo (`-table`, `-lineprinter`, `-simple`, `-layout`). Sem `pdftotext`, leia o PDF pela ferramenta do ambiente. Texto vazio ou quase: é escaneado.
2. **Escaneado:** uma ou duas páginas, leia visualmente e digite a tabela. Mais que isso, OCR em português se houver (`tesseract -l por`), mais lento e menos exato; a prova pelo saldo continua obrigatória.
3. **Escolha o formato** em `bancos-br/`: compare o texto com o modelo. Empate entre dois é normal; teste os dois e fique com o que concilia. Pontuação alta não garante formato certo: a prova é sempre o saldo.
4. **Rode:**
   ```bash
   python -I scripts/extrato.py --formato referencias/bancos-br/dc-por-linha.json --entrada extrato.txt --saida extrato-tabela.csv --xlsx extrato-tabela.xlsx --ano 2026
   ```
5. **Leia o resultado.** Só entregue com "SALDO BATE". O código de saída 2 significa não bate ou prova incompleta.
6. **Confira por amostra:** primeira linha, última, um total, contra o PDF. Diga que conferiu.

## Tabela de saída
`data` (AAAA-MM-DD) · `descricao` · `valor` com sinal · `saldo_impresso` · `saldo_calculado` · `diferenca` · `referencia` · `tipo` (`movimento`, `saldo_inicial`, `saldo_final`) · `pagina` e `linha_origem`. Documento e referência são texto. O `--xlsx` grava a planilha com número como número e data como data, sem depender de biblioteca; o CSV é o que o `ofx.py` lê.

Conta em moeda estrangeira: colunas de cotação e valor convertido, sem misturar moedas no total.

## Dois modos de prova
- **Por linha:** cada movimento traz o saldo: saldo anterior + valor = saldo atual.
- **Por grupo:** saldo só em marcadores ("saldo do dia"): soma dos movimentos entre dois marcadores.
O programa compara cada linha com o saldo anterior **impresso**, para que uma quebra conte uma vez e não contamine as seguintes.

## Quando não bate
| A diferença | Significa | O que fazer |
|---|---|---|
| É o valor de um movimento | a linha não foi lida | procure valor sem descrição por perto, ou valor na linha de baixo |
| É o dobro de um valor | sinal D/C invertido | conserte o formato, não a planilha |
| Só no início e depois tudo bate | saldo inicial de período anterior | confira o saldo de abertura |
| Em todas as linhas | formato errado | teste outro modelo |
| Valores cortados ou gigantes | separador invertido | o último separador decide |
| Totais e texto legal entrando | faltam as linhas de fim de seção | acrescente em `ignorar` |
| Linhas repetidas por página | faltam cabeçalho e rodapé | acrescente em `ignorar` |

O mesmo banco muda de layout por produto e por ano. Irregular demais depois de 2 ou 3 tentativas: diga ao usuário.

Se o banco imprimir um saldo que nenhuma leitura consegue fechar, a diferença fica à vista como achado do extrato, com a página e o valor. Não invente movimento para fechar.

## OFX
Ler: `python -I scripts/ofx.py ler --entrada arquivo.ofx --saida tabela.csv --saldo-inicial 1000,00`. O arquivo traz a lista de movimentos e o saldo final, então a prova precisa do saldo inicial (ou diz qual ele deveria ser). `TRNAMT` tem o sinal do ponto de vista do cliente; `TRNTYPE` não muda o efeito no saldo; `FITID` repetido pode ser arquivo importado duas vezes (especificação OFX 2.2, seção 11.4.4 e 3.2.3).

Gerar: `python -I scripts/ofx.py gerar --entrada extrato-tabela.csv --saida extrato.ofx --banco 000 --conta 0000`. Recusa extrato com diferença, salvo com `--aceitar-diferenca`, e então diga isso. Teste a importação num ambiente de teste do sistema contábil antes de usar em produção.

## Dados do cliente
Número de conta, CPF e chave Pix não aparecem no chat. Um formato de banco nunca guarda dado do extrato de exemplo.
