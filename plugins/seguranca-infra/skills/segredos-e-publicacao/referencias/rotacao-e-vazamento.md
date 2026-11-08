# Rotação e vazamento

## Tabela de rotação
Ordene pelo raio de dano: segredo (mascarado), local, no histórico?, repositório já foi público?, ainda válido?, raio de dano, ação.

## Ordem, sempre
1. **Rotacionar:** credencial nova, implantar, revogar a velha.
2. **Procurar abuso:** logs de auditoria e cobrança desde o vazamento. Chave pública há meses é chave usada.
3. **Limpar o histórico:** reescreve, exige force push, quebra clones e não adianta se alguém já baixou. É cosmético e destrutivo: só com sim.
4. **Prevenir:** cofre, varredura no CI, proteção de push.

## Conter um vazamento (funciona sem terminal)
1. Pergunte qual serviço e para onde foi, **sem pedir o valor**.
2. Rotacione primeiro, limpe depois. Siga os passos do serviço.
3. Avise quem cuida: o quê, onde, quando.
4. Dado pessoal de terceiros não se rotaciona: vai para o fluxo de incidente no mesmo dia.
5. Depois da rotação, leia o log de auditoria desde o vazamento.
6. Limpar: cada passo com sim.

**Segredo no chat ou na sessão do agente:** já foi ao provedor do modelo e está no transcript local. Rotacione. Limpar as cópias locais só com sim explícito; isso não apaga o que o provedor recebeu.

## Por serviço (conferido em 08/11/2026)
| Serviço | Rotacionar |
|---|---|
| Supabase, chave secreta | crie outra em Settings, API Keys; troque onde usa; apague a antiga. Use uma chave por componente: se um vazar, só ele troca. A doc tem um guia próprio para chave vazada: siga a versão atual |
| Supabase, `anon` e `service_role` legadas | criar chave nova não as revoga: continuam valendo até desligar em Settings, API Keys |
| Supabase, senha do banco | troque, atualize os apps, encerre as sessões |
| Vercel, variável | gere a nova no serviço terceiro **sem invalidar a velha**; edite a variável; marque os ambientes certos; redeploy (produção e previews); confirme; só então invalide a velha. Variável de time: redeploy em cada projeto que usa. Deploy antigo continua com o valor antigo e quebra ao invalidar |
| Vercel, `CRON_SECRET` | edite, redeploy, espere ficar Current, veja a primeira execução voltar 2xx. Rollback restaura o segredo antigo daquele deploy |
| Vercel, token | a Vercel revoga automaticamente credencial achada pelo secret scanning do GitHub; confira no painel |
| Certificado A1 | revogue na autoridade certificadora e emita outro; troque nos sistemas; a senha do arquivo sozinha não resolve |
| GitHub, AWS, Google Cloud, Stripe, OpenAI, Anthropic, Slack | princípio geral: credencial nova, trocar onde se usa, revogar a antiga, ler o log do período; caminho exato no console do provedor |
| Chave SSH | gere par novo, troque em `authorized_keys`, retire a antiga |

Comandos que apagam ou publicam: `referencias/comandos-destrutivos.md`.

## Cópia segura para compartilhar
`arquivo.redacted.ext` ao lado do original, sem abrir o original pela conversa. Avise o que o redator não troca: nomes, endereços, datas de nascimento, telefones, senha no meio de uma frase. Não versione a cópia.
