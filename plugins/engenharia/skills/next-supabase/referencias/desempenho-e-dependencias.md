# Desempenho e dependências

## Medir antes de otimizar
- Meça o build de produção (`next build` + `next start`), não o servidor de desenvolvimento; três rodadas ao comparar.
- Linha de base com número e meta ("2,3 s; meta abaixo de 500 ms"), ataque o maior custo, meça de novo com a mesma carga, relate antes e depois.
- O maior custo quase sempre é estrutural: N+1, laço com consulta, índice faltando, cascata de `await`, trabalho repetido.
- Cache só com plano de invalidação. Paralelismo sem medida traz corrida, não velocidade.
- O Next 16 tirou do `next build` as métricas de tamanho por rota (eram imprecisas com Server Components). Use o Lighthouse ou a análise da hospedagem para Core Web Vitals; rodar `npx lighthouse` ou instalar algo pede o sim do usuário.
- Sinais de alerta: "deve ficar mais rápido"; otimizar no meio de outra tarefa; cache ou paralelismo preventivo. Nunca prometa nota.

## Ordem de prioridade
1. Cascatas: mova o `await` para o ramo que usa; `Promise.all` para buscas independentes; `<Suspense>` para transmitir aos poucos.
2. Bundle: importe do módulo, não de um arquivo-barril; `next/dynamic` para o que é pesado e tardio; scripts de terceiros depois da interação.
3. Servidor: `cache()` do React para deduplicar na mesma requisição; passe pouco dado ao Client Component; busque em paralelo.
4. Busca no cliente: com estado de carregando, erro e sucesso; `response.ok` conferido; `AbortController`.
5. Render: derive no render; atualização funcional de estado; `useTransition`; nunca defina componente dentro de componente.

Métricas de laboratório, como referência: LCP até 2,5 s, CLS até 0,1, TBT até 200 ms (substituto do INP). LCP: a imagem principal no HTML, com `fetchpriority="high"`, nunca `loading="lazy"`. CLS: largura e altura ou `aspect-ratio`, espaço reservado para o que chega depois.

## Supabase
- `.from()` dentro de `map` é N+1: traga a relação no próprio `select` (`select('*, itens(*)')`).
- Colunas explícitas no `select`, não `*`, no que vai ao cliente.
- Listas com limite e ordem estável (`.order(...).range(...)`).
- Índice nas colunas usadas pelas policies e pelos filtros (proposta para a revisão de banco, não migração feita aqui).

## Antes de adicionar uma dependência
- A plataforma ou o projeto já resolve? (`Intl.DateTimeFormat` em vez de biblioteca de data; `fetch` em vez de cliente HTTP; dez linhas em vez de uma biblioteca inteira.)
- O pacote existe de verdade? Confira no registro oficial antes de instalar: nome inventado por IA pode ter sido registrado por atacante, e instalar "para ver se existe" já é o ataque. Desconfie de pacote publicado há pouco, quase sem downloads, com nome a uma letra de um popular, sem repositório.
- Versão conferida no registro; lockfile commitado; sem `latest` ou `*`.
- Saúde e licença: repositório ativo; avisos de segurança (`npm audit`); script de `postinstall` que acessa rede ou disco; licença compatível (copyleft em código fechado é problema).
- Peso: medir o build antes e depois; desconfiar de pacotes conhecidos por pesar (biblioteca de datas antiga, utilitários inteiros, conjuntos inteiros de ícones, `import * as`, a mesma biblioteca em duas versões no lockfile).
- Diga o custo ao usuário antes de instalar; instalar só com o sim.
