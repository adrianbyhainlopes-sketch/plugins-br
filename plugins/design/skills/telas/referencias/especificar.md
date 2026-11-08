# Especificar a tela antes do código

Princípio: **todo elemento declara por que existe.** "Tabela" é um nome; "tabela, porque o atendente tria 200 pedidos por status" é uma decisão.

## Fluxo
1. Aterrar no que existe: documentos, rotas vizinhas, componentes do projeto; reutilize os nomes do produto.
2. Perguntar só o que bloqueia (tarefa, quem usa e com que papel, dados e volume, de onde vem e para onde vai, restrições), numa rodada, com opções.
3. Sem resposta, escolher o mais razoável e registrar em Premissas.
4. Rascunhar, conferir, entregar e oferecer as telas vizinhas (detalhe, criar ou editar, confirmação) sem supor que estão no escopo.

## Leve (padrão) ou completa
- **Leve**, para tela pequena, diálogo, aviso ou passada rápida: as seções 1, 3, 6, 8, 9, 12, 13 e 14 abaixo. Fecha com uma linha dizendo o que ficou de fora e oferecendo a completa.
- **Completa**, para tela central do produto: as 15. Mesmos títulos nas duas, para expandir sem reescrever.

## As 15 seções
1. Propósito e o que fica fora.
2. Usuários e objetivos (papel, pode, não pode).
3. Premissas e perguntas abertas (A1, Q1; impacto se estiver errado; situação).
4. Entradas e saídas (direção, tela, gatilho, estado ao carregar).
5. Dados (dado, leitura ou escrita, volume, atualização).
6. Árvore de layout (notação abaixo).
7. Detalhe por região.
8. Componentes (tipo, por que existe, dados, campos, comportamento, validação e os estados vazio, carregando, preenchido, erro).
9. Fluxo principal e alternativos.
10. Regras de interação (gatilho, resultado, retorno ao usuário, reversível ou não).
11. Validação entre campos.
12. Estados de tela (primeiro uso, sem resultado, carregando, erro, sem permissão).
13. Responsivo (largo, médio, estreito, com o porquê).
14. Acessibilidade (teclado, foco, leitor de tela, sinais além da cor, alvo de 24 px no mínimo, contraste 4,5:1, movimento). Aqui números de requisito são bem-vindos.
15. Extensibilidade.

Seção que não se aplica leva "não se aplica" e o porquê. Sem estilo (cor, fonte, px) fora da seção 14. Projete para o volume informado; desconhecido, suponha que cresce (paginação, filtro, ação em lote) e registre.

## Notação da árvore
- Um nó por linha, recuo de 2 espaços, nome pelo papel (`listaPedidos`, `barraFiltros`).
- Contêiner com 2 filhos ou mais declara a direção: `row`, `col` ou `grid` (`cols=N`), e pode levar `justify`, `align`, `wrap`, `gap=xs..xl` (token relativo, nunca px) e `scroll=x|y`.
- Filho: `flex=N`, `fill`, `hug`, `w=NN%`, `sticky`, `overlay` (por último, filho da raiz).
- `nome*` repete por item; `nome?` é condicional, com a condição escrita.
- A árvore descreve a tela larga; se a estreita reestrutura, segunda árvore.

```
pagina col gap=lg
  cabecalho row justify=between
    titulo
    acoes row gap=sm
  barraFiltros row wrap gap=sm
  listaPedidos col scroll=y
    pedido*
  avisoSemResultado?   (quando o filtro não acha nada)
```

## Conferência antes de entregar
- Tudo que está na árvore está no texto, e vice-versa.
- Todo `?` tem condição.
- Toda ação tem resultado e retorno; a destrutiva tem confirmação ou desfazer.
- "Sem dados ainda" e "sem resultado para este filtro" são estados diferentes.
- Cada premissa aparece em Premissas; nenhuma decisão escondida no texto.
- Ordem de leitura, níveis de título e texto alternativo anotados para quem desenha.
