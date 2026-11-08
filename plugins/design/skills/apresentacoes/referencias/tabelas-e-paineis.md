# Tabelas e painéis (o que a skill de gráficos não cobre)

O gráfico em si fica com a skill de visualização de dados, se houver. Aqui: quando usar tabela, como montá-la, e como compor um painel de indicadores ou um slide de dado.

## Tabela ou gráfico
- Tabela: consultar valores individuais, comparar números exatos, unidades misturadas, anexo.
- Gráfico: padrão, tendência, comparação de forma.
- Em apresentação ao vivo, tabela só curta (até 4 ou 5 linhas); o resto vai para o anexo ou o material distribuído.

## Montar a tabela
- Itens nas linhas, medidas nas colunas; ordem com sentido (valor decrescente, sequência natural ou a chave de consulta; alfabética só para procurar por nome).
- Números: mesma precisão na coluna; separador de milhar; vírgula decimal (`formatos-br.md`); unidade, R$ e % no cabeçalho, não em cada célula; algarismos tabulares; alinhados à direita, com o cabeçalho também à direita. Texto à esquerda. Nunca centralizado.
- Linhas: espaço primeiro; fio fino e claro só quando o espaço não separa; nunca grade completa; total em negrito com um fio.
- HTML: `<caption>`, `<th scope="col">`; nada de tabela para diagramar.

## Slide de dado
- Título de ação com a conclusão ("Vendas caíram 12% depois do aumento"), não o tema.
- Um número só: texto grande, com o que ele significa e a comparação (meta, período anterior).
- Destaque a série que importa e deixe o resto em cinza.
- Anotação junto do dado, não numa legenda distante.
- Todo número com a fonte do usuário. Peça sem dado real é esquema e diz isso.

## Painel de indicadores
- Uma tela, sem rolagem; se não cabe, divida em visões.
- Passos: quem usa, com que frequência e que decisão apoia; ranqueie as métricas (1 a 3 respondem à pergunta principal, o resto é contexto, cada uma com meta ou limiar); escolha a forma por métrica; arrume (principais no alto à esquerda, apoio no meio, detalhe embaixo); confira cor e contraste; teste dos 5 segundos (dá para dizer a manchete e o que está fora da meta?).
- Formas: número com linha pequena de tendência e variação; barra contra meta com faixas; barra ordenada (horizontal para rótulo longo, base zero); linha com até 3 séries; mapa de calor com escala sequencial e legenda.
- Evite: mostrador de ponteiro (use barra contra meta), pizza, 3D; semáforo só com ícone ou rótulo junto da cor; vermelho de alerta como a única cor viva.
