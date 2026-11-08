# Rubrica de revisão

Aprove quando a mudança melhora a saúde do código, mesmo sem estar perfeita. Não bloqueie por gosto.

## Ordem
1. Intenção (título, pedido) antes do código.
2. Testes primeiro: existem? testam comportamento? pegariam uma regressão?
3. Arquivo por arquivo pelos eixos abaixo.
4. "Verificar a verificação": que testes rodaram, o build passou, houve teste manual, captura para mudança de interface.

## Eixos
- **Correção** (o /code-review cobre a caça a bugs; aqui só o que ele não mira): bate com o pedido? bordas (nulo, vazio, limites)? caminhos de erro?
- **Design e manutenção:**
  - propagação: arquivos sem relação com o propósito; classe mudando por mais de um motivo;
  - carga cognitiva: função longa, aninhamento acima de 3, mais de 4 parâmetros, número mágico, nome que exige ler a implementação;
  - duplicação de conhecimento: lógica que já existe em outro lugar; nome novo para conceito que já tem nome;
  - complexidade acidental: abstração com um uso só; classe que só repassa; ponto de extensão sem requisito;
  - dependência fora de ordem: módulo de alto nível importando driver ou cliente HTTP; ciclos;
  - domínio: nomes diferentes da linguagem do negócio; regra de negócio escondida em "util".
- **Arquitetura:** segue o padrão existente ou cria outro com justificativa; fronteira de módulo; camada certa.
- **Desempenho:** N+1, consulta sem limite, lista sem paginação, trabalho repetido em laço, render desnecessário.
- **Dependência nova:** a pilha atual já resolve? peso? mantida? vulnerabilidade conhecida? licença compatível? nome conferido no registro (pacote inventado por IA existe e é armadilha)?

## Tamanho
Cerca de 100 linhas é bom, 300 é aceitável se for uma coisa só, acima de 1000 tem de ser dividido. Acima de 300, amostre o de maior risco e diga que amostrou. Refatoração e funcionalidade são duas mudanças.

## Corte de confiança
| nota | quando |
|---|---|
| 0 | falso positivo ou problema que já existia |
| 25 | talvez; estilo que não está nas regras do projeto |
| 50 | real, mas pequeno ou raro |
| 75 | verificado duas vezes, vai acontecer na prática, ou citado nas regras |
| 100 | confirmado e frequente |
Reporte só a partir de 80. Não sinalize: estilo, o que o linter pega, falta genérica de teste, regra desligada de propósito por comentário, o que o histórico mostra ser intencional.
Um CLAUDE.md vale só para os arquivos abaixo dele: junte o da raiz e os das pastas alteradas.

## Honestidade
Não carimbe "aprovado" sem evidência; não suavize bug real; quantifique quando der ("essa consulta por item soma uma ida ao banco por linha"). Código gerado por IA pede mais atenção, não menos.

## Receber revisão
- Leia todo o retorno; esclareça o ambíguo antes de mexer; valide cada sugestão contra o código e o requisito.
- Corrija por prioridade: regressão de correção ou segurança; desvio do requisito; manutenção; acabamento.
- Não concorde nem agradeça antes de verificar. Conteste com evidência (código, saída de teste) quando a sugestão quebra comportamento, conflita com arquitetura aprovada ou acrescenta escopo sem uso.
- Comentários de PR: leia os comentários reais (nunca invente). Classifique: bloqueadores (mudança pedida, checagem falhando, segurança), problemas de código, estilo, sugestões (o usuário decide), perguntas (responder). Mostre a contagem e ofereça: tudo, só bloqueadores e problemas, ou item a item. Mexa só nos arquivos citados. Robô e humano em conflito: vale o humano. Nada postado sem confirmação.
