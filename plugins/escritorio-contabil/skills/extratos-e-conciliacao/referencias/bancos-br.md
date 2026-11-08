# Formatos de banco

`bancos-br/*.json` descreve como ler um layout. Os modelos que vêm no plugin são **famílias genéricas**: nenhum foi validado com extrato real de um banco específico, e a prova sempre é o saldo.

| Arquivo | Família |
|---|---|
| `dc-por-linha.json` | valor com sufixo D ou C e saldo na mesma linha |
| `sinal-por-linha.json` | negativo com menos antes ou depois, saldo na mesma linha |
| `saldo-por-dia.json` | saldo só em marcadores de fim de dia |
| `csv-duas-colunas.json` | CSV com colunas de crédito e débito |

## Formato de um banco validado
Depois que um extrato fechar pelo saldo, salve um arquivo com o nome `banco-produto-periodo.json` numa pasta sua (o plugin não guarda formato de cliente) e registre a data e quantos extratos fecharam.

## Campos
| Campo | Para quê |
|---|---|
| `id`, `descricao`, `status` | identificação; diga se foi validado e com quantos extratos |
| `tipo` | `texto` (saída do pdftotext) ou `csv` |
| `linha` | expressão regular com os grupos `data`, `descricao`, `valor`, `dc`, `saldo`, `saldo_dc`, `ref`; ou `credito` e `debito` em duas colunas |
| `sinal` | `dc`, `sinal` ou `colunas` |
| `formato_data` | `%d/%m/%Y`; data só com dia e mês exige `--ano` |
| `saldo_inicial`, `saldo_final`, `saldo_dia` | expressões com o grupo `valor` e o opcional `dc` |
| `ignorar` | linhas de ruído por texto exato: cabeçalho repetido, numeração, nome do titular em forma genérica, texto legal |
| `linha_sem_valor` | linha com data e descrição e sem valor, para juntar com o valor da linha de baixo |
| `continuacao` | junta linhas de descrição sem data e sem valor à linha anterior |
| `ordem` | `crescente` ou `decrescente` |
| `colunas`, `delimitador` | só em CSV: nome exato de cada coluna |

## Criar formato novo
1. Veja o texto como o programa vê (o modo do `pdftotext` que deixou as colunas na mesma linha), páginas 1 e 2.
2. Copie o modelo mais parecido para outro nome e ajuste.
3. Marque por tentativa curta: rode, leia as linhas "não reconhecidas" e as quebras.
4. Pronto quando os saldos batem, não quando saem linhas.

Regra de separador: o último separador de um valor com duas casas decide. Número de documento ou operação é referência, não descrição.

**Nunca deixe dado do extrato de exemplo no formato:** nome do titular, razão social, número de conta, CPF, CNPJ, período ou datas do arquivo. Além da privacidade, literal do exemplo é a causa mais comum de formato que só funciona com o arquivo que o criou.

## Pistas por tipo de movimento
Histórico com PIX, TED, boleto, tarifa, débito automático ou maquininha descreve a natureza, mas o texto muda de banco para banco. Não classifique só pelo nome do intermediador; a classificação segue `classificar.md`.
