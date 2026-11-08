# TypeScript estrito e parse na borda

## Configuração mínima
`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax`; `tsc --noEmit` no CI. Ligar opção nova num projeto grande gera erros em cascata: proponha e meça antes.

## Modelar o domínio
- União de literais em vez de `string` ou `number` soltos (`'rascunho' | 'enviado' | 'pago'`).
- Uma união de estados em vez de dois booleanos (`carregando` e `erro` juntos permitem estados impossíveis).
- União discriminada em vez de "saco de campos opcionais", com um nome de discriminante só no projeto.
- Tipo marcado (brand) para IDs e unidades que dividem o mesmo primitivo (`Centavos`, `ClienteId`).
- Tipos derivados da fonte (`z.infer`, tipos gerados do Supabase) em vez de cópia que deriva.

## Sem mentir para o compilador
- `unknown` em vez de `any` para tudo que vem de fora (fetch, `JSON.parse`, `catch`, armazenamento, env, linha do banco).
- Sem `as` e sem `as unknown as`; os únicos aceitos são `as const` e o de dentro de um construtor de tipo marcado.
- Sem `!`; índice de array é `T | undefined` (trate, não force `arr[0]!`).
- Por que o compilador não infere → correção: falta discriminante → união discriminada; tipo de origem largo → estreitar onde é produzido; fronteira sem tipo → parse com esquema; impossível de expressar → brand ou `satisfies`.
- Estreitamento: `switch` por discriminante > `in` > `typeof`/`instanceof` > guarda própria (que prova o que diz; guarda mentirosa é pior que `as`).
- Exaustividade: `switch` sobre união termina em `default: return assertNever(x)`.
- `satisfies` em vez de anotação quando quer conferir a forma sem alargar os literais.

## Parse, não valide
"Validar devolve um booleano; fazer parse devolve um tipo mais estreito."
- Separe as fases: entrada → parse (todas as checagens, nenhum efeito) → valor válido → ação (todos os efeitos, nenhuma checagem). Checagem depois do primeiro efeito deixa registro pela metade.
- Parse na borda mais externa: Server Action, rota, argumento de linha de comando, consumidor de fila e também a linha lida do banco (linhas antigas foram gravadas por código antigo).
- Cheiros: `!` ou `as` abaixo da borda; o mesmo `if (x == null)` em três funções da cadeia; comentário "supõe que já foi validado".
- Zod: confira a versão no lockfile. No Zod 4 os erros se formatam com `z.flattenError()` (objeto raso, bom para formulário), `z.treeifyError()` (aninhado) e `z.prettifyError()` (texto); `z.formatError()` está obsoleto. Código escrito para o Zod 3 (`.flatten()`, `.format()`, `typeToFlattenedError`) precisa ser conferido.
- Não use em script com um chamador só: parse pesado ali é cerimônia.

## Checklist de revisão de tipos
`any` novo; `as` novo; `!` novo; `@ts-ignore` ou `@ts-expect-error` novos; booleano duplo virando estado impossível; união sem `assertNever`; tipo copiado em vez de derivado; `unknown` estreitado sem prova; índice sem tratar `undefined`; data como `Date` de um lado e texto do outro; dinheiro como `number` com casas decimais.
