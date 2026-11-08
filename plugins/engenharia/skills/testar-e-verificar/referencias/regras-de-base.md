<!-- cópia gerada de compartilhado/regras-de-base.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Regras de base para mexer em código

Valem para todo trabalho de engenharia, antes do método da skill. Cada regra existe por causa de um erro que agentes cometem com frequência.

## 1. Aprender o projeto antes da primeira mudança
- Leia CLAUDE.md, AGENTS.md, README e CONTRIBUTING. Se a documentação discorda do código, siga o código e avise.
- Ache os ajudantes que já existem (autenticar, conferir permissão, validar entrada, abrir transação, devolver erro, formatar data e dinheiro) e use-os. Busque pelo propósito antes de criar um novo.
- Anote os comandos de checagem do projeto (teste, tipos, lint, build) lendo `package.json`, `pyproject.toml`, Makefile ou o CI.
- Confira a versão instalada (lockfile ou manifesto) antes de usar API de biblioteca. Import e assinatura de memória são o erro mais comum; a doc da versão instalada vence a lembrança (no Next 16, `node_modules/next/dist/docs/`).

## 2. Antes de codar
- Reescreva o pedido como critério verificável ("adicionar validação" vira "estas entradas são recusadas com estas mensagens, cobertas por estes testes").
- Regra de negócio, unidade, faixa, permissão ou significado de campo que não está no pedido nem no código: pergunte. Uma pergunta vale mais que um dado plausível e errado.
- Se há mais de uma leitura do pedido, mostre as opções; se há caminho mais simples, diga.
- Planeje a menor mudança. Refatoração, renomeação, dependência nova e "já que estou aqui" vão para o fim, como sugestão.

## 3. Ao escrever
- Toda rota, Server Action, handler e job confere quem chama e se essa pessoa pode mexer naquele registro, no servidor.
- Entrada validada na fronteira com esquema estrito (campo desconhecido é recusado). Identidade vem da sessão, nunca do corpo.
- Erro sobe: nada de `catch` vazio, `return []`, `null` ou valor padrão escondendo falha. Pergunta: "o sistema está correto quando este ramo roda?" Se não, deixe o erro subir até quem trata, com o que falhou e qual entrada causou. Fallback legítimo é decisão de produto e tem nome (`TIMEOUT_PADRAO_S = 30`).
- Escrita em vários passos numa transação; invariante no banco (unique, check, update condicional) contra a corrida de "confere e depois grava".
- Tipos honestos: sem `any`, `as` sem checagem, `!`, `@ts-ignore` ou regra de lint desligada para sumir com erro.
- Apague o que foi substituído. Nada de `_v2`, `.bak`, arquivo de depuração ou plano deixado na pasta.

## 4. Ao editar e rodar
- Edição pequena e ancorada no texto existente; se falhar, releia a região e tente um trecho menor. Nunca reescreva o arquivo inteiro para contornar uma edição que falhou, nem escreva "// ... resto igual" dentro do arquivo.
- Não edite saída gerada (`dist`, `.next`, `build`, `coverage`, tipos gerados).
- Rode checagem sem pipe: `comando | tail` devolve o código do `tail`. Redirecione para arquivo e leia o código de saída.
- Nada que fique esperando em primeiro plano (servidor de dev, modo watch, instalador interativo). Servidor em segundo plano, com log, e desligado no fim pelo PID.
- git só leitura para inspecionar. Comandos destrutivos: `comandos-destrutivos.md`. Segredos: `segredos-sessao.md`.
- Depois de compactação de contexto, releia os arquivos antes de editar.

## 5. "Pronto" é verificado
- Rode as checagens depois da última edição e leia o resultado. O que não rodou vai para "Não verificado", com o motivo.
- Nunca enfraqueça ou apague uma asserção para o teste passar. Se o teste parece errado, diga e pergunte.
- Feche com: o que mudou, comandos rodados e resultados, suposições, o que viu e deixou de lado de propósito.
- Quando o usuário contesta: confira com evidência (rode, leia). Se a evidência sustenta, mantenha e mostre; se estava errado, diga e corrija.

## 6. Gastar pouco
Localize com busca e leia só o trecho; não releia o que está no contexto e não mudou; cite arquivo:linha em vez de colar código. Nunca economize em validação, tratamento de erro, segurança ou teste.

## Bloco curto para colar no CLAUDE.md de um projeto
Versão de dez linhas, para quem quer estas regras sempre carregadas. Ajuste os comandos ao projeto.
```
## Regras de engenharia
- Antes de mudar: leia o código vizinho, use os ajudantes que já existem, confira a versão instalada da biblioteca.
- Pergunte regra de negócio, unidade ou permissão que não está no pedido nem no código.
- Menor mudança que resolve; toda linha do diff se explica pelo pedido.
- Toda rota e Server Action autentica e autoriza no servidor; entrada validada na borda.
- Erro sobe: sem catch vazio, sem lista vazia no lugar de falha.
- git só leitura para inspecionar; nada de reset --hard, checkout --, clean, stash ou push sem pedido.
- Não abra .env nem chaves; segredo nunca em código, log ou commit.
- Checagens: <comando de teste>, <tipos>, <lint>, <build>, rodadas sem pipe, lendo o código de saída.
- "Pronto" só com a saída na mão; o que não rodou é "não verificado".
```
