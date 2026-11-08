# Estado, passagem e retomada

Arquivo de estado é retrato: sobrescreve. Log e lições só recebem acréscimo. Decisões são superadas, nunca apagadas.

## Arquivo de estado
Um por projeto; se já existe outro, use esse. Só estado: nem lição, nem arquitetura, nem histórico. Cabe em cerca de uma tela.

```markdown
# Estado de <projeto>
Atualizado: AAAA-MM-DD; evidência: <versão, N testes passando no commit X, ou arquivo e data conferidos>
Rumo: rumo de AAAA-MM-DD (se houver)

## Onde está
Fase; branch e commit, se há git; se foi enviado; estado da verificação.

## Pela metade
O quê, em que estado, quais arquivos; tarefa delegada e onde ler o resultado.

## Alertas abertos
Teste vermelho, decisão não verificada, dado sob suspeita, cada um com a evidência.

## Dívidas
Numeradas, com contexto para agir.

## Próximo passo
Uma ação que dá para começar já.
```

- Sobrescreva: nada de seção por sessão. Alerta resolvido sai. O que está listado está vivo. Se nada mudou, confirme data e evidência.
- Escreva no fim e na hora em que algo importante aparece (teste vermelho, suposição errada, decisão do usuário).
- Sem git: backup datado antes de sobrescrever, se o arquivo guarda algo que não está em outro lugar.

## Passagem para outra sessão
`PASSAGEM.md` ou `PASSAGEM.<frente>.md` para frentes paralelas, na pasta do projeto, nunca em pasta temporária. Sem poder criar arquivo: um único bloco copiável. Se já existe: leia e funda. Trabalho que não bate com a tarefa do arquivo: avise e pergunte (sobrescrever ou outro nome).

Identifique a **tarefa atual**, não o pedido original. Confira o estado real (arquivos alterados) e não a memória da conversa.

Modelo fixo, sem seções a mais:

```markdown
# Passagem: <tarefa>
De: <quem escreveu, data e hora do relógio>. Para: <próxima sessão ou ferramenta>. Rumo de AAAA-MM-DD, se houver.

## Tarefa ativa
Uma frase.

## Estado
Feito: com `arquivo:linha`.
Em andamento: ...
Tentado e rejeitado: o quê, e por quê.

## Próximos passos
Executáveis sem perguntar. Ruim: "corrigir o bug". Bom: "em `pagamento.ts:42` o timeout está em ms e a API espera segundos".

## Decisões
Decisão, porquê, alternativa.

## Perguntas abertas
- [ ] ...

## Ambiente
Comandos, o que está quebrado ou pulado, arquivos alterados, o que reanexar.

## Contexto para quem pega
Três a cinco frases autossuficientes, reescritas do zero toda vez.
```

Sem fato, a seção diz "Nenhum" ou some; nunca fica cheia de "desconhecido". Regra e dado exato são copiados palavra por palavra; só a discussão é resumida. O que falta vira pergunta aberta, não invenção. Separe o que o usuário decidiu do que o Claude só sugeriu.

Saída: "Passagem salva em `<caminho>`; próximo: <até 15 palavras>".

Sessão longa: passando do limite combinado, procure um ponto limpo (próximo passo concreto, nenhuma investigação guardada só no contexto), escreva a passagem e sugira sessão nova. Não encerre sozinho.

## Prompt da próxima sessão
Um bloco para colar: o que fazer primeiro, caminho completo do arquivo de estado ou passagem, regras da sessão que não estão em arquivo, o que não repetir (tentado e rejeitado), entradas de memória que ficaram por gravar, escritas por extenso (nunca "ver o fechamento": a próxima sessão não tem esta conversa).

## Retomar
Comece pelo arquivo de estado ou passagem, antes de explorar. É hipótese com evidência, não prova.
1. Pedido por nome e arquivo inexistente: liste os que existem e pare, sem adivinhar.
2. Confira contra a realidade: branch ou pasta diferente, pare e pergunte; arquivos que contradizem o "em andamento", aponte; passagem com mais de 7 dias, avise; quem escreveu não bate, aponte.
3. Se passagem e realidade divergem, a realidade vence. O arquivo de estado se corrige (com o sim); a passagem não se edita ao retomar.
4. Resumo fixo: de onde veio (quando e quem), tarefa, próximo, divergências.
5. Execute **só o primeiro passo** e pergunte se segue. Passo vago ou pergunta bloqueante: pergunte antes.
