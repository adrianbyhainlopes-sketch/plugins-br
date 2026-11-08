# Testes de RLS

Forma conferida em 08/11/2026 em https://supabase.com/docs/guides/database/postgres/testing-row-level-security e nos guias de teste. O esqueleto abaixo foi escrito a partir da doc e **não foi rodado** contra um banco: adapte às colunas reais e rode localmente.

## Regra
Três atores em toda tabela com dado de usuário: **anônimo** falha, **dono** consegue, **outro usuário** falha. Mais: A contra o id de B, em leitura, edição e exclusão. Sem o teste negativo há só uma intenção de isolamento.

Combine as regras de acesso antes e escreva um teste por regra.

## Esqueleto com pgTAP
Crie com `supabase test new tabela_rls`. Rode com `supabase test db` (banco local). Roda em transação e desfaz no fim.
```sql
begin;
select plan(6);

-- Preparação (antes de trocar de papel). Ajuste às colunas reais.
insert into auth.users (id, email) values
  ('11111111-1111-1111-1111-111111111111', 'a@exemplo.test'),
  ('22222222-2222-2222-2222-222222222222', 'b@exemplo.test');
insert into public.notas (id, user_id, texto) values
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 'de A');

-- Anônimo. Sem grant, o select lança 42501: troque por throws_ok.
set local role anon;
select is_empty($$ select id from public.notas $$, 'anônimo não lê');

-- Dono
set local role authenticated;
set local request.jwt.claim.sub = '11111111-1111-1111-1111-111111111111';
select results_eq($$ select count(*)::int from public.notas $$, array[1], 'A lê a própria');
select results_eq(
  $$ update public.notas set texto = 'novo' where id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa' returning id::text $$,
  array['aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'],
  'A edita a própria'
);

-- Outro usuário
set local request.jwt.claim.sub = '22222222-2222-2222-2222-222222222222';
select is_empty($$ select id from public.notas where id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa' $$, 'B não lê a de A');
select is_empty(
  $$ update public.notas set texto = 'x' where id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa' returning id $$,
  'B não edita a de A'
);
select throws_ok(
  $$ insert into public.notas (user_id, texto) values ('11111111-1111-1111-1111-111111111111', 'forjada') $$,
  '42501',
  null,
  'B não cria em nome de A'
);

select * from finish();
rollback;
```

## O que muda o resultado
- **UPDATE e DELETE barrados pelo `using` não dão erro:** filtram e devolvem zero linhas. Teste com `returning` e `is_empty`. UPDATE barrado só pelo `with check` lança `42501`.
- **INSERT negado lança** `42501`: use `throws_ok`.
- **`lives_ok` em escrita permitida passa com zero linhas:** use `results_eq` com `returning`. Junto de cada escrita negada, confira que a linha continua intacta.
- Teste por papel e olhe o que volta; olhar `pg_policies` não prova nada.
- Filtre pelas linhas que o teste inseriu, por id.
- **A claim:** a doc usa `request.jwt.claim.sub` no guia e `request.jwt.claims` (JSON) em outras páginas. Se `auth.uid()` vier nulo, teste a outra forma na versão instalada.
- Falhou? Diga qual asserção e qual política discordam, e deixe o dono decidir. **Nunca mude a política para o teste passar.**

## Prove que o teste consegue falhar
Quebre de propósito: acrescente uma política temporária `using (true)`, veja o teste falhar, retire. Apagar a política verdadeira não prova nada.

## Ajudantes
A doc mostra o pacote de terceiros `supabase_test_helpers` (`tests.create_supabase_user`, `tests.authenticate_as`, `tests.rls_enabled('public')`), instalado por gerenciador de pacotes do banco. Instalar exige o sim do usuário. O esqueleto acima dispensa.

## Pelo cliente
Alternativa: dois usuários de teste em ambiente local, com a chave publicável, tentando ler e alterar o registro um do outro. Nunca com contas reais nem em produção. Lembre: RLS filtra, então o update "dá certo" sem mudar nada; confira a linha depois.

## Entregue
Os testes, o comando para rodar, o resultado de verdade ou "escrito, não rodado: motivo".
