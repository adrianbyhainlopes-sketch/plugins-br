# Frontend e corrigir a classe

## Trilha de frontend
Portões:
- sem correção sem reprodução;
- sem edição antes de nomear a causa no formato "entrada correta vira saída errada em arquivo:linha porque <suposição que não vale>";
- sem editar código compartilhado antes de listar quem o usa;
- nunca uma flag numa função compartilhada para dois chamadores discordarem: são duas funções.

Localize descendo: página → seção → componente. Mapeie as referências nos dois sentidos (quem importa o arquivo e o que ele importa). Rastreie da tela para o dado: componente → hook → Server Action ou serviço → banco ou HTTP. O bug costuma morar onde se decide, não onde se mostra.

Valor errado sem erro na tela, três perguntas em cada ponto:
- De onde vem o valor (parser, `??`, conversão, `new Date(...)`, `.find()`, cache, atualização otimista)?
- Por que tem esta forma aqui?
- Como cada consumidor o lê? Unidade, forma ou fuso diferentes entre quem grava e quem lê é bug de acoplamento (centavos lidos como reais; data sem hora lida como meia-noite UTC e mostrada como o dia anterior).

Bugs de React costumam vir do momento do estado, das dependências do effect e de closures velhas. Hidratação diferente: algo que muda entre servidor e navegador no render (hora, aleatório, `localStorage`, fuso).

Raio de impacto antes de corrigir: se algum consumidor depende do comportamento quebrado, o código compartilhado era duas coisas: separe.

## Corrigir a classe
1. Reproduza com teste que falha, na camada mais baixa que reproduz de ponta a ponta.
2. Nomeie a classe numa frase que dê para buscar: "status conferido fora da transação e depois gravado"; "marcador de feito gravado antes do trabalho"; "chamada a fornecedor sem tempo limite"; "tela lê `isLoading` e não `isError`"; "data de hoje calculada em UTC".
3. Procure o padrão no escopo (o código coberto, quem lê ou grava os mesmos dados; se o pedido é corrigir esse bug, o repositório inteiro). Buscas típicas: ler e depois gravar sem trava; feito antes da chamada; fetch sem tempo limite; `catch` que devolve `[]` ou `null`; consultas sem limite; `new Date()` onde se quer o fuso do usuário; `toISOString().slice(0, 10)`. Cada achado: mesmo bug, seguro (por quê) ou incerto.
4. Premortem da própria correção (uma trava pode prender o pedido; uma guarda pode bloquear um segundo pagamento legítimo).
5. Corrija os do escopo, cada um com teste que falha antes; os de fora, uma linha "fora desta tarefa" com arquivo:linha, sem editar.
6. Prevenção, da mais forte para a mais fraca: um ajudante que é o único jeito de fazer a coisa; restrição no banco; checagem que falha o CI; invariante registrada; regra no arquivo de instruções ("regra aconselha, checagem obriga").
7. Relatório: Classe, Padrão, Outros achados (n corrigidos, n registrados, n seguros), Prevenção.
