<!-- cópia gerada de compartilhado/evidencia-numerica.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Regras de evidência numérica

Valem para toda conta feita com números do usuário: margem, preço, caixa, conciliação, relatório. A conta é dele; a skill só mostra o caminho.

## O que entra na conta
- Só número que o usuário deu ou que está no arquivo dele. Custo, taxa, alíquota, demanda, prazo ou tratamento fiscal que ninguém deu fica **desconhecido**, nunca estimado.
- Com algo desconhecido, o resultado é **parcial**, e o rótulo diz o que falta. A parte que dá para calcular é entregue mesmo assim.
- Falta que muda a conta: marcador `[DETALHE NECESSÁRIO: o quê]` ou uma pergunta só. Falta que não muda: siga e diga numa linha.
- Taxa real do usuário vence taxa publicada, média de mercado ou "típica". Nunca troque uma pela outra. Benchmark só entra se o usuário der, com o rótulo "seu benchmark".
- Regra fiscal ou legal (alíquota, limite, prazo) vem do arquivo de dados com vigência e fonte, consultado pela data do fato. Sem linha vigente, o valor é desconhecido.
- **Repasse não é receita.** Dinheiro que só passa pela empresa (repasse a parceiro, imposto retido, valor de terceiro) não entra como receita dela.

## Sinais e denominadores
- Entenda o que positivo e negativo significam em cada relatório. Ou subtraia valores positivos, ou some com o sinal original; nunca subtraia um negativo. Mostre o valor original ao lado.
- Toda proporção tem o denominador nomeado ("margem sobre a receita líquida").
- Denominador zero ou negativo: mostre o valor e deixe a razão indefinida.
- Moedas e períodos diferentes ficam separados, salvo taxa ou regra de conversão dada pelo usuário.
- Cada custo entra numa categoria só. Sobreposição incerta entre duas fontes fica em aberto, dita.

## Fechamento
- **Não force o fechamento.** Se os lados não batem, a diferença aparece com o valor, nunca vai para um "ajuste" sem nome.
- **Valor igual não prova casamento.** Dois lançamentos com o mesmo valor só casam com outro elemento em comum (data, documento, descrição).
- **O resto fica à vista:** o que não foi explicado ou casado é listado, com valor e quantidade.
- Identidades que precisam fechar são conferidas e o resultado é dito: início + entradas − saídas = fim; soma das partes = total; efeito volume + efeito preço = variação.

## Como mostrar a conta
- Uma linha por passo que decide: fórmula, números do usuário, resultado.
- Arredonde só no fim e diga a regra (duas casas, para cima). Quando houver execução de código, use aritmética decimal (no Python, `decimal.Decimal`), não ponto flutuante.
- Sem execução de código, a conta aparece passo a passo para o usuário refazer. Diga "conta feita à mão, confira".
- Suposição (janela de 12 meses, preço sem desconto) é dita como suposição, numa linha, e trocada pelo dado real quando ele vier.
