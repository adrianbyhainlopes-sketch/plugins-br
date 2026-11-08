# Dinheiro, datas e identificadores brasileiros no código

Complementa `formatos-br.md` (que trata da exibição). Aqui é como guardar, calcular e comparar.

## Dinheiro
- Nunca `float` para dinheiro. Python: `decimal.Decimal` criado de texto (`Decimal("10.50")`, nunca `Decimal(10.5)`). TypeScript e banco: inteiro em centavos (`valor_centavos`) ou `numeric(14,2)` no Postgres; nunca `real` ou `double precision`.
- Unidade no nome: `valor_centavos`, `preco_reais`, `duracao_min`.
- Arredondamento é decisão escrita: diga a regra (meio para cima, `ROUND_HALF_UP`, ou meio para o par, `ROUND_HALF_EVEN`, que é o padrão do `decimal` do Python) e onde ela acontece (uma vez, no fim, ou por linha). Soma de valores arredondados por linha pode não bater com o total arredondado: diga qual dos dois vale.
- Ler texto brasileiro: "1.234,56" vira `Decimal("1234.56")` tirando o ponto de milhar e trocando a vírgula. Confira antes se o arquivo não usa o padrão americano: "1,234.56" lido do jeito brasileiro vira 1,23456.
- Crédito e débito: guarde o sinal ou a natureza (D/C) explicitamente; nunca deduza pelo texto da descrição.

## Datas
- Data sem hora (vencimento, competência, emissão) é data, não instante: `datetime.date` em Python, `date` no Postgres, texto `AAAA-MM-DD` em JSON. Nunca guarde como meia-noite UTC: vira o dia anterior no horário de Brasília.
- Competência é mês: guarde como `AAAA-MM` ou como o primeiro dia do mês, e diga qual.
- Instante (quando algo aconteceu): `timestamptz` no Postgres, UTC por dentro, ISO 8601 com offset na troca entre sistemas.
- "Hoje" é no fuso do negócio: `datetime.now(ZoneInfo("America/Sao_Paulo")).date()` em Python. Em JavaScript, `new Date().toISOString().slice(0, 10)` dá a data em UTC, que à noite já é amanhã: use `Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' })` ou a biblioteca do projeto.
- Fuso pelo nome IANA (`America/Sao_Paulo`), nunca offset fixo (`-03:00`): a regra de horário de verão muda por decisão de governo. No Windows, o Python precisa do pacote `tzdata` para o `zoneinfo` funcionar.
- Duração e timeout pelo relógio monotônico (`time.monotonic()` em Python, `performance.now()` em JS), não pela diferença entre dois `now()`.
- Agendamento: diga o fuso do agendador. Cron em hora local dispara duas vezes ou nenhuma na troca de horário, onde houver.
- Prazo em dias úteis depende de calendário de feriados (nacional, estadual, municipal): sem a tabela, diga "dias corridos" ou peça o calendário. Não invente feriado.

## Identificadores
- CPF, CNPJ, CEP, telefone, número de nota, de conta e de processo são texto: guarde com zeros à esquerda, compare normalizado (só dígitos, ou só os caracteres válidos) e nunca converta para número. Planilha que abriu e virou `1,23E+13` já perdeu dígitos: volte ao arquivo original.
- Validar na borda (parse uma vez, devolvendo um tipo próprio) e confiar no núcleo. Dígito verificador de CPF e CNPJ: confira a regra na Receita Federal antes de escrever, porque o CNPJ está passando a aceitar letras.
- Em log, mensagem de erro e fixture: identificador mascarado ou sintético, nunca o real.
