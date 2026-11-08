# Entrega no git

Commit, push, PR, merge e comentário só com o sim do usuário, pedido para aquela ação. Comandos que apagam trabalho: `comandos-destrutivos.md`.

## Fluxo solo (padrão, ajuste ao do projeto)
- `main` sempre implantável; trabalho numa branch curta; commits pequenos, um assunto cada.
- Mensagem no idioma do projeto. Proponha o commit (arquivos e mensagem) e espere o sim.

## Commit verificado
"O usuário mandou commitar" não autoriza pular teste, tipos e lint.
1. Ache os comandos (package.json, pyproject, CI, CLAUDE.md).
2. Rode, leia a saída inteira e o código. Falhou: corrija ou pare; nunca "conserto no próximo commit".
3. Irmãs: API pública mudou → documentação; regra nova → teste.
4. Foco: `git diff --stat`; tudo ligado ao propósito? Senão, divida.
5. Prepare só os arquivos nomeados (nunca `git add .` ou `-A`); confira o que foi preparado atrás de segredo e arquivo solto.
6. Formatação nunca no mesmo commit que mudança de comportamento.
- Repositório sem checagem nenhuma: diga e pergunte (commitar assim ou montar uma checagem mínima).
- Sinais de parar: sem saída recente de teste no contexto; `--no-verify`.
- Mensagem: tipo (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`...), assunto imperativo, curto, sem ponto final, que se entende sozinho ("Corrige duplicação ao reprocessar a pasta", não "Fix bug"); corpo com o porquê e as limitações. Mudança incompatível marcada.

## Conflito de merge ou rebase
1. Veja o estado (`git status`, os commits de cada lado).
2. Leia a intenção de cada lado (mensagens, PR), nunca resolva pela aparência do texto.
3. Preserve as duas intenções; incompatíveis, fique com a do objetivo do merge e anote o custo. Não invente um terceiro desenho. Não aborte sem ordem.
4. Rode tipos, testes e lint de verdade: conflito que mescla limpo no texto pode quebrar o sentido.
5. Conclua e confirme árvore limpa e checagens verdes.

## Fechar uma branch
Suíte verde antes de oferecer opções (falhando: relate e pare). Confirme a branch base ("saiu de main, certo?"). Ofereça: 1 juntar localmente; 2 enviar e abrir PR; 3 deixar como está. Descartar só se o usuário pedir com todas as letras, mostrando antes o que será apagado. Push recusado não se resolve com force.

## Descrição de PR
- Base e rota conferidas no repositório, não presumidas. Issue ligada só se o usuário disser qual.
- Corpo: Problema; Comportamento (o que muda para quem usa); Escopo (e o que não é objetivo); Riscos (só fatos verificados); Verificação (comando → resultado observado; arquivo de teste → o que cobre, sem dizer que passou se não rodou).
- Classes de evidência: implementação (arquivo do diff), fonte de teste (mostra intenção, não prova), verificação executada (comando com resultado), estado implantado (registro de deploy). Configuração é intenção, não estado implantado.
- Mostre título e corpo antes de criar; crie só com o sim.
