# Bugs de hospedagem serverless

Modelo mental: cada requisição pode cair numa instância diferente e de vida curta, o processo pode congelar logo depois da resposta e o disco é só leitura. Por isso as falhas parecem aleatórias. Leia cada achado no arquivo antes de julgar. Números: `referencias/vercel-conferido.md`.

Ordem por consequência, começando pelo que perde dados.

1. **Trabalho cortado depois da resposta.** Promise sem `await` (e-mail, recibo, fetch solto, `.then/.catch` como instrução própria) pode nunca terminar. Corrija com `await`, `after()` do Next (15.1 ou mais nova) ou `waitUntil` fora dele. O que já está dentro de `await`, `return`, `after` ou `waitUntil` está certo.
2. **Estado em memória é por instância.** Limite de taxa em memória deixa passar muito mais; mapa de deduplicação de webhook deixa repetir. Cache só se a falta dele apenas deixa mais lento. Use armazenamento compartilhado (linha com constraint única; KV ou Redis para limite). Mapa em memória na frente de uma reserva no banco é otimização; como única guarda, é bug. Nunca dado de usuário em escopo de módulo: vaza entre requisições simultâneas.
3. **Variáveis de ambiente.** `NEXT_PUBLIC_` é embutida no build e referência dinâmica (`process.env[nome]`) não é. Variável de servidor lida em `'use client'` vira `undefined` e o recurso falha calado. Mudar no painel não muda o deploy que está no ar.
4. **Timers.** `setTimeout` e `setInterval` em código de requisição não sobrevivem: `after()`, cron ou fila.
5. **Disco.** Só `/tmp` é gravável e é efêmero. O que dura vai para storage. Upload grande vai do navegador direto para o storage com URL assinada, por causa do limite de corpo.
6. **Cron.** Toda rota de cron confere o segredo, senão qualquer um dispara. Horário em UTC. Pode falhar ou repetir: idempotente e por reconciliação (lock contra execução simultânea). Não segue redirect. Só em produção. Sem retentativa.
7. **Builda no PC e falha no host.** Import com caixa diferente (Windows e macOS ignoram, Linux não); variável lida no carregamento do módulo derruba o build (leia dentro do handler); dependência só global ou em `devDependencies` usada em tempo de execução; leia o log de build do deploy.
8. **Limites.** Corpo, duração, webhook (verifique a assinatura, registre, responda rápido, trabalho lento em `after()`). Conexões ao banco: use o pooler.

Fuga comum: lista de grep é sinal, não relatório. O que já está protegido por `await` ou por constraint no banco não é achado.
