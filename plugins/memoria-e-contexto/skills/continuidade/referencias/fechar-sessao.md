# Fechar a sessão

Oferecer só depois de sessão substancial. Sessão curta fecha em uma linha.

## 1. Laços abertos primeiro
Leia a conversa do começo ao fim e liste, uma linha por item:
- todo pedido, inclusive os atendidos em parte;
- toda promessa ("depois eu", "em seguida");
- item de lista de tarefas não concluído;
- pergunta ao usuário sem resposta;
- rascunho ou mudança esperando o sim;
- tarefa de fundo, lembrete ou agendamento sem retorno;
- arquivo criado e não salvo no lugar certo; aba ou servidor aberto.

Fonte que não se aplica é pulada sem comentário. A que pode se aplicar e não dá para checar vira "Não conferido: X", com um passo para o usuário. Compactação da conversa: use o resumo e avise o que pode ter ficado de fora.

## 2. Cada item com exatamente um destino
| Destino | Regra |
|---|---|
| **Feito** | conferido agora, só leitura, com a evidência. Não vale ter dito antes |
| **Terminar agora** | pequeno e aberto por esta sessão. Mostre a mudança e espere o sim. Nunca apagar, mover, redigir trabalho novo, mexer no CLAUDE.md, agendar ou enviar |
| **Passo seu** | só o usuário pode, em um ou dois passos concretos |
| **Próxima sessão** | entra no prompt pronto, com o que falta |
| **Descartado** | com o motivo em uma linha |

Não feche com item sem destino.

## 3. Reconferir o afirmado
Para cada "feito" e cada "pendente, bloqueado, não existe": confira no objeto real, não relendo a mensagem. Antes de entregar um próximo passo, veja se algo mais tarde o superou. Afirmação falsa vira item, sem drama.

## 4. Sinais para a memória
- Correção: a regra por trás dela.
- Preferência declarada ("sempre", "nunca", "prefiro", "de agora em diante"): literal.
- Decisão fixada ("vamos com X daqui para frente"), com a alternativa rejeitada.
- Pedido pontual: ignorar. Em dúvida: marcar como incerto, o usuário decide.
- Nada a guardar: diga em uma linha, sem inventar sinal.

Vale o roteamento e o formato da skill memoria, se estiver disponível: camada mais funda, sem duplicar, conferindo o que já existe na memória. Sem ela: um fato por entrada, tipo, Por quê e Como aplicar, data absoluta.

Antes de propor mexer num arquivo de memória, confira se ele tem linha no índice: sem linha, ele não existe para a próxima sessão, e a proposta traz a linha por extenso.

Entrada que pertence ao CLAUDE.md da raiz vira "Passo seu" com a linha exata. Arquivo cheio: "Próxima sessão", com a entrada escrita por extenso no prompt. Achado que contradiz decisão fixada: mostre os dois lados.

Uma coisa feita duas vezes ou pedida três: sugira que vire skill ou regra (Próxima sessão).

## 5. Uma lição
Uma frase acionável, só o que aconteceria de novo numa sessão nova. Digitação, falha de rede e decisão única não são lição. Se a lição aponta para mudança, proponha (alvo e mudança) e aplique só quando o sinal se repetir ou o usuário pedir. Não invente: "sem lição desta vez" é resposta válida, mas rara.

## 6. Saída, nesta ordem
1. Contagem: "9 laços: 4 feitos, 1 terminar agora, 2 seus, 2 próxima sessão."
2. Tabela `item | destino | evidência ou próximo passo`.
3. Proposta numerada para a memória: sinal, arquivo de destino e **entrada exata**. "Salvar tudo" só vale para o que foi mostrado por inteiro; o incerto é escolhido item a item.
4. A lição.
5. O prompt da próxima sessão, num bloco copiável (`passagem.md`).

E pare. Depois do sim: só acrescente o aprovado (nunca reescreva nem reordene o arquivo); depois os "Terminar agora", com cópia datada antes de substituir; feche dizendo o que foi salvo e onde.
