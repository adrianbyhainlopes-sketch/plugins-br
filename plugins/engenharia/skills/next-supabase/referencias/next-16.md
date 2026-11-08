# Next.js 16 (conferido em 08/11/2026)

Fonte: guia de atualização para a versão 16 e referência de `fetch` em nextjs.org (atualizados em novembro e agosto de 2026). Se a versão instalada for outra, vale a documentação dela (`node_modules/next/dist/docs/`).

## Requisitos e ferramentas
- Node 20.9 ou mais novo; TypeScript 5.1 ou mais novo.
- Turbopack é o padrão em `next dev` e `next build`. Configuração `webpack` própria (ou de um plugin) faz o build falhar; `--webpack` sai do Turbopack. A configuração `turbopack` fica no topo do `next.config`, não mais em `experimental`.
- `next lint` foi removido e `next build` não roda lint: use o ESLint ou o Biome direto.
- `next dev` grava em `.next/dev`; há trava contra dois `next dev` ou `next build` no mesmo projeto.

## Proxy
- `middleware.ts` virou `proxy.ts`, e a função exportada, `proxy`. O runtime do proxy é `nodejs` e não muda; quem precisa do runtime `edge` continua com `middleware`.
- Opções com "middleware" no nome foram renomeadas (por exemplo `skipProxyUrlNormalize`).
- O proxy é roteamento, não fronteira de segurança: autorização também na action, na rota e na camada de dados (a CVE-2025-29927 contornava autorização feita só no middleware; confira a versão afetada no advisory, não de memória).

## APIs de requisição assíncronas
Acesso síncrono foi removido: `await cookies()`, `await headers()`, `await draftMode()`, `await params`, `await searchParams` (em page, layout, route, default e nas imagens de metadados). `next typegen` gera `PageProps<'/rota/[id]'>`, `LayoutProps` e `RouteContext` para tipar.
```tsx
export default async function Page(props: PageProps<'/clientes/[id]'>) {
  const { id } = await props.params
  ...
}
```

## Cache e invalidação
- `fetch` no servidor: padrão "auto no cache" (busca a cada requisição se a rota usa API de requisição; uma vez no build se a rota é estática). Cachear é opcional: `cache: 'force-cache'`, `next: { revalidate: n }`, `next: { tags: [...] }`.
- `revalidateTag(tag, perfil)`: o segundo argumento (um perfil do `cacheLife`, como `'max'`) é obrigatório; a forma de um argumento é obsoleta e dá erro de tipo. Quem lê vê o dado antigo enquanto o novo carrega.
- `updateTag(tag)`: só dentro de Server Action; quem escreveu vê a mudança na hora (lê o que escreveu). Use em formulário e configuração do usuário.
- `refresh()`: atualiza o roteador do cliente de dentro de uma Server Action.
- `revalidatePath(caminho)` continua existindo.
- `cacheLife` e `cacheTag` estáveis (sem `unstable_`).
- `cacheComponents: true` liga o modelo de Cache Components (`"use cache"`) e substitui `experimental.dynamicIO`, `experimental.useCache` e o PPR experimental. Ligar não é só renomear: pode gerar erro de build para dado sem cache fora de `<Suspense>`. Não ligue só para concluir uma atualização.
- Erros comuns: esquecer de invalidar depois da mutação; misturar `revalidate` de segmento com `"use cache"` no mesmo dado; `cache()` do React em volta de `fetch` já cacheado.

## React
- O App Router do Next 16 usa o React 19.2 (canário), com `ViewTransition`, `useEffectEvent` e `Activity`.
- React Compiler: `reactCompiler: true` é estável, mas desligado por padrão. Com ele ligado, não acrescente `useMemo` e `useCallback` "faltando".
- Página continua Server Component; `'use client'` só nas folhas interativas.
- Nada de `Date.now()`, `Math.random()` ou `localStorage` no render de componente que roda no servidor (quebra a hidratação).
- Estado derivado se calcula no render, não num `useEffect` que sincroniza; resetar estado trocando a `key`; nunca desligar a regra de dependências do effect.

## next/image (mudanças que quebram)
`images.qualities` padrão só `[75]`; `minimumCacheTTL` padrão de 4 horas; `16` saiu de `imageSizes`; imagem local com query string exige `localPatterns.search`; `images.domains` obsoleto (use `remotePatterns`); no máximo 3 redirecionamentos; IP local bloqueado por padrão.

## Outros
- Rotas paralelas exigem `default.js` em cada slot.
- `serverRuntimeConfig` e `publicRuntimeConfig` saíram: variáveis de ambiente direto no servidor; `NEXT_PUBLIC_` para o cliente; `await connection()` antes de ler `process.env` quando o valor tem de ser lido em tempo de execução.
- AMP removido.
- Atualização: o codemod `upgrade` não roda todas as migrações (as APIs assíncronas têm codemod próprio). Feche a lista de conferência do guia antes de dizer que a atualização terminou: build verde sozinho não fecha achado de execução.
