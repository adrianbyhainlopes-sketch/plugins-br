# Contrato com o arquivo de rumo (RUMO.md)

Algumas pessoas mantêm um chat ou sessão "orquestradora" que registra o rumo de todos os projetos num arquivo `RUMO.md`. As skills leem esse arquivo; nunca o escrevem.

## Onde procurar
- No chat: arquivo do Project chamado RUMO.md.
- No Claude Code e no Cowork: o caminho citado no CLAUDE.md ou nas instruções (procure por "RUMO.md").
- Não achou: siga normalmente, sem pedir nem cobrar.

## Quando ler (só três momentos)
1. Ao abrir ou retomar uma sessão de trabalho.
2. Ao registrar uma decisão.
3. Quando um pedido parece contradizer o rumo.

## O que fazer
- Passou da data "revisar em": avise uma vez, numa linha.
- Pedido contra uma decisão vigente: uma linha de aviso citando o id da decisão e uma pergunta. Vale o que o usuário confirmar na hora; a mudança vira proposta.
- Nunca edite o RUMO.md. Mudança vira um bloco para o usuário levar ao orquestrador:

```
Proposta para o RUMO
de: <chat ou sessão>, <AAAA-MM-DD>
frente: <frente>
decisão proposta: <uma frase>
motivo: <até duas linhas>
substitui: <id ou nada>
```

- Se o projeto tiver uma pasta de passagem entre chats (com caixas de entrada e um LEIA-ME), siga as regras dela para entregar a proposta e para receber ordens.

## Formato do RUMO.md (para reconhecer)
Datas "atualizado" e "revisar em"; "Agora" (até 5 linhas); decisões vigentes (id, decisão, desde, substitui, frente); "não fazer ou suspenso"; perguntas abertas; uma linha por frente. Ids são estáveis: decisão superada sai das vigentes e fica citada em "substitui" da nova.
