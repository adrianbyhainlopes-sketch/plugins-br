<!-- cópia gerada de compartilhado/anti-generico.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Anti-genérico: a lista única

Uma lista só para tela, slide, documento e peça gráfica. Critério: **o que o brief ou a marca fixa se segue à risca; onde o brief deixa livre, estes padrões só entram com justificativa escrita no plano.** A lista envelhece com os modelos: revise quando ela parar de pegar o que salta aos olhos.

## Os cinco agrupamentos que denunciam um padrão pronto
1. Fundo creme (perto de `#F4F1EA`), serifada display contrastada e acento terracota (perto de `#D97757`).
2. Fundo quase preto com um único acento verde-ácido ou vermelhão.
3. Layout de jornal: fios finos, raio zero, colunas densas, sem motivo no conteúdo.
4. Kit de cards: tudo em cards iguais, um raio, a mesma sombra cinza suave, gradiente decorativo.
5. Cromo de modelo: sobretítulo em caixa-alta espaçada acima de cada título, metadados "A · B · C", rótulos "PALAVRA: fragmento", `#0B0B0B` no lugar de preto, fonte mono em rótulo de dado, seta "→" no fim de link e botão.

Teste: imagine um pedido parecido de outra pessoa. Se a sua peça sairia igual, revise e diga o que mudou e por quê.

## Matriz S1 a S15 (interface de produto)
| # | Sinal | Como achar | Exceção | Correção |
|---|---|---|---|---|
| S1 | gradiente arco-íris em botão principal | gradiente com 3 cores ou mais | nenhuma na interface | botão sólido |
| S2 | gradiente roxo para laranja | `linear-gradient` com violeta e laranja | marca que já usa | uma matiz só |
| S3 | painel de vidro | `backdrop-filter` | sobre foto, com borda de 1 px a 3:1 e fundo opaco de reserva | superfície opaca |
| S4 | barra lateral fosca | `backdrop-filter` na navegação | nenhuma | fundo sólido com degrau de luminosidade |
| S5 | bolhas desfocadas no fundo | `filter: blur` em formas soltas | arte e capa decididas no plano | tirar |
| S6 | borda neon | `box-shadow` colorido com espalhamento | nenhuma | borda de 1 px neutra |
| S7 | sombra dura | alfa 0,2 ou mais, deslocamento 8 px ou mais | nenhuma | sombra suave em camadas ou borda |
| S8 | pílulas pastel em texto parado | `border-radius: 999` em metadado | status que muda | texto simples |
| S9 | ícone em todo campo | ícone dentro de cada `input` | lupa, limpar, mostrar senha | tirar |
| S10 | bonequinhos ilustrados | ilustração em vazio ou erro | marca com ilustração própria | texto e ação |
| S11 | spinner gigante como estado vazio | spinner sem conteúdo | nenhuma | estado vazio de verdade |
| S12 | borda em gradiente aninhada | borda com gradiente dentro de outra | nenhuma | uma borda neutra |
| S13 | tudo muito arredondado | raio de 24 px ou mais em campo, tabela e botão juntos | marca lúdica declarada | raio de 6 a 8 px |
| S14 | título com gradiente | `background-clip: text` | uma vez em peça gráfica, decidida no plano | cor sólida |
| S15 | sombra, gradiente e desfoque no mesmo componente | os três juntos | nenhuma | ficar com um |

Ação: S1 a S5 no caminho principal impedem a entrega; S6 a S9 se corrigem na mesma passada; S10 a S15 se corrigem salvo exceção escrita. **Anti-genérico apaga enfeite, não estrutura:** tirar o quadro de uma lista, os divisores ou a busca é erro.

## Sinais que a matriz não tem
- Seta "→" colada no rótulo do botão.
- Uma palavra destacada no título como única ideia tipográfica.
- Numeração 01, 02, 03 em conteúdo que não é sequência.
- Sobretítulo em caixa-alta em todo bloco.
- A mesma sombra cinza sob todo card parado.
- Corpo só em Inter, Roboto ou fonte do sistema, sem escolha declarada.
- Violeta padrão do Tailwind (`#8b5cf6`, `#7c3aed`) como cor principal.
- Neon ciano, magenta e roxo; bolhas de gradiente.
- Emoji no começo de item de lista ou como marca de gravidade.

Pergunta final: a peça seria reconhecível ao lado de um modelo genérico escuro e violeta?

## Componente limpo (padrão quando nada foi decidido)
Botão sólido, raio de 6 a 8 px, rótulo em peso médio com o verbo da ação. Card em superfície com borda de 1 px. Vazio com título, uma frase e um botão com verbo. Campo com rótulo visível e validação ao sair do campo. Modal com fundo escurecido de 50 a 70% e painel opaco com borda. Item de navegação ativo com fundo sutil ou borda à esquerda.

## Contenção
- Ousar num lugar só: um elemento memorável por tela, slide ou página.
- Na dúvida, tirar um enfeite antes de pôr outro.
- Estrutura é informação: borda, número, divisória e rótulo precisam codificar algo.
- Piso sem alarde: responsivo até o celular, foco visível, movimento reduzido respeitado, contraste conferido.

## Arte, capa, pôster e ilustração
A matriz vale para interface. Em peça gráfica, gradiente, desfoque e profundidade são permitidos quando fazem parte do conceito escrito no plano. O logotipo continua funcionando em uma cor e a 16 px.

## Testes de 1 minuto
- Apertar os olhos ou desfocar a captura: ainda há um elemento dominante?
- Três segundos de exposição: o que se lembra é o que devia ser o principal?
- Escala de cinza: a hierarquia continua sem a cor?
- Contar os níveis de hierarquia: mais de 4 ou 5 vira gradiente.
- Tirar todas as bordas: a estrutura cai? Devolva só onde caiu.
- Captura a 25%: a forma geral se sustenta?
- Trocar o texto de exemplo pelo pior caso real (nome longo, número grande, vazio).
