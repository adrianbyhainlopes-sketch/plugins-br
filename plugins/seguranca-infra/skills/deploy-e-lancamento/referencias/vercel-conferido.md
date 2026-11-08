# Vercel, conferido em 08/11/2026

Reconfira depois de 6 meses (a partir de 08/05/2027) ou antes de decidir por um número. Data ao lado de cada fonte: atualização indicada pela página.

## Limites por plano
| Item | Hobby | Pro | Enterprise | Fonte |
|---|---|---|---|---|
| Duração de função (padrão e máximo, com Fluid compute) | 300 s e 300 s | 300 s e 800 s; 1.800 s em beta | 300 s e 800 s; 1.800 s em beta | functions/limitations (24/08/2026) |
| Memória máxima | 2 GB | 4 GB | 4 GB | mesma |
| Corpo de requisição ou resposta | 4,5 MB (resposta em streaming fora) | igual | igual | mesma |
| Cron: número por projeto | 100 | 100 | 100 | cron-jobs/usage-and-pricing (15/07/2026) |
| Cron: frequência mínima | uma vez por dia | por minuto | por minuto | mesma |
| Cron: precisão | dentro da hora (mais ou menos 59 min) | dentro do minuto | dentro do minuto | mesma |
| Retenção de logs de execução | 1 hora | 1 dia (30 com Observability Plus) | 3 dias (30 com Observability Plus) | logs/runtime (28/08/2026) |
| Rollback | só o deploy imediatamente anterior | qualquer deploy que já foi produção | igual | instant-rollback (07/07/2026) |
| WAF | sim | sim | sim | vercel-firewall (10/09/2026) |
| Limite de taxa na borda | 1 regra, dentro de 3 regras custom | 40 regras por projeto | 250 | vercel-waf/rate-limiting (28/08/2026) |

Contadores do limite de taxa são por região: tráfego espalhado pode passar do limite.

## Cron
- `CRON_SECRET` (aleatório, 16 caracteres ou mais, só caracteres válidos em cabeçalho) chega como `Authorization: Bearer <valor>`. A rota compara e devolve 401 também se a variável não existir.
- Só roda em produção. Não testa em preview nem em `next dev`.
- Vercel não refaz execução que falhou; entrega é de melhor esforço: pode perder ou repetir. Trabalho idempotente, por reconciliação, com lock se puder sobrepor.
- Não segue redirect: `trailingSlash` engole o cron. Rota dinâmica com `export const dynamic = 'force-dynamic'`.
- A documentação marca Cron Jobs como legado, a migrar para Schedules: confira antes de construir novo.
- O deploy guarda sua cópia de `CRON_SECRET`: mudar na configuração só vale depois de novo deploy, e rollback restaura o valor antigo daquele deploy.

## Variáveis de ambiente
- Ambientes: Production, Preview, Development e personalizados. Mudança só vale em deploy novo.
- Tipos: **Config** (legível por quem tem acesso) e **Secret** (só escrita, ex-Sensitive). Padrão na CLI: Secret em Production e Preview; Config em Development. `NEXT_PUBLIC_` é sempre Config.
- Build mascara Secret com 32 caracteres ou mais que apareça no log.
- Política de time pode exigir valor diferente de produção para cada Secret.
- Limite: 64 KB por deploy no total.
- `vercel env pull` grava valores reais em `.env.local` (Secret vira espaço reservado ou mantém o valor local). `vercel pull` grava em `.vercel/.env.$target.local`. Os dois têm de estar no `.gitignore`. `vercel env run -- comando` injeta sem gravar arquivo: prefira.
- Preview por branch: valor de branch vence o de todos os previews.

## Proteção de preview
Deployment Protection, em todos os planos: **Standard Protection** (tudo menos domínio de produção) com Vercel Authentication; **All Deployments** também protege produção. Senha: paga no Pro, não existe no Hobby. A página não diz qual o padrão de projeto novo: confira no painel de cada projeto. Bypass para automação é um segredo: trate como tal.

## Preview e banco
A Vercel usa o que estiver no ambiente Preview. Se os valores do Supabase foram aplicados a Preview e Production sem separar, o preview escreve no banco de produção. A integração do Supabase lista as variáveis, sem dizer em quais ambientes: abra o painel e confira.

## Rollback e promoção
- Instant Rollback aponta o domínio para deploy que **já foi produção**: não refaz build; variáveis ficam as daquele deploy.
- Depois do rollback, deploys novos não vão ao ar sozinhos, até desfazer (`vercel promote`).
- Promover preview refaz o build com as variáveis atuais de produção. Promover build em espera (staged) não refaz.
- Lembre: migração de banco não volta com rollback.

## Trabalho depois da resposta
`after()` no Next 15.1+; `waitUntil` de `@vercel/functions` fora dele. Mesmo tempo da função.

## Fontes
https://vercel.com/docs/functions/limitations ; https://vercel.com/docs/cron-jobs/manage-cron-jobs ; https://vercel.com/docs/cron-jobs/usage-and-pricing ; https://vercel.com/docs/environment-variables ; https://vercel.com/docs/environment-variables/sensitive-environment-variables ; https://vercel.com/docs/cli/env ; https://vercel.com/docs/cli/pull ; https://vercel.com/docs/deployment-protection ; https://vercel.com/docs/instant-rollback ; https://vercel.com/docs/deployments/promoting-a-deployment ; https://vercel.com/docs/vercel-firewall ; https://vercel.com/docs/vercel-firewall/vercel-waf/rate-limiting ; https://vercel.com/docs/logs/runtime ; https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package
