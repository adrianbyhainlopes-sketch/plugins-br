# Auditoria da memória em 10 critérios

Só leitura. Nada é corrigido, movido ou apagado: o resultado é um relatório e uma proposta. Sem script: leitura, busca e contagem por comando. Comece pelos fatos medidos, depois julgue.

## Primeiro, medir (por comando, nunca a olho)
- Linhas e bytes do índice (`(Get-Content MEMORY.md -Encoding UTF8).Count` e `(Get-Item MEMORY.md).Length` no PowerShell; `wc -lc` no Bash). Limite de carga: 200 linhas ou 25 KB, o que vier primeiro (Claude Code, conferido em 08/11/2026). O que passar disso fica invisível no início da sessão.
- Linha do índice sem arquivo; arquivo sem linha no índice (invisível). Link quebrado entre memórias.
- Cópias de conflito de sincronização: `nome (1).md`, `conflicted copy`, `MEMORY-<máquina>.md`.
- Arquivos grandes (cerca de 10 KB, heurística da fonte).
- Linhas do índice maiores que o resto, e o que têm de volátil (versão, "atual", contagem, data recente).

Abra cada arquivo citado no veredito; não julgue pelo nome. Não abra `.env`, chave nem certificado: um ponteiro para eles já é achado (só confira se o caminho existe).

## Os 10 critérios
Um ponto cada; 0,5 se parcial; N/A se não dá para ver (a nota é reescalonada e o N/A é dito). Cada nota com evidência: `arquivo:linha` ou contagem.

| # | Critério | Como conferir |
|---|---|---|
| 1 | Global universal e curto | CLAUDE.md global sem projeto, caminho, stack ou tarefa |
| 2 | Raiz só com regras e ponteiros | CLAUDE.md do projeto sem histórico nem "como fazer"; abaixo de 200 linhas |
| 3 | Regras locais só onde há invariante | regras e CLAUDE.md de pasta não repetem o que o código mostra |
| 4 | Índice dentro do orçamento e sem órfãos | medições acima; toda linha tem arquivo e vice-versa |
| 5 | Memórias bem formadas | um fato, tipo, Por quê e Como aplicar onde cabe, datas absolutas |
| 6 | Registros, direção única e questões fechadas | não há duas "direção atual"; decisão substituída tem rastro; opção rejeitada registrada |
| 7 | Ponteiros resolvem e há portão que roda | cada caminho citado existe; algo confere isso, ou está dito que nada confere |
| 8 | Autoridade e estado declarados | dá para saber o que vale e o que é histórico |
| 9 | O caro tem bloqueio | a regra que não pode falhar está em hook, permissão ou CI, não só em texto |
| 10 | Privado e versionado conferidos | nada privado em arquivo versionado; segredo fora de memória e de índice |

Ao aplicar o 7, confira de fato. Caminho, arquivo ou comando citado numa memória que não existe mais é o achado mais comum e o mais barato de provar. Citação relativa ("ontem", "mês que vem", "semana passada"): sem data absoluta, é falha do critério 5.

## Relatório
1. **Em três linhas:** saúde, maior problema, nota (x de y, N/A ditos).
2. **Medições:** tabela com comando e resultado.
3. **Os 10 critérios:** tabela `# | nota | evidência | conserto`.
4. **Proposta por arquivo:** tabela `arquivo | ação (apagar, arquivar, destilar, corrigir, manter) | motivo | conserto seguro ou decisão sua`, com a versão nova de cada linha mexida, exatamente como ficaria. Fato duvidoso vira pergunta, não correção.
5. **As 3 correções de maior valor**, com o custo de cada. Se a correção custa mais do que a falha, pule e diga.
6. **Não verificado:** o que não deu para conferir e o que resolveria.

Termine perguntando o que aplicar. Daí em diante, siga `poda.md`.

Repositório pequeno pode ficar em 7 sem drama. Nota não é meta: é um jeito de achar o que dói.
