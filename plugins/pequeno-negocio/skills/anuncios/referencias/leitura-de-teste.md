# Leitura de teste de criativo

Ordem: checar os dados → fixar a métrica principal → taxas → diferenças → desenho do teste → veredito por conceito → amostra e dias → diagnóstico de vídeo (se houver) → próximo teste.

## 1. Checar os dados
Se falhar, liste os problemas em vez de apontar vencedor.
- Cliques ≤ impressões; conversões por clique ≤ cliques; visualizações ≤ impressões.
- Mesmo período e mesma janela de atribuição em todas as linhas.
- Linha com zero impressões sai e é listada.
- Coluna que falta vai para "Não checado", com o que ela teria permitido.
- Pergunte se o campo conta eventos únicos ou repetidos (repetidos pedem outro modelo).

## 2. Métrica principal, declarada antes de ler
A do usuário; senão, conversões (contato, mensagem, venda) por impressão. Taxa de clique e retenção de vídeo são guarda-corpos e nunca elegem vencedor sozinhas. Se o usuário escolher taxa de clique, aceite e lembre numa linha que clique não é comprador. **Nunca troque a métrica porque outra mostra diferença maior.**

## 3. Fórmulas
- Taxa = k ÷ n, com intervalo de Wilson de 95%: centro = (p + z² ÷ (2n)) ÷ (1 + z² ÷ n); meia-largura = z × √(p(1 − p) ÷ n + z² ÷ (4n²)) ÷ (1 + z² ÷ n); z = 1,96; limites l = centro − meia-largura e u = centro + meia-largura.
- Diferença contra uma referência nomeada (o controle do usuário, ou o anúncio com mais impressões): intervalo de Newcombe (método 10), que combina os dois intervalos de Wilson: inferior = d − √((p1 − l1)² + (u2 − p2)²); superior = d + √((u1 − p1)² + (p2 − l2)²), com d = p1 − p2.
- p-valor: teste z de duas proporções. Com mais de duas variantes, correção de Holm, ou o rótulo "exploratório".
- Amostra por braço: α de 0,05 bilateral e poder de 80%, n = (1,96 × √(2p̄(1 − p̄)) + 0,8416 × √(p1(1 − p1) + p2(1 − p2)))² ÷ (p1 − p2)², com o menor ganho que importa dado pelo usuário.
- Dias a mais = (n − impressões já feitas) ÷ impressões por dia, arredondado para cima; o braço mais lento define a duração.
- Sem execução de código: imprima os passos intermediários (p, centro, meia-largura) numa seção "Cálculo" para o usuário refazer.

**Linguagem:** "o intervalo exclui zero" só quando exclui; senão, "não resolvido". Os intervalos supõem observações independentes e não corrigem pessoa que viu várias vezes, entrega escolhida pela plataforma nem espiadas repetidas.

## 4. Desenho
Anúncios no mesmo conjunto são **observacionais**: a plataforma escolheu quem viu cada um. Só é randomizado se o usuário disser que usou a ferramenta de teste A/B da plataforma. Diferença observacional é pista, não causa.

## 5. Vereditos
- **Continuar testando:** métrica principal não resolvida, amostra curta.
- **Mudar uma variável:** só um guarda-corpo resolvido num teste randomizado, ou conceito misturado entre formatos.
- **Candidato a desligar:** só com randomização, atribuição madura e limite de perda fixado antes. No observacional: "atrás no observado, confirmar".
- **Provável vencedor:** limite inferior da diferença acima de zero num teste randomizado. No observacional: "na frente: confirmar com teste A/B".
Com poucas conversões, agrupe por conceito antes de julgar.

"Não dá para concluir com esse volume de entrega" é resposta válida, com duas saídas: buscar uma diferença maior (conceitos mais distintos) ou declarar, antes do próximo teste, uma métrica mais cedo no funil.

Espiar o teste e parar quando aparece um vencedor infla falsos vencedores: a amostra ou a data final se fixa antes.

## 6. Verba pequena: leitura por limiar
Quando o n necessário está fora de alcance (é o caso comum de pequeno negócio), troque a comparação estatística por um limiar declarado **antes** de rodar: "o anúncio continua se trouxer ao menos k contatos em N dias com até R$ V". k vem do teto por cliente (`formulas-gerenciais.md`, seção 6) e da taxa de contato que vira cliente do usuário. Ao fim, compare o observado com o limiar e diga que é decisão de negócio, não prova estatística.

## 7. Vídeo
- Retenção inicial = visualizações dos primeiros segundos ÷ impressões; retenção até o fim = visualizações completas ÷ impressões (o nome do campo muda na plataforma; use o que o usuário colar).
- Os dois com intervalo e o rótulo "diagnóstico, não venda", sem faixa de "bom" ou "ruim".

## 8. Sem normas inventadas
Nada de "taxa de clique boa é X". Meta do usuário leva o rótulo "seu benchmark"; o menor ganho que importa se pergunta; sem resposta, cenários rotulados.

## 9. Próximo teste
Uma variação concreta, como hipótese, com o resto fixo. Separe "confirmar a dupla atual com teste A/B" de "testar um criativo novo".
