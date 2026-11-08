# App inteiro, por stack

## Mapear a superfície antes de caçar bug
Para cada endpoint: exige login? qual papel? custa dinheiro? altera dados? A interseção "sem login e caro" é o alvo principal. Depois: ingestão (upload, importação, webhook), fetch de saída com URL influenciada pelo usuário, fronteiras de confiança (cliente e API, API e banco, API e provedor de IA, API e cobrança; checagem ausente nelas é o achado), fluxos de segredo e de dado pessoal.

## Varredura por prioridade
| Prioridade | O que procurar |
|---|---|
| P0, comprometimento imediato | segredo no código; `.env` exposto ou commitado; segredo com prefixo público (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`); chave de servidor do Supabase no cliente; pastas de ferramentas de IA com segredo; endpoint de debug em produção; `console.log` de token, senha ou objeto de usuário |
| P1, exploração direta | injeção; XSS (`dangerouslySetInnerHTML`, `href` com `javascript:`); rota sem autenticação ou IDOR; RLS desligada ou `USING (true)`; atribuição em massa (`...req.body` gravado direto); SSRF; path traversal; matcher do proxy que exclui `/api` |
| P2, abuso | falta de limite de taxa (autenticação, IA, upload); CSRF; CORS `*` com credenciais; JWT com `alg none`, segredo curto ou sem expiração; falta de validação; corrida; webhook sem assinatura |
| P3, defesa em profundidade | cabeçalhos; erro verboso; objeto inteiro do banco na resposta; source maps; listagem sem paginação; `Math.random` para token; soft-delete vazando; EXIF em upload; autenticação de mentira (TODO, `next()` incondicional, `if (true)`) |

P0 a P3 é ordem de busca; a gravidade do relatório segue a escala da skill.

## Corridas e pagamentos
UPDATE atômico com condição (`... WHERE saldo >= valor`), chave de idempotência, UNIQUE no banco em vez de SELECT antes do INSERT. Webhook com assinatura sobre o corpo cru, recusa de timestamp velho e id do evento guardado contra repetição. Preço sempre calculado no servidor.

## Quando o relatório não cobre tudo
Classes que costumam sobreviver à verificação: corridas em endpoint de uso único, cotas que contam artefatos (apagar o registro libera a cota), leitores antigos de regra nova, canais laterais em rota pública, rótulo maior que o predicado, caminho de recuperação (restore ressuscita token revogado). Raramente sobrevivem: injeção onde há escape central, falta de limite com limitador global, segredo fixo que é placeholder recusado no início, achado tirado só do controller.

## Ferramentas e o que sai da máquina
Diga antes de rodar. Instalar ou usar a rede só com o sim; no Windows, winget ou scoop com versão fixa; nunca `curl | sh`, nunca imagem `latest`.
| Ferramenta | Modo | O que sai |
|---|---|---|
| Gitleaks | local | nada |
| Semgrep CE | `--metrics=off`, nunca `--config auto` | nada com regras locais |
| OSV-Scanner | tem modo offline | nomes e versões, se online |
| Checkov | `--skip-download` | nada |
| zizmor | `--offline` | nada |
| `npm audit`, `pip-audit` | padrão | árvore de dependências ao registro |

Confira as flags na versão instalada. Scan que não rodou é "não medido", nunca "zero". Código de saída diferente de zero quase sempre é "achou algo". Consertar ferramenta quebrada: no máximo duas tentativas.

Sem verificação ativa de segredo na API do provedor: segredo achado é tratado como vivo até ser rotacionado.

## Sempre, mesmo sem scanner
Arquivos sensíveis rastreados; `.env` em pasta publicável (`public`, `dist`, `build`); variável pública com nome de segredo; source maps no build; senha dentro de connection string; manifesto contra lockfile; cobertura do `.gitignore`.

## Saída para o dono do app
Tabela única (número, gravidade, problema, arquivo, linha), uma ou duas frases leigas por achado ("qualquer um vê dados de outro usuário trocando o id na URL") e, para quem quer detalhe, matriz por endpoint: autenticação, papel, checagem de dono, limite de taxa, nota, e coluna "dado pessoal: sim ou não".

Registro para quem trabalha só: um arquivo de achados com IDs estáveis, fora do repositório público; "falso positivo" e "risco aceito" com motivo numa linha e data para rever. Tendência entre auditorias: novo, piorando, estável, melhorando.
