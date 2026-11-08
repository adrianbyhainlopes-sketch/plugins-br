# SVG à mão: arte final, figura e diagrama

## Fluxo
1. Olhe os ativos que já existem (cores e fontes do projeto, logotipo, `BRAND.md` ou `DESIGN.md`) e reaproveite.
2. Decida antes de desenhar: o que a figura precisa mostrar, formato de saída (SVG, PNG, PDF) e tamanho. O pedido sempre vence o padrão.
3. Escreva o SVG num arquivo com nome descritivo (com execução) ou como artefato (no chat).
4. **Veja o resultado antes de responder**, numa captura ou no artefato, e corrija: texto cortado ou sobreposto, contraste fraco, desalinhamento, espaço morto.
5. Responda curto: o que se vê, as decisões e 2 a 4 variações possíveis (cor, peso, layout). Itere editando o arquivo atual, não refazendo do zero.

Sem conseguir ver (chat sem artefato, sem navegador): entregue e marque "Não verificado: render".

## Contrato do arquivo
- Um `<svg>` completo com `viewBox` e `xmlns="http://www.w3.org/2000/svg"`. Tamanhos de partida: figura 800 × 600; pôster 600 × 800; tela de celular 390 × 844; post quadrado 1080 × 1080; carrossel 1080 × 1350.
- Primeiro elemento: um `<rect>` de fundo do tamanho todo (sem fundo, o PNG sai transparente e o PDF pode sair estranho).
- XML válido: `&amp;` para "e comercial"; nada de `&nbsp;` (use `&#160;`).
- Autossuficiente: sem imagem, fonte ou script de fora. Fonte pela pilha do sistema (`Georgia, serif`) ou convertida em contorno quando a forma exata importa (logotipo).
- Cor por classe ou atributo; `var()` do CSS não funciona em atributo de apresentação do SVG.
- Animação só onde ajuda, entrada em menos de 1 s, e nunca em figura que vai para impressão.

## SVG acessível
- Informativo: `role="img"` e `aria-labelledby` apontando para `<title>` (nome curto) e `<desc>` (o que a figura mostra e a conclusão dela).
- Decorativo: `aria-hidden="true"` e nenhum título.
- Texto que importa fica como `<text>` (lido e selecionável), não convertido em contorno, salvo logotipo.
- Gráfico: o `<desc>` diz a conclusão primeiro, depois os números principais.
- Contraste do texto e das linhas que carregam sentido conferido contra o fundo real (4,5:1 texto, 3:1 linha e forma).

## Ofício
- Paleta deliberada, poucas cores, cada acento com um significado (principal, ação, alerta, sucesso).
- Grade mental, hierarquia de tipo, espaço generoso; conceito acima de enfeite.
- Gradiente e desfoque (`feGaussianBlur`) só em arte, capa e ilustração, quando fazem parte do conceito; em figura técnica, cor chapada.
- Logotipo: funciona em uma cor e a 16 px; mostre a linha de variações (símbolo, ícone, assinatura horizontal). Conceito de logo é proposta, não prova de que a marca está livre para registro.

## Diagrama
- Nó: retângulo arredondado, borda de linha, título curto; seta de cerca de 1,8 px com ponta pequena na cor da própria linha; rótulo acima da linha.
- Meça o rótulo contra o espaço (fonte mono: cerca de 0,6 em por caractere).
- Cruzamento de linhas ganha uma ponte (meio círculo).
- Mais de cerca de 7 nós vira dois diagramas.
- Fluxo, estados, sequência ou relação de dados com muito nó: considere uma ferramenta de diagrama (Mermaid) se o destino a suportar sem internet; comparação vira tabela; linha do tempo vira lista com datas.
- Peças de gráfico desenhadas à mão são esquema, não dado: nunca apresente como número medido.

## Para PNG ou PDF
- Não suponha que o SVG tem `width` e `height`: leia o `viewBox` antes.
- Para um tamanho de saída, defina a escala ou a largura, nunca as duas (com uma dimensão só, a proporção se mantém).
- PNG pelo navegador sem janela (receita, seção 2), com o SVG dentro de um HTML do tamanho exato.

## Antes de entregar
Visto de fato; nada encostando na borda; todo cruzamento com ponte; no máximo um gradiente; acentos com significado; fatos e números conferidos com o usuário; formato escolhido, não herdado.
