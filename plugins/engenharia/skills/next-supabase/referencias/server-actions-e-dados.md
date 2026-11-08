# Server Actions e fronteira de dados

Conferido em 08/11/2026 no guia de segurança de dados e na referência de `serverActions` e de `redirect` do Next, e na referência de `useActionState` do React.

## Módulo por rota
- `page.tsx`: Server Component assíncrono e fino (busca e compõe).
- `actions.ts` com `'use server'`: actions finas que chamam a camada de dados.
- Camada de acesso a dados (por exemplo `data/` ou `lib/dal/`) com `import 'server-only'`: autentica, autoriza, consulta e devolve objetos mínimos (DTO). É o único lugar que lê `process.env` e fala com o banco. Recomendada pelo Next para projeto novo.
- `schemas.ts`: esquemas Zod; tipos inferidos deles.
- `components/`: ilhas de cliente.

## Uma Server Action segura
```ts
'use server'
import { z } from 'zod'
import { updateTag } from 'next/cache'
import { criarClienteServidor } from '@/lib/supabase/servidor'

const Entrada = z.strictObject({ id: z.uuid(), nome: z.string().trim().min(1).max(120) })

export async function renomearProjeto(_: unknown, form: FormData) {
  const lido = Entrada.safeParse({ id: form.get('id'), nome: form.get('nome') })
  if (!lido.success) return { ok: false as const, erro: 'Confira os campos.', valores: { nome: String(form.get('nome') ?? '') } }

  const supabase = await criarClienteServidor()
  const { data } = await supabase.auth.getClaims()
  const usuario = data?.claims?.sub
  if (!usuario) return { ok: false as const, erro: 'Entre de novo para continuar.' }

  const { data: linha, error } = await supabase
    .from('projetos').update({ nome: lido.data.nome })
    .eq('id', lido.data.id).eq('dono_id', usuario)   // defesa a mais; quem protege é o RLS
    .select('id').maybeSingle()
  if (error) throw error                     // erro sobe; não vira "ok"
  if (!linha) return { ok: false as const, erro: 'Projeto não encontrado.' }   // 404 para "existe mas não é seu"

  updateTag(`projeto-${lido.data.id}`)
  return { ok: true as const }
}
```
Confira na versão instalada: a API do Zod (`z.strictObject`, `z.uuid()` são do Zod 4; no Zod 3, `z.object({...}).strict()` e `z.string().uuid()`) e o nome dos seus ajudantes.

Regras:
- Autenticar e autorizar dentro de cada action. IDs cifrados e a remoção de action não usada reduzem o risco, mas não substituem a checagem.
- Validar todo argumento (FormData, parâmetros de URL, cabeçalhos): esquema estrito recusa campo desconhecido (evita `{ "papel": "admin" }` passar).
- Devolver o mínimo: nunca o registro inteiro do banco; o retorno é serializado e vai ao cliente.
- União discriminada no retorno (`{ ok: true, ... } | { ok: false, erro }`), argumentos e retorno serializáveis.
- Variável capturada em closure de action vai cifrada ao cliente e volta: não ponha segredo nela.
- `redirect()` lança um erro especial: chame fora do `try` (dentro, ele é engolido). Em action com formulário enviado sem JavaScript responde 303; nos outros casos, 307.
- Mutação nunca como efeito do render (apagar cookie ou invalidar cache dentro de um Server Component): só em action.
- Operação cara (e-mail, gravação em massa): considere limite de taxa.

## Origem, tamanho e proxy reverso
- O Next compara o host do cabeçalho `Origin` com o host da aplicação (`x-forwarded-host` ou `host`) e recusa se forem diferentes. Pedido sem `Origin` passa, com aviso.
- Atrás de proxy reverso que não repassa o host público: `experimental.serverActions.allowedOrigins` com o host que aparece na barra do navegador.
- Corpo da action: até 1 MB por padrão (`experimental.serverActions.bodySizeLimit`); upload grande vai por outro caminho.
- Vários servidores com a mesma build: chave de cifra fixa por `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`, tratada como segredo.

## O que vai ao cliente
- Props de Client Component só com os campos que ele mostra; tipo da prop estreito.
- Funções e classes já são barradas de passar ao cliente.
- APIs de taint do React (`experimental_taintObjectReference`, `experimental_taintUniqueValue`) com `experimental.taint: true` são uma camada a mais, não substituem filtrar na camada de dados.

## Formulário no cliente (React 19)
```tsx
'use client'
import { useActionState } from 'react'
const [estado, enviar, pendente] = useActionState(renomearProjeto, null)
<form action={enviar}>
  <input name="nome" defaultValue={estado && !estado.ok ? estado.valores?.nome : ''} disabled={pendente} />
  <button disabled={pendente}>Salvar</button>
  {estado && !estado.ok && <p role="alert">{estado.erro}</p>}
</form>
```
- O formulário com `action` reseta sozinho depois do envio: para manter o que o usuário digitou depois de um erro, devolva o valor e use como `defaultValue`.
- Botão desabilitado enquanto pendente; o servidor valida de novo de qualquer jeito.
- Campo numérico vazio vira `null`, não `0`; `NaN` é tratado como vazio.
- Rótulo visível ligado ao campo; erro perto do campo, ligado por `aria-describedby`; foco no primeiro campo inválido.

## Auditoria rápida
Arquivos `'use server'`: argumentos validados? usuário reautorizado? dono do recurso conferido? retorno filtrado? banco só pela camada `server-only`? Pastas com colchetes (`[id]`) são entrada do usuário: validadas? `proxy.ts` e `route.ts` merecem tempo extra.
