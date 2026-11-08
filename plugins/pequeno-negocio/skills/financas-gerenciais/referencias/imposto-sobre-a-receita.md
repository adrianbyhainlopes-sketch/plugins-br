# Imposto sobre a receita como custo variável

Na margem, no ponto de equilíbrio e no preço, o imposto que incide sobre a venda é custo variável: sobe e desce com a receita. A skill **nunca** escreve uma alíquota, um limite ou um valor fixo de memória.

## Onde está a regra
`dados/regras-fiscais-br.csv`, com as colunas id, assunto, regra, valor, unidade, vigência, status, fonte e conferido_em. Antes de usar:
1. Procure uma cópia mais nova do arquivo (arquivos do Project, pasta de trabalho, camada pessoal). Use a de `conferido_em` mais recente e diga qual usou.
2. Filtre pela **data do fato** (o mês da venda ou do preço que se quer formar).
3. Só linha com status "vigente" naquela data sustenta um número. "Anunciado" não é "vigente". "A conferir" e valor vazio = **desconhecido**.
4. Linha com `conferido_em` mais velho que 6 meses: avise uma vez.
5. Diga o id da linha usada ("FIS-SN-003") ao lado do número.

## A ordem de preferência
1. **A alíquota que o usuário informar** a partir de documento dele (guia paga, extrato do Simples, cálculo do contador). É a melhor fonte: vale para o caso dele e a data é conhecida. Registre de onde veio.
2. **A linha vigente do arquivo**, quando houver e o caso do usuário couber nela.
3. **Nenhuma das duas:** o imposto fica desconhecido, a margem e o preço saem **parciais**, e a resposta mostra a conta com o imposto como variável ("margem = 38% − alíquota do imposto sobre a receita") e diz o que perguntar ao contador.

## Regime do usuário
Pergunte uma vez, se não estiver no material: MEI, Simples Nacional (e qual anexo), Lucro Presumido, outro, ou não sabe. "Não sabe" é resposta válida: segue como desconhecido.
- **Simples Nacional:** a alíquota efetiva depende da receita dos 12 meses anteriores (FIS-SN-001), da fórmula (FIS-SN-002) e da faixa do anexo da atividade (FIS-SN-010 a 014, com as linhas `-F1` a `-F6` de cada anexo). Prefira a alíquota efetiva que o usuário trouxer. Sem ela, calcule com as linhas vigentes na data do fato e mostre a receita, a faixa e a conta. Sem saber o anexo ou a receita dos 12 meses, fica desconhecido. As faixas têm fim de vigência registrado no arquivo: fora dele, não há número.
- **MEI:** o valor fixo por mês (FIS-MEI-002, com fim de vigência registrado) entra como custo fixo, não como percentual variável. O limite de receita está em FIS-MEI-001.
- **Lucro Presumido:** as linhas FIS-LP-001 a 005 sustentam o cálculo. O acréscimo sobre a receita acima do limite anual (FIS-LP-006) está a conferir: se a receita puder passar desse limite, diga que a conta não o considera.
- **ISS:** o mínimo e o máximo nacionais estão em FIS-ISS-002, mas a alíquota do município (FIS-ISS-001) está a conferir: peça ao usuário.
- **Reforma dos tributos sobre o consumo:** a transição está em FIS-REF-001 e nas linhas seguintes, ano a ano. Só linha "vigente" sustenta número. Se a data do fato cair num ano sem linha vigente, diga que a regra pode ser outra e peça a conferência.

## Como mostrar
- Na margem: "imposto sobre a receita: [alíquota]% (informada pelo usuário, guia de setembro)" ou "imposto sobre a receita: desconhecido (regime a confirmar); margem parcial".
- No preço: o percentual do imposto entra na soma dos percentuais sobre o preço (`formulas-gerenciais.md`, seção 3).
- Mudança de faixa: se o preço ou o volume novos podem mudar a faixa do Simples, diga que a alíquota pode mudar junto e que a conta precisa ser refeita com o contador.

Isto é apoio a decisão gerencial, não apuração de imposto. A apuração, a guia e a declaração ficam com quem faz a contabilidade.
