# Autenticação e autorização

Controle de acesso quebrado é falha de omissão: o endpoint vulnerável é igual ao seguro, menos uma linha. Só funciona listar tudo e checar um por um.

## Quatro fases, sem pular
1. **Inventário** de todas as entradas: método, caminho ou gatilho, handler em `arquivo:linha`, exige login, papéis, notas. Divergência com OpenAPI ou esquema já é achado.
2. **Matriz:** quem deveria acessar, que checagem existe, que checagem vem antes, qual a lacuna.
3. **Catálogo:** varra pelo catálogo abaixo, confirmando cada grep lendo o arquivo.
4. **Relatório.**

## Quem deveria acessar
- Pelo caminho: `/admin`, admin; `/api/me`, o próprio; `/x/:id`, dono ou mesmo cliente; `/webhooks`, assinatura; `/login` e `/reset`, público com limite de taxa.
- Pelo verbo: PATCH, PUT e DELETE, dono ou admin; listagem, só os itens do dono; impersonar, promover, conceder, estornar, admin com reforço.
- Pelo dado: pessoal ou financeiro, no mínimo o dono; agregado de vários, admin.

## Tipos de lacuna
Nenhuma; sem autenticação; sem autorização; autorização fraca (id ou papel vindos da requisição, ou só confere se há token); confia em entrada do cliente; inconsistente; desconhecida (vai para perguntas abertas).

## Conferir uma checagem existente
Roda em todos os caminhos (ordem dos middlewares)? Checa a coisa certa (autenticar não é autorizar)? Está na própria consulta? Nenhuma rota irmã escapa (`/users/:id` protegida, `/users/:id/profile` aberta)? Alguma peculiaridade do framework a desliga?

## O que escapa do mecanismo
Rota registrada noutro router ou antes do middleware; guard comentado ou marcado público; lista de caminhos públicos larga demais (`/api/public` casa com `/api/publicadmin`); rotas novas fora do padrão das vizinhas; estáticos ou proxy servindo conteúdo protegido por fora do app.

## IDOR, endpoint por endpoint
A posse está na mesma consulta? Escrita separada da leitura (GET certo, PATCH e DELETE esquecidos); rotas aninhadas (o filho pertence ao pai?) e em lote (só o primeiro id checado); referências indiretas (chaves de storage, convites, exportações, notas); ações entre usuários (compartilhar, transferir, adicionar membro). Por campo: lista de permitidos, nunca de proibidos (`role`, `is_admin`, `tenant_id`, `owner_id`, `balance`, `price`, `status`, `email_verified`, plano).

## Isolamento entre clientes
Identificador do cliente sempre de claim verificado, nunca de cabeçalho, rota ou corpo. Filtro central (RLS ou consulta base), para que esquecer falhe fechado. Jobs, exportações, índices de busca e caches: chave de cache compartilhada vaza dado. Com RLS, confirme que o app conecta com um papel ao qual ela se aplica: superusuário, papel com `bypassrls` e a chave secreta do Supabase passam por cima em silêncio.

**Teste negativo:** não basta A ver os próprios dados; as credenciais de A contra o id de B precisam ser negadas. Sem esse teste há só uma intenção de isolamento.

## Next.js com Supabase
Matriz: rota ou ação, acesso pretendido, porteiro, verificado no servidor?, barreira na camada de dados? Regras e chamadas em `referencias/supabase-auth.md` e `referencias/next16-seguranca.md`. Todo `getSession(` em código de servidor é achado até provar que roda só no navegador.

## Recuperação de conta, o fluxo mais atacado
Token de gerador criptográfico, vida curta, uso único; link montado com o host da configuração, nunca do cabeçalho Host; a redefinição derruba as sessões abertas; troca de e-mail avisa o antigo e verifica o novo; não pula o segundo fator. Enumeração por mensagem, status, tempo ou redirect. OAuth: state, PKCE, `redirect_uri` exata, vincular contas pelo e-mail só se o provedor verificou o e-mail. Com provedor gerenciado, revise a integração, não reimplemente o provedor.

## Catálogo
Autenticação ausente ou quebrada; JWT (`alg none`, decodificar sem verificar, iss, aud, exp); sessão (flags, logout que não invalida, fixação); IDOR; escalada e atribuição em massa; OAuth e OIDC; recuperação de senha; segundo fator que dá para pular; limite de taxa ausente ou só por IP; CSRF e CORS; SSRF e token em log.

## Proibições
Não mude código; não rode o app nem faça requisições (sonda é modo separado, autorizado e fora de produção); não reporte sem `arquivo:linha`; não diga que falta checagem sem confirmar que nenhum middleware, guard ou proxy a aplica; não pare no primeiro bug; não confie em comentário.
