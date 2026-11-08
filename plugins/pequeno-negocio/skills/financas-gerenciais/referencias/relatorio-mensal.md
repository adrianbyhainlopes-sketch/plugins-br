# Relatório mensal ao dono

Pequeno negócio raramente tem orçamento. A base de comparação padrão é o **mês anterior** (tendência) e o **mesmo mês do ano anterior** (sazonalidade); orçamento ou meta só se o usuário tiver.

## Fluxo
1. **Dados:** o que o usuário colar (planilha, extrato resumido, DRE do contador, relatório da maquininha ou do sistema). Peça o período atual, o de comparação e os ajustes já conhecidos (venda fora do comum, despesa do ano pago de uma vez).
2. **DRE gerencial simples em colunas:** atual | comparação | variação em R$ | variação em %.
   - Receita bruta → (−) descontos e devoluções → receita líquida → (−) custos variáveis (produto, embalagem, frete, taxas de venda, comissão, imposto sobre a receita) → **margem de contribuição** → (−) despesas fixas por grupo (pessoal, aluguel, sistemas, outras) → **resultado operacional** → (−) retirada do dono, se o usuário quiser vê-la aqui → **sobra do mês**.
   - Diga que é visão gerencial, não demonstração contábil. Resultado não é sobra de caixa: se o usuário quiser o caixa, use a seção 4 de `formulas-gerenciais.md`.
3. **Variação por linha:** em R$; em % sobre o valor absoluto do período de comparação; margens em pontos percentuais.
4. **Indicadores em pontos percentuais:** crescimento da receita, margem de contribuição, margem operacional, despesa fixa sobre receita, ticket médio e número de vendas (se houver).
5. **Variações relevantes:** linha, valor, %, direção, causa provável, ação.
6. **Perguntas** sobre o que ficou sem explicação, numa rodada só.

## O que é relevante
Dispara pelo valor **ou** pelo percentual. Padrões ajustáveis, ditos como padrão: variação acima de 15% contra o mês anterior, ou acima de 1% da receita do mês em valor. Linha grande pede um percentual menor para disparar. Ordem de investigação: maior valor absoluto, maior %, direção inesperada, linha que era estável e saiu do trilho, tendência que cresce há meses.

## Preço e volume
- Efeito volume = (quantidade atual − quantidade anterior) × preço anterior.
- Efeito preço = (preço atual − preço anterior) × quantidade atual.
- A soma dos dois tem de dar a variação da receita: confira e diga que conferiu.
- Com vários produtos e mudança de mix, separe três efeitos, cuja soma também tem de dar a variação total:
  - volume = (quantidade total atual − quantidade total anterior) × preço médio anterior (com o mix anterior);
  - mix = Σ (quantidade atual do item − quantidade total atual × participação anterior do item) × preço anterior do item;
  - preço = Σ (preço atual do item − preço anterior do item) × quantidade atual do item.
  Se não fechar, mostre a diferença; não force.

## Causas de variação
Volume, preço, mix, produto novo ou descontinuado, fato que não se repete, deslocamento no tempo (pagamento adiantado ou atrasado), sazonalidade. Despesas por natureza: ligadas a pessoas, ligadas ao volume, discricionárias, contratuais ou fixas, pontuais.

## Narrativa por variação (2 a 4 frases)
- Linha; favorável ou desfavorável; valor e %; base de comparação; período.
- **Causa:** com números do usuário.
- **Perspectiva:** pontual, continua, melhora ou piora.
- **Ação:** nenhuma, acompanhar, investigar ou rever a projeção.

Não fazer: causa circular ("a receita subiu porque vendeu mais", sem dizer o quê); "foi pontual" sem dizer o que foi; "deslocamento no tempo" sem dizer o que adiantou ou atrasou e quando normaliza; "vários itens pequenos" numa variação relevante; falar só da maior causa e esquecer as que compensam.

## Ponte do resultado
Início + soma das causas = fim (confira). De 5 a 8 causas em ordem lógica, o resto em "outros". Em texto ou tabela (causa | valor | % da variação | acumulado); um % pode passar de 100% quando há causas que compensam. Gráfico, se pedirem, com a skill de visualização que houver.

## Índices
Tabela da seção 7 de `formulas-gerenciais.md`, com explicação quando a variação passar do limite escolhido.

## Formato do relatório
1. **Resumo em 3 linhas:** como foi o mês, a principal causa, a decisão que o dono precisa tomar.
2. DRE gerencial com as colunas.
3. Variações relevantes com a narrativa.
4. Ponte do resultado.
5. Três ações para o mês seguinte, cada uma ligada a uma linha.
6. O que não deu para calcular e por quê (resultado parcial).

Valores no formato brasileiro (R$ 1.234,56; datas DD/MM/AAAA), pelas regras de `formatos-br.md`.
