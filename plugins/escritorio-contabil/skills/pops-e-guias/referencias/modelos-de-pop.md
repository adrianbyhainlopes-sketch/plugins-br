# Modelos de POP

Dois modelos: **padrão** (até 5 passos, um dono de ponta a ponta, poucos casos de borda) e **detalhado** (6 ou mais passos, ramificações, várias equipes ou ferramentas, processo crítico ou executado por agente).

## Modelo padrão
```markdown
# POP: nome do processo
**Objetivo:** o risco concreto que este POP evita.
**Escopo:** onde se aplica e exceções explícitas.
**Dono:** papel ou pessoa.
**Dispara quando:** evento ou data.
**Periodicidade:** mensal, por competência, sob demanda.

## Entradas
Nomes exatos de arquivos, acessos (só onde pedir) e decisões.

## Procedimento
1. Verbo no imperativo. Resultado esperado: o que se vê quando deu certo.

## Saídas
O que existe, observável, quando termina.

## Definição de pronto
- [ ] item checável isoladamente

## Erros comuns
| Erro | Impacto | Como evitar ou corrigir |
|---|---|---|

## Histórico
| Data | Autor | Mudança |
|---|---|---|
```

## Modelo detalhado
O padrão, mais: inventário de sistemas (portal, sistema contábil, pasta); variáveis por empresa (regime, CNPJ por referência, pasta); ramificações (se X, vá ao passo N); controles de qualidade (quem confere e o quê); escalonamento (quando chamar quem); conformidade (obrigação legal, com o id da linha do arquivo de dados); capturas de tela com legenda; para agente, comandos e verificação por máquina.

## Exemplos de escritório para os erros comuns
- Baixar o extrato do mês errado: conferir o período no cabeçalho antes de salvar.
- Importar o mesmo arquivo duas vezes: comparar o hash com o histórico.
- Portal mudar o caminho do menu: registrar data da captura e pedir atualização ao dono.

## Atualizar
Leia o POP atual, pergunte o que mudou, acrescente uma linha no histórico e suba a versão. Não reescreva linhas antigas do histórico.

## Auditoria
Para cada POP da pasta (menos os modelos), confira: seções obrigatórias; texto de modelo restante (colchetes e data-modelo); dono nomeado; passos no imperativo; data real no histórico; erros comuns preenchidos; senha ou token escritos (bloqueio).

Saída: `Arquivo | Seções faltando | Texto de modelo | Dono | Última atualização | Situação`, com oferta de corrigir um por vez. Liste o que foi lido e o que não abriu.
