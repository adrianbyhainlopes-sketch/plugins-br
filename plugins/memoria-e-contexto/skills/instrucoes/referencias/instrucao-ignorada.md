# Instrução que parece ignorada

Conferido na documentação oficial em 08/11/2026. Separe três coisas: **descoberta** (o arquivo existe e está no lugar), **carregada** (entrou no contexto) e **seguida** (o modelo obedeceu). Nome na pasta prova presença; carga não prova obediência.

## Descoberta
- Está num lugar que carrega nesta sessão? (`claude-md-e-projeto.md`)
- `.claude/CLAUDE.md` ou `./CLAUDE.md`, nunca `~/.claude.json`, que é outro arquivo.
- Pacote colado pode estar incompleto: arquivo ausente num trecho colado não prova ausência no disco.
- Skill: precisa estar em pasta com `SKILL.md`. Hook: sob a chave `hooks` de um settings; não há arquivo de hook avulso para projeto ou usuário.

## Carregada
Peça ao usuário `/context all` e olhe "Memory files". `/memory` lista os arquivos e abre a pasta da memória automática.
- CLAUDE.md de subpasta não aparece nesse quadro: carrega sob demanda. Peça para ler um arquivo ali e veja a linha `Loaded`.
- Regra com `paths` só entra depois que o arquivo é tocado; YAML inválido derruba a restrição.
- Depois de `/compact`, regras de pasta e com `paths` podem não ter voltado.
- Arquivo grande carregado sob demanda vem cortado (40 mil caracteres em janela de 200 mil; 150 mil em janela de 1 milhão nos modelos mais novos).
- Hook de `InstructionsLoaded` registra o que carregou, quando e por quê (`load_reason`): útil para regra com `paths` e subpasta.
- Subagentes: os agentes nativos de exploração e planejamento não leem o CLAUDE.md; agente próprio lê, salvo `omitClaudeMd`. Regra crítica vai no pedido de delegação ou no corpo do agente.
- `claude --safe-mode` desliga personalizações: sumiu o problema, a causa está nelas.

## Seguida
Carregou e não seguiu:
- **Vaga?** Interpretável de dois jeitos: reescreva concreta.
- **Longa?** Regra afogada no meio de arquivo grande perde atenção.
- **Contraditória?** Dois arquivos com orientação diferente: o modelo pode escolher qualquer um. "Vale a mais funda" não é regra do Claude Code. Cite as duas instruções, e a situação em comum, e distinga: exceção intencional, ferramenta diferente, referência velha, falha de carga ou política não decidida.
- **Concorre com o que o próprio Claude Code acrescenta?** Commit e PR têm instrução nativa: `includeGitInstructions` e `attribution` resolvem.
- **Tem de valer sempre?** Não é caso de CLAUDE.md: hook ou permissão.

## Conserto
Comece pelo pedido. Política indecisa: conserto incontestável mais **uma** pergunta exata. Trocar comando velho só com o substituto comprovado. Preserve todo, algum, só, nunca, exceções e incertezas. Fato que falta: `[DETALHE NECESSÁRIO: ...]`.

Depois: referência velha saiu, escopo e restrições ficaram. E não afirme conserto de comportamento a partir de checagem de documento: rode o teste antes e depois, ou diga "não testado".

## No chat
Instruções de Projeto carregam em toda conversa do Projeto; conversa de fora não as vê. Regra dita numa conversa não passa para outra. Conferir: abra conversa nova no Projeto e pergunte o que as instruções dizem; depois teste com um pedido real.
