<!-- cópia gerada de compartilhado/escala-e-medidas.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Escalas, medidas e decisões que as fontes discordam

Valores padrão de todas as skills de design. O que o projeto já tem (tokens, marca, DESIGN.md) vence estes padrões: estenda o que existe, não crie sistema paralelo.

## Tipografia
- Na interface: pesos 400, 500 e 600. 700 só em título grande (display, hero), capa de slide, título de documento impresso e tipografia de marca.
- Tamanhos de interface: corpo 16 px, secundário 14 px, metadado 12 px; nada abaixo de 12. Conteúdo principal (célula, card, valor de campo) é corpo ou secundário.
- Escala modular, tamanho = base × razão elevada ao passo. Razão pela densidade: 1,125 produto denso; 1,2 equilibrado; 1,25 editorial; 1,333 expressivo. No máximo 4 ou 5 tamanhos por tela.
- Entrelinha cai quando o tamanho sobe: display 1,1 a 1,15; títulos 1,2 a 1,25; corpo 1,5 a 1,6.
- Uma família na interface; uma segunda só em título. Toda fonte com disponibilidade dita: instalada, arquivo local ou "[precisa instalar]" com o substituto que funciona.
- Medida da linha: 65 caracteres como padrão na tela (`max-width: 65ch`), 75 como teto. No impresso, medida em mm ou pt, entre 45 e 75 caracteres por linha.
- Números em coluna com `font-variant-numeric: tabular-nums`, alinhados à direita.
- Texto justificado só no impresso, com `hyphens: auto`, `lang="pt-BR"` e conferência de rios na amostra. Na tela, sempre à esquerda.

## Espaço
- Escala: 4, 8, 12, 16, 24, 32, 48, 64. Fio de 1 px liberado. Nada de 13 ou 22 sem correção óptica escrita.
- Dentro do grupo, menos espaço que entre grupos, e a diferença tem de ser óbvia: níveis vizinhos de agrupamento diferem 1,5 a 2 vezes (4 e 6 parecem iguais; 4 e 16 não). 12 e 16 não separam níveis.
- O título fica mais perto do próprio conteúdo que do bloco anterior.

## Cor e contraste
- Texto 4,5:1; texto grande (18 pt, ou 14 pt em negrito) e partes de controle 3:1.
- Medir no par renderizado com o alfa achatado, sempre que o fundo for liso. Captura de tela só sobre imagem, gradiente ou vídeo, relatando a pior razão. Todo número com o método.
- Cor nunca é o único sinal (erro com ícone e texto, série com cor e padrão).
- Modo escuro nunca por inversão: os papéis mudam, a paleta de base fica.

## Larguras e grade
- Pontos de quebra: os do projeto. Em Tailwind, os dele (sm 640, md 768, lg 1024, xl 1280), sem ponto novo para uma tela só.
- Larguras de teste: 375, 768 e 1280, mais 320 para o refluxo da acessibilidade.
- Limitar a página, não o app: só o conteúdo principal leva largura máxima.

## Superfície e elevação
- Borda delimita o que está no plano da página (card, lista, tabela, sempre com moldura ou degrau de fundo).
- Sombra suave só no que flutua (menu, popover, modal), com alfa baixo (até cerca de 0,08 no claro).
- São achados: borda no lugar de sombra num elemento que flutua; a mesma sombra sob todo card parado.

## Alvo de toque e clique
- Piso que reprova: 24 × 24 px CSS (WCAG 2.2, critério 2.5.8, nível AA, com as exceções do critério).
- Meta de projeto: 44 × 44 em controle de toque (celular e ações principais). Abaixo da meta e acima do piso é achado baixo, nunca "falha AA". 48 não é critério da WCAG.

## Comportamento
- **Ação destrutiva:** reversível executa e oferece "Desfazer"; irreversível pede confirmação com título que nomeia a ação, corpo com a consequência, botão que repete a ação e saída clara. Destrutiva sem desfazer e sem confirmação reprova.
- **Botão de enviar:** antes do clique, não desabilitar para validar (o clique mostra os erros). Durante o envio, travar o segundo clique com rótulo "Salvando...". Desabilitado por permissão ou pré-condição mostra o motivo ao lado.
- **Erro de campo:** fica até a primeira tecla que corrige ou até o valor ficar válido; nunca some só porque o campo recebeu foco.
- **Movimento reduzido:** nas telas, menos e mais suave, não zero (sem deslocamento, só opacidade até 150 ms); significado nunca só no movimento. Reset global de animação só como rede de segurança em HTML avulso (deck, documento).
- **Modal:** use o componente acessível que o projeto já tem (por exemplo, o Dialog do shadcn); em HTML avulso, `<dialog>` nativo com `showModal()`. Nunca os dois, nem armadilha de foco manual por cima. Confira os 5 comportamentos: leva o foco, prende o Tab, fecha com Esc, devolve o foco, deixa o fundo inerte.

## Slides
- Formato segue o entregável: arquivo .pptx ou editável no PowerPoint vai para a skill de pptx, se houver; apresentar do navegador ou entregar PDF vai em HTML. Na dúvida, pergunte uma vez.
- Tamanho mínimo de letra para projeção: não há número com fonte. Teste na sala ou na tela de destino (ver a skill de apresentações).

## Fontes e arquivos
- Fontes locais ou do sistema em tudo que vira PDF ou é entregue. Fonte pela internet só em protótipo descartável.
- Antes de embutir, confira a permissão de embutir da fonte e a licença de uso.

## Decisões e perguntas
- As decisões de design do projeto ficam num par só: `BRAND.md` (marca) e `DESIGN.md` (aplicação por superfície, incluindo preferências de saída). Pergunte antes de criar o arquivo.
- Uma rodada de perguntas, no máximo 3 bloqueantes, cada uma com opções e um padrão proposto. O resto vira premissa registrada.
- Especificação de tela sem estilo (sem cor, fonte nem px), exceto os requisitos de acessibilidade, que são números de requisito (alvo de 24 px, contraste 4,5:1).
