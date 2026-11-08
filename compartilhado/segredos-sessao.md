# Segredos na sessão

- Não abra `.env`, chave, certificado (`.pfx`, `.pem`) nem cofre de senhas. Para saber quais variáveis existem, leia o `.env.example` ou pergunte o nome, nunca o valor.
- Nunca peça ao usuário para colar chave, token ou senha no chat. A credencial fica onde ela mora (variável de ambiente, cofre, credencial do n8n, painel do provedor) e o código a lê pelo nome.
- Segredo nunca vai em código, commit, log, mensagem de erro, fixture, print de tela, JSON exportado nem prompt para outro serviço. Para depurar, registre só presença ou ausência ("CHAVE_X definida: sim").
- No Next, tudo que começa com `NEXT_PUBLIC_` vai para o navegador: chave secreta nunca leva esse prefixo.
- Se um segredo apareceu onde não devia (commit, log, chat), diga na hora e recomende trocar a chave: apagar do arquivo ou reescrever o histórico não desfaz o vazamento.
