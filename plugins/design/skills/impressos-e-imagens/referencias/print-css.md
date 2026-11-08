# Documento longo em HTML que imprime limpo

A skill entrega estrutura e estilo, nunca conteúdo: não acrescenta frase, número, citação nem análise ao texto do usuário. Campo que falta vira `<span class="placeholder">{{o que falta}}</span>` com fundo amarelo-claro, para achar na revisão (e sair antes do PDF final).

Regra-mãe: **se fica certo na tela e quebra na impressão, está errado.** O que vale é o PDF.

## Esqueleto
Partes lineares, só as que o documento pede:
1. **Abertura:** título, subtítulo ou autor; sem cabeçalho nem número (página nomeada).
2. **Sumário:** a partir de 4 seções, ou quando pedido; numa página própria ou logo abaixo da abertura.
3. **Corpo:** seções `h2`, subseções `h3`; figuras e tabelas numeradas com legenda.
4. **Notas:** o Chrome e o Edge não fazem nota no pé da página (`float: footnote` não funciona). Dois contornos:
   - **No fim do capítulo ou da seção** (padrão), com link de ida e volta. Robusto: não quebra quando o texto muda.
   - **No pé da página, por paginação feita no próprio HTML:** um script no documento mede o texto, monta cada página A4 como um bloco de altura fixa e põe cada nota no pé da página onde a chamada caiu; o PDF sai com `@page { margin: 0 }` e as margens dentro do bloco. Use quando o usuário pedir nota no pé explicitamente. Diga o custo: é frágil (qualquer mudança no texto exige gerar de novo), e cada página precisa ser olhada (nota que não cabe, página com buraco antes de figura). O cabeçalho, o número e o sumário passam a vir do script, não das caixas de margem.
5. **Referências, anexos ou assinatura**, se o gênero pedir. Contrato termina na assinatura; relatório, no rodapé de autoria; nunca os dois.

Pedido ambíguo sobre o gênero (livro, relatório, contrato, trabalho acadêmico): pergunte uma vez. Trabalho acadêmico com norma (ABNT ou a da instituição): pergunte qual norma e não invente regra de margem ou de citação.

## Contrato de impressão (base)
```css
@page {
  size: A4;
  margin: 25mm 22mm 22mm 25mm;              /* topo, direita, baixo, esquerda */
  @top-left     { content: "Título do capítulo"; font: italic 8.5pt Georgia, serif; color: #555; }
  @bottom-center { content: counter(page); font: 9pt Georgia, serif; }
}
@page abertura { @top-left { content: none; } @bottom-center { content: none; } }
.abertura { page: abertura; }

body { font: 11pt/1.5 "Fonte do texto", Georgia, serif; margin: 0; color: #1a1a1a; }
h1, h2, h3 { line-height: 1.2; break-after: avoid; }
p { margin: 0 0 3mm; text-align: justify; hyphens: auto; orphans: 3; widows: 3; }
figure, table { break-inside: avoid; }
figure svg, figure img { width: 100%; height: auto; display: block; }
figcaption, caption { font-size: 9pt; color: #555; caption-side: bottom; text-align: left; }
.notas { break-before: page; }
a { color: inherit; text-decoration: none; }        /* link não aparece azul no papel */
@media print { * { print-color-adjust: exact; -webkit-print-color-adjust: exact; } }
```
- `lang="pt-BR"` no `<html>`: sem ele, não há hifenização nem idioma no PDF.
- `break-after: avoid` no título impede título órfão no pé da página; `orphans` e `widows` evitam linha solta.
- Tabela longa que precisa quebrar: tire o `break-inside: avoid` dela; o Chrome costuma repetir o cabeçalho (`<thead>`) na página seguinte; confira no PDF.
- Cabeçalho que muda por capítulo: uma página nomeada por capítulo (`@page cap2 { @top-left { content: "Capítulo 2" } }` e `section.cap2 { page: cap2 }`). `string-set` não funciona no Chrome nem no Edge.
- "Página X de Y": `content: "Página " counter(page) " de " counter(pages)`.
- Margens: as do pedido ou da norma; sem pedido, as da base acima. Margem espelhada (livro encadernado) usa `@page :left` e `@page :right`; confira na amostra.

