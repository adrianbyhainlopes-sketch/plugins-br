# Lentes de revisão

Use só a lente pedida ou a que o diff pede. Cada achado vai no formato de `achados.md`.

## 1. Código que mente ao usuário
Pergunta: "o usuário vê algo que não é verdade?". Dois quadros, de preferência em dois subagentes separados (juntos num prompt só, os dois pioram):
- **Caminho de erro:** `catch` que engole, fallback que esconde falha, "registra e segue" quando o chamador não consegue seguir certo, promessa rejeitada sem tratamento, aviso de sucesso com resposta 5xx, "copiado" quando a área de transferência falhou, lista vazia no lugar de erro de carga.
- **Caminho feliz falso:** `onClick` vazio, dado fixo na rota, retorno de mentira, componente que ignora a prop, ação que não avisa o servidor, TODO antigo em algo entregue.
Gravidade: Alto quando o usuário acha que deu certo e não deu (bloqueia a entrega); Médio para risco real que hoje não mente; Baixo para cosmético. Nunca rebaixe um Alto por conta própria. Superfície que o usuário diz ser limpa de propósito entra como "intencional", com nota, nunca some.

## 2. Testes adulterados
Pergunta: "se o comportamento quebrasse agora, algum teste acusaria?". Quem revisa não participou da mudança e só lê. Compare os testes antes e depois, tomando como base o ponto em que o ramo saiu da linha principal (assim entra o que já foi commitado e o que ainda não foi), e leia por inteiro os arquivos de teste que o git ainda não rastreia.
- **Teste antigo que ficou fácil de passar:** valor esperado mudou sem o requisito mudar; comparação exata virou "contém", "não é nulo" ou "não lançou erro"; caso removido, ignorado ou comentado; duas funções de teste com o mesmo nome no mesmo arquivo (em Python, a última definição apaga a primeira sem aviso); esperado transferido para um arquivo auxiliar alterado na mesma mudança.
- **Teste novo que não prova nada:** continuaria passando com a versão anterior do código; calcula o esperado com a própria função testada; usa como esperado uma saída copiada da execução; olha detalhe interno em vez de comportamento.
- **O tipo da mudança define o que é suspeito:** numa refatoração o comportamento não muda, então teste alterado precisa de motivo; numa mudança só de testes, código de produção alterado precisa de motivo.
- Explicação em commit ou comentário é a versão de quem fez a mudança; prova é o teste falhar quando o código está errado.
- Resultado: sem problemas, N problemas, ou não deu para revisar (e por quê). Cada problema nomeia o erro que deixaria de ser detectado.

## 3. Refatoração em massa (codemod)
Compilar e passar no lint não prova que se comporta igual (exemplo: `||` virou `??` e o preço 0 deixou de cair no valor padrão).
- Caracterize a ferramenta (AST ou texto; texto = mais risco) e a regra em palavras; auditar a regra acha o furo mais rápido que ler 300 diffs.
- Armadilhas de equivalência: precedência sem parênteses; verdadeiro/falso contra nulo; `async/await` contra `then` mudando a propagação de erro; `return await` trocado por `return` dentro de `try` (a rejeição deixa de ser capturada ali); referência contra cópia; import com efeito colateral diferente; mudança "só de tipo" que muda o runtime (enum para const); regex que casou dentro de texto ou comentário; reformatação no mesmo commit escondendo lógica.
- Casos perdidos: alias, reexportação, import dinâmico, testes, `.mdx`; busque o padrão VELHO (sobreviventes = duas convenções vivas, pior que nenhuma).
- Os testes passam pelos caminhos transformados? Codemod sobre código sem teste é "não verificado". Rastreie à mão autenticação, dinheiro e mutação de dados.

## 4. Fronteira servidor e cliente (Next)
- O HTML do servidor e o primeiro render do cliente usam os mesmos dados (nada de `Date.now()`, `Math.random()` ou `localStorage` no render de componente que roda no servidor).
- O que vai serializado ao cliente (props de Client Component, retorno de Server Action, closure de action) só expõe o que a identidade da requisição pode ver. Retorno de action é o mínimo que a tela precisa, nunca o registro inteiro do banco.
- Toda mutação no servidor valida a entrada e confere dono e permissão com identidade confiável (sessão conferida, não campo do formulário).
- Depois da mutação, a tela e o cache concordam (invalidação certa: `updateTag`, `revalidateTag(tag, perfil)`, `revalidatePath`, `refresh()`; conferir na versão instalada).
- Carregando, erro, navegação e nova tentativa continuam usáveis e não criam efeito duplicado.
- Hidratação só se prova em navegador real; console limpo com conteúdo faltando não é aprovação. Nunca "consertar" suprimindo o aviso ou desligando o SSR; nunca mover segredo para o bundle para resolver erro de import.
- Prioridade: P0 exposição de dado de outro usuário ou mutação não autorizada; P1 render, navegação ou mutação quebrados; P2 inconsistência limitada.

## 5. Contratos e consultas
- **Deriva de contrato:** para cada entidade, compare os tipos do cliente, do servidor (handlers, esquemas Zod) e do banco (migrações, tipos gerados): nomes de campo; tipo (data como `Date` ou texto ISO; `bigint` tipado como `number`); opcional e nulo; valores de enum; objeto aninhado ou só o ID. Confirme com `tsc --noEmit`, sem instalar nada. Três níveis: quebra em execução, arriscado, cosmético.
- **N+1, seis formas:** laço com consulta; relação carregada sob demanda; serializador que consulta por item; `Promise.all` com uma consulta por linha ("N em paralelo continua N"); chamada a outro serviço em laço; formatador ou log que consulta escondido. No Supabase, `.from()` dentro de `map`, resolvido com o relacionamento no `select`. Ignore laço só em memória e script pontual; não proponha reescrita de arquitetura.
