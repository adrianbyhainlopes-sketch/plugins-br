<!-- cópia gerada de compartilhado/next16-seguranca.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Segurança no Next.js 16 (App Router)

Conferido em 08/11/2026 na documentação online do Next.js (guias de segurança de dados, atualização para a versão 16, CSP, `after`, `use cache`). Confira a versão no lockfile antes de afirmar: se o `next` instalado traz documentação em `node_modules/next/dist/docs/`, ela vence este arquivo.

## Portas de entrada
Toda revisão lista estas portas, uma a uma:
- `route.ts`: cada método exportado (GET, POST etc.) é uma porta.
- Server Actions: cada função assíncrona exportada de arquivo `'use server'`, ou com a diretiva no corpo. Alcançável por POST direto, mesmo sem nenhuma tela chamando.
- `proxy.ts` (`middleware.ts` até a 15): roda antes, tem muito poder e não é fronteira de segurança.
- Pastas `[param]`: o valor é entrada do usuário e precisa de validação.
- `pages/api/**`, se o projeto ainda tiver.
- Fora do HTTP: cron, webhook, fila, função de borda, WebSocket.

## Autenticar e autorizar
- A checagem da página não vale para a Server Action definida nela. Dentro de cada action: quem é (identidade do token conferido), pode mexer neste registro (posse), entrada validada, retorno filtrado.
- O proxy só decide roteamento. CVE-2025-29927 mostrou autorização no middleware sendo contornada pelo cabeçalho `x-middleware-subrequest`: confira a versão instalada no advisory (GHSA-f82v-jwr5-mffw), nunca de memória.
- Matcher estreito é buraco: rota de API e Server Action podem escapar do proxy da página. Layout também não protege: a página e a action têm de conferir.
- IDs cifrados de action e eliminação de action sem uso reduzem o risco e não substituem a checagem.

## O que o auditor olha (lista da própria documentação)
- Há Camada de Acesso a Dados isolada? Pacote de banco e variável de ambiente importados fora dela são sinal.
- Arquivos `'use client'`: as props esperam dado privado? A assinatura é larga demais (recebe o objeto inteiro)?
- Arquivos `'use server'`: argumentos validados, usuário reautorizado, posse conferida, retorno só com o necessário, banco delegado a módulo `server-only`?
- `/[param]/`: parâmetros validados?
- `proxy.ts` e `route.ts`: gaste mais tempo aqui.

## Vazamento para o cliente
- O retorno da Server Action e a prop de Client Component vão serializados ao navegador. Objeto inteiro do banco leva junto o que a tela não mostra.
- `import 'server-only'` faz o build falhar se o módulo for puxado pelo cliente. Só variável com `NEXT_PUBLIC_` chega ao cliente; variável sem o prefixo lida em `'use client'` vira `undefined`.
- APIs de taint do React (`experimental.taint`) são camada extra e experimental: não dispensam filtrar na camada de dados.
- Variável capturada por closure vai cifrada ao cliente e volta; a doc não recomenda confiar só nisso.

## Cache com dado de usuário
- `'use cache'` não pode ler `cookies()`, `headers()` nem `searchParams`, inclusive em função auxiliar chamada lá dentro. Passe como argumento: argumentos e variáveis capturadas entram na chave.
- Risco real: função cacheada que devolve dado de usuário sem o identificador nos argumentos serve a mesma resposta para todos, ou prende o resultado no shell estático. Procure `'use cache'` em volta de consulta por usuário e confira o que forma a chave.
- `'use cache: private'` existe para dado de requisição: em produção não guarda no servidor entre requisições; o roteador do cliente pode manter por um tempo.
- Com Supabase, os cabeçalhos `Cache-Control`, `Expires` e `Pragma` que o `setAll` recebe têm de ir para a resposta, senão a CDN pode entregar a página de um usuário a outro.
- Resposta autenticada de rota: `Cache-Control: no-store`, salvo decisão consciente.

## Server Actions e CSRF
Só POST invoca a action. O Next compara o `Origin` com o `Host` (ou `x-forwarded-host`) e aborta se forem diferentes. Com proxy reverso, `serverActions.allowedOrigins`, sem curinga largo. Corpo limitado a 1 MB por padrão (`bodySizeLimit`).

## CSP
- Com nonce: gerado no `proxy.ts`, a cada requisição, posto no cabeçalho `Content-Security-Policy` e em `x-nonce`; o Next aplica aos scripts dele. Exige renderização dinâmica em todas as páginas (sem otimização estática, sem ISR, sem cache de CDN) e é incompatível com Partial Prerendering.
- Sem nonce: cabeçalho em `next.config` com `'unsafe-inline'`.
- `'unsafe-eval'` só no desenvolvimento.
- Hash por SRI (`experimental.sri`) mantém a página estática e ainda é experimental.
- Matcher sugerido pela doc pula `api`, `_next/static`, `_next/image` e prefetch: não confunda esse matcher de CSP com o de autenticação.

## Trabalho depois da resposta
`after()` (estável desde a 15.1) roda depois da resposta, até o `maxDuration` da rota, e roda mesmo se a resposta falhou. Em rota e Server Function pode ler `cookies()` e `headers()` dentro do callback; em Server Component, não: leia antes e passe o valor.

## Sondas fora de produção
Só em local ou ambiente de teste, com autorização, registrando esperado, obtido e evidência:
1. Rota protegida sem login: tem de negar sem devolver dado.
2. Token depois do logout.
3. Cookie adulterado.
4. Usuário A pedindo o registro de B (IDOR).
5. Cabeçalho `x-middleware-subrequest`, se a versão for afetada.
6. Senha errada contra usuário inexistente (mensagem e tempo iguais).

Reproduza duas vezes. Confirme que a porta funciona, não só que ela existe.
