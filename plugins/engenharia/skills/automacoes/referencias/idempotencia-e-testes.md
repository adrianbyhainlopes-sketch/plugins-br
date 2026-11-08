# Idempotência e testes de automação

## Por que duplica
Automação roda mais de uma vez: alguém roda de novo depois de um erro, o agendador repete, o provedor reenvia o evento, a pasta ganha um arquivo novo e o script relê os antigos. Duplicação é o normal se nada impede, não um acidente.

Causas típicas, em ordem de frequência:
1. **Acrescenta sem conferir:** abre a saída em modo de acréscimo (`"a"`, `append`, `INSERT`) e grava tudo o que leu, inclusive o que já estava lá.
2. **Relê tudo:** processa a pasta inteira a cada execução, sem saber o que já foi feito.
3. **Marcador na hora errada:** marca "processado" antes de gravar (cai no meio e o item some para sempre) ou depois de enviar (cai entre enviar e marcar e envia de novo).
4. **Chave instável:** usa como identidade algo que muda (nome do arquivo renomeado, ordem da linha, data de modificação, hora da execução).
5. **Memória que não dura:** deduplica num `set` ou variável que some quando o processo termina; a próxima execução começa do zero.

## Mecanismos, do mais forte para o mais fraco
- **Saída reconstruída do zero:** a cada execução, gera a saída inteira a partir das entradas e substitui a antiga (escrevendo ao lado e trocando no fim). Mais simples e mais seguro quando a saída é um arquivo que o script domina inteiro.
- **Chave única + conferir antes de gravar:** cada item tem uma identidade estável (hash do conteúdo do arquivo, número da nota, ID do evento); a saída guarda a chave; gravar é "se a chave não existe". No banco, `UNIQUE` + `ON CONFLICT DO NOTHING` (ou `DO UPDATE`).
- **Marcador junto com o efeito:** registro de processados gravado na mesma operação que o efeito (mesma transação; mesmo arquivo trocado de uma vez). Efeito fora do seu controle (e-mail, cobrança, API) precisa da chave de idempotência do destino, ou de estado `processando`/`feito` com retomada.
- **Mover para "processados":** funciona, mas é efeito destrutivo sobre a entrada; só com o sim do usuário e com log.

Para cada efeito, escreva: efeito, chave, mecanismo, o que acontece se cair no meio.

## Chave estável
- Arquivo: hash do conteúdo (`hashlib.sha256(caminho.read_bytes()).hexdigest()`) vence nome e data. Mesmo arquivo com nome "(1)" tem o mesmo hash.
- Linha de dado: a combinação de campos que identifica o fato (número da nota + emitente; data + valor + documento), escolhida com o usuário. Duas linhas iguais de verdade (duas compras iguais no mesmo dia) quebram a chave: pergunte como distinguir.
- Evento: o ID do evento que o provedor manda, nunca a hora de chegada.

## Modo de ensaio
- Mostra a lista do que faria: "gravaria 14 linhas novas em saida.csv; pularia 3 já existentes; moveria 0 arquivos".
- Não toca em nada: nem cria pasta, nem trava arquivo, nem chama serviço.
- O mesmo código decide nos dois modos; só a execução dos efeitos muda. Ensaio com caminho de código separado não prova nada.

## Testes
Rode o script, de verdade, sobre uma pasta sintética numa pasta temporária de nome único (nunca a pasta real):
1. **Primeira execução:** a saída bate com a esperada, escrita antes de rodar.
2. **Segunda execução, mesma entrada:** nada novo (0 gravados, N pulados); a saída é idêntica byte a byte à da primeira.
3. **Entrada nova:** só o item novo entra.
4. **Duplicata disfarçada:** o mesmo arquivo com outro nome (`nota (1).pdf`) não entra de novo, se a chave for o conteúdo.
5. **Item ruim:** arquivo vazio, corrompido ou com encoding errado aparece como "falhou" no log, os outros continuam, e o código de saída é diferente de 0.
6. **Queda no meio** (quando o efeito importa): interrompa depois do primeiro item e rode de novo; nada duplicado, nada perdido.

Com pytest:
- `tmp_path` para a pasta de teste; arquivos de entrada pequenos em `tests/fixtures/`, com a saída esperada gravada ao lado.
- O teste que reproduz o bug vem primeiro e tem de falhar no código atual pelo motivo certo (a contagem de linhas, não um erro de import). Só então a correção.
- Valor esperado escrito à mão a partir da entrada, nunca copiado da saída do próprio script.
- OCR: fixture com o texto que o OCR devolve (não a imagem), mais um caso com os erros típicos (`0`/`O`, vírgula/ponto) para provar que a conferência pega.

Sem pytest no projeto: um script de teste curto que monta a pasta, roda duas vezes, compara e sai com código 1 se algo não bater. Diga que não é a suíte do projeto.

## O que dizer no fim
"Rodei duas vezes sobre a pasta de teste: 1ª gravou 6, 2ª gravou 0 e pulou 6; saída idêntica (comparada por hash)." Sem execução: "checado lendo o código; execução não verificada", e o comando exato para o usuário rodar.
