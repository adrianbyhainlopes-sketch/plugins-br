# Workflows n8n

Esta referência é genérica de propósito: nós, campos e comandos do n8n mudam entre versões. Antes de montar ou mexer, peça a versão da instância de destino (`n8n --version`, a tag da imagem Docker ou a tela "Sobre"). Use só tipos de nó e `typeVersion` que existem nessa versão; na dúvida, confira na documentação oficial do n8n para essa versão, nunca de memória.

## Entrada antes de tudo
- Workflow existente: peça o export em JSON. Ao mexer, mantenha os IDs e nomes dos nós e toda configuração que não tem a ver com o pedido (isso também deixa o diff legível).
- Workflow novo: feche gatilho, exemplo de entrada, saída desejada e as gravações externas antes de montar.

## Travas
- **Credencial fora do JSON.** O export pode trazer nome e ID de credencial: tudo bem, a credencial fica na instância. Num exemplo para compartilhar, tire as ligações de credencial. Nunca peça para o usuário colar chave; nunca ponha chave em nó Code nem cabeçalho `Authorization` escrito no JSON.
- **Entrega desligada.** O JSON sai com `"active": false`. Caminho de webhook de produção e agendamento ficam desligados até o usuário pedir para ativar.
- **Revisar não é executar.** Pedido de revisão autoriza ler o export, não rodar nós Code, chamadas HTTP ou serviços conectados.
- **Sem nó da comunidade, sem serviço novo** sem pedido.

## Desenho (padrões, confira os nomes na versão)
- Gatilho: manual para teste; agendado; webhook (com caminho de teste e de produção separados).
- Dados correm em itens (`$json` é o item atual; `$('Nome do nó')` lê outro nó). Nó que recebe N itens normalmente roda N vezes; quem espera 1 item e recebe 0 não roda o resto do ramo.
- Ramos: IF e Switch para decidir; Merge para juntar (confira o modo); laço em lote para APIs com limite; Wait para esperar; sub-workflow para reaproveitar.
- Binário (PDF, imagem) viaja em `binary`, separado de `json`: o nó que lê o arquivo e o que manda para OCR precisam apontar o mesmo nome de propriedade.

## Erro e repetição
- Workflow de erro (gatilho de erro) que avisa alguém com o nome do workflow, o nó e a execução. Falha silenciosa é o pior caso.
- "Repetir em falha" por nó só em operação que pode repetir sem efeito duplo (leitura, ou escrita com chave de idempotência). Escrita sem chave não se repete às cegas: depois de timeout, consulte o destino antes.
- "Continuar em falha" esconde erro: só com o item com problema indo para um ramo que registra.
- Leia o histórico de execuções para ver a saída real de cada nó; o "sucesso" verde do workflow não diz que os dados estão certos.

## HTTP, paginação e limites
- Paginação: siga a página seguinte até acabar e diga o critério de parada; lista que para na primeira página esconde o resto.
- Limite de taxa: lote menor e espera entre lotes; respeite `Retry-After` em 429.
- Timeout explícito; 4xx não se repete; 5xx e timeout se repetem poucas vezes, com espera crescente.

## Idempotência no n8n
- Deduplicar dentro de um lote (no próprio nó) não é o mesmo que entre execuções: variável ou `Set` de JavaScript some no fim da execução, e a próxima aceita o primeiro evento de novo.
- Entre execuções: chave estável do evento de negócio + unicidade durável no destino (índice único no banco, planilha conferida antes de acrescentar) ou a chave de idempotência da API de destino.
- Nunca chame de "exatamente uma vez" só porque há um nó de deduplicação.

## Testar
- Instância descartável: pasta de usuário e banco próprios, sem credencial de produção. Nunca importe no n8n do usuário nem resete o banco dele para testar.
- Trio mínimo de entrada: um válido, o mesmo de novo (tem de sair como duplicado e não gravar), um inválido (sem ID, valor não numérico: tem de ser recusado e registrado). Escreva a saída esperada antes.
- Pela linha de comando, só na instância descartável: importar e executar pelo ID existem em versões recentes (`n8n import:workflow`, `n8n execute`), mas confira `n8n --help` e `n8n execute --help` na versão de destino antes de usar. Nó Code pode exigir os executores de tarefa (task runners) configurados.
- Efeitos colaterais vão para destino sintético.
- Sem como rodar: entregue o JSON e o procedimento exato de teste, com o rótulo "checado na estrutura, execução não verificada".

## Checagem estrutural (só leitura do JSON)
IDs e nomes de nó únicos; conexões que apontam para nó inexistente; `active`; campos com cara de segredo (`apiKey`, `token`, `Authorization`, `password`) preenchidos; nós Code e expressões lidos à mão. Isso não prova compatibilidade de nó, JavaScript correto nem ausência de segredo.

## Versionar
Exporte o JSON para uma pasta no git a cada mudança, com IDs mantidos (o diff fica legível). Credencial nunca vai junto.

## Entrega
O arquivo do workflow; a versão de destino; as credenciais a ligar (pelo nome); o estado do gatilho (desligado); exemplo de entrada e saída; as checagens que rodaram de verdade; o que ficou em aberto (versão de nó, paginação, repetição, duplicata entre execuções).
