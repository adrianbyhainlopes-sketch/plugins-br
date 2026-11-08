# Pronto com evidência

## Portão antes de afirmar
Sem ter rodado nesta mensagem o comando que prova, não se diz que passa.
1. Ache o comando que prova a afirmação.
2. Rode completo e do zero, sem pipe.
3. Leia a saída inteira e o código de saída; conte falhas e pulados.
4. A saída confirma? Só então afirme, junto com a evidência. Se não confirma, diga o estado real.

| afirmação | prova | não basta |
|---|---|---|
| testes passam | saída com 0 falhas e código 0 | "deve passar" |
| lint limpo | saída com 0 erros | |
| build ok | código 0 | lint verde |
| bug corrigido | o sintoma original testado | teste novo passando sem ter falhado antes |
| teste de regressão | ciclo vermelho e verde | |
| agente terminou | o diff no git | o relato do agente |
| requisitos atendidos | lista linha a linha | testes verdes |

Sinais de parar: "deve", "provavelmente", "parece"; comemorar antes de rodar; ir commitar sem saída recente; confiar no relato de outro agente.
Depois que passou, pare: polimento de carona vira proposta à parte.
Sem como verificar (ambiente, credencial, serviço pago): diga exatamente o que falta, peça para o usuário rodar e colar a saída, e declare "não verificado". Passo pulado significa "construído, não pronto", nunca "pronto com ressalvas".

## Tamanho da verificação
Mudança sem lógica (comentário, documentação): formato, lint e build. Qualquer constante, condição, padrão, preço ou rótulo cujo sentido muda: tudo. Na dúvida, não é erro de digitação.

## Escada de evidência
1. "Eu disse." 2. Apontei a linha (arquivo:linha, ou o fonte da biblioteca na versão instalada). 3. Percorri o caminho de falha e mostrei que ele não chega. 4. Rodei um script ou teste que chama o código real e falha alto se eu estiver errado. 5. Reproduzi no app rodando.
Abaixo do degrau 4 o fato é "não provado", com essas palavras. Diga em que degrau está cada afirmação.

**Fato de segurança:** a frase que torna a mudança segura ("só remove entradas já expiradas"). Mais de três fatos = várias mudanças juntas; diga.
**Onde o grep para:** chamada por texto (rota em tabela, chave de configuração, despacho dinâmico), coluna de banco, JSON de API, outra linguagem lendo os mesmos dados, flag, código três saltos adiante.
**Script de prova:** mesmo runtime e versões do projeto; importa o código real (reimplementar a lógica no script é degrau 1 disfarçado); falha alto; fica fora do repositório; mostre comando, código de saída e saída.

## Conferir as afirmações de outro agente
Junte as afirmações de três lugares: mensagens de commit, descrição do PR e o resumo final da conversa (o mais forte, e que nunca chega ao git). Confira cada commit contra o próprio diff e o resumo contra o intervalo inteiro.

Sinais de contradição: arquivo dito alterado que não mudou; "adicionei testes" sem arquivo de teste; teste novo que não importa o código alterado; `.skip`, `.only`, `xfail` novos com "os testes passam"; configuração de seleção de testes alterada no mesmo intervalo; asserção reescrita com "sem mudança de comportamento"; palavras de prova ("verificado", "funciona") sem nada que as sustente.

Receita por afirmação (a evidência mais barata que poderia provar que é falsa):
- "Corrigi X": o menor teste que reproduz o sintoma; falha no commit anterior e passa no novo, cada versão num worktree; confirme que o arquivo mexido é o que o app carrega. Passa nos dois commits = não prova nada.
- "Adicionei testes": cada teste importa X? Quebre X de propósito numa cópia e veja falhar.
- "Os testes passam": conte executados, aprovados, falhos e pulados; o CI roda o mesmo comando e não está liberado para falhar (`continue-on-error`, `|| true`)?
- "Removi código morto": procure quem importa por todos os caminhos (alias, relativo, `import()` dinâmico, caminho em configuração).
- "Liguei": nomeie a porta de entrada e trace cada salto até o código novo.
- "Sem mudança de comportamento": os mesmos testes nos dois commits; todo assert editado precisa de motivo.
- Banco, variável de ambiente, outro serviço: "não dá para saber", salvo a checagem mais estreita e só de leitura. Nunca um comando amplo (`db push`, novo deploy) para descobrir.

Vereditos: vale; não vale (dizer o que é verdade); não dá para saber (dar o comando que resolve). Antes de "não vale", confira o instrumento.
Relatório: uma linha com a contagem ("N afirmações: a valem, b não, c sem como saber"), a tabela "o agente disse | veredito | o que é verdade | evidência", e "o que dizer ao agente", pronto para colar.

## Sonda de mutação (a checagem consegue falhar?)
1. Rode a checagem e registre saída e código. 2. Quebre uma única coisa que ela deveria pegar, no código e não na checagem, com a menor edição. 3. Rode: tem de falhar, e a mensagem tem de nomear o que foi quebrado. 4. Desfaça a partir da cópia, rode de novo (verde) e confirme pelo `git status` e `git diff` que a árvore voltou idêntica. 5. Só então diga que a checagem funciona.
Se o passo 3 continua verde, achou uma checagem que não consegue falhar: é um achado. Uma mutação por vez; vermelho por crash não conta.

## Validação em execução
Suíte de mocks verde não prova que o sistema roda. Suba o app com o log zerado, exercite, procure erro no log; passe a resposta real de novo pelo esquema (`parse` do Zod, `model_validate` do Pydantic); confira piso e teto de todo número derivado (percentual entre 0 e 100; soma das partes igual ao total; débito igual a crédito).

## Sinais de implementação incompleta
Corpo vazio; função que só devolve o argumento; retorno com a forma certa e conteúdo vazio; "não implementado"; `catch {}` ou `.catch(() => {})`; `@ts-ignore` ou `as any` novos no diff; TODO, FIXME; valores como "changeme" ou "SUA_CHAVE_AQUI"; `if (false)`.

## Relatório final
Sem seção vazia (escreva "nenhum"):
- **Verificado:** o que foi conferido e como, com a saída.
- **Suposto:** o que não deu para inspecionar; a entrega fica condicionada.
- **Não verificado:** o que dependia de algo que não houve, com o comando que resolveria.
- **Visto e não tocado:** o que notou fora do pedido; registre, não corrija.
