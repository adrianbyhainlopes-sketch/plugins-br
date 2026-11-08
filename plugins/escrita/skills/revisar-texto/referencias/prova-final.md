# Prova final

A prova não melhora o texto: só pega erro. Tudo que exige reescrever vai uma vez para "fora da prova". Mais de cerca de 10 problemas de clareza por mil palavras: "precisa de copidesque antes da prova".

## Cabeçalho (uma linha)
Modo (só a final, ou aprovada mais final), tipo de texto, contagem exata de palavras. Mudanças que o usuário disse que fez viram MP1, MP2… e são esperadas na comparação.

## Doze passadas separadas
Uma leitura combinada deixa escapar. Faça uma passada por categoria:
1. Ortografia e digitação.
2. Gramática e concordância.
3. Pontuação e espaçamento (aspas e parênteses sem par, espaço duplo, espaço antes de pontuação).
4. Confusáveis (`confusaveis-pt.md`).
5. Palavra dobrada ou faltando.
6. Números: contagem declarada contra itens listados ("três motivos" e quatro na lista), porcentagens que deviam somar 100, somas, intervalos, unidades.
7. Datas: dia da semana contra a data, data impossível (31/04), formatos misturados.
8. Nome ou termo grafado de dois jeitos.
9. Referências internas: numeração de lista, níveis de título, "ver seção 3", "acima" e "abaixo", notas.
10. Link cujo texto não diz o destino.
11. Marcadores esquecidos: TODO, XX, colchetes de espaço reservado, campos `{{ }}`, os próprios `[FALTA]`.
12. Detritos de revisão: frase duplicada depois de inserção, menção a algo removido, tempo verbal quebrado no ponto de inserção, sobra de chat ou de Markdown.

**Contagem zero:** as doze linhas aparecem sempre, inclusive "9. referências internas: 0". Linha faltando quer dizer passada não feita.

## Bloqueadores (qualquer um leva a Segurar)
- Marcador esquecido.
- Mudança inesperada em item travado.
- Números que não batem.
- Dia da semana errado ou data impossível.
- Possível negação faltando ou sobrando.
- Detrito visível ao leitor ou instrução embutida.

Campo de mala direta intencional (`{{nome}}`) não é erro, mas exige confirmação de que será preenchido. Sem bloqueador: **Liberar após n correções**. Os bloqueadores são nomeados na linha do veredito.

## Comparar a versão aprovada com a final
- Alinhe por parágrafo, depois por frase, e compare palavra a palavra (por código quando houver).
- Cada diferença: texto aprovado, texto final, tipo (inserção, remoção, troca, movimento) e classe (esperada; inesperada; adição inesperada a confirmar).
- Mudança inesperada em valor travado é bloqueador, e também a remoção inesperada de frase com condição ou limite.
- Armadilhas: número mudado num lugar e não na repetição; data movida com o dia da semana antigo; frase removida e ainda citada adiante.

## Saída
1. **Veredito:** Liberar após n correções, ou Segurar (com os bloqueadores).
2. Tabela de achados: `# · passada · onde (parágrafo.frase) · trecho · correção ou pergunta · Corrigir, Perguntar ou Deixar`.
3. As doze contagens.
4. O texto corrigido, só com as correções.
5. Perguntas.
6. Tabela de versões, se houve comparação.
7. Decisões de estilo não aplicadas e a linha do orçamento.
