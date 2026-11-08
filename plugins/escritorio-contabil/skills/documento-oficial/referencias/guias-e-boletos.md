# Guias e boletos

Confere DAS, DARF, GPS e boleto contra o que foi apurado. Regra de código de barras conferida no "Layout Padrão de Arrecadação/Recebimento com Utilização do Código de Barras", versão 08, FEBRABAN, vigência a partir de 01/06/2026 (lido em 08/11/2026).

## O que comparar
| Campo | Com o quê |
|---|---|
| CNPJ ou CPF | o cadastro do cliente, por referência |
| Período de apuração | a competência que se quer pagar |
| Vencimento | a linha do calendário (`dados/obrigacoes-br.csv`, se a skill de contabilidade estiver à mão) e a Agenda Tributária do mês |
| Valor principal, multa, juros, total | o apurado, com a soma mostrada |
| Código de receita (DARF) | o código da Agenda Tributária do mês; o nome do tributo tem de bater |
| Código de barras e linha digitável | o valor impresso e os dígitos, abaixo |

Não recalcule multa e juros de memória: diga o que está impresso e o que não pôde ser conferido. Guia vencida: diga, sem estimar o valor atualizado.

## Arrecadação: 44 posições (a representação numérica começa com 8)
| Posição | Tamanho | Conteúdo |
|---|---|---|
| 1 | 1 | Produto: constante 8 |
| 2 | 1 | Segmento: 1 prefeituras; 2 saneamento; 3 energia e gás; 4 telecomunicações; 5 órgãos governamentais; 6 carnês e assemelhados ou demais identificados pelo CNPJ numérico; 7 multas de trânsito; 9 uso exclusivo do banco |
| 3 | 1 | 6 valor em reais, dígito módulo 10; 7 quantidade de moeda ou referência, módulo 10; 8 valor em reais, módulo 11; 9 referência, módulo 11 |
| 4 | 1 | Dígito verificador geral |
| 5 a 15 | 11 | Valor (duas casas implícitas) |
| 16 a 19 | 4 | Empresa ou órgão |
| 20 a 44 | 25 | Campo livre; se trouxer vencimento, AAAAMMDD nas 8 primeiras posições do campo livre |

Na representação numérica, são 4 grupos de 11 posições, cada um seguido de 1 dígito (módulo 10 ou 11, conforme a posição 3). Os dígitos dos grupos não entram no código de barras.

## Cálculo
- **Módulo 10:** multiplique cada algarismo por 2, 1, 2, 1... da direita para a esquerda; some os **dígitos** dos produtos; dígito = 10 − resto da divisão por 10; resto 0 dá 0.
- **Módulo 11:** multiplique por 2, 3, 4, 5, 6, 7, 8, 9, 2, 3... da direita para a esquerda; some os produtos; dígito = 11 − resto; resto 0 ou 1 dá 0; resto 10 dá 1.
- **Dígito geral:** calculado sobre as 43 posições, sem a posição 4.

```python
def mod10(s):
    total = 0
    for i, c in enumerate(reversed(s)):
        p = int(c) * (2 if i % 2 == 0 else 1)
        total += p // 10 + p % 10
    r = total % 10
    return 0 if r == 0 else 10 - r

def mod11(s):
    total, peso = 0, 2
    for c in reversed(s):
        total += int(c) * peso
        peso = 2 if peso == 9 else peso + 1
    r = total % 11
    return 0 if r in (0, 1) else 1 if r == 10 else 11 - r
```
Exemplo do manual, conferido: módulo 10 de `01230067896` dá 3.

Quem confere: rode com `python -I` e diga "dígitos conferidos por código", ou mostre a conta. Linha que não bate: confira digitação antes de chamar de erro. Valor da posição 5 a 15 diferente do total impresso é Errado.

## Boleto bancário (47 dígitos, não começa com 8)
Este leiaute não foi lido na fonte primária: a checagem dos dígitos do boleto de cobrança fica **não verificada**. Compare valor, vencimento, beneficiário e o que estiver impresso, e diga que os dígitos não foram conferidos.

## DAS e DARF
- **DAS do Simples:** compare o período, o valor e o vencimento com o PGDAS-D; o vencimento vem de `OBR-SN-001` (dia não útil adia).
- **DAS do MEI:** o valor mensal vem de `FIS-MEI-002` para a data do fato, em `dados/regras-fiscais-br.csv`.
- **DARF:** o código sai da Agenda Tributária; se a guia tiver código diferente do tributo que se quer pagar, é achado.

Saída: tabela `campo | guia | apurado | situação`, a conta dos dígitos e a conclusão em uma linha ("guia confere", "não confere em: …", "não verificado: …"). Não diga que pode pagar: diga o que bate.
