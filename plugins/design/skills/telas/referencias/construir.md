# Construir telas que funcionam

## Estados: toda tela com dados tem seis
1. **Ideal:** dados normais.
2. **Vazio:** com o tipo certo (abaixo).
3. **Carregando:** pelo tempo (abaixo).
4. **Erro:** com ação de recuperação e o que o usuário digitou preservado.
5. **Excesso:** título longo, mil itens, tela pequena, sem esconder ações.
6. **Dependência fora do ar** (pagamento, mapa, login de terceiro): mensagem própria com caminho adiante, nunca o erro cru do fornecedor.

### Vazio
- **Primeiro uso:** título dizendo o que mora ali, uma frase de valor, botão de criar ou importar.
- **Filtrado:** "nada corresponde aos filtros", sugestão e "Limpar filtros", que zera tudo num clique.
- **Sem permissão:** por que, sem culpar, e "Pedir acesso"; nunca mostrar Criar a quem não pode.
- **Concluído:** comemorar breve e sugerir o próximo.
- Contagem zero sem filtro = primeiro uso; com filtro = filtrado. Mesma área do conteúdo cheio (tabela mantém o cabeçalho), para nada pular. Nunca um "Sem dados" seco.

### Carregando
- Até 100 ms: nenhum indicador.
- De 100 ms a 1 s: indicador no próprio controle ("Salvando...", `aria-busy`).
- Acima de 1 s, num bloco de conteúdo: esqueleto com a forma final, um por contêiner.
- Acima de 5 s: esqueleto e dica de progresso, ou carga em etapas.
- Espere 100 ms antes de mostrar qualquer indicador e cancele se a resposta chegar. Spinner de tela cheia só na primeira carga do app ou em operação que o usuário pediu, com cancelar. Nada pula de lugar quando o dado chega.

## Formulários
- Por campo: intocado, tocado, válido, inválido. Nada de erro enquanto se digita num campo intocado; valida ao sair do campo; depois disso, revalida ao digitar.
- O erro fica até a primeira tecla que corrige; não some ao receber o foco.
- Enviar não fica desabilitado para validar: no clique incompleto, marque todos os campos, leve o foco ao primeiro inválido e, com 3 erros ou mais, anuncie "3 campos precisam de atenção" num `role="alert"`. Durante o envio, trave o segundo clique ("Salvando...").
- Mensagem começa pela correção ("Digite um e-mail como nome@dominio.com.br"), uma por campo, ao lado do campo, no lugar da ajuda.
- Menos campos: nome completo num campo só; CEP preenche cidade e UF (com o usuário podendo corrigir); sem "confirme o e-mail"; opcional coletado depois.
- `autocomplete` e teclado certos: `name`, `email`, `tel`, `postal-code`, `street-address`, `current-password`, `new-password`, `one-time-code`; `inputmode="numeric"` para CPF, CNPJ, CEP e código.
- **Formatos do Brasil** (`formatos-br.md`): CPF, CNPJ, CEP e telefone são texto, com zeros à esquerda; máscara que não briga com o cursor e aceita colar com ou sem pontuação; normalize ao sair do campo. Valor em reais: guarde o número, mostre `R$ 1.234,56`, aceite vírgula decimal ao digitar. Data `dd/mm/aaaa` ou seletor. Telefone com DDD. Nome com vários sobrenomes e partículas ("da", "dos").
- Teclado: Enter envia campo de uma linha; Ctrl+Enter em área de texto; Esc cancela edição em linha.
- Erro do servidor cai no mesmo lugar do erro local, preservando tudo.

## Fluxo e navegador
- Botão parece botão, link parece link. Ícone sozinho só para o universal.
- Toda ação responde em até 100 ms; acima de 1 s, progresso. A localização atual fica marcada.
- Ação destrutiva: reversível executa e oferece desfazer; irreversível pede confirmação (`escala-e-medidas.md`). Nunca ao lado da principal com o mesmo peso.
- O que escreve na URL lê de volta: endereço colado abre a mesma tela; Voltar volta um passo. Roteiro: três passos, Voltar duas vezes, Avançar; abrir o endereço em aba nova.
- Fluxo completo: saída que não perde nada e um fim que diz o que aconteceu e onde está o resultado.
- Nunca resolver problema de uso tirando capacidade. Se precisa de tutorial, o achado é simplificar a função.

## Estresse de conteúdo
- Comprimento: nomes de 1 a mais de 60 caracteres, e-mail longo, número de documento que o usuário copia.
- Valores: de R$ 0,01 a R$ 999 milhões; contagens abreviadas ("12,4 mil").
- Imagem faltando, na proporção errada, enorme ou carregando.
- Vazio, um caractere, só espaços, emoji.
- CSS: `min-width: 0` no filho de grid ou flex para poder truncar; `overflow-wrap: anywhere` em nome; reticências com o texto inteiro acessível; coluna numérica com largura do pior caso e `tabular-nums`; avatar com iniciais de reserva.
- Larguras: 320 sem rolagem horizontal; 375, 768 e 1280; acima de 1440 respeitando a largura máxima. Teste: `document.documentElement.scrollWidth <= document.documentElement.clientWidth`.

## Layout
- Modelos com a ordem das seções: painel (números, gráficos, atividade); detalhe (cabeçalho, números, abas, barra de ação); lista (filtros, tabela ou cards, paginação; cards no celular, tabela no computador); formulário (grupos, campos, barra de ação fixa; uma coluna); configurações (navegação lateral e painel; abas no celular); vazio (centralizado).
- Navegação: barra lateral no computador; só ícones no tablet; 3 a 5 abas embaixo e menu de excesso no celular.
- No celular nada some, tudo muda de lugar: o secundário vai para seção recolhível, o terciário para "Mais".
- Limite a página, não o app: só o conteúdo principal leva largura máxima.
- Hover é extra: toda ação existe sem hover; efeitos de hover dentro de `@media (hover: hover)`.

## Movimento
- Antes de animar, dois portões: **frequência** (o que se usa dezenas ou centenas de vezes por dia não anima; atalho de teclado nunca anima) e **propósito** numa palavra (retorno, posição, estado, continuidade). Sem propósito, não anima.
- Curvas: entrar e sair com desaceleração (`ease-out`); mover na tela com `ease-in-out`; `ease-in` em interface é achado.
- Durações: pressão de botão 100 a 160 ms; dica 125 a 200 ms; menu 150 a 250 ms; modal e gaveta 200 a 500 ms; o resto abaixo de 300 ms.
- Só `transform` e `opacity`; nunca começar de `scale(0)` (comece em 0,95 com opacidade 0); nunca `transition: all`.
- Movimento reduzido: menos e mais suave, não zero; significado nunca só no movimento ("Salvo" escrito, não só um brilho).

## Dashboard dentro do app
Uma tela, sem rolagem; 1 a 3 números principais, cada um com meta ou limiar; o resto é contexto. Barra contra meta em vez de mostrador; sem pizza nem 3D; alerta vermelho como a única cor viva.
