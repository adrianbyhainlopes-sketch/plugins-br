# Ler um documento

## Leitura em 9 partes
1. **Remetente e tipo de documento**, sem acrescentar poderes ou como o órgão costuma agir.
2. **O que pedem:** cada pedido em palavras simples, com a linha de origem citada.
3. **Até quando**, nas palavras do documento.
4. **Se não:** só o que o documento diz, entre aspas; se não diz, "o documento não diz".
5. **Valores e referências:** tabela, caractere por caractere, com o que cada um é. O número de conta do próprio usuário é nomeado e conferido, não repetido inteiro. Aritmética sobre os valores é permitida e mostrada.
6. **O que conferir:** nome, número e endereço são seus; compare cada número de referência com os outros do documento (dois números quase iguais, com dígitos trocados, são achado: pergunte se são documentos diferentes); datas em ordem possível e dia da semana de toda data de prazo; valores somam; o que o documento diz que você fez bate com o que você sabe.
7. **Como falar com o remetente:** se pedem pagamento ou dados por canal inesperado ou dão prazo de horas, contatar pelos canais que você mesmo encontra.
8. **O que está ambíguo.**
9. **Perguntas numeradas ao remetente** e opções que o documento oferece (pagar, recorrer, responder), sem dizer qual é a certa.

## Cartão de leitura
Tabela de duas colunas: de · o que é · o que pedem · até quando · se não · valores e referências · ambíguo · pergunte a eles.

## "É grave?"
Responde só pelo documento: o que pede, até quando nas palavras dele e o que diz que acontece.

## Cláusula de contrato
Parte por parte: quem faz o quê, até quando, como, que dinheiro e quando. Diga o que a cláusula não diz. Não opine se é justa, legal ou exigível. As perguntas vão à outra parte e, sobre validade, a um advogado.

## Documento fiscal de escritório
Notificação da Receita, intimação, termo de exclusão do Simples, cobrança da prefeitura: separe o que é fato do documento (número do processo, período, valor, data de ciência) do que é hipótese do leitor. Liste os documentos que o próprio órgão pede e, ao lado, se o usuário já os tem (`[?]` onde não souber).

Quando o prazo contar a partir de ciência ou recebimento, peça a data e o comprovante; não a suponha pela data de emissão.

Ao citar norma que o documento cita, copie a citação; só diga o que ela determina se a norma estiver na tabela do plugin com status vigente para a data do fato.

## Registro do documento
Bloco de código, colável depois para atualizar:
```text
item:
órgão:
referência:
o que pedem:
valor:
prazo: (nas palavras do documento)
situação: aberto | enviado | aguardando | concluído
próxima ação:
confirmar com o órgão:
log: (linhas só acrescentadas; data não dada vira [data?])
guardar: (cópia, recibo, comprovante de envio)
```
"Concluído" só quando o usuário diz.
