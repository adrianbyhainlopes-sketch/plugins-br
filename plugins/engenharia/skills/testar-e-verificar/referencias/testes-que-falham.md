# Testes que conseguem falhar

## Laço
- Um comportamento por vez, em fatia vertical: o primeiro teste atravessa o caminho de ponta a ponta; cada teste seguinte reage ao que o anterior ensinou. Escrever todos os testes antes testa um comportamento imaginado.
- Vermelho pelo motivo certo → verde com o código mínimo → refatorar com o teste como rede. Nunca refatorar no vermelho.
- Pular o ciclo só com o sim do usuário: protótipo descartável, código gerado, configuração, componente só visual.

## Antes de cada teste novo (anti-alfaiataria)
- Estou fixando o que o contrato diz ou a implementação que já imaginei?
- Eu escreveria este teste só com o contrato, sem ter lido o código que acabei de escrever?
- Outra implementação que cumprisse o mesmo contrato passaria? Se não, é teste de detalhe interno: reescreva contra o contrato ou descarte.

## A asserção (o ponto mais frágil quando a IA escreve teste)
- Corresponde ao que o usuário quer?
- É a forma mais precisa ("igual a 42", não "verdadeiro"; o corpo do erro, não só o status)?
- Um bug de um caractere passaria?
- O esperado foi calculado por outro caminho, não copiado da função?
- Afirme sobre o que o chamador observa (retorno, linhas gravadas, e-mail na fila), não sobre chamadas internas.

## O que testar
- Denso: regra de negócio com ramos (preço, agenda, elegibilidade, estados, retentativa, deduplicação), parser de dado externo, fronteiras (validação, autorização), tudo que já quebrou uma vez.
- Fino ou nada: encanamento do framework, getters, boilerplate.
- Para cada comportamento: caminho feliz com valores do requisito; autorização (sem login; registro de outro usuário: 404 ou 403); validação (faltante, malformado, fora da faixa, campo extra); falha de dependência (erro visível, não lista vazia); duas vezes ao mesmo tempo (um sucesso só); limites (vazio, nulo, zero, máximo, fuso, data sem hora).

## Borda N-1, N, N+1
Toda palavra de limite ("até", "no máximo", "excede", "pelo menos", "dentro de") ganha três casos, com o esperado calculado à mão a partir da frase. Ligue a palavra ao substantivo que ela modifica (posição, tamanho ou contagem): o teste vai exatamente ali.
| frase | casos |
|---|---|
| "excede N", "até N" | N-1, N, N+1 |
| "no dia X ou antes" | em X, antes, depois |
| "se A, faça B" | A verdadeiro e falso |
| vazio citado | entrada vazia e entrada sem conteúdo válido |

## Bug: provar que o teste segura carga
Depois do verde: restaure a versão com bug (de uma cópia, num worktree), rode só o teste novo, veja falhar com o sintoma exato, volte à correção. Se a correção depende de uma sutileza, teste também a alternativa ingênua errada.

## Mock só na fronteira
| o que | como testar |
|---|---|
| banco, fila, armazenamento que você roda | serviço real local (contêiner ou Supabase local), migrações reais aplicadas, isolado por teste |
| serviço de terceiro (pagamento, e-mail, mapa) | mock gravado ou à mão (MSW, `responses`, `httpx_mock`), mais um teste ocasional no ambiente de teste deles |
| relógio, aleatório, sistema de arquivos | relógio congelado, semente fixa, pasta temporária |
Pergunta-teste: "se eu tirar este mock, um sistema externo de verdade é chamado?" Se não, tire. Mock com a forma completa do dado real. Nada de método "só para teste" no código de produção. Diga no relatório o que é mock e, portanto, não provado.

## Determinismo
Sem `sleep` (espere pela condição, com tempo limite e mensagem); sem rede; relógio congelado (meio-dia UTC evita virar o dia); aleatório com semente; independente da ordem. Teste instável se corrige ou se apaga no mesmo dia.

## Os bugs moram nas costuras
- Fixture fiel ao formato real (o que o serializer e a migração produzem). Verde com o usuário reclamando: suspeite primeiro da fixture.
- Fiação: rota montada uma vez só; guarda e middleware com teste que prende o contrato.
- Ler o que escreveu: "não salvou" pode ser leitura de cache ou de view velha.
- Um teste de ponta a ponta do caminho feliz por fluxo de dinheiro.

## Sinais de teste que mente
Mocka a própria função testada; snapshot de tudo; passa com a funcionalidade removida; `toBeTruthy`, `toBeDefined`, `is not None` como única asserção; cobertura sem asserção; `try/except` em volta da chamada (passa se a exceção não vier: use `pytest.raises`). Pergunta de inversão: "se a funcionalidade quebrar, este teste falha?"

## Sem teste unitário possível
Suba a menor parte viva do sistema. Mudança que toca banco roda contra banco real (mock de query builder não executa SQL). Cuidado com efeito real (e-mail, webhook) e derrube tudo no fim.
