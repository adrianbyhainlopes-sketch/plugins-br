# Migrações

Comandos e comportamento da CLI conferidos em 08/11/2026 em https://supabase.com/docs/guides/local-development/cli-workflows e https://supabase.com/docs/guides/deployment/database-migrations. A CLI muda: confira `supabase --version`.

## Bloco de risco, antes de qualquer resposta
`Risco: SEGURO | ATENÇÃO | PERIGOSO`, os problemas e as correções.

## Cinco condições
Compatível com a versão anterior do app (no deploy as duas rodam contra o mesmo banco); compatível com a próxima migração; reversível, ou a irreversibilidade dita; lock estimado e aceitável; testada num retrato realista.

## Padrões perigosos e a forma segura
| Mudança | Forma segura |
|---|---|
| Apagar coluna ou tabela | parar de escrever (deploy), parar de ler (deploy), apagar numa migração separada, com cópia antes |
| Renomear ou mudar tipo | expandir e contrair: criar a nova anulável, escrever nas duas, backfill em lotes, ler da nova, parar de escrever na velha, apagar a velha. Parar entre dois passos deixa o sistema certo |
| `NOT NULL` em tabela populada | anulável, backfill em lotes, `CHECK (col IS NOT NULL) NOT VALID`, `VALIDATE CONSTRAINT`, `SET NOT NULL` (Postgres 12+ aproveita a constraint e não varre) |
| Default | constante não reescreve a tabela (Postgres 11+); não constante reescreve |
| Índice | `CREATE INDEX CONCURRENTLY`, em migração própria |
| FK e CHECK novos | `NOT VALID` e `VALIDATE` em migração separada; toda FK nova ganha índice |
| Dados e esquema juntos | separar; backfill longo em script por lotes, sem transação longa, retomável pelo último id |

**Fila de lock:** DDL esperando lock bloqueia até os SELECT atrás dele. Sempre `SET lock_timeout = '3s';` antes (ajuste à sua tabela).

**Tamanho:** regra de bolso da fonte, grande é acima de cerca de 100 mil linhas. Conte de verdade, com permissão, em vez de deduzir pelo nome.

**Provar que ninguém usa antes de apagar:** leituras por campo e por cliente ao longo de um ciclo completo, inclusive fechamento mensal; sem `SELECT *` no código.

## Rollback
Toda migração responde "o que eu rodo se o deploy der errado". Destrutiva: script de volta e backup da coluna antes; vira plano de vários deploys.

## Camada Supabase
- Tabela nova nasce com RLS ligada e políticas na mesma migração. Grants conferidos.
- Funções e views novas pelas regras de `referencias/objetos-adjacentes.md`.
- Migração sem segredo. Dado de exemplo em `supabase/seed.sql`, não em migração.
- Uma mudança lógica por arquivo: `supabase/migrations/<timestamp>_<descricao>.sql`, criado com `supabase migration new nome`.

## CLI
| Comando | O que faz | Cuidado |
|---|---|---|
| `supabase db reset` | recria o banco **local**, reaplica migrações e seed | com `--remote` apaga **todos** os dados do projeto ligado |
| `supabase migration up` | aplica pendentes no local | |
| `supabase db diff -f nome` | gera migração a partir de mudanças | leia antes de aceitar |
| `supabase db push --dry-run --remote` | mostra o que seria aplicado | |
| `supabase db push --remote` | aplica pendentes no remoto | quem roda é o usuário |
| `supabase migration list --remote` | compara local e remoto | |
| `supabase migration repair` | só altera a tabela de controle; não aplica nem desfaz SQL | |

Comandos de banco agem no local por padrão; `--remote` age no projeto ligado. Confirme com `supabase projects list`. Nunca `--include-seed` em produção.

**Transação.** Migração cujas instruções não rodam em transação começa com, na primeira linha:
```sql
-- pg-delta: transaction=false
```
`db reset`, `db push` e `migration up` honram a diretiva. A CLI detecta `create index concurrently` e o roda isolado mesmo sem ela. Sem transação, falha deixa aplicado o que já rodou: um comando por arquivo. **A integração com GitHub e o branching não honram a diretiva** e rodam tudo em transação: essas migrações falham lá.

**Depois de migrar:** `supabase db reset` local, advisors, regenerar tipos. Comandos e destrutivos: `referencias/comandos-destrutivos.md`.

## Antipadrões
"Funcionou no staging"; "rodo na janela de manutenção" (a migração reaplica em todo ambiente novo); mega-migração; migração como ETL; mudar default em silêncio; editar migração já aplicada; aplicar em produção de dentro da sessão.

## Ordem de leitura na revisão
A tabela é grande? Há DROP, RENAME, NOT NULL ou FK sem índice? Todo índice é CONCURRENTLY? Há UPDATE ou INSERT embutido? O rollback está esboçado? RLS e grants da tabela nova?
