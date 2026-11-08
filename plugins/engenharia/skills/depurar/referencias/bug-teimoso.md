# Bug teimoso, depurador e bisect

Ordem: primeiro a checagem barata (estou editando o arquivo que roda?), depois o depurador, só então a escalada.

## Estou editando o arquivo que roda?
A mudança "não faz efeito" quase sempre é isto.
- Cópia morta: arquivo que ninguém importa, ou importado só por outros órfãos. Ache em rodadas.
- Gêmeos: o mesmo nome exportado em vários arquivos; qual deles é alcançável a partir da porta de entrada (rota, página, job)?
- Prove em execução qual cópia roda: log temporário com prefixo único em cada uma, ou quebre a suspeita numa cópia e veja que nada muda.
- Outras causas do mesmo sintoma: cache de build (`.next`, `__pycache__`), servidor antigo ainda rodando na mesma porta, variável de ambiente diferente, pacote instalado em vez do código local, navegador com cache.
- Apagar cópia morta: por referência, nunca por nome, uma rodada por commit, com o sim do usuário.

## Depurador (quando ler não basta)
- Duas falhas seguidas: o modelo mental está errado; procure uma teoria totalmente diferente.
- Hipótese falseável antes de cada ponto de parada; pare onde o problema começa, não onde aparece; suba a pilha até o quadro em que o valor ficou errado.
- Ponto de parada condicional como invariante (`saldo < 0`); bissecção dentro de laço.
- Mais de três passos seguidos sem descobrir nada: falta um ponto de parada.
- Programa travado: pause, liste as threads, olhe a pilha de cada uma.
- Avalie só expressões sem efeito colateral.

## Escalada (depois de três correções que falharam)
- Recuse "acho que já sei" e "só mais uma coisinha".
- Procure no registro de bugs anteriores do projeto, se houver.
- Em paralelo (no Claude Code, subagentes só de leitura): documentação e problemas conhecidos da biblioteca; logs que traçam o caminho real; histórico (blame, mudanças recentes, quando funcionou); o fonte da biblioteca na versão instalada (`node_modules`, `site-packages`); uma segunda opinião.
- Síntese num olhar novo (subagente só de leitura, modelo forte), recebendo os achados colados: mecanismo, não sintoma; cada afirmação com evidência; causa mais provável e alternativas; o que confirmaria ou derrubaria cada uma.
- Apresente causa com a confiança, uma evidência por fonte, correção, alternativas e como validar; peça aprovação. Se as fontes não convergem, vale a evidência de execução.
- Causa numa dependência: fixar a última versão boa e propor abrir um relato ao projeto dela (com o sim do usuário).

## Regressão com git bisect
Precisa de: um commit ruim, um commit bom e um comando que sai 0 quando bom e diferente de 0 quando ruim (teste focado, build, script curto).
- Rode num `git worktree` separado, nunca na cópia do usuário e nunca com `git stash`.
- O script de reprodução fica FORA da árvore (dentro dela, ele some nos commits antigos).
- `git bisect start <ruim> <bom>`, depois `git bisect run <comando>`.
- Commit que não compila ou não dá para testar: o script sai com o código 125 (pular).
- Dependências que mudam entre commits: reinstale no passo do script.
- No fim, sempre `git bisect reset`, e remova o worktree que você criou.
- Analise o culpado (o diff, a mensagem, o PR) e sugira pelo tipo: erro claro, reverter; correto mas incompleto, o que falta; expôs um problema antigo, explicar o problema de fundo. Push, PR ou merge só com o sim.
