# pytest e Vitest

## pytest
1. Nome que explica a falha: `test_<verbo>_<expectativa>_<cenario>` (`test_recusa_cnpj_com_digito_errado`).
2. Docstring só quando o nome não carrega o motivo de negócio (exigência legal, invariante, pegadinha). Nunca repita o nome.
3. Sem número mágico de domínio: constante nomeada; `pytest.approx` para float; `is None`, não `== None`. Código HTTP em teste de rota pode ficar literal.
4. Teste autocontido: sem estado mutável compartilhado, sem depender da ordem; limpeza em fixture com `yield`. Confira rodando só ele e depois a suíte.
5. Comportamento pela interface pública: nunca método privado, nunca asserção sobre a sequência de chamadas internas.
6. Mock só na fronteira (cliente HTTP, SDK, driver de banco, fila, relógio quando o tempo é regra), aplicado onde o nome é usado (`mocker.patch("meu_modulo.requests.get")`).
- Arrange, Act, Assert; uma preocupação por teste (vários asserts sobre um mesmo resultado tudo bem).
- `pytest.raises(Erro, match="...")` em vez de try/except.
- `tmp_path` para arquivos; `parametrize` para tabela de casos; marcadores `slow` e `integration` para rodar à parte.
- Argumento padrão mutável no código testado: o certo é `if itens is None: itens = []` (o `itens or []` troca também uma lista vazia passada de propósito).
- `conftest.py` só para fixture usada por vários módulos; escopo de fixture é contrato (`function` por padrão).

## Vitest e Testing Library
- Testes "sociáveis": mock só do que você não controla (rede, timers, sistema de arquivos, SDK de terceiro). Setup visível no teste ou numa fábrica chamada explicitamente, não espalhado em três `beforeEach`.
- `describe` com o nome da unidade (até dois níveis); `it` como afirmação no presente, começando por verbo; arquivo `.test.ts(x)` ao lado do fonte.
- Consulta por papel, depois rótulo, texto, alt e, por último, `testId`; nunca por classe CSS. `userEvent.setup()` em vez de `fireEvent`.
- Assíncrono: sempre `await`; `findBy*` para o que aparece, `waitForElementToBeRemoved` para o que some, `await expect(p).rejects.toThrow()` para promessa rejeitada.
- `vi.mock` é içado para o topo do arquivo: a fábrica não enxerga variável declarada fora dela. `vi.mocked(obj)` para tipar o mock (confirmado na doc do Vitest em 08/11/2026). O nome do tipo exportado para mocks varia entre versões: confira no `node_modules/vitest` instalado antes de importar.
- `vi.spyOn` não intercepta chamada interna dentro do mesmo módulo.
- `clearMocks` e `restoreMocks` na configuração; timers falsos restaurados no `afterEach`; `vi.setSystemTime` para datas; `advanceTimersByTimeAsync` quando timer e promessa se misturam.
- Sem `as any` em teste: fábricas tipadas `criarUsuario(sobrescritas)`.
- Componente que busca dado: três testes (carregando com promessa que nunca resolve, sucesso, erro). MSW com `onUnhandledRequest: 'error'` e `server.use` por teste para simular falha.
- Snapshot só pequeno e sempre junto de uma asserção explícita.
