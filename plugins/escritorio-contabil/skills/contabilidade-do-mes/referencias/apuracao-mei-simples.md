# Apuração de MEI e Simples Nacional

Nenhum número fiscal fica neste texto. Cada passo aponta para a linha do arquivo de dados; use a linha vigente na **data do fato**. A partir de 01/01/2027 há linhas `anunciado` (`FIS-SN-021`, `FIS-SN-022`, `FIS-MEI-010`, `FIS-MEI-011`): antes de apurar competência de 2027, confira se já viraram `vigente`.

## Passo 0: enquadramento do período
Regime no mês; atividades e anexo de cada uma; regime de receita (`FIS-SN-008`); início de atividade (data). Sem isso, a resposta é parcial.

## MEI
1. Valor mensal: `FIS-MEI-002`, com a contribuição `FIS-MEI-004` e o salário mínimo do ano (`FIS-SM-2026`). Competência, conforme `FIS-MEI-005`.
2. Limite anual: `FIS-MEI-001`; início de atividade: `FIS-MEI-003`; transportador: `FIS-MEI-006`.
3. Excesso: `FIS-MEI-007`, com o percentual calculado e mostrado, e a comunicação `OBR-MEI-005`.
4. Empregado: `FIS-MEI-008`.
5. Obrigações: `OBR-MEI-001` a `OBR-MEI-004`. Documento fiscal: `FIS-MEI-009` (até 2026) e `FIS-MEI-010` (anunciado).

## Simples Nacional
1. **Receita do mês, segregada** (`FIS-SN-020`): por anexo, por retenção de ISS, por substituição do ICMS, por tributação concentrada, exportação.
2. **RBT12** (`FIS-SN-001`). Início de atividade: `FIS-SN-007`. Zero: `FIS-SN-009`.
3. **Fator R**, se a atividade estiver na regra (`FIS-SN-015`): folha de 12 meses (`FIS-SN-016`) ÷ RBT12; casos sem histórico em `FIS-SN-017`. Mostre o r com 4 casas e o anexo resultante.
4. **Faixa:** `FIS-SN-010-F1` em diante para o anexo certo. A coluna `valor` tem `alíquota nominal|parcela a deduzir`.
5. **Alíquota efetiva** (`FIS-SN-002`): mostre a conta com os números.
6. **Partilha** por tributo: `FIS-SN-010-R1` em diante; teto do ISS em `FIS-SN-018`; ISS retido em `FIS-SN-019`; sublimite de ICMS e ISS em `FIS-SN-005`; exclusão e excesso em `FIS-SN-006`.
7. **Valor do DAS:** cada receita segregada × alíquota efetiva, sem o percentual do tributo já pago fora.
8. **Compare** com o PGDAS-D, a guia e o razão: apurado = conta a recolher = declarado.
9. **Vencimento e declaração:** `OBR-SN-001` e `OBR-SN-002`. Anual: `OBR-SN-003`; a partir de 2027, `OBR-SN-004` (anunciado).

Um caso de teste de cada linha está na coluna `caso_de_teste`: refaça um deles antes de confiar num cálculo novo.

## Modelo de apuração
```text
Empresa: [nome interno]   Período: [mês/ano]   Regime: [ ]   Data do fato: [ ]
Arquivo de regras usado: [local e conferido_em]

Receita do mês por segregação
  [segregação] | [anexo] | [receita] | [origem: arquivo, nota]
RBT12: [valor] (soma de [mês/ano] a [mês/ano]) [id]
Fator R: [folha] ÷ [RBT12] = [r] → Anexo [ ] [id]
Faixa [n] do Anexo [ ]: nominal [ ]; deduzir [ ] [id]
Alíquota efetiva: ( [RBT12] × [nominal] − [deduzir] ) ÷ [RBT12] = [ ] [id]
Valor por segregação: [ ]   Total: [ ]
Vencimento: [ ] [id]; conferido na Agenda do mês: [sim/não]

Preparado por: [ ]  em [ ]   Conferido por: [ ]  em [ ]   Recibo: [ ]
Pendências: [ ]
```

## Checklist antes de transmitir
Periodicidade certa; todas as notas de saída lançadas e canceladas fora; segregações corretas; RBT12 fecha com os 12 meses; contas do razão = valores do formulário = papel de trabalho; diferenças resolvidas; aprovação, prazo e pagamento.

Plausibilidade: comparar com o mês anterior; mudança de faixa ou de anexo dita em linha própria; alíquota efetiva abaixo da nominal fora da 1ª faixa. Se perguntarem por opção mais vantajosa, faça a conta dos cenários e devolva a decisão ao responsável técnico.

## Erros comuns
Usar o mês corrente na RBT12; esquecer a segregação da retenção; Fator R sem a folha da competência certa; misturar anexo de atividades diferentes; aplicar tabela de um ano à competência de outro.
