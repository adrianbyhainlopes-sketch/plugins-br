# Fechamento do mês e calendário

## O que vence este mês
1. Regime do cliente e, se houver, empregados e retenções.
2. Filtre `dados/obrigacoes-br.csv` por `regime` (e `Todos`) e pela data: `vigencia_inicio` ≤ data ≤ `vigencia_fim`.
3. Calcule a data pela coluna `valor` e `unidade`; aplique `dia_nao_util`:
   - `dia útil posterior` ou `dia útil anterior`: desloque contando feriado nacional e o que o usuário informar de feriado local;
   - `a conferir`: diga que o dia não útil não foi conferido.
4. **Confira na Agenda Tributária do mês** (`OBR-GER-001`): quando a conta e a agenda divergirem, vale a agenda.
5. Devolva: `obrigação | competência | data | id | status`. Linhas `a conferir` aparecem como tal, com o que fazer. Estadual e municipal: `OBR-GER-008`, pela legislação ou guia do usuário.
Nunca conte o dia pela data de hoje sem dizer a data usada.

## Checklist por dia (ajuste ao porte)
- **Pré-fechamento:** aviso de prazos, corte combinado, conciliação bancária preliminar, pedidos em aberto, transações incomuns.
- **T+1:** auxiliares encerrados, provisão do recebido sem nota, folha, recebimentos e pagamentos, conciliação bancária final, depreciação, antecipadas.
- **T+2:** receita e receita diferida, demais provisões, conciliação de clientes e fornecedores, estoque.
- **T+3:** contas patrimoniais e ajustes, balancete preliminar, análise de variação preliminar.
- **T+4:** provisão de tributos, patrimônio líquido, fechamento suave, demonstrações em rascunho, revisão.
- **T+5:** ajustes finais, fechamento definitivo, trava do período, pacote de relatórios.

## Dependências
Lançamentos de caixa, pagar e receber → conciliações dos auxiliares → patrimoniais → tributos → demonstrações → revisão → fechamento. Cada nível depende do anterior terminado.

## Painel
`tarefa | responsável | prazo (T+N) | status | bloqueio | notas`. Status: não iniciada; em andamento; concluída (significa revisada); bloqueada; em risco. No escritório, uma linha por cliente e competência, com o painel da carteira na camada pessoal.

## Autoverificação antes de liberar
1. Ativo = passivo + PL.
2. Imposto a pagar confere com o apurado e a conta a recolher.
3. Pessoal confere com a folha.
4. Depreciação do mês confere com o quadro.
5. Contas de conciliação sem diferença.
6. Tudo lançado; competência respeitada.

## Retrospectiva
Gargalo, causa e solução; o que manter; o que demorou e por quê; que surpresa dava para ver antes; o que automatizar. Métricas ao longo do tempo: duração do fechamento, ajustes depois do fechamento suave, tarefas atrasadas, exceções de conciliação.
