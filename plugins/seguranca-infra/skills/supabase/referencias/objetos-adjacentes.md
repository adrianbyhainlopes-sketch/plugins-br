# Grants, views, funções, Storage e Realtime

Conferido em 08/11/2026 na documentação do Supabase. O que aparece aqui fura RLS por fora da tabela.

## Grants
- Em projeto existente, objeto novo em `public` recebe por padrão todos os privilégios de tabela, `execute` em função e `usage, select, update` em sequência para `anon`, `authenticated` e `service_role`. "Sem RLS" significa aberto.
- A doc diz que a plataforma vai revogar esses grants automáticos (exposição opcional), sem data na página. **Confira o projeto real** antes de afirmar: ajuste "Automatically expose new tables" e `\dp`.
- Para desligar o padrão: ajuste no painel e `alter default privileges for role postgres in schema public revoke all on tables from anon, authenticated, service_role;` (e o mesmo para `sequences` e `functions`). Depois disso, função usada em política precisa de `grant execute`, senão a política falha.
- Dê a cada papel só o que ele usa: `grant select on public.t to authenticated;`.
- Para não expor, um esquema só para a API (`api`) e o resto em esquemas fora das "exposed schemas". App que não usa a Data API pode desligá-la.

## Views
Views passam por cima da RLS por padrão, porque são criadas por `postgres`. No Postgres 15 ou mais novo:
```sql
create view public.vw_resumo with (security_invoker = true) as select ...;
```
Em versão antiga, revogue de `anon` e `authenticated` ou mova para esquema não exposto. Advisor: `0010_security_definer_view`. View materializada não tem RLS: `0016_materialized_view_in_api`.

## Funções
RLS não vale para função: quem tem `execute` chama pela API.
- Prefira `security invoker` (padrão).
- Definer só para lógica de autorização que precisa ler tabela protegida. Sempre `set search_path = ''`, nomes qualificados (`public.tabela`), corpo enxuto, entrada validada e `(select auth.uid())` conferido dentro quando a função muda dado.
- Fora de esquema exposto.
- `revoke execute on function ... from public;` e de `anon`, e `grant execute` só a quem chama. Padrão global: `alter default privileges for role postgres revoke execute on functions from public;` (sem `in schema`: revogar por esquema não anula o padrão global).
- Advisors: `0011_function_search_path_mutable`, `0028_anon_security_definer_function_executable`, `0029_authenticated_security_definer_function_executable`.

Função security definer exposta que muda papel, saldo ou dono sem conferir quem chama é escalada: **crítico**, mesmo com a tabela blindada.

## Storage
- Política em `storage.objects`. Upload pede `INSERT`; upsert pede também `SELECT` e `UPDATE`.
- Bucket privado: toda operação, inclusive download, passa por política. Bucket público: leitura livre para quem tem a URL; upload, delete, mover e copiar seguem controlados. `0025_public_bucket_allows_listing` avisa listagem.
- Uma pasta por usuário:
```sql
create policy "comprovantes: dono envia"
on storage.objects for insert to authenticated
with check (
  bucket_id = 'comprovantes'
  and (storage.foldername(name))[1] = (select auth.uid()::text)
);
```
Faça o mesmo para SELECT, UPDATE e DELETE: política só com `bucket_id` libera o bucket inteiro a todo logado.
- `owner_id`: nos exemplos da doc é comparado a `auth.jwt()->>'sub'`; o tipo não está dito na página, confira no projeto.
- Limite de tamanho e tipo no bucket; no cliente é só experiência.
- URL assinada de minutos, não de dias. A chave secreta ignora a política.

## Realtime
- Postgres Changes obedece às políticas de SELECT da tabela. A tabela precisa estar na publicação; desligue onde não usa.
- Broadcast e Presence: políticas em `realtime.messages`, usando `realtime.topic()` e `extension`; o cliente abre canal `private: true`; e desligue "Allow public access" nas configurações do Realtime.
- A política fica em cache durante a conexão: acesso revogado persiste até o JWT expirar ou ser renovado.

## Edge Function
Valida o JWT logo no início; CORS explícito; código comum em `_shared`. Com a chave secreta, a autorização é do código.

## Checklist final
RLS em todas as tabelas, inclusive junção; chave secreta fora do cliente; nenhum `USING (true)` sem intenção; nada em `raw_user_meta_data`; confirmação de e-mail ligada; buckets com limite; índices nas colunas das políticas; SQL parametrizado (inclusive em `.rpc`); políticas de `anon` no mínimo; Realtime só onde precisa; papel nunca checado só na interface; migração sem segredo.
