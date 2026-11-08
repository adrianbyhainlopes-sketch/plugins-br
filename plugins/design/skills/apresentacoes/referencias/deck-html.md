# Deck em HTML de arquivo único, com PDF vetorial

Um arquivo `.html` que abre em qualquer navegador sem internet, apresenta em tela cheia e vira PDF com texto selecionável. Testado em 08/11/2026 no Edge 157: 3 slides geraram 3 páginas de 1440 × 810 pt (16:9) com o texto extraível.

## Antes do código: a marca
Cores com hex exato (primária, acento, neutros), fontes (proprietária vira a equivalente livre ou do sistema mais próxima), regra de uso ("o azul domina, o vermelho é só acento"). Sem marca: direção sóbria, uma família, um acento. Marca institucional ou registrada (universidade, empresa de terceiro): não reproduza o logotipo, use o nome em texto. Anote tudo num bloco de comentário no topo do `<style>`.

## Casca
```html
<main class="deck">
  <section class="slide" aria-label="Slide 1"><h2>Título de ação</h2>...</section>
</main>
<div class="contador" aria-hidden="true"></div>
```
```css
.deck { position: relative; width: 100vw; height: 100vh; overflow: hidden; }
.slide { position: absolute; inset: 0; margin: auto;
  width: min(100vw, calc(100vh * 16 / 9)); height: min(100vh, calc(100vw * 9 / 16));
  box-sizing: border-box; padding: 6% 7%; display: flex; flex-direction: column; justify-content: center;
  opacity: 0; pointer-events: none; font-size: min(2.2vw, 3.9vh); }
.slide.ativo { opacity: 1; pointer-events: auto; }
@media print {
  @page { size: 1920px 1080px; margin: 0; }
  html, body { background: none; height: auto; }
  .deck { width: auto; height: auto; overflow: visible; }
  .slide { position: relative; inset: auto; width: 1920px; height: 1080px; opacity: 1; font-size: 40px; break-after: page; }
  .contador { display: none; }
  * { transition: none !important; animation: none !important; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
}
```
```js
// setas, PageUp/PageDown e espaço navegam; Home e End; F tela cheia; #n abre o slide n
var s = document.querySelectorAll(".slide"), c = document.querySelector(".contador");
var atual = Math.min(Math.max(parseInt(location.hash.slice(1), 10) || 1, 1), s.length);
function mostra(n) { atual = Math.min(Math.max(n, 1), s.length);
  s.forEach(function (el, i) { el.classList.toggle("ativo", i === atual - 1); });
  c.textContent = atual + " / " + s.length; history.replaceState(null, "", "#" + atual); }
document.addEventListener("keydown", function (e) {
  if (["ArrowRight", "PageDown", " "].indexOf(e.key) >= 0) { e.preventDefault(); mostra(atual + 1); }
  if (["ArrowLeft", "PageUp"].indexOf(e.key) >= 0) { e.preventDefault(); mostra(atual - 1); }
  if (e.key === "Home") mostra(1); if (e.key === "End") mostra(s.length);
  if (e.key === "f" && document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
});
mostra(atual);
```
- Tamanhos em `em` dentro do slide: a tela escala pelo `font-size` do slide e a impressão fixa em 40 px por slide de 1080 de altura.
- 16:9 por padrão (projetor e TV). 4:3 só se a sala pedir: troque as proporções e o `@page`.
- Passador de slides (o controle remoto comum) costuma mandar PageDown e PageUp: já está coberto.
- Sem `@page`, o navegador imprime em papel Carta e corta o slide sem avisar.

## Regras do slide
- Um slide, uma tarefa, uma ideia visual dominante. No máximo 3 pontos.
- Um slide é uma tela: nada de rolagem. Conteúdo que não cabe vira outro slide, nunca letra menor.
- Tipos: título, divisória de seção, conteúdo, dividido (texto e imagem), dado (um número grande ou um gráfico), tabela curta, citação, referências.
- Numeração 01, 02 só em sequência real; sem sobretítulo em caixa-alta; sem emoji no começo de item (`anti-generico.md`).
- Imagem e fonte locais; nada pela internet.
- Contraste conferido: texto 4,5:1, texto grande 3:1. Projetor lava as cores: prefira contraste alto ao sutil.

## Tamanho da letra para projeção
Não há número com fonte para o menor tamanho legível em projeção; não invente um. Faça assim:
1. Anote o menor tamanho usado em cada tipo de slide (no PDF de 1920 × 1080: corpo, rótulo, fonte).
2. **Teste na sala** (ou na tela de destino), do lugar mais distante do público, lendo o menor texto. Sem sala, diga que o tamanho é "a testar" e onde ele está no CSS para ajustar.
3. O que não se lê do fundo sai do slide (vai para as notas ou para o texto distribuído), não fica menor.

## Exportar e conferir
PDF pela receita (`receita-pdf-windows.md`, seção 1) e verificação da seção 4: páginas igual ao número de slides; tamanho 1440 × 810 pt; texto de cada página extraído; olhar o primeiro, o último e todo slide com imagem ou tabela. Um slide maior que a página é cortado em silêncio: o olhar pega isso, a contagem não.

## Edição segura do arquivo
- Nada de substituição em massa por expressão regular num arquivo com JavaScript (pode trocar `atual - 1` por outra coisa).
- "Slide 3: muda X" muda só isso.
- Depois de editar o script, confira a navegação (abrir, avançar, voltar).

## PowerPoint
Se o entregável é `.pptx` ou precisa ser editado no PowerPoint, passe para a skill de pptx, se houver, com o roteiro e a direção visual prontos. Não gere PPTX por conta própria nesta skill.
