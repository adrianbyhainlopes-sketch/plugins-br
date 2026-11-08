# Tokens em Tailwind v4 com shadcn

Conferido na documentação do Tailwind (v4.3) em 08/11/2026: namespaces do `@theme`, `@theme inline` e reset por `initial`. Confira de novo se a versão do projeto for outra.

## Regras duras
- Detecte a stack e estenda. Em Tailwind, os tokens são o tema dele, não um sistema paralelo. Com shadcn, as variáveis dele são o sistema: não renomeie.
- Dois níveis só: primitivas (a rampa de cores, a escala) e papéis (`--primary`, `--border`). Componentes usam papéis (`bg-primary`, `border-border`), nunca a primitiva crua.
- Modo escuro desde o primeiro dia: os papéis mudam de valor, as primitivas não.
- Deriva se relata em contagem e arquivo:linha, nunca como "parece inconsistente".

## Sistema mínimo
- Papéis do shadcn: `--background`, `--foreground`, `--card`, `--primary`, `--secondary`, `--muted`, `--accent`, `--border`, `--ring`, `--destructive` (e os `-foreground` de cada um). Cores em OKLCH.
- Cor: um acento e uma rampa neutra de uma matiz só (quente ou fria, escolhida uma vez). Sucesso e aviso só se o produto mostrar.
- Espaço: a escala padrão do Tailwind (base 4).
- Raio: um `--radius` base e no máximo três derivados.
- Tipo: até 2 famílias, 5 a 7 tamanhos, pesos 400, 500 e 600.
- Sombra: 2 ou 3 níveis, baixa opacidade, só no que flutua.
- Camadas (z-index) com nome e folga: conteúdo, fixo, menu, gaveta, modal, aviso.

```css
@import "tailwindcss";

:root {
  --background: oklch(0.99 0.003 250);
  --foreground: oklch(0.22 0.02 250);
  --primary: oklch(0.48 0.12 250);
  --primary-foreground: oklch(0.99 0 0);
  --border: oklch(0.90 0.01 250);
  --radius: 0.5rem;
  /* ...demais papéis do shadcn */
}
.dark {
  --background: oklch(0.17 0.01 250);
  --foreground: oklch(0.94 0.005 250);
  --primary: oklch(0.70 0.10 250);
  --border: oklch(0.30 0.01 250);
}
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-border: var(--border);
  --radius-md: var(--radius);
  --radius-sm: calc(var(--radius) - 2px);
}
```
Os valores acima são exemplo de forma, não paleta: calcule o contraste de cada par antes de usar.

## O que pega no v4
- `@theme inline` quando a variável aponta para outra (`var(...)`): sem `inline`, a referência pode resolver no lugar errado e cair no padrão.
- Tamanho de fonte é `--text-*` (gera `text-xl`); `--font-*` é família; `--font-weight-*` é peso.
- Nome que gera classe esquisita: `--color-bg` vira `bg-bg`; prefira `--color-background`.
- Trocar o tema inteiro de um grupo: `--color-*: initial;` antes das suas cores.
- Pontos de quebra padrão: sm 40rem, md 48rem, lg 64rem, xl 80rem, 2xl 96rem. Não crie ponto novo para uma tela só.
- Classe arbitrária com equivalente nativo vira a nativa (`z-[60]` por `z-60`, `h-[100vh]` por `h-screen`, `aspect-[9/16]` por `aspect-9/16`), conferindo na versão do projeto.
- Tamanho de fonte próprio com prefixo `text-` pode ser derrubado pelo `tailwind-merge` quando combinado com cor (`cn('text-brand', 'text-hero')`): registre o grupo no `extendTailwindMerge`.

## Medir deriva (por busca no código)
| Sinal | Limite |
|---|---|
| cor crua (`#abc`, `rgb(`) fora do arquivo de tokens | 0 |
| classe arbitrária de cor (`bg-[#eee]`) | 0 |
| espaçamento fora da escala | 0 (fio de 1 px liberado) |
| raios distintos | 3 (`calc()` sobre o token conta como derivado) |
| z-index cru | 0 |
| arquivos de paleta | 1 |
| `outline: none` ou `outline-none` sem anel de foco no lugar | 0 |

Exclusões legítimas, nomeadas no relatório: HTML de e-mail, CSS de impressão, widget de terceiro, código gerado. Sombra não conta como cor crua; `50%` e `9999px` são círculo e pílula. Projeto que nunca usou a base 4: derive a escala dos valores que cobrem 90% das ocorrências e meça contra ela.

## Migrar sem quebrar
1. Acrescente os tokens novos. 2. Crie os componentes. 3. Aplique arquivo por arquivo, com build a cada passo. 4. Troque as classes. 5. Remova os tokens antigos e confirme por busca. Meta: nenhuma mudança visual. Nomes de token e quais padrões extrair são decisão do usuário.

## Componente
Variantes tipadas (`variant: "primary" | "secondary" | "ghost"`), nunca `style` solto; estados padrão, hover, active, focus-visible, disabled, loading e error; texto vindo de propriedade, nunca fixo. Extraia a partir de 3 repetições. Anti-padrões: `<div onClick>` no lugar de botão; card que busca os próprios dados; `className` sobrescrevendo token; `loading` e `isLoading` juntos; mais de 15 propriedades (são dois componentes).

## Relatório de tokens
Criação: o bloco de tokens, o mapa de valores antigos para tokens e as contagens antes e depois. Revisão: tabela sinal, contagem, gravidade, piores ocorrências, correção, no máximo 10 linhas, com a escala de `achados.md`.
