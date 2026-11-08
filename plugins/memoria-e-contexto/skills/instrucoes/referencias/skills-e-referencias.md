# Skills e referências

Se a skill nativa de criar skills estiver disponível, use-a para o ciclo de avaliação. Aqui fica o que costuma dar errado na escrita.

O objetivo é o agente seguir o mesmo processo a cada execução, não produzir a mesma saída.

## A linha sempre carregada decide
Descrição de skill, linha do CLAUDE.md: é o ponteiro. É a redação do ponteiro, e não o alvo, que decide se o agente vai buscar. Material essencial atrás de ponteiro fraco é erro de variância: afie o ponteiro primeiro.
- Palavra-chave no começo. Um gatilho por ramo. Corte o que o corpo já diz.
- Dizer também quando **não** usar evita disputa com a skill vizinha.
- Cada descrição custa contexto em toda resposta: curta. Skill que só o usuário chama pode não gastar nada.

## Escada de informação
Passo no arquivo; referência no arquivo; referência revelada (outro arquivo, atrás de ponteiro). O que todo caminho usa fica dentro; o que só alguns usam vai para trás de um ponteiro. Referência no meio dos passos transforma seguir os passos em cara ou coroa: a ordem de ler vem antes do passo.

Depois de `/compact`, o corpo da skill volta cortado (limite de 5 mil tokens por skill, ficando o começo): o mais importante vai no topo.

## Escrita
- Critério de conclusão em todo passo, com clareza e exigência ("todo modelo alterado considerado" força trabalho; "produza uma lista" não).
- Definição, regras e ressalvas de um conceito sob o mesmo título.
- Negação puxa o proibido para o contexto: escreva o comportamento desejado; proibição só como guarda dura, com o alvo positivo.
- Fonte única para cada significado. O ambiente já é fonte de verdade: repetir `package.json` é cache que envelhece.
- Cace instruções que o modelo já seguiria e apague a frase inteira.

## Forma
- Frontmatter válido em toda superfície: só `name` e `description` (o chat recusa outros campos). No Claude Code, campo desconhecido é ignorado sem aviso, e `allowed-tools` pré-aprova mas não restringe.
- `name` em minúsculas, números e hífen, até 64 caracteres, igual ao nome da pasta. `description` até 1.024 caracteres.
- Pasta: `skills/<nome>/SKILL.md`. Arquivo solto em `skills/<nome>.md` não aparece.
- No chat, a skill só enxerga a própria pasta: peça usada por duas skills é copiada para as duas.
- Plugin: caminho com `${CLAUDE_PLUGIN_ROOT}`, nunca absoluto.

## Testar
1. Disparo: pedidos que deveriam e que não deveriam acionar.
2. Com e sem a skill, no mesmo pedido, em sessões novas.
3. Trate o que falhou: skill que não dispara quase sempre é descrição; skill que dispara e erra é corpo.

Esconder uma skill não é fronteira de segurança.
