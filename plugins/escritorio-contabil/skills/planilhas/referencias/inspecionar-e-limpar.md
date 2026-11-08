# Inspecionar, limpar e unir

## 1. Inspecionar
- Registre identidade do arquivo, abas, cabeçalhos, codificação, delimitador e contagem de linhas. Formato adivinhado é proposta até conferir que o arquivo lê certo.
- Entenda o que uma linha significa, os totais informados, as chaves, as convenções de data e número e quem vai abrir o arquivo.
- Em XLSX, distinga valor guardado, formato de exibição e texto da fórmula. Resultado salvo pode estar velho; não recalcule fórmula de terceiro.
- Cheque todas as linhas: largura inconsistente, cabeçalho duplicado, chave vazia ou repetida, tipos misturados, identificador que perdeu formatação. Se checou só amostra, diga.
- Saída: lista de arquivos e colunas; tabela de problemas com arquivo, aba e linha; mapeamento proposto separado das regras aprovadas; data ambígua mostra as datas possíveis; uma pergunta só, a que mais afeta o próximo passo.

## 2. Limpar
- Trecho ilegível: guarde os bytes e cite o intervalo, sem inventar número. Se não dá para saber onde os registros começam, diga que as contagens estão incompletas.
- Texto não resolvido em coluna numérica precisa de decisão antes de virar número; não vira vazio.
- Log de cada célula alterada: referência, coluna, antes, depois, regra.
- Fórmulas da origem são lidas e guardadas como texto, nunca trocadas pelo resultado salvo.

## 3. Unir
- Exemplo: dois pedidos do cliente `0042` e duas linhas de cadastro com a mesma chave viram 4 linhas; mantenha os pedidos e sinalize a chave, sem escolher o primeiro cadastro nem apagar nenhum.
- Conflito vira coluna de candidatos ou tabela de pendências, sem escolher.
- Numa junção, feche por lado: casados + não casados + não resolvidos + excluídos. Mostre a contagem de saída e os casamentos por chave separadamente (junção acrescenta colunas, não linhas).

## 4. Injeção de fórmula
Texto que começa com `=`, `+`, `-`, `@`, tabulação, CR ou LF (e as versões de largura total) é suspeito. Aspas no CSV não impedem a execução. Prefira XLSX com a célula tipada como texto. Negativos aprovados continuam números. Nunca execute macro, fórmula ou link das células.

## 5. Pendências
- Cada pendência ligada a arquivo, aba e linha; distinga valor aguardando decisão de registro excluído; uma linha pode ter várias pendências.
- Colunas: referência (sem dado pessoal), problema, escolhas possíveis, situação da decisão, evidência.
- Só marque como aprovado o que o usuário aprovou, no escopo que ele deu. Correção de uma linha não é regra para todas. Contradições ficam visíveis.
- Candidato parecido, valor vazio ou valor repetido sozinhos não autorizam unir, preencher ou apagar.
- Conte cada linha afetada uma vez (linhas 5 e 9 com 3 rótulos são 2 registros).

## Dados pessoais
Não repita e-mail, telefone ou endereço no chat: use referência de linha. Cópia para compartilhar leva só as colunas necessárias.
