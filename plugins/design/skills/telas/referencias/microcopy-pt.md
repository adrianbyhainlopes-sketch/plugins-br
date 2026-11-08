# Texto de interface em português do Brasil

A trava de fatos vale aqui: preço, prazo, limite, número e nome de plano só como o usuário disse (`trava-de-fatos.md`). Texto com aparência de pronto e sem o dado vira `[FALTA: ...]`.

## Voz
- 3 a 5 atributos de como o produto soa, cada um como "é X, não Y" ("direto, não seco"). O tom muda com o contexto (primeiro uso, erro, ação destrutiva, sucesso); a voz fica.
- Tratamento por "você", sem misturar com "o senhor". Sem "a gente" e "nós" alternando: escolha um para o produto falar de si.
- Gênero: prefira construções neutras quando não se sabe quem lê ("Boas-vindas" em vez de "Bem-vindo"; "Quem pode editar" em vez de "Os usuários que podem editar"). Não use "x" ou "@" no lugar da vogal: o leitor de tela lê mal.
- Nomeie pelo que o usuário entende ("Avisos", não "Configuração de webhook"); voz ativa; caixa de frase (só a primeira letra maiúscula); sem enchimento.
- Passe o texto pelos vícios de `vicios-pt.md` antes de entregar.

## A mesma ação, o mesmo nome
O botão "Publicar" gera o aviso "Publicado". O botão "Salvar rascunho" gera "Rascunho salvo". O nome não muda no meio do fluxo.

## Botões
- Um principal por tela, com o verbo da ação do usuário: "Criar projeto", "Enviar proposta", não "OK" nem "Enviar" sozinho quando há o que dizer.
- Secundário subordinado; cancelar e voltar sempre visíveis.
- Destrutivo nomeia a consequência: "Excluir projeto e arquivos".

## Erro em 3 partes
1. O que aconteceu, específico: "O arquivo não subiu porque passa de 25 MB" (com o limite real do produto, informado pelo usuário).
2. Por que importa (pule em erro simples de campo).
3. O que fazer: "Reduza o arquivo ou envie em partes". Se não há o que fazer, diga com honestidade.
- Sem "Ops!", sem "Ocorreu um erro", sem código sem explicação, sem culpar ("Você digitou errado"), sem pedido de desculpa automático.
- Tom pela gravidade: campo, útil e curto; falha do sistema, honesto; risco de perder dado, direto e calmo.

## Confirmação
Título nomeia a ação ("Excluir este projeto?"); corpo diz a consequência ("Os 12 arquivos serão apagados e não dá para recuperar", com o número real da tela); botão repete a ação ("Excluir projeto"); saída clara ("Manter projeto").

## Vazio, carregamento, sucesso
- Vazio de primeiro uso: o que mora ali, por que vale, o que fazer ("Nenhum cliente ainda. Cadastre o primeiro para emitir cobranças.").
- Carregando específico: "Enviando arquivo 2 de 5". Progresso: "Passo 2 de 4: escolha o plano".
- Sucesso específico, com o próximo passo: "Proposta enviada para a cliente. Você recebe um aviso quando ela abrir."

## Dica, rótulo e exemplo
- Rótulo sempre visível; o exemplo no campo (`placeholder`) mostra formato e nunca é o único rótulo: "Ex.: 000.000.000-00".
- Dica suplementar, curta, abre com mouse e com foco, não repete o rótulo. Se é necessária, vai na tela.
- Obrigatório marcado com texto ("obrigatório"), não só com cor ou asterisco solto.

## Pronto para traduzir e para leitor de tela
- Não monte frase colando pedaços ("Você tem " + n + " itens"): plural muda a frase ("1 item", "2 itens", "nenhum item").
- Sem data relativa fixa no texto; sem expressão idiomática; sem texto dentro de imagem.
- Preveja texto 20 a 35% mais longo em outra língua.
- Lido em sequência pelo leitor de tela, o texto faz sentido ("Excluir" sozinho não diz o quê; "Excluir projeto Alfa" diz).

## Legibilidade
Frases curtas, uma ideia por frase, palavra concreta. Escreva para quem está com pressa, no celular, cansado ou lendo em segunda língua. Métrica numérica de legibilidade para o português: só com fonte conferida; sem ela, leitura em voz alta e a pergunta "faz sentido para quem nunca viu o produto?".

## Entregáveis possíveis
Guia de voz curto; texto por tela (tabela: lugar, texto, limite de caracteres, observação); inventário de erros (gatilho, texto, gravidade); perguntas pendentes.
