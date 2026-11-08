# PDF de nota: plano B

Use só quando não há XML. Peça o XML primeiro: é o documento autorizado.

## Regras
- Classifique antes: é nota? Se não, diga o motivo.
- Transcreva o cabeçalho antes dos itens.
- Campos críticos, conferidos de novo: número, emitente, CNPJ, data, chave, valor líquido, imposto, total.
- Preserve todos os dígitos, inclusive zeros à esquerda.
- Use os totais impressos. Não calcule o que não está impresso. Não mude preço nem quantidade de descrição.
- Trazer menos itens é aceitável: cabeçalho e totais certos importam mais.
- Ilegível vira nulo, com confiança baixa e o motivo. Não adivinhe.

## Esquema por página
id da página · é nota · número · emitente · CNPJ · data · itens (descrição, quantidade, unitário, total) · líquido · imposto · alíquota · total · confiança (alta, média, baixa) · notas.

## Validação
- Confiança baixa fica no registro, marcada.
- Duplicada sai do registro e vai para o relatório.
- Resumo com contagens, totais e número de alertas.
- Antes do lote inteiro, teste numa amostra.

Se a nota tiver chave de acesso impressa, a chave é o que liga o PDF ao XML: peça ao usuário para baixar o XML pela chave.
