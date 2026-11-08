# Lint e frescor

Varredura completa antes de qualquer conserto. Base: índice e as últimas 10 entradas do log. Rode comandos só de leitura e conte por comando.

## O que olhar
**Estrutura:** órfãs (veja antes os campos de relação nas propriedades); páginas fora do índice; links quebrados; maiúscula diferente da do disco (404 no GitHub e no Linux); propriedades sem os campos do esquema ou em YAML inválido; esboços (menos de 3 linhas); cópias de conflito de sincronização (`Conflicted copy`, `nome (1).md`); nomes repetidos.

**Conteúdo:** contradições marcadas e implícitas (estas só quando claras e relevantes); trechos desatualizados e se uma fonte nova os resolve; consultas com resposta substancial não arquivadas; lacunas de conceito (link para página inexistente, conceito citado em 3 ou mais páginas sem página própria); panorama velho (3 ou mais ingestões desde a última atualização); links de mão única; entidades duplicadas.

**Frescor em duas classes** (limiares de partida, ajuste ao cofre):
- Velha e ativa: 90 dias ou mais sem atualização, mas o tema aparece nas últimas entradas do log ou num projeto ativo. Prioridade alta: o cofre está mentindo sobre o trabalho atual.
- Velha e dormente: 180 dias ou mais. Proponha, página a página: atualizar, manter como arquivo (com nota datada) ou depreciar.

Frescor é decisão do usuário. Idade sozinha não condena página.

Menos de 10 páginas: pule consultas não arquivadas e panorama.

## Relatório fixo
Estrutura, conteúdo, resumo (N problemas, N automáticos, N pedem você), em Alta, Média e Baixa, um achado por linha: página, problema, conserto. Cofre limpo: uma linha, sem seções vazias.

Quatro opções para o usuário: consertar o automático e mostrar o resto; um a um; só uma categoria; só o relatório.

## Conserto seguro (depois do sim)
Entrada no índice com resumo de uma linha; esboço para alvo de link quebrado claro; campos de propriedades inferidos, marcados como inferidos; órfã ligada às 2 ou 3 páginas mais relevantes; erro de digitação óbvio em link; link para fora da raiz vira aviso. Alvo incerto: nomeie; nunca invente o arquivo. Índice existente não se sobrescreve. Depois do conserto, rode de novo a checagem afetada.

Não corrija o que o usuário escreveu como dele; o lint trata do que o Claude produziu e da estrutura.

## Decisão do usuário, sempre com opções
- Contradição: atualizar, marcar, deixar.
- Desatualizado: atualizar com a fonte, marcar, pular.
- Lacuna: criar agora, pôr na lista "a criar", pular.
- Consulta não arquivada: refazer e arquivar, pular.

Duas listas no fim: "consertado" e "precisa da sua decisão".

## Log do lint
Encontrados, automáticos por tipo, resolvidos com o usuário, adiados, contradições pendentes, próximo lint sugerido.

## Regras
Nunca resolver contradição sozinho. Nunca apagar (depreciar e tirar do índice). Não ingerir durante o lint. Nunca tocar na pasta bruta. Ferramenta que baixa e executa pacote (`npx`, `pipx run`) não entra: faça com leitura e busca.
