# Power Query, quando pedem processo no Excel

1. Importe todas as colunas como texto e mantenha identificadores como texto.
2. Duplique o campo antes de converter, para o original continuar visível.
3. Use "Alterar tipo", "Usando localidade", com a convenção informada (Português do Brasil para `1.234,56` e dd/mm/aaaa).
4. Deixe erros e todas as linhas visíveis. Nunca troque erro por zero.
5. Crie uma coluna com o nome do arquivo de origem e o número da linha, para rastrear.
6. Ao unir, confira a contagem de cada chave antes da junção (mesma regra de `inspecionar-e-limpar.md`, seção 3).
7. Salve a consulta e explique como trocar o arquivo de origem e atualizar.

Excel em português: fórmulas de planilha com `;` e nomes em português; dentro do editor do Power Query a linguagem M usa nomes em inglês e vírgula entre argumentos.

Conferir depois de atualizar: contagem de linhas, soma por moeda e amostra de 2 ou 3 linhas contra a origem.
