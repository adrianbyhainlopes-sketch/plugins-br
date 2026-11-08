# Portão de lançamento

Cada bloqueante: passa, falha ou não comprovado, com evidência. Não comprovado bloqueia até ser testado.

## Bloqueantes
1. Segredo vivo no repositório ou no build, inclusive no histórico.
2. Endpoint com dado de usuário sem autenticação, ou com bypass.
3. Trocar o id devolve dado alheio.
4. Injeção alcançável sem login.
5. Senha fora de bcrypt, scrypt ou argon2.
6. Debug, stack trace, console de admin ou source maps do servidor em produção.
7. Banco ou serviço interno exposto com credencial fraca.
8. TLS ausente ou verificação desligada.
9. Vulnerabilidade explorada ativamente numa dependência direta, sem controle compensatório.
10. Upload servido da própria origem sem controle de tipo.
11. **Supabase:** tabela de esquema exposto sem RLS, ou com `USING (true)` em dado de usuário.
12. **Supabase:** chave secreta no cliente ou em `NEXT_PUBLIC_`.
13. **Supabase e Next:** `getSession()` usado para decidir acesso no servidor.
14. **Vercel:** preview acessível sem proteção e apontando para o banco de produção. Confira à mão os dois lados: Deployment Protection e os valores das variáveis no ambiente Preview. A Vercel não escolhe banco: o preview usa o que estiver no ambiente Preview.
15. **Vercel:** rota de cron sem conferir `CRON_SECRET`.
16. **Migração** pendente que quebra a versão no ar: `referencias/vercel-conferido.md` e a skill supabase.

## Corrigir antes, sem bloquear
Limite de taxa em login, redefinição, cadastro, OTP e endpoints caros; enumeração de contas; flags de cookie; CSRF em rotas com cookie; CORS sem `*` com credenciais; cabeçalhos (CSP, nosniff, HSTS, Referrer-Policy, frame-ancestors); limites de tamanho; assinatura de webhook; nada pessoal em log e analytics; erro genérico ao cliente.

## Prontidão operacional
- Falhas de login, negações e ações de admin registradas (quem, o quê, alvo, hora).
- Alguma forma de saber que está sendo atacado; alerta que chega num canal real, com quem recebe e o roteiro.
- Backup com restauração testada (backup que nunca foi restaurado é só esperança).
- Revogar sessão, chave ou usuário na hora.
- Canal para reportar vulnerabilidade (SECURITY.md, security.txt).
- Quais terceiros guardam dados dos usuários.
- Modos de falha com nome: serviço fora, carga inesperada, dependência degradada, perda de dados.
- Rollback que nunca foi exercitado não conta.
- Todo custo sem teto (chamadas de IA, gravações, tráfego, APIs) limitado ou aceito por escrito.
- Produção e desenvolvimento separados: banco, chaves, contas.
- E-mail transacional com SPF, DKIM e DMARC.

Fica com o dono: domínio, DNS, chaves vivas, verificação de pagamento. Feche com as três mudanças que mais reduzem risco por esforço.

## Pós-deploy
Registre o comando de volta **antes** do deploy.
- No primeiro minuto: saúde, banco e serviços críticos.
- Em cinco minutos: cadastrar e logar um usuário de teste, percorrer o fluxo principal, conferir o e-mail de redefinição, apagar as contas de teste.
- Em quinze minutos: monitorar erros e tempo de resposta.

**Regra de rollback** (limiares a ajustar por você): erro acima de 1% por 5 minutos, saúde falhando, erro crítico novo que afeta usuário ou desempenho pior que o dobro da linha de base. Logs do plano gratuito somem rápido: copie o que importa.

A correção vai num ramo, nunca às pressas em produção.

## Checagem passiva do próprio site
Só no domínio do próprio usuário, sem sondagem ativa de terceiros.
Cabeçalhos (CSP, HSTS, frame-ancestors ou X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy); `Server` e `X-Powered-By`; flags de cookie; redirect para https; caminhos sensíveis (`.env*`, `.git/config`, `.git/HEAD`); HTML (script externo sem integridade, comentários com senha, token ou IP); JS (padrões de chave, `postMessage` sem conferir a origem, `sourceMappingURL`, URLs internas).
