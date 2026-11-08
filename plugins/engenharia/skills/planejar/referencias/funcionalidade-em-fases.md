# Funcionalidade em fases (Claude Code)

Para funcionalidade nova que toca vários arquivos. O modo completo chega a oito subagentes: para mudança pequena, use o modo leve (um explorador, um arquiteto, um revisor). No chat e no Cowork, faça as fases na própria conversa e diga que não houve contexto separado.

## Fases
1. **Descoberta.** Lista de tarefas com todas as fases. Pedido vago: qual problema resolve, o que deve fazer, restrições. Resuma e confirme.
2. **Exploração.** Dois ou três agentes `explorador` em paralelo, cada um num ângulo (funcionalidades parecidas, arquitetura, testes e pontos de extensão), cada um devolvendo de 5 a 10 arquivos-chave com arquivo:linha. Depois você LÊ esses arquivos e resume os padrões. Documentação do projeto é mapa, não prova: quando discorda do código, vale o código.
3. **Perguntas (não pule).** Casos-limite, erros, integração, limites de escopo, preferências, compatibilidade, desempenho. Uma rodada com opções; espere as respostas. "Faça o que achar melhor": recomende e peça confirmação explícita.
4. **Arquitetura.** Dois ou três subagentes arquitetos com focos diferentes (mudança mínima; arquitetura limpa; equilíbrio pragmático), cada um comprometido com a sua proposta: padrões achados com arquivo:linha, decisão com motivo e custos, componentes, arquivos a criar e alterar, fluxo de dados, sequência de construção, detalhes críticos (erro, estado, teste, desempenho, segurança). Você forma opinião e apresenta cada um, as diferenças concretas e a recomendação. Pergunte qual.
5. **Implementação**, só com aprovação explícita, seguindo as convenções do projeto, com o premortem (`plano-e-premortem.md`) e testes que falham antes (skill testar-e-verificar).
6. **Revisão.** O agente `revisor-independente` (sem a conversa de quem escreveu) e o /code-review para bugs. Consolide e pergunte: corrigir agora, depois ou seguir assim.
7. **Resumo.** O que foi feito, decisões, arquivos tocados, o que foi verificado e como, próximos passos.

## Delegar bem
- Delegue quando a trilha é independente e grande, ou quando a saída é volumosa (exploração ampla, suíte inteira, logs). Poucas chamadas de ferramenta: faça você mesmo.
- O brief é único e completo, porque o subagente não vê a conversa: objetivo, comportamento atual e esperado, arquivos, restrições, critério de aceite, o que reportar e a fronteira de arquivos que ele pode tocar.
- Lance os independentes juntos; integre um resultado por vez; não refaça em paralelo o trabalho do delegado.
- Subagente que escreve trabalha em worktree isolado; dois agentes nunca são donos do mesmo arquivo (o último a gravar vence e o trabalho do outro some sem aviso).
- Status do implementador: FEITO; FEITO COM DÚVIDAS (leia as dúvidas antes da revisão); PRECISA DE CONTEXTO (dê e redispare); BLOQUEADO (mais contexto, tarefa menor, ou o plano está errado e volta ao usuário). Nunca marque como feita uma tarefa bloqueada.
- Revisão em dois portões por tarefa: primeiro "faz o que a especificação pede?", requisito por requisito, com arquivo:linha; só então qualidade.
- Não acredite no "testes passam" do delegado: rode você.
- Processo que um subagente subiu: só ele sabe o PID. Confira a porta antes de subir serviço e pare só o que foi iniciado pela sessão.
- Contagens e tamanhos que não saíram de ferramenta nesta sessão vão marcados "(estimativa não verificada)".
