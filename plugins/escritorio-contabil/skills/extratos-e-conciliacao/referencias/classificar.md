# Classificar extrato, com portão antes de qualquer total

## Sequência
1. Tire as linhas que não movimentaram dinheiro.
2. Compense pré-autorizações e estornos dentro do mesmo estabelecimento.
3. Ache o mesmo gasto em duas fontes (cartão e conta) e escolha a preferida, dizendo qual.
4. Busque o veredito no mapa.
5. Confira a contagem: linhas de entrada = linhas classificadas, todas num balde.

## Mapa de vereditos
Arquivo JSON do cliente, fora do plugin. Chave: trecho em minúsculas do nome do estabelecimento ou da descrição; valor: o balde.
- Vence a chave mais longa que casar. Torne a chave específica em vez de depender da ordem.
- **Nunca use o nome do intermediador de pagamento como chave**: ele aparece em estabelecimentos diferentes e engoliria todos.

## Baldes
`receita` · `entrada que não é receita` (empréstimo, aporte, reembolso) · `despesa da atividade` · `despesa rateada` (com a fração, aplicada uma vez) · `retirada ou pró-labore` · `imposto ou contribuição` · `transferência interna` · `tarifa bancária` · `revisar`. Código desconhecido é erro: falha fechado.

## Resolver pendências
- Maior valor absoluto primeiro.
- Decida sozinho quando o nome ou a referência não deixam dúvida.
- Na dúvida, **uma pendência por vez**: cada opção traz o valor, a direção, a consequência em linguagem simples e a referência do pagamento entre aspas.
- Grave cada decisão no arquivo na hora.
- Não pergunte de novo o que já está decidido no mapa. Para mudar: edite o mapa e reclassifique.

## Portão
Com pendência ou item `revisar`, não saem totais: liste cada um. Só repita até a contagem dar certo e as pendências chegarem a zero.

## Resumo
Por balde, com quantidade e soma. Fechamento: entradas = soma dos baldes, com desconhecidos em zero.

Moeda estrangeira: taxa oficial do dia, guardada ao lado de cada linha, com a fonte.
