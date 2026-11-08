# CLAUDE.md e Instruções de Projeto

Conferido na documentação oficial em 08/11/2026.

## O que entra
Só o que o agente não descobre, do mais ao menos importante:
1. comandos exatos de build, teste e lint;
2. ambiente não óbvio (variáveis, serviços, onde ficam os segredos, pelo nome);
3. restrições que quebram algo se violadas ("nunca editar `generated/`, é sobrescrito");
4. padrões que diferem do normal só neste projeto.

Fica de fora: visão geral, árvore de pastas, resumo de arquitetura (só a restrição que causa erro), o que repete README ou `package.json`, boas práticas genéricas, histórico.

Regra concreta o bastante para conferir: "indentação de 2 espaços", e não "formate bem". Meta da documentação: menos de 200 linhas por arquivo; rascunho novo costuma caber em muito menos.

Processo: ler as configurações; achar o que o agente erraria sem aviso; perguntar só o que o repositório não responde; filtrar linha a linha ("dá para descobrir lendo o código? corta"); apresentar dizendo, em uma frase por seção, por que ela sobreviveu.

Antes de auditar a fundo, o Claude Code tem `/doctor prompt-audit` (v2.1.283 ou mais nova) e o `/init`, que cria o arquivo. Use o que eles dão e complemente.

## Como o Claude Code carrega
- Da raiz do disco até a pasta de trabalho, tudo é somado, nada sobrepõe. O mais perto da pasta é lido por último. `CLAUDE.local.md` vem depois do `CLAUDE.md` do mesmo nível.
- Subpastas: sob demanda, quando se lê, grava ou edita um arquivo ali.
- `AGENTS.md`: lido só se não há CLAUDE.md nem `CLAUDE.local.md` na pasta ou acima (padrão; v2.1.277 ou mais nova). Para usar os dois, `@AGENTS.md` no CLAUDE.md.
- Comentário HTML em bloco sai antes de chegar ao modelo: serve para nota de manutenção.
- O conteúdo chega como mensagem de usuário depois do prompt de sistema.

## `@import`
- Sintaxe `@caminho/arquivo`, fora de crase e de bloco de código. Relativo ao arquivo que importa. Até quatro saltos.
- Caminho com espaço: barra invertida antes de cada espaço. Caminho entre aspas **não importa**.
- Import para fora da pasta do projeto pede aprovação uma vez; se recusada, fica desligado sem novo aviso.
- **Import não economiza contexto:** carrega junto. Quem economiza é regra com `paths:` ou skill.

## Regras em `.claude/rules/`
Sem `paths`, carrega sempre. Com `paths`, ao ler, gravar ou editar arquivo do padrão. `paths` é o único campo lido. YAML inválido: o arquivo carrega como se não tivesse `paths`, e a restrição some sem aviso (`claude --debug` mostra). Padrão relativo à pasta que contém o `.claude`.

## Encolher um CLAUDE.md grande
Classifique cada seção: essencial (toda sessão), referência (às vezes), redundante. Tabela `seção | linhas | categoria | destino | motivo`, e só execute com o sim. Extraia literalmente, sem resumir, para arquivos com nome de assunto. No lugar da seção, uma sinopse curta com o concreto e o link. Não mova o que se usa em mais da metade das sessões. Valide: linhas antes e depois, diff do extraído sem perda, links funcionando. Na dúvida, fica.

Na cascata (global, projeto, pasta), cada nível só acrescenta o que é dele. Classifique o que encontrar: manter, mover, afiar, remover, aplicar em outro lugar (hook, lint, teste) ou decisão bloqueada (pergunte).

## Ponteiro para o rumo
Se o usuário mantém um `RUMO.md` (`contrato-rumo.md`), o CLAUDE.md e as Instruções de Projeto levam uma linha só: onde está e quando ler. Teste antes e depois: uma sessão nova sabe onde ler sem ser avisada?

## Instruções de Projeto (chat)
- Colar em "Set project instructions": valem em todas as conversas do Projeto.
- Curtas, com as mesmas regras acima: comportamento nas instruções; material nos arquivos do Projeto (base de conhecimento). Nome e descrição do Projeto não chegam ao Claude.
- Uma conversa não enxerga outra: o que precisa ser comum vai para os arquivos.
- A skill entrega o texto final num bloco para colar, e diz onde. Não há como testar por aqui: o teste é o antes e depois em duas conversas novas, feito pelo usuário.

Entrevista, se não há nada escrito: uma pergunta por vez, com opções, sem perguntar o que o chat já respondeu. Cada correção do usuário vira uma regra curta.
