# Desenho

## Componente de servidor em seis passos
Vale para endpoint, Server Action, job agendado, consumidor de evento, webhook, script e integração. Nada de código antes dos seis; a profundidade acompanha o risco (verificação de saúde: uma linha por passo; pagamento: parágrafos). Resumo de 10 a 20 linhas ao usuário antes de implementar. Não preencha o modelo quando as respostas são óbvias.

1. **Contexto.** Que tipo de componente é (síncrono, job, consumidor de evento, agendado, linha de comando, carga de dados). Cada tipo tem orçamento de latência, modo de falha e modelo de concorrência próprios. Carga esperada: pergunte se faltar.
2. **Dados.** Entidades; invariantes que nunca podem ser falsas, impostas no esquema quando der (CHECK, UNIQUE, FK, NOT NULL); dono e escopo de cada dado; ciclo de vida e transições permitidas.
3. **Falhas por tipo.** Integração externa: 4xx não se repete; 5xx se repete com espera crescente e aleatória; tempo esgotado é estado desconhecido e exige chave de idempotência. Para cada uma: como detectar, como mostrar, como recuperar. Depois, uma passada com olhar de segurança.
4. **Autorização.** Quem dispara, com que escopo, sobre que recursos. "Qualquer autenticado" não é resposta. Dado de vários clientes fica separado no banco (RLS), não só no código.
5. **Idempotência e concorrência.** Rodar duas vezes; duas instâncias juntas (trava de linha, coluna de versão, ou "o último vence" justificado); evento fora de ordem.
6. **Observabilidade.** Log estruturado na fronteira com um ID de correlação; o que medir; verificação de saúde que testa de verdade.

Sinais para voltar ao passo 2: consulta escrita antes de definir os dados; "trata erro depois"; e-mail, pagamento ou terceiro sem o passo 5; try/catch sem log nem recuperação.

## Desenhar duas vezes
Quando a decisão é a forma de um módulo ou de uma API, o primeiro desenho raramente é o melhor.
- **Requisitos primeiro:** que problema resolve, quem chama, operações principais, restrições (desempenho, compatibilidade, padrões existentes), o que fica escondido e o que fica exposto.
- **Três desenhos, cada um com uma restrição diferente:** A, a menor superfície (uma a três operações); B, máxima flexibilidade; C, otimizar o caso comum. Opcional D, inspirado num padrão ou biblioteca conhecida. No Claude Code, quando a decisão pesa, um subagente por desenho, com o mesmo brief e restrições diferentes; quando o espaço é pequeno, em sequência na própria resposta.
- **Cada desenho traz:** assinatura, um exemplo de uso real pelo chamador, o que esconde e os custos.
- **Comparar em prosa:** simplicidade da superfície; geral contra especializado; eficiência que a forma permite; profundidade (superfície pequena escondendo muita complexidade é bom); facilidade de usar certo contra facilidade de usar errado. O melhor costuma juntar pedaços de vários.
- **Erros comuns:** desenhos que convergem (restrições fracas); pular a comparação; implementar nesta etapa; escolher pelo esforço de implementação (puxa para o desenho raso).
