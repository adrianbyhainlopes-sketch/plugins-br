<!-- cópia gerada de compartilhado/supabase-auth.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Supabase Auth no código (Next.js 16 com @supabase/ssr)

Conferido em 08/11/2026 na documentação do Supabase (SSR com Next.js, criação do cliente, `getClaims`, chaves de API) e no exemplo oficial `with-supabase` do Next.js. Antes de escrever código, confira a versão instalada de `@supabase/ssr` e de `@supabase/supabase-js` no lockfile: se o tipo ou a assinatura abaixo não bater com a versão instalada, vale a instalada.

Este arquivo cobre a chamada no código. RLS, migrações, grants e Storage são assunto de segurança e banco: revise com o plugin de segurança, se houver, e nunca troque uma policy "para funcionar".

## Chaves
| Chave | Formato | Onde | Papel no Postgres |
|---|---|---|---|
| Publicável | `sb_publishable_...` | pode ir ao navegador | `anon` sem login, `authenticated` com login |
| Secreta | `sb_secret_...` | só no servidor (rota, job, função de borda) | `service_role`, que ignora o RLS (`BYPASSRLS`) |
| `anon` e `service_role` antigas | JWT longos | equivalentes antigas das duas acima | em descontinuação até o fim de 2026; valem até serem desligadas no painel |

- A chave publicável é pública por definição: quem protege o dado é o RLS. Filtro `.eq('user_id', ...)` no cliente não é proteção.
- A secreta nunca com prefixo `NEXT_PUBLIC_`, nunca em Client Component, nunca em log. O Supabase recusa a secreta vinda de navegador (401), mas isso não desfaz o vazamento: se ela apareceu no bundle ou no git, troque a chave.
- Código que usa a secreta (ignora o RLS) confere a autorização no próprio código, antes de ler ou gravar.

## Variáveis
`NEXT_PUBLIC_SUPABASE_URL` e `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` (nomes da doc atual; projeto antigo pode usar `..._ANON_KEY`). A secreta, se precisar, com nome sem prefixo público (por exemplo `SUPABASE_SECRET_KEY`), lida só em módulo com `import 'server-only'`.

## Clientes
- **Navegador:** `createBrowserClient(url, chavePublicavel)` em Client Component. É instância única: chamar de novo devolve a mesma.
- **Servidor:** `createServerClient(url, chavePublicavel, { cookies: { getAll, setAll } })`, **um por requisição** (precisa dos cookies daquela requisição). Nunca guarde o cliente de servidor numa variável global ou de módulo.
  - `getAll()` devolve `(await cookies()).getAll()` (no Next 16, `cookies()` é assíncrono).
  - `setAll(...)` grava os cookies; em Server Component não dá para gravar cabeçalho, então a gravação fica num `try/catch` que ignora o erro (a renovação acontece no proxy).
  - O `setAll` também recebe os cabeçalhos `Cache-Control`, `Expires` e `Pragma`: aplique-os à resposta para a CDN não guardar a página de um usuário e entregar a outro. Confira na versão instalada como eles chegam ao `setAll`.
- **Proxy (`proxy.ts`, Next 16; `middleware.ts` até o 15):** cria o cliente de servidor com os cookies da requisição, chama `supabase.auth.getClaims()` para renovar o token, passa o token novo aos Server Components (`request.cookies.set`) e ao navegador (`response.cookies.set`), e devolve **o mesmo objeto de resposta** que o `setAll` montou. Se precisar de outra resposta, crie com `NextResponse.next({ request })`, copie os cookies e os três cabeçalhos de cache. Use um `matcher` para não rodar em rota que não toca no Supabase.
  - Não rode código entre `createServerClient` e `getClaims()` (aviso do exemplo oficial: causa logout aleatório difícil de achar).
  - Renovar em dois lugares desloga: o token de renovação vale uma vez, e o reuso fora da exceção permitida revoga a sessão.

## Quem é o usuário: `getSession`, `getClaims`, `getUser`
| Chamada | O que faz | Use para |
|---|---|---|
| `getSession()` | lê a sessão do cookie, sem revalidar | só no navegador. **Nunca no servidor** (proxy, Server Component, Server Action, rota): o cookie pode ser forjado |
| `getClaims()` | confere a assinatura do JWT a cada chamada (com chave assimétrica, pelo JWKS em cache; sem ela, chama o servidor de Auth) | proteger página e dado no servidor; renovar no proxy |
| `getUser()` | sempre consulta o servidor de Auth e devolve o registro atual | quando precisa do registro atual (a conta ainda existe, metadados novos) |

Sessão encerrada: o token de acesso de uma sessão revogada continua válido até o `exp` (doc de sign-out, conferida em 08/11/2026), e o padrão recomendado é 1 hora. Logo, `getClaims()` com chave assimétrica não percebe o logout antes de expirar (inferido da doc, não testado). Para ação muito sensível (dinheiro, troca de e-mail ou senha, apagar conta), a doc de sessões dá a forma garantida: comparar a claim `session_id` com a chave primária de `auth.sessions`; sem linha, o usuário saiu. Se `getUser()` recusa token de sessão encerrada: não dito nas páginas lidas, a conferir.

## Onde conferir a identidade
- O proxy é roteamento, não fronteira de segurança. Confira de novo na Server Action, na rota e na camada de dados (CVE-2025-29927 mostrou autorização só no middleware sendo contornada; confira a versão afetada no advisory, não de memória).
- Toda Server Action é um POST público: autenticar (`getClaims`) e autorizar (este usuário pode mexer neste registro?) dentro de cada uma.
- Identidade vem do token conferido (`claims.sub`), nunca de um campo do formulário ou do corpo.

## Sinais de problema numa revisão
- `getSession(` em arquivo de servidor: achado até provar que roda só no navegador.
- Cliente de servidor em variável de módulo.
- Proxy que cria uma resposta nova sem copiar cookies e cabeçalhos.
- Chave secreta em arquivo com `'use client'`, em `NEXT_PUBLIC_*` ou em código importado pelos dois lados.
- Página protegida só no layout ou só no proxy, com Server Action ou rota sem conferência própria.