## Tipografia de documento
- Corpo serifado de 10,5 a 12 pt, entrelinha 1,4 a 1,6; títulos por tamanho, peso e espaço, sem caixa-alta espaçada.
- Medida: 45 a 75 caracteres por linha. Em A4 com margens laterais de 22 a 25 mm e corpo de 11 pt, a coluna única fica no limite alto: confira contando uma linha do PDF; se passar de 75, aumente a margem ou o corpo.
- Justificado só com hifenização funcionando (dicionário no perfil, ver a receita). Sem hifenização: à esquerda.
- Cor: tons de cinza e um acento só. Qualquer outra cor é decisão escrita.
- Números de tabela à direita, com algarismos tabulares; formatos brasileiros (`formatos-br.md`).

## Sumário
```html
<nav class="sumario" aria-label="Sumário">
  <h2>Sumário</h2>
  <ol>
    <li><a href="#sec-1">Primeira seção</a><span class="pontos"></span><span class="pg">{{p1}}</span></li>
  </ol>
</nav>
```
```css
.sumario ol { list-style: none; padding: 0; }
.sumario li { display: flex; align-items: baseline; gap: 2mm; }
.sumario .pontos { flex: 1; border-bottom: 1pt dotted #bbb; }
.sumario .pg { font-variant-numeric: tabular-nums; }
```
O número vem das duas passadas da receita. Cada título do corpo leva o `id` correspondente; o link funciona no PDF.

## Figuras, imagens e fontes
- Figura em SVG embutido no HTML ou arquivo local ao lado; nunca imagem pela internet (some no PDF sem rede).
- Toda figura numerada, com legenda e texto alternativo (`svg.md` para SVG).
- Fonte: do sistema ou arquivo local com `@font-face { src: url("fontes/arquivo.woff2") }`. Nunca pela internet.
- **Licença da fonte antes de embutir:** o PDF leva a fonte embutida. Confira (1) a permissão de embutir, no campo `fsType` da fonte (0 instalável, 2 restrita: não embutir, 4 ver e imprimir, 8 editável), que se lê com o trecho abaixo, e (2) a licença de uso da fonte para o fim do documento. Fontes sob a OFL podem ser embutidas em documento, inteiras ou em subconjunto, sem mudar a licença do documento. Fonte que vem com o sistema tem a licença do sistema: diga isso ao usuário quando o documento for distribuído, em vez de afirmar que está liberada.

```python
# python -I fstype.py "C:\Windows\Fonts\georgia.ttf"   (só lê o arquivo)
import struct, sys
d = open(sys.argv[1], "rb").read()
base = 12 if d[:4] != b"ttcf" else struct.unpack(">I", d[12:16])[0] + 12   # .ttc: primeira fonte
for i in range(struct.unpack(">H", d[base - 8:base - 6])[0]):
    tag, _, ofs, _ = struct.unpack(">4sIII", d[base + 16 * i:base + 16 * i + 16])
    if tag == b"OS/2":
        print("fsType = 0x%04x" % struct.unpack(">H", d[ofs + 8:ofs + 10])[0])
```

## Acessibilidade do PDF
- O Chrome e o Edge geram PDF com marcação (tags) e idioma por padrão; não use `--disable-pdf-tagging`.
- Texto real, nunca texto em imagem; títulos em ordem (`h1`, `h2`, `h3`); tabela com `<th scope>` e `<caption>`; figura com alternativa.
- Isso atende ao que a LBI chama de formato acessível (arquivo lido por leitor de tela): ver `dados/acessibilidade-br.md`, item ACE-003. Diga "segue as práticas de formato acessível", nunca "certificado".

## Antes de gerar o PDF final
- Nenhum `{{...}}` sobrando (procure no HTML).
- Nenhum recurso pela internet (procure `http` em `src`, `href` de folha de estilo e `@import`).
- `lang`, título do documento (`<title>`), ordem dos títulos.
