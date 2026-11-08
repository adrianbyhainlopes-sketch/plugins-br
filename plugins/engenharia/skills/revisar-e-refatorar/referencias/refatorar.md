# Refatorar com segurança

Refatorar não muda comportamento observável. Sem teste cobrindo, fixe o comportamento atual antes, ou declare que a mudança não foi verificada e por quê. Nunca refatoração e mudança de comportamento no mesmo commit. A limpeza do que acabou de mudar é do /simplify; aqui ficam o legado e as decisões maiores.

## Antes de tocar (cerca de Chesterton)
Qual a responsabilidade, quem chama, o que chama, quais bordas e erros, que testes definem o comportamento, por que foi escrito assim (o histórico do git ajuda)? Sem essas respostas, não simplifique.
Armadilhas do excesso: inlinar um ajudante que dava nome a um conceito; fundir duas funções simples numa complexa; tirar uma abstração que existia para teste ou extensão; medir sucesso por linhas a menos. Se a simplificação exige mudar teste, mudou comportamento.

## Modo limpeza (funciona, ler dói, há teste ou é barato fazer)
- Escopo: arquivos tocados na sessão e chamadores diretos.
- Meça antes: tamanho de função, parâmetros, aninhamento, duplicação, nome enganoso, flag booleana, responsabilidade fora do lugar.
- Prioridade: P0 nome enganoso ou duplicação que já divergiu; P1 função que mistura decisão, efeito e formatação; P2 aninhamento acima de 3 ou função longa, só quando destrava P0 ou P1; P3 cosmético (pule). "Não vale a pena" é entrega válida.
- Uma transformação por vez, reversível: renomear para a intenção; extrair o bloco mais profundo; condicional aninhada vira retorno antecipado; juntar duplicação só na terceira ocorrência e se as cópias codificam a mesma decisão; empurrar efeitos (arquivo, rede, log) para as bordas. Testes depois de cada passo; vermelho = desfaça o passo, nunca remende para frente.

| cheiro | movimento |
|---|---|
| função longa | extrair por tarefa |
| função que usa mais os dados de outro módulo | mover para perto dos dados |
| uma mudança exige mexer em muitos lugares | juntar num dono |
| os mesmos parâmetros andando juntos | objeto de parâmetros |
| texto ou número carregando significado | tipo próprio |
| generalidade que ninguém usa | inline ou apagar |

## Modo legado (sem teste)
1. Liste os pontos de mudança.
2. Ache as costuras: o ponto mais próximo onde dá para observar ou trocar comportamento sem editar o código sob mudança (parâmetro, construtor, fronteira de import).
3. Quebre a dependência com o menor movimento nomeado (brotar função nova, embrulhar a existente, parametrizar), sem redesenhar.
4. **Teste de caracterização, falhando primeiro:** afirme um valor inventado, rode, leia o valor real na falha, fixe o real e veja passar. O valor gravado é a especificação mesmo que pareça errado; surpresa vira nota para o usuário, nunca correção silenciosa.
5. Mude dentro da rede. Caracterização vermelha = desfaça, nunca ajuste o teste.

## Duplicata semântica e teste da deleção
- Catálogo das funções exportadas (nome, arquivo:linha, assinatura), agrupadas por domínio (validação, formatação, datas, caminhos, HTTP); leia as implementações para julgar a intenção, nunca pelo nome.
- Consolide só quando o sobrevivente tem teste, todos os chamadores foram atualizados e a suíte e os tipos estão verdes.
- Teste da deleção: "se eu apagar este módulo e colar o código em cada chamador, para onde vai a complexidade?" Some: módulo raso (apague ou aprofunde). Reaparece em N lugares: módulo profundo (mantenha).

## Aprofundar módulos
Módulo profundo é interface pequena escondendo implementação grande. Anote o atrito ao explorar (pular entre muitos arquivos pequenos para entender um conceito; interface quase tão complexa quanto a implementação). Proponha candidatos numerados, sem interface ainda; o usuário escolhe. Para cada um: problema, interface, como tratar as dependências (em processo; trocável localmente, como banco local; remota mas sua; externa de verdade, com mock na porta), estratégia de testes (substituir os testes dos módulos rasos, não empilhar). Nada de criar issue sem o sim.

## Quando não refatorar
Código estável, isolado e que ninguém lê; gerado, de terceiros ou migração já aplicada; sem testes, sem tempo e só cosmético; preferência contra o formatador. Mudança em API pública ou formato gravado: confirme antes. Nunca reescreva um módulo inteiro quando três extrações resolvem.

## Relatório
Arquivos; métricas antes e depois; cada movimento ligado ao cheiro; testes verdes antes e depois (com a saída); o que ficou sem corrigir e por quê; riscos não descartados.
