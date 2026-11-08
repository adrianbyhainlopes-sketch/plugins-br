# Acessibilidade: WCAG 2.2 AA na prática

Alvo: nível AA em tudo, AAA onde for prático (texto, contraste, alvo). Critérios conferidos na Recomendação W3C de 12/12/2024 (https://www.w3.org/TR/WCAG22/) em 08/11/2026. A lei brasileira e o eMAG estão em `dados/acessibilidade-br.md`.

## Critérios que mais aparecem
| Critério | Nível | O que pede |
|---|---|---|
| 1.4.3 Contraste mínimo | AA | texto 4,5:1; texto grande (18 pt, ou 14 pt em negrito) 3:1; logotipo e controle inativo isentos |
| 1.4.11 Contraste não textual | AA | 3:1 para o que identifica controle e estado, e para parte de gráfico necessária |
| 1.4.10 Refluxo | AA | sem rolagem nas duas direções a 320 px CSS de largura (256 de altura para conteúdo de rolagem horizontal) |
| 1.4.12 Espaçamento de texto | AA | nada se perde com entrelinha 1,5, parágrafo 2, letra 0,12 e palavra 0,16 vezes o tamanho |
| 2.4.7 Foco visível | AA | o foco do teclado aparece |
| 2.4.11 Foco não encoberto | AA | o elemento com foco não fica totalmente escondido por conteúdo do autor (cabeçalho fixo, banner) |
| 2.5.7 Movimento de arrastar | AA | tudo que se faz arrastando também se faz com um ponteiro sem arrastar |
| 2.5.8 Tamanho do alvo | AA | 24 × 24 px CSS, ou espaçamento que compense; exceções: equivalente, em linha, controle do navegador, essencial |
| 2.5.5 Tamanho do alvo (ampliado) | AAA | 44 × 44 px CSS |
| 3.2.6 Ajuda consistente | A | ajuda repetida em várias páginas fica no mesmo lugar relativo |
| 3.3.7 Entrada redundante | A | não pedir de novo, no mesmo processo, o que o usuário já informou |
| 3.3.8 Autenticação acessível | AA | nenhum passo de login exige teste de função cognitiva (lembrar uma senha, resolver um quebra-cabeça) sem alternativa ou mecanismo de ajuda; leia as exceções no critério |

Também do 2.2: 2.4.12 (foco não encoberto, AAA) e 2.4.13 (aparência do foco, AAA).

## Processo em 5 camadas, nesta ordem
1. **Varredura automática** (axe, Lighthouse, WAVE): pega uma parte dos problemas, não a maioria. Nunca "passou" só por ela.
2. **Só teclado:** alcançar tudo, ordem lógica, foco visível, sair de qualquer modal, nenhuma armadilha, foco no lugar certo depois de abrir, enviar ou apagar, foco não escondido atrás de cabeçalho fixo (`scroll-padding-top`).
3. **Leitor de tela** (NVDA no Windows, VoiceOver no Mac): imagens, rótulos, nome de botão e link, títulos em ordem, regiões, mensagens de status, decorativos ocultos, estado de componente próprio.
4. **Visual:** contraste nos dois modos e contra o fundo real; cor nunca sozinha; link distinguível; zoom de 200%; refluxo a 320 px; espaçamento de texto; alvos.
5. **Fluxo:** erros de formulário, obrigatório avisado antes, entrada redundante, login sem teste cognitivo, ajuda consistente, link para pular ao conteúdo, limite de tempo, legenda, movimento reduzido.

## Teclado e foco
- `:focus-visible` com contorno de 2 px e afastamento de 2 px, a 3:1 contra o fundo; ou anel duplo em `box-shadow` (superfície e cor) para valer no claro e no escuro.
- Teste com Tab de verdade: `element.focus()` por script não aciona `:focus-visible`.
- Grupo (barra de ferramentas, abas, rádios, linhas de grade): um item no Tab, setas movem dentro (tabindex móvel).
- Atalhos: Esc fecha; `/` foca a busca fora de campo; Ctrl+Enter envia em área de texto. Nunca roubar Ctrl+W, Ctrl+T nem a busca do navegador; atalho de uma tecla precisa poder ser desligado.

## Modal: os 5 comportamentos
Leva o foco para dentro; prende o Tab; fecha com Esc; devolve o foco ao gatilho; deixa o fundo inerte. `role="dialog"`, `aria-modal="true"`, `aria-labelledby`. Use o componente acessível do projeto ou `<dialog>` com `showModal()`; nunca os dois.

## Leitor de tela
- Ordem do código igual à visual (cuidado com `order` e grid).
- Um `main`; `nav` com rótulo quando há mais de uma.
- Títulos sem pular nível; um `h1`.
- `aria-live="polite"` para o que pode esperar; `assertive` só para o urgente.
- Estado exposto: `aria-expanded`, `aria-selected`, `aria-checked`, `aria-current`, `aria-pressed`.
- Texto só para leitor com classe de ocultar visualmente, nunca `display: none`.
- Primeira regra do ARIA: se existe elemento nativo, use o nativo. ARIA errado é pior que nenhum.

## Texto alternativo
Decorativa: `alt=""`. Funcional (botão, link): a ação ou o destino. Informativa: o conteúdo. Complexa (gráfico): alternativa curta e descrição longa perto. Imagem de texto: o próprio texto.

## Cognitivo e motor
Linguagem simples; padrões consistentes; prevenir erro (seletor de data, padrões sensatos, formato mostrado antes); reconhecer em vez de lembrar; progresso visível; nada de pop-up surpresa. Toda ação de gesto tem alternativa de toque simples; arrastar tem botões subir e descer; nada escondido só no hover.

## Correções prontas
```html
<button aria-label="Fechar"><svg aria-hidden="true" focusable="false">...</svg></button>

<label for="cpf">CPF</label>
<input id="cpf" inputmode="numeric" autocomplete="off" aria-invalid="true" aria-describedby="cpf-erro">
<p id="cpf-erro">Digite os 11 números do CPF, como 000.000.000-00.</p>

<div role="status" aria-live="polite">Salvo.</div>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
```
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```
O bloco de movimento reduzido acima é a rede de segurança para HTML avulso; nas telas do produto, prefira ajustar por componente (`escala-e-medidas.md`).

## Testes que podem barrar a entrega (com execução)
`eslint-plugin-jsx-a11y` como erro; `jest-axe` ou `@axe-core/playwright` com as tags `wcag2a`, `wcag2aa`, `wcag22aa`; testar cada estado (acordeão aberto e fechado); buscar elementos por papel (`getByRole`), não por `data-testid`. Instalar qualquer um deles só com o sim do usuário.

## Achado de acessibilidade
Critério e nível, onde, quem é afetado, como reproduzir, evidência (medida ou trecho de código), correção. Gravidade pela escala de `achados.md`: bloqueia o acesso ou falha nível A → Crítico ou Alto; falha AA → Médio (Alto no caminho principal); AAA e boa prática → Baixo. Relatório diz "atende à WCAG 2.2 AA nos critérios verificados", nunca "acessível" sem ressalva.
