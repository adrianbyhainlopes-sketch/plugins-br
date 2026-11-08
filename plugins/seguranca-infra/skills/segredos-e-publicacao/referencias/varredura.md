# Varredura

Só extensões de texto, fora de `node_modules`, `.git`, `dist`, `build`, `vendor` e de pasta de terceiros já ignorada. Prefixos do Supabase e da Vercel conferidos em 08/11/2026.

## Por nome de arquivo
`.env` e variantes, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `id_rsa`, `id_ed25519`, `credentials.json`, `service-account*.json`, `.npmrc`, `.pypirc`, `.netrc`, `*.tfvars`, `*.tfstate`, `.sqlite`, `.db`, `*.sql` de dump.

## Por conteúdo
| Família | Padrões |
|---|---|
| Supabase | `sb_secret_` (crítico); `sbp_` (token pessoal, inclusive `sbp_fc` com escopo); JWT longo com `role` `service_role` (legada). `sb_publishable_` e `anon` são feitas para o navegador: não são achado, mas confira a RLS |
| Vercel | `vcp_` (pessoal), `vci_` (integração), `vca_` e `vcr_` (app), `vck_` (chave de API); `CRON_SECRET` literal |
| Provedores | `sk-`, `sk-ant-`, `sk-proj-`, `ghp_`, `gho_`, `github_pat_`, `glpat-`, `xoxb-`, `SG.`, `sk_live_`, `rk_live_`, `npm_`, `dckr_pat_`, `AKIA`, `ASIA`, `AIza`, `ya29.` |
| Chave privada | `-----BEGIN ... PRIVATE KEY-----` |
| Connection string | `://usuario:senha@` (a senha no meio passa despercebida) |
| Atribuição genérica | `password=`, `secret=`, `token=`, `api_key=` com literal |
| JWT literal | três blocos base64url; decodifique cabeçalho e carga, sem imprimir a assinatura, para ver se é real e se expirou |
| Prefixo público | `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `EXPO_PUBLIC_` com nome de segredo: crítico se o valor for secreto |
| Dado brasileiro | `referencias/dados-pessoais-br.md`; certificado A1 entra como segredo de alto risco |

## Arquivos esquecidos
Dockerfile e compose, workflows do CI, saídas de notebooks, README e docs, relatórios antigos, exportações, `.vercel/` (`vercel pull` grava lá valores reais, em `.vercel/.env.$target.local`), `.env.local` (`vercel env pull` grava valores reais; Secret vem como espaço reservado).

Pasta de ferramenta de IA com segredo (`.cursor/`, `.aider*`, `.claude/settings.local.json`).

## Histórico (se houver commits)
`git ls-files` por nomes sensíveis; arquivos adicionados ao longo de todo o histórico; `git log -S` por cabeçalho de chave, `AKIA`, `password`; stashes, reflog, outros ramos e tags. Para cada achado: o commit que trouxe, se o repositório já foi público, fork, espelho ou cache de CI (se sim, comprometido). O `.env` estava no `.gitignore` antes do primeiro commit?

## Vazamento na execução e na distribuição
Segredo em ARG ou ENV de Dockerfile (fica nas camadas); ecoado em log de CI; exposto por `pull_request_target`; source maps; relatórios de erro e analytics; log com token, cabeçalho ou corpo.

CI: chave estática de nuvem vira OIDC; varredura de segredos como checagem obrigatória, porque o hook local cobre uma máquina e é pulado com `--no-verify`.

## Ler o resultado
Severidade por tipo: chave privada e credencial de nuvem, críticas; chave de API, alta; senha genérica, média; placeholder, baixa. Urgência: formato de provedor e enviado primeiro. Scan que parou cedo ou pulou arquivo grande: "nada encontrado" não está provado.

Gestão: de onde vêm os segredos em produção? Há rotação? Escopo mínimo? As mesmas credenciais em desenvolvimento e produção já são achado.

## No repositório
- Bloco do `.gitignore`, sem conflitar com o existente: `.env`, `.env.*`, `!.env.example`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `.npmrc`, `.pypirc`, `*.tfvars`, `.vercel/`.
- `.env.example` com as mesmas chaves e valores claramente falsos.
- Ao achar segredo: arquivo, linha e tipo; o valor vai para variável e o nome para o `.env.example`; garanta o `.gitignore`. Já commitado ou enviado: revogar e rotacionar.
- Automações locais (senha de portal, certificado): Gerenciador de Credenciais do Windows ou `keyring`; CPF e CNPJ fora de log.

## Comandos no Windows
Veja `referencias/windows.md`. No Git Bash ou no PowerShell, `git` é o mesmo. Busca: a ferramenta Grep do Claude Code. Scanner por `winget` ou `scoop`, com versão fixa e o sim. Filtro de máscara testado numa amostra antes de olhar arquivo sensível.
