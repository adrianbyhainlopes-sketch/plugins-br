# Webhooks que não repetem efeito

Vale para rota de código (Next, Python) e para o nó Webhook do n8n.

## Premissa
O provedor entrega pelo menos uma vez. Duplicata, reenvio depois de resposta perdida e ordem trocada são operação normal. O caminho feliz da documentação sempre passa; produção quebra no resto.

## 1. Entender o receptor
Ache no código: o ponto de entrada e como o corpo cru e os cabeçalhos chegam; os tipos de evento tratados e os recusados; todo efeito (banco, e-mail, cobrança, fila, cache); a chave de ordem (a qual entidade o evento pertence); o que já existe para idempotência. Pergunte só o que o código não responde.

## 2. Contrato por evento
Para cada tipo de evento e cada efeito:
| efeito | idempotente? | guarda (o mecanismo concreto) | condicional? |
|---|---|---|---|
| marcar pedido como pago | sim | `UPDATE ... SET status='pago' WHERE id=$1 AND status <> 'pago'` | não |
| enviar recibo | não | chave única do evento gravada na mesma transação, e envio só se a gravação foi nova | não |

"É idempotente" não é guarda. Se não dá para nomear o mecanismo, o receptor não está pronto.

## 3. Seis cenários por evento
| cenário | o que é | o que pega | teto de efeitos |
|---|---|---|---|
| duplicado | o mesmo evento duas vezes | falta de dedupe pelo ID do evento | 1 |
| reenvio após falha | a primeira resposta se perde | marcador gravado tarde ou fora da transação | 1 |
| fora de ordem | o mais novo chega antes | estado novo sobrescrito por evento velho | o da ordem certa |
| intercalado entre entidades | 4 eventos de 2 entidades, uma invertida | estado global ("último evento") | o da ordem certa |
| tipo desconhecido | tipo não tratado | erro 4xx ou 5xx (o provedor pode desligar o endpoint) | 0, resposta de sucesso |
| malformado | corpo que não é JSON | 500 e efeito parcial antes do parse | 0, resposta de malformado |

Também um piso de efeitos (o receptor que não faz nada não pode passar). Nos de ordem, reprocessar na ordem natural a partir do estado zerado e exigir o mesmo estado final. Sem versão ou sequência por entidade, pule os testes de ordem e diga por quê.

## 4. Diagnóstico
| falha | causa | conserto |
|---|---|---|
| duplicado passou do teto | sem dedupe pelo ID do evento | guardar IDs vistos e conferir antes dos efeitos |
| reenvio passou do teto | marcador não gravado ou conferido depois dos efeitos | marcador e mudança de estado na mesma transação; efeito fora do banco com idempotência no destino ou fila de saída (outbox) |
| fora de ordem mudou o estado | evento velho sobrescreveu o novo | aplicar só se a versão for mais nova |
| intercalado mudou o estado | estado global | separar todo estado pela entidade |
| tipo desconhecido com status errado | sem caso padrão | responder sucesso e ignorar |
| malformado com status errado | erro de parse vira 500 | capturar e responder o status de malformado |

## Regras
- Responder rápido com sucesso e processar depois, se o processamento é lento (o provedor reenvia se a resposta demora).
- Assinatura conferida com o SDK ou o método documentado do provedor, antes de qualquer lógica. Nunca invente verificação de assinatura.
- Marcador gravado antes dos efeitos precisa de estado `processando`/`feito` (ou prazo); senão, uma tentativa que caiu fica "vista" para sempre e o reenvio parece duplicata.
- Timeout depois de uma gravação tem resultado incerto: consulte o destino antes de repetir.
- O teste por reenvio não vê o processo morrer entre o marcador e o efeito: isso só se fecha no código (transação ou estado intermediário).

## Provedores
Cada provedor tem regras próprias de reenvio, cabeçalhos de ID, assinatura e ordem. Antes de escrever, confira na documentação oficial atual do provedor que o usuário usa: quanto tempo reenvia, qual campo identifica o evento, se manda o mesmo fato em dois eventos diferentes, como assina. Não use a regra de um provedor para outro, e não use a memória.

## Revisar um receptor (só leitura)
Evento por evento:
1. Todo efeito tem no código o mecanismo que o contrato promete, condicional no código, não no comentário.
2. A chave de dedupe é o ID do evento do provedor, gravada na mesma transação da mudança de estado.
3. Suposição de ordem (UPDATE cego, "o último vence", comparação de horário sem versão) é achado.
4. Nada de estado compartilhado entre entidades do mesmo tipo.
5. Tipo desconhecido recebe "ignorado", não erro, e não dispara efeito.
6. Corpo malformado recebe a resposta de malformado, gera log e zero efeito.
7. Nenhum caminho de exceção roda efeito antes de falhar.

Achado: gravidade, tipo de evento, arquivo:linha, o que o contrato promete, o que o código faz e a entrega concreta que quebra ("um evento de pagamento reenviado manda um segundo recibo"), mais o conserto em uma linha. No fim, o que foi conferido e está sólido.

## Dado de teste
Só sintético e com cara de sintético: `exemplo.com`, IDs `evt_teste_001`, valores como 4200. Nunca payload real, log de produção ou valor copiado do painel do provedor.
