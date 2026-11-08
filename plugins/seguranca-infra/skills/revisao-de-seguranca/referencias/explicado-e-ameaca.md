# Modo explicado e modelo de ameaça

## Modo explicado ("posso pôr na internet?")
Para quem não é especialista. A consequência vem primeiro, em português comum, com o termo técnico entre parênteses. Ordem pelo dano mais frequente em app pequeno:
1. Um estranho lê ou muda dados de outra pessoa?
2. O login é checado no servidor em toda rota?
3. Há chaves no código ou no histórico?
4. O que o usuário digita chega a banco, shell, arquivo ou HTML?
5. Senhas guardadas com hash?
6. Alguém pode aumentar a sua conta (cadastro, e-mail, SMS, IA, upload sem limite)?
7. Algo privado ficou público?
8. O recurso de IA faz o que não deve?
9. Você saberia se algo desse errado?

**Formato:** corrigir antes de alguém usar; corrigir logo; vale fazer um dia (3 ou 4 itens); o que já está bem; o que não deu para checar. Fecha respondendo "posso pôr na internet agora?": sim, não ou sim depois de X. Sem fabricar dúvida quando pode ir.

**Testes que dispensam ler código,** que a própria pessoa faz:
- abrir a URL protegida deslogado;
- duas contas de teste trocando o id na URL;
- procurar "key", "secret" e "token" no código-fonte da página;
- ver na aba de rede se vem mais dado do que a tela mostra.

**Linhas vermelhas (chamar um profissional):** dado de saúde, de criança ou financeiro em volume; pagamento feito pelo próprio app; incidente com dado de terceiros (comunicação à ANPD: ver a skill de segredos); exigência contratual de auditoria. Não é parecer jurídico.

No fim, ofereça de 10 a 20 linhas para o arquivo de regras do projeto (CLAUDE.md), para o erro não voltar. Só escreva com o sim.

## Modelo de ameaça
Uma vez por sistema ou recurso grande: aqui o achado é um controle que nunca foi construído.
1. Pergunte só o que não dá para inferir: o que o sistema faz, ativos em ordem, atores (inclusive os incômodos), realidade da implantação.
2. Diagrama de fluxo com cada travessia de fronteira marcada.
3. STRIDE por elemento.
4. Probabilidade e impacto, com controle existente, lacuna, controle proposto e risco que sobra.
5. Saída: os cinco maiores, riscos aceitos, suposições. Ofereça salvar, perguntando antes.
