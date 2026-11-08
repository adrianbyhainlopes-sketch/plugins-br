# Peças estáticas: post, carrossel, story, pôster, infográfico

O texto da peça não é escrito aqui. Ele vem pronto do usuário ou de uma skill de conteúdo (por exemplo, a de Instagram do plugin de pequeno negócio). Esta referência transforma esse texto em imagem sem mudar uma palavra.

## Receber um roteiro de carrossel ou de Stories
O roteiro costuma trazer: a espinha numa frase; por slide, número, texto exato (título e apoio) e nota de design; a especificação do modelo (formato, margem segura, fonte e cores do perfil); a legenda; o alt text por slide.
- **Texto exato é intocável.** Não encurte, não troque palavra, não corrija sem perguntar. Se não couber, aponte o slide e proponha a divisão ou o corte para o autor decidir.
- **Marcadores ficam visíveis.** `[CONFERIR: ...]`, `[FALTA: ...]` e `{{...}}` são renderizados como estão, em destaque, e a peça sai marcada "rascunho, não publicar". Nunca preencha um número de lei, preço ou resultado para "fechar" o slide.
- **Nota de design** orienta, não manda inventar: nada de texto novo na imagem, selo, número ou depoimento que o roteiro não traz.
- Faltou a especificação (fonte, cores): use `BRAND.md` ou `DESIGN.md` se houver; sem eles, pergunte numa rodada só ou proponha uma direção pela skill de direção visual.
- Legenda e alt text não vão na imagem: devolva-os junto, como vieram.

## Formatos de partida
| Peça | Tamanho em px | Observação |
|---|---|---|
| Carrossel e post retrato | 1080 × 1350 (4:5) | layout igual em todos os slides; número do slide num canto fixo |
| Post quadrado | 1080 × 1080 | |
| Story e capa de Reels | 1080 × 1920 (9:16) | zona segura: texto e botão longe do topo e da base, onde a interface do app cobre |
| Pôster, folheto | A4, A3 ou o tamanho pedido, em mm | PDF pela receita, `@page` com o tamanho e margem de segurança |

Limites e zonas de cada rede mudam: confira no app ou na central de ajuda da rede no dia. Não use número de zona segura sem fonte datada; sem ela, deixe uma folga generosa e diga que é folga, não regra.

## Modelo em HTML (um arquivo, todos os slides)
```html
<section class="slide">...</section>   <!-- um por slide -->
<script>
  var n = parseInt((location.hash || "#1").slice(1), 10) || 1;
  document.querySelectorAll(".slide")[n - 1].classList.add("ativo");
</script>
```
```css
html, body { margin: 0; }
.slide { width: 1080px; height: 1350px; box-sizing: border-box; padding: 96px; display: none; }
.slide.ativo { display: flex; flex-direction: column; justify-content: center; }
@media print { @page { size: 1080px 1350px; margin: 0; } .slide { display: flex; break-after: page; } }
```
O mesmo arquivo dá um PNG por slide (`arquivo.html#3`, receita seção 2) e um PDF com todos (receita seção 1), útil para revisão.

## Legível no celular
- Slide é cartaz: título com a ideia e no máximo uma linha de apoio.
- Hierarquia fixa: título, apoio, número do slide, um acento de cor.
- Texto grande o bastante para ler na tela do celular sem ampliar: confira abrindo o PNG no tamanho de um celular, não no monitor.
- Contraste conferido no par real (texto sobre foto: pior ponto, com película se precisar).
- Fonte local ou do sistema; nunca pela internet.

## Infográfico e pôster
- Conta uma história, não junta fatos: quem decide, que ação, a história em 3 minutos.
- Um número ou dois viram texto grande; comparação vira barra com base zero; tendência vira linha.
- Uma ideia por painel, anotação junto do dado, só o principal de cada parte em destaque.
- Enfeite aceitável em peça pública, mas a codificação do dado (comprimento, posição) continua exata.
- Todo número com fonte do usuário; peça de gráfico sem dado real é esquema e diz isso.

## Entrega
Os arquivos (PNG por slide, PDF de revisão, HTML-fonte), a contagem e o tamanho conferidos por código, um slide aberto e visto, a legenda e o alt text devolvidos como vieram, e a lista de marcadores que ainda bloqueiam a publicação.
