# Recursos com IA, agentes e MCP próprio

**Premissa:** prompt não é fronteira de segurança. Qualquer conteúdo que chega ao contexto pode dirigir o modelo: documento recuperado, página, resultado de ferramenta, nome de arquivo, PDF, texto em imagem, e-mail. A pergunta é: se o atacante controlasse toda a saída do modelo, o que conseguiria? Delimitadores e "ignore instruções do documento" são endurecimento, nunca controle.

## Dez regras
1. A identidade do modelo não é a do usuário: cada chamada de ferramenta confere autorização como uma requisição HTTP desse usuário, tirado da sessão.
2. Autoridade mínima por ferramenta: cinco específicas em vez de uma genérica. SQL arbitrário é comprometimento esperando um documento envenenado.
3. O par de exfiltração: ler dado privado e ter qualquer canal para fora (fetch, e-mail, webhook, escrever em documento, imagem markdown com dado na URL) no mesmo agente já é achado.
4. Ação irreversível ou cara passa por um humano que vê a ação concreta (destinatário, valor, arquivo), não o resumo do modelo.
5. Saída do modelo é entrada não confiável: sanitize HTML e markdown, bloqueie `javascript:`, `data:` e imagem remota, parametrize, valide JSON por esquema, nunca decida acesso por ela.
6. Isole clientes na busca vetorial dentro da consulta.
7. Limite o laço (iterações, chamadas, tokens, tempo e gasto por requisição e por usuário) e registre cada chamada.
8. Sandbox para executar código: sem rede ou com lista, sem montagens, sem credenciais, descartável.
9. Nada de segredo, dado de outro cliente ou dado pessoal desnecessário no contexto. Suponha que o prompt de sistema pode ser extraído. Prompt em log é dado pessoal.
10. Cadeia de suprimentos: fixe a versão do modelo e revise servidores MCP antes de liberar (a descrição da ferramenta entra direto no contexto).

**Antes de lançar,** complete a frase: "se um atacante controla a saída deste modelo, ele consegue ___". Se termina em dado de outros, dinheiro ou execução de código, mude a arquitetura, não o prompt.

## Acréscimos para app web
Chave do provedor de IA só no servidor, atrás de uma rota própria. `max_tokens`, limite por usuário e teto de custo. Histórico com escopo por usuário. Ferramenta de leitura roda sozinha; de escrita pede confirmação, gera registro e tem parâmetros validados por lista. Modere antes de indexar. Streaming com autenticação e tempo limite.

## Teste no CI
Cargas pequenas contra os prompts e ferramentas reais: instrução escondida num documento; resultado de ferramenta mandando chamar outra; nome de arquivo com instrução; pedido para gerar imagem markdown com dado na URL.

## MCP próprio
Planeje as ferramentas a partir das perguntas reais, não uma por tabela. Comece só com leitura. Cada consulta com um cliente criado com o token do usuário, sob RLS, nunca com a chave secreta. Escrita uma por vez, dizendo o que muda. Olhe campo por campo: nomes e telefones de terceiros se escondem nos registros. O redirect `next` do login só aceita caminho do próprio site (começa com `/`, não com `//`, sem barra invertida). Armadilha: o proxy de login redireciona o cliente de IA, que recebe HTML em vez de 401.
