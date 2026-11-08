# Laço de evidência

## Registro de investigação
Só acréscimo: sintoma, comandos, códigos de saída, saída decisiva, hipóteses, experimentos, veredito. Numa pasta de rascunho da sessão; se o pedido é só leitura, na própria resposta.

## 1. Contrato
Componentes envolvidos, comportamento esperado, sintoma exato. Confira build, branch, configuração e versões (lockfile) antes de qualquer hipótese.

## 2. Fazer falhar: o sinal
Um sinal útil é específico do sintoma, capaz de ficar vermelho, determinístico (ou com taxa medida), rápido de repetir e executável por você. Em ordem de preferência:
1. teste que falha no ponto que alcança o bug;
2. script HTTP contra o servidor local;
3. linha de comando com entrada fixa, comparada com uma saída boa;
4. navegador automatizado conferindo DOM, console e rede;
5. reprodução de um registro capturado (requisição, payload, log salvo);
6. um pedaço mínimo do sistema montado só para isso;
7. laço de propriedade ou entradas aleatórias com semente;
8. `git bisect run` (ver `bug-teimoso.md`);
9. diferencial: versão velha contra nova, duas configurações;
10. último recurso: roteiro que guia o usuário passo a passo e captura a saída.
Melhore o sinal: mais rápido, mais nítido (afirmar o sintoma, não "não quebrou"), mais determinístico (fixar relógio, semente, arquivos, rede). Um sinal de 2 segundos determinístico vale mais que um de 30 instável. Intermitente: suba a taxa de reprodução antes (com 50% dá para depurar; com 1%, não).
Sem sinal possível: pare, liste o que tentou e peça acesso, um artefato (log, HAR, gravação com horários) ou permissão para instrumentar. Não hipotetize sem sinal.

## 3. Minimizar
Tire uma entrada, dependência, configuração ou passo por vez; mantenha a remoção só se o mesmo sintoma continua.

## 4. Hipóteses
Comece comparando um exemplo do mesmo padrão que funciona com o caminho que falha. De 3 a 5 hipóteses ranqueadas, cada uma com previsão e com o que a derrubaria. Mostre a lista ao usuário, sem travar se ele não responder.

## 5. Sondar
Uma variável no primeiro ponto em que as previsões divergem. Depurador antes de log; log só nas fronteiras que separam hipóteses. Sistema em várias etapas (CI, build, deploy; API, serviço, banco): instrumente cada fronteira numa rodada só (segredo: registre só presença ou ausência). Rastreie para trás na pilha até o gatilho original, não até onde o erro aparece.

## 6. Afirmar só o que discrimina
Causa verificada (com a evidência que a separa das outras) ≠ inferência ≠ mudança proposta.

## Corrigir (só se pedido)
- A reprodução minimizada vira teste de regressão no ponto público mais alto que exercita o defeito; veja-o falhar antes de mexer.
- Menor correção; rode o mesmo teste e o sinal original.
- Quando barato, desfaça a correção uma vez para ver a falha voltar.
- Sem ponto bom para o teste, não invente um raso: diga a limitação.
- Depois de achar a causa, defesa em camadas quando o custo do bug é alto: validar na entrada, na regra de negócio, guarda de ambiente, registro antes da operação perigosa.
- Tire a instrumentação.
- Pergunte "o que teria evitado este bug?"; se a resposta é de arquitetura, recomende depois da correção, não junto.

## Fechamento
Causa sustentada; evidência que discriminou; checagens com resultado; correção autorizada; instrumentação removida; o que não foi verificado. Recuperação sem explicação não é correção.

## Onde olhar primeiro, por sintoma
Lentidão: medição e consultas lentas, não logs. Erro: taxa por rota e o que mudou no último deploy. Dado errado: qual linha, qual gravação, qual job. Intermitente: por instância, por usuário, por horário.

## Vieses
"Vimos isso semana passada"; "não pode ser X"; "óbvio que é o cache"; ver só o que confirma; esquecer que as requisições que falham podem nem chegar ao log; culpar a primeira coisa que mudou. Antipadrões: mudar ao acaso; reiniciar primeiro; culpar a rede; parar na primeira explicação plausível.
