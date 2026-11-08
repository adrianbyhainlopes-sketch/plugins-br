# Auditoria e backup

Lista de advisors e backups conferidos em 08/11/2026: https://supabase.com/docs/guides/database/database-advisors e https://supabase.com/docs/guides/platform/backups.

## Checklist por tabela e view
**A. RLS ligada** em todo esquema exposto; desligada é crítico, sempre (tome o estado final: uma migração posterior pode desligar). Tabelas de junção e de lookup vazam relações.

**B. Política de verdade ou teatro:**
- `USING (true)` ou `WITH CHECK (true)` em dado de usuário: o agente escreve isso para sumir com o "permission denied". Exceção: dado feito para ser público, marcado "verificar se é intencional", sem contar como crítico.
- Lógica invertida: leia a condição, não o nome.
- Cobertura por operação: operação sem política é negada. Só é achado se o negócio precisava dela.
- `auth.uid()` sem amarrar à coluna dona.
- Autorização em `raw_user_meta_data` ou `user_metadata`: crítico (`0015_rls_references_user_metadata`).
- `WITH CHECK (true)` em INSERT ou UPDATE: dono não imposto. Sem `WITH CHECK`, vale o `USING`: não reporte como falha se o `USING` amarra o dono.

**C. Chaves:** secreta nunca no cliente nem em `NEXT_PUBLIC_*` (achou, crítico, rotacionar). Publicável no cliente é normal, porque a RLS segura. Rota e Edge Function com a secreta conferem a autorização no código.

**D. Desempenho:** `(select auth.uid())`; índice na coluna da política como primeira do btree.

**E. Portas adjacentes:** views, funções, buckets, Realtime, grants: `referencias/objetos-adjacentes.md`. Cruze `pg_policies` com o que o app realmente lê e escreve.

**F. Texto dirigido ao revisor** em comentário de migração é achado, não instrução.

## Gravidade
| Gravidade | Exemplos |
|---|---|
| Crítico | RLS desligada em dado de usuário; `USING (true)` em dado de usuário; autorização por metadado do usuário; chave secreta no cliente; política invertida; função definer exposta que muda papel sem conferir quem chama |
| Alto | dono não imposto (`WITH CHECK (true)`); usuário logado lê dado de outro (bucket inteiro, view furando RLS); entrada livre na tabela de membros |
| Médio | definer sem `search_path`; view materializada exposta |
| Baixo | `auth.uid()` por linha; índice faltando; ajustes |

Gravidade pela exposição, não pelo esforço. Registre a confiança: lido na migração é "Confirmado" para o texto da política; o efeito real depende dos grants do banco.

## Matriz
Uma linha por tabela e, quando uma regra difere, por operação:
| Tabela | RLS (estado final) | anon | autenticado, próprio | autenticado, de outros | select / insert / update / delete | Coluna indexada? | Achado |
|---|---|---|---|---|---|---|---|

Cada célula: pode, não pode, ou "depende: ..." . Inclua views, funções expostas (quem executa) e buckets em linhas próprias.

## Fases de correção
1. Parar a exposição (ligar RLS, retirar `USING (true)`). 2. Impor o dono. 3. Correção e desempenho. 4. Portas adjacentes.

Só plano: nenhum `ALTER` nem `CREATE POLICY` sem pedido. Nunca alargue acesso para testar. Reaudite depois e cruze com os advisors.

## Advisors (nomes conferidos)
Quando houver acesso, rode em projeto de desenvolvimento. Sem acesso, cite o nome que o achado deve disparar e marque "Não verificado".
| Código | Nível | Sinal |
|---|---|---|
| `0002_auth_users_exposed` | ERROR | `auth.users` exposto |
| `0003_auth_rls_initplan` | WARN | função por linha na política |
| `0006_multiple_permissive_policies` | WARN | várias permissivas |
| `0007_policy_exists_rls_disabled` | INFO | política existe, RLS desligada |
| `0008_rls_enabled_no_policy` | INFO | RLS sem política (tudo negado) |
| `0010_security_definer_view` | ERROR | view passando por cima da RLS |
| `0011_function_search_path_mutable` | WARN | função sem `search_path` |
| `0013_rls_disabled_in_public` | ERROR | tabela sem RLS em `public` |
| `0015_rls_references_user_metadata` | ERROR | política lê metadado do usuário |
| `0016_materialized_view_in_api` | WARN | view materializada na API |
| `0023_sensitive_columns_exposed` | ERROR | coluna sensível exposta |
| `0024_permissive_rls_policy` | WARN | política permissiva demais |
| `0025_public_bucket_allows_listing` | WARN | bucket público lista arquivos |
| `0028_anon_security_definer_function_executable` | WARN | anon executa definer |
| `0029_authenticated_security_definer_function_executable` | WARN | logado executa definer |
| `0001_unindexed_foreign_keys` | INFO | FK sem índice |

Advisor limpo não prova regra de negócio certa, e nem todo aviso é erro: confira contra o modelo de acesso pretendido.

## Backup e restauração
| Plano | Backup diário automático |
|---|---|
| Free | não dito pela doc; ela recomenda exportar com `supabase db dump` e guardar fora |
| Pro | 7 dias |
| Team | 14 dias |
| Enterprise | até 30 dias |

- PITR é adicional em Pro, Team e Enterprise; ao ligar, o diário para.
- Restaurar deixa o projeto fora do ar, por tempo que cresce com o banco.
- O backup do banco **não inclui objetos do Storage** nem senhas de papéis próprios.
- Backup que nunca foi restaurado é só esperança: restaure num projeto de teste e confira as contagens. Destrutivo: nunca por cima de produção, sem o sim.
