# Testes com Next.js 16 e Supabase

Confira as versões no lockfile antes; o Next 16 exige Node 20.9+ e removeu o acesso síncrono a `params`, `searchParams`, `cookies()` e `headers()` (doc de atualização do Next 16, conferida em 08/11/2026).

## Onde testar cada coisa
| peça | nível | como |
|---|---|---|
| regra de negócio pura (cálculo, validação, parse) | unidade | Vitest, sem Next, sem rede |
| Server Action | integração | chame a função exportada direto, com um `FormData` montado no teste; mock só de `next/headers` (cookies) e do cliente de terceiros; banco real local |
| Server Component assíncrono | integração leve ou ponta a ponta | prefira testar o carregador de dados que ele chama; o componente inteiro, pelo navegador (Playwright) |
| Client Component | unidade | Vitest com Testing Library; mock de `next/navigation` (`useRouter`, `usePathname`) |
| fluxo completo (login, formulário, gravação) | ponta a ponta | Playwright contra `next build` + `next start` e Supabase local |

## Server Action
- Teste o que importa na fronteira: sem sessão é recusado; sessão de outro usuário não mexe no registro alheio; entrada inválida volta erro de validação sem gravar; entrada válida grava e devolve só o que a tela precisa.
- Confira o retorno E o estado gravado (leia de volta do banco).
- `redirect()` lança um erro especial (`NEXT_REDIRECT`): no teste, espere essa exceção ou isole o redirecionamento; no código, ele fica fora do `try`.
- Duas chamadas em paralelo com a mesma entrada: um efeito só, se a ação deve ser idempotente.

## Supabase local
- `supabase start` sobe Postgres, Auth e a API localmente (precisa do Docker); `supabase db reset` reaplica as migrações e o seed **no banco local**. Nunca rode `db reset` ou `db push` contra o projeto remoto sem o sim do usuário (ver `comandos-destrutivos.md`).
- Os testes usam a URL e as chaves do ambiente local, que a CLI mostra ao subir; nunca as do projeto de produção.
- Isolamento: cada teste cria os próprios dados com IDs únicos, ou roda numa transação desfeita no fim.
- RLS se testa com três atores: anônimo, usuário dono, outro usuário. O teste de RLS com pgTAP e a revisão das policies são do plugin de segurança, se houver.
- Tipos gerados (`supabase gen types`) são a fonte da verdade do formato: fixture com a forma completa do tipo, não um objeto parcial.

## Playwright
- Contra o build de produção, não contra o servidor de desenvolvimento.
- Espere por elemento e estado, nunca por tempo fixo.
- Login por API ou estado salvo, não pela tela a cada teste.
- Rode as larguras de computador e de celular quando a mudança é de interface.
- Servidor que você subiu para o teste: pare pelo PID no fim.

## O que não dá para provar localmente
Comportamento de CDN e cache da hospedagem, variáveis de ambiente de produção, limites do plano, e-mail real. Vai para "Não verificado", com o que conferiria (um preview, um log).
