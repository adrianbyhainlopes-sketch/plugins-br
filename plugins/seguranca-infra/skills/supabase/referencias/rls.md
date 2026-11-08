# RLS

Conferido em 08/11/2026: https://supabase.com/docs/guides/database/postgres/row-level-security e guia de desempenho de RLS.

## O que cada cláusula faz
| Operação | Cláusula | Efeito |
|---|---|---|
| SELECT | `using` | quais linhas o papel enxerga |
| INSERT | `with check` | a linha nova tem de passar |
| UPDATE | `using` e `with check` | `using` escolhe as linhas existentes; `with check` confere a linha resultante |
| DELETE | `using` | quais linhas pode apagar |

- Sem `with check`, o `using` também governa a linha nova. Um UPDATE com `using` que amarra o dono e sem `with check` **não** permite trocar o dono. O problema é `with check (true)`, ou `with check` que não amarra a coluna.
- UPDATE precisa de política de SELECT correspondente, senão não funciona como esperado.
- Negação não é igual em toda operação: INSERT que não passa no `with check` lança erro; UPDATE ou DELETE em linha que o `using` não alcança filtram e "dão certo" sem mudar nada; UPDATE que passa no `using` e falha no `with check` lança erro.
- RLS não é automática para tabela criada por SQL. A doc oferece event trigger para ligar em toda tabela nova.
- Grant e RLS são camadas separadas: sem grant, o papel nem chega à política.

## Formato conferido
```sql
alter table public.notas enable row level security;

create policy "notas: dono lê"
on public.notas for select to authenticated
using ((select auth.uid()) = user_id);

create policy "notas: dono cria"
on public.notas for insert to authenticated
with check ((select auth.uid()) = user_id);

create policy "notas: dono edita"
on public.notas for update to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "notas: dono apaga"
on public.notas for delete to authenticated
using ((select auth.uid()) = user_id);

create index on public.notas (user_id);
```

- `(select auth.uid())`: o otimizador guarda o valor por instrução, em vez de chamar a cada linha. Vale para `auth.jwt()` e para função security definer, **só** quando o resultado não depende da linha. Função que recebe valor da linha não pode ser envolvida assim. O advisor aponta como `0003_auth_rls_initplan`.
- `to authenticated`: a política nem é avaliada para os outros papéis. `to anon using (true)` libera para todo visitante.
- Índice em toda coluna usada na condição, como **primeira** coluna do btree. Chave primária composta `(org_id, user_id)` não indexa `user_id`.
- Depois da RLS, filtre também na consulta (`.eq('user_id', id)`) por desempenho. Isso ajuda o plano e não é proteção.

## Modelos
**Leitura pública, escrita do dono:** select `to anon, authenticated using (publicado = true)`; escrita como acima. `using (true)` só em dado feito para ser público, e dito por quem decide.

**Membros de organização.** Consulta à tabela de membros dentro da política passa pelo RLS dela e pode virar recursão. Use função em esquema não exposto:
```sql
create schema if not exists privado;

create or replace function privado.orgs_do_usuario()
returns setof uuid
language sql stable security definer
set search_path = ''
as $$
  select org_id from public.org_membros
  where user_id = (select auth.uid());
$$;

revoke execute on function privado.orgs_do_usuario() from public, anon;
grant usage on schema privado to authenticated;
grant execute on function privado.orgs_do_usuario() to authenticated;

create policy "lancamentos: membros leem"
on public.lancamentos for select to authenticated
using (org_id in (select privado.orgs_do_usuario()));
```
Compare a coluna com um conjunto (`in`, `any`) em vez de juntar tabela por linha. Lista enorme (a doc cita cerca de 10 mil itens) pede análise.

**Administrador por claim:** `((select auth.jwt()) -> 'app_metadata' ->> 'papel') = 'admin'`. Só `app_metadata`: o usuário não o altera. O JWT pode estar velho até renovar: revogação de papel não vale na hora; para isso, tabela.

**Inserir com dono fixo:** `with check` sempre confere o dono; o valor vem do chamador, nunca aceite o dono do corpo.

**Dono imutável:** `using` e `with check` amarrando o dono já impedem a troca. Coluna imutável que a política não cobre: trigger ou constraint.

**Segundo fator:** `(select auth.jwt()) ->> 'aal' = 'aal2'`, em política restritiva.

## Como políticas se combinam
Permissivas somam por OU: uma frouxa anula as outras. Restritivas somam por E. Várias permissivas para o mesmo papel e operação custam desempenho (`0006_multiple_permissive_policies`).

## Quem passa por cima
Chave secreta (papel `service_role`, com `bypassrls`), só quando a requisição não leva token de usuário; papel com `bypassrls`; função security definer de dono `postgres`; view criada por `postgres`. O app tem de conectar com um papel ao qual a RLS se aplica.

## Depurar
Nenhuma linha volta: RLS ligada? Política existe para essa operação? Claims certos? `TO` certo? Permissão negada: falta grant, ou INSERT que não passa no `with check`. Nunca resolva afrouxando.
