# Python no Windows para automação

## Esqueleto de um script que roda de novo sem estragar
```python
"""O que faz, em uma frase. Entrada: <pasta ou arquivo>. Saída: <arquivo>. Efeitos: <o que grava>."""
import argparse, csv, logging, sys
from pathlib import Path

def principal(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("entrada", type=Path)
    p.add_argument("saida", type=Path)
    p.add_argument("--valer", action="store_true", help="grava de verdade; sem isto, só ensaia")
    a = p.parse_args(argv)
    ...  # ler, decidir, e só então gravar se a.valer
    return 0 if sem_falhas else 1

if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
```
- Ensaio por padrão; gravar exige a flag (`--valer`, `--executar`). O contrário (gravar por padrão, `--dry-run` opcional) é aceitável se o projeto já usa assim; diga qual.
- Separe as fases: ler e validar tudo, decidir o que fazer, executar os efeitos. Validação depois do primeiro efeito deixa trabalho pela metade.
- Código de saída diferente de 0 quando algo falhou, para o agendador e quem chama perceberem.
- `pathlib.Path` em vez de juntar texto; caminho com espaço e acento funciona sem aspas dentro do Python, mas precisa de aspas na linha de comando.
- Rode com `python -I` quando o script lê arquivos de fora (o `-I` isola de módulos da pasta atual).

## Texto e encoding
- Sempre `encoding=` explícito ao abrir: `utf-8` por padrão; `utf-8-sig` para CSV que vai para o Excel (sem o BOM, o Excel mostra "Ã§"); arquivo vindo de sistema ou portal antigo pode estar em `cp1252` ou `latin-1`.
- Arquivo de encoding desconhecido: tente `utf-8` com `errors="strict"`; se falhar, `cp1252`; diga qual funcionou. Nunca `errors="ignore"` em dado (some letra sem aviso).
- CSV: `newline=""` ao abrir para o módulo `csv`; separador `;` é comum em planilha brasileira (o Excel em português usa `;` porque a vírgula é decimal). Confira olhando o arquivo, não supondo.
- Texto vindo do macOS ou de alguns PDFs chega decomposto (acento separado da letra): normalize com `unicodedata.normalize("NFC", s)` antes de comparar. Compare nomes com `casefold()`.
- Console mostrando caractere estranho é quase sempre o console. Confira lendo o arquivo gerado.

## Pastas e arquivos
- Liste com ordem estável (`sorted(pasta.glob("*.pdf"))`); a ordem do sistema de arquivos não é garantida.
- Filtre o que não é seu: `~$planilha.xlsx` (arquivo de trava do Office aberto), `Thumbs.db`, `desktop.ini`, arquivos ocultos, a própria pasta de saída se estiver dentro da de entrada (senão o script lê o que acabou de escrever).
- Arquivo aberto no Excel fica travado: o erro de permissão vira "falhou: arquivo aberto em outro programa", não queda do script.
- Pasta sincronizada (OneDrive, Google Drive) pode duplicar arquivo como "nome (1).pdf" e travar durante a escrita. Escreva fora e copie no fim, se der problema, e trate "(1)" como possível duplicata, não como arquivo novo.
- Gravar com segurança: escreva em `saida.tmp` na mesma pasta e troque no fim com `Path.replace()`; se o script cair no meio, a saída antiga continua inteira.
- Nunca apague nem mova a entrada. Se o fluxo pede "mover para processados", isso é efeito: entra no ensaio e no log.

## Planilhas
- `openpyxl` lê e escreve `.xlsx` preservando o arquivo; `pandas` é bom para transformar, mas reescreve o arquivo inteiro (perde formatação, fórmula e abas que você não leu).
- Fórmula: `openpyxl` lê a fórmula, não o valor, a menos que abra com `data_only=True` (e aí lê o último valor salvo pelo Excel, que pode estar velho). Diga qual dos dois usou.
- Identificador como texto: ao ler, force a coluna para texto (`dtype=str` no pandas) para CPF, CNPJ, CEP e conta não perderem zero à esquerda. Ao escrever, formato de célula texto.
- Datas: o Excel guarda número de dias; `openpyxl` converte para `datetime` quando a célula tem formato de data. Data digitada como texto ("05/11/2026") continua texto: converta explicitamente como dia/mês/ano.
- Valores: célula pode trazer `float` (1234.5) ou texto ("1.234,50"). Converta para `Decimal` pelo texto (`dinheiro-e-datas-no-codigo.md`).

## PDF e OCR
- PDF com texto (gerado por sistema): extraia o texto direto; é exato. PDF escaneado (imagem): precisa de OCR, que erra.
- Para saber qual é: tente extrair texto; página sem texto ou com lixo é imagem.
- OCR em português: Tesseract com o pacote de idioma `por` (confira se está instalado: `tesseract --list-langs`). Instalar o Tesseract ou o idioma é decisão do usuário (winget ou instalador oficial, versão fixa).
- OCR erra de forma previsível: `0` e `O`, `1`, `l` e `I`, `5` e `S`, vírgula e ponto, cedilha. Todo número lido por OCR passa por uma conferência (soma que fecha, dígito verificador, formato esperado) antes de virar dado. O que não fecha vai para revisão humana, marcado, não para a planilha final.
- Guarde a origem de cada valor (arquivo e página) para o usuário conferir.
- Biblioteca de PDF: confira a licença antes de propor (há bibliotecas populares com licença AGPL, que obriga o projeto inteiro a seguir a mesma licença se for distribuído).

## Log legível para quem não programa
- Uma linha por item: `[PROCESSADO] nota_123.pdf -> 14 linhas`, `[PULADO] nota_123.pdf (já processado em 2026-11-05)`, `[FALHOU] nota_124.pdf: página 2 sem texto`.
- No fim, o resumo: quantos processados, pulados e falhados, e onde está a saída.
- Log em arquivo com data no nome (`log-2026-11-08.txt`), em UTF-8, sem dado pessoal por inteiro (mascare CPF e conta).
- Em ensaio, o log começa com "ENSAIO: nada foi gravado".

## Ambiente
- Use o ambiente do projeto (`.venv`, `uv`, `requirements.txt`): não instale pacote global. Pacote novo só com o sim do usuário, conferido no registro (nome certo, versão fixa).
- Python 3.9+ tem `zoneinfo`; no Windows ele precisa do pacote `tzdata`.
- Agendar no Windows é o Agendador de Tarefas: o script roda com outro diretório atual e outro usuário; use caminhos absolutos e grave o log num lugar conhecido.
