# Lucro Presumido, retenções e reforma

Nenhum número fiscal fica neste texto. Use a linha vigente na data do fato. Status `a conferir` é desconhecido.

## Lucro Presumido
| Item | Linha |
|---|---|
| PIS e Cofins | `FIS-LP-001`; vencimento `OBR-LP-001` |
| Presunção do IRPJ, por atividade | `FIS-LP-002` |
| Presunção da CSLL | `FIS-LP-003` |
| Alíquota e adicional do IRPJ | `FIS-LP-004` |
| Alíquota da CSLL | `FIS-LP-005` |
| Acréscimo sobre receita maior que o limite | `FIS-LP-006`, a conferir: resposta parcial até confirmar a vigência |
| Trimestre e quotas | `OBR-LP-002` |

Conta: receita por atividade × presunção = base; base × alíquota; adicional sobre o que passar do limite do período; menos retenções já sofridas, com o comprovante. ISS, ICMS e IPI: da legislação ou da guia do usuário (`FIS-ISS-001`, `FIS-ICMS-001`).

Passo 0: confirme se a empresa é do regime no ano, e a data de opção.

## Retenções
`FIS-RET-001` (CSLL, Cofins e PIS), `FIS-RET-002` (INSS), `FIS-RET-003` (IRRF, a conferir), `FIS-SN-019` (ISS no Simples), `FIS-ISS-002` (mínimo e máximo do ISS). Vencimentos: `OBR-RET-001`, `OBR-RET-002`.

Retenção não é despesa de quem sofreu: é crédito ou antecipação, com comprovante. Conferir a incidência para optante do Simples antes de calcular.

## Reforma: IBS e CBS
Faça uma linha por ano, sem misturar `vigente` com `anunciado`.
- Ano de teste: `FIS-REF-002`, `FIS-REF-003` e `FIS-REF-004`. Simples: `FIS-REF-005`.
- 2027 em diante: `FIS-REF-006` e `FIS-REF-007`, anunciado; CBS depende de resolução do Senado; opção do Simples em `FIS-SN-022` e `OBR-SN-006`.

Se a data do fato cair em ano de transição, diga que a regra é a do ano e cite o id. O que não estiver na tabela é desconhecido.

## Preparador e revisor
Mesmo modelo de `apuracao-mei-simples.md`, com a seção por tributo.
