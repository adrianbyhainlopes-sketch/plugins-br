# Plano e premortem

## O plano em oito passos
1. **Alvos verificáveis.** "Adicionar validação" vira "estas entradas são recusadas com estas mensagens, cobertas por estes testes".
2. **Suposições declaradas.** Pedido ambíguo: pergunte. "Não sei" vale mais que chute.
3. **Mudanças:** cada arquivo que muda e por que se liga ao pedido. Mais a lista **fora de escopo**: arquivos e comportamentos parecidos que ficam intocados.
4. **Abordagem mais simples**, sem abstração especulativa.
5. **Rastreabilidade:** para cada função ou componente novo, quantos arquivos o leitor precisa abrir para entender. Mais de dois (fora a infraestrutura comum) pede um desenho mais achatado.
6. **Pronto** definido como comandos do projeto com resultado esperado.
7. **Paradas:** as suposições de que o plano depende; se uma cair, parar e relatar.
8. **Esperar o sim.** Conciso.

## Passo 0 do premortem: o escopo
Escreva "Escopo / Dentro / Finais / Fora (cada um com o porquê de o objetivo valer sem ele)" e a lista de tudo que é tocado: campos, status, opções, filas, agendamentos, eventos, endpoints e serviços externos. Essa lista alimenta as dez perguntas.

## As dez perguntas
Suponha que a mudança foi ao ar e quebrou. Onde?

1. **Duas vezes.** Duplo clique, duas abas, retentativa do cliente ou da fila, duas instâncias, webhook reenviado. Guarda de verdade: índice único, chave de idempotência, UPDATE condicional com a contagem de linhas conferida, trava que cobre conferir e gravar. Ler e depois gravar sem trava não é guarda; marcador em memória não vale com dois processos. Teste: disparar duas vezes ao mesmo tempo e esperar um efeito só.
2. **No meio do caminho.** Se o processo morrer depois de cada gravação, que estado fica e o que a retentativa faz? Marcador de feito antes do trabalho faz a retentativa pular o que não aconteceu; gravações que andam juntas vão numa transação; o tempo limite do job cobre a execução mais longa.
3. **Chamada externa.** Tempo limite explícito (o padrão das bibliotecas costuma ser longo ou nenhum). Depois de tempo esgotado ou erro 5xx, a chamada pode ter acontecido? Então chave de idempotência ou consulta antes de repetir. Quais erros repetem e quais chegam ao usuário.
4. **Falha não é vazio.** Carga que falhou não aparece como "nada aqui"; leitura que falhou tratada como vazia e regravada apaga dados; todo `catch` que engole chega a quem monitora.
5. **Vizinhos.** Busque cada campo, status e fila no repositório inteiro. Ache o mesmo trabalho feito em dois lugares (dois caminhos de exclusão; webhook e job de conciliação; unitário e em lote; tela e script de administração).
6. **Finais.** O que acontece com o que foi criado ao cancelar, apagar (o registro e a conta), desconectar, expirar, rebaixar o plano? Algo fica rodando, cobrado, guardado ou prometido?
7. **Dinheiro.** Quem paga cada chamada paga e qual o teto (no banco, atômico); estorno em falha ou cancelamento, se pode rodar duas vezes e se volta para onde veio.
8. **Usuário hostil.** Autenticação e limite de tamanho antes de ler a entrada; teto burlável por chamadas em paralelo ou por apagar e refazer; links e tokens de uso único e curtos; texto do usuário chegando a consulta, shell, caminho de arquivo, HTML ou prompt sem guarda.
9. **Palavras.** Busque na interface, e-mails, ajuda, documentação e termos as frases sobre o que muda; cada uma continua verdadeira ou muda junto.
10. **Escala e tempo.** Toda consulta com limite e índice; lista que para na primeira página esconde o resto; laço com consulta por linha; fuso do usuário (`America/Sao_Paulo`), fim de mês, ano bissexto, data sem hora.

Invariantes: nomeie as que a mudança toca e como continuam valendo.

## Bloco de saída no plano
```
Premortem
Escopo: ...   Dentro: ...   Finais: ...   Fora: ... (porquê)
Toca: campos ..., status ..., filas ..., endpoints ..., externos ...
1 Duas vezes: ...
...
10 Escala e tempo: ...
Invariantes: ...
Testes a escrever (cada um falha no código atual): ...
```
Todo "não tratado" vai ao usuário antes de construir o que depende dele.
