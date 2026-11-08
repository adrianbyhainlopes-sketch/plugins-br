<!-- cópia gerada de compartilhado/windows.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Windows e PowerShell

Armadilhas que se repetem quando o Claude roda comando num Windows. Valem para qualquer skill que gere arquivo, rode script ou chame programa.

## Shell
- Há dois shells possíveis: o PowerShell (5.1, que vem com o Windows, ou 7) e o Git Bash. O Git Bash não é Linux: caminho vira `/c/Users/...`, alguns programas não existem e `/tmp` não é a pasta temporária do Windows.
- No PowerShell 5.1 não existem `&&`, `||`, `?:` nem `??`. Para "rodar B só se A deu certo": `A; if ($?) { B }`.
- Rode o bloco de comandos direto no PowerShell. Salvar como `.ps1` pode esbarrar na política de execução, e chamar um `.ps1` por outro `powershell -File` pode terminar sem mensagem.
- No Claude Code, a ferramenta PowerShell e a ferramenta Bash são caminhos diferentes: uma regra ou permissão escrita para `Bash` não cobre o que passa pela PowerShell.
- Programa nativo que escreve no fluxo de erro (navegador, compilador) pode ser dado como falha no 5.1 se o erro for redirecionado com `2>&1`. Julgue pelo código de saída e pelo arquivo gerado, não pela cor da linha.

## Caminhos e nomes
- `python`, não `python3`. Rode script com `python -I` quando ele ler arquivo de fora.
- Caminho com espaço ou acento sempre entre aspas: `"C:\Users\Nome Sobrenome\Documentos\relatório.html"`.
- Para virar endereço de navegador: `([uri]"C:\caminho\arquivo.html").AbsoluteUri` (troca espaço por `%20` e acerta as barras).
- Pasta temporária: `$env:TEMP` com nome único (`[guid]::NewGuid()`), nunca um caminho fixo; apague no fim só o que você criou.
- Pasta sincronizada na nuvem (OneDrive, Google Drive) pode travar ou duplicar arquivo enquanto ele é escrito. Gere o arquivo fora e copie no fim, se der problema.

## Texto e codificação
- Arquivo de texto novo em UTF-8. No PowerShell 5.1, `Set-Content` e `Add-Content` gravam na página de código do sistema: use `-Encoding utf8` ou `[IO.File]::WriteAllText(caminho, texto, (New-Object Text.UTF8Encoding($false)))`.
- Planilha ou CSV que vai para o Excel: `utf-8-sig` (com BOM), senão os acentos quebram. Arquivo antigo do Windows pode estar em `cp1252`.
- Console mostrando "Ã§" no lugar de "ç" é quase sempre o console, não o arquivo. Confira lendo o arquivo, não a tela.

## Programas e processos
- Instalar só com o sim do usuário, por `winget` ou `scoop`, com versão fixa. Nunca `curl ... | sh` nem script baixado na hora.
- Docker Desktop usa WSL2: fim de linha CRLF quebra `entrypoint.sh`, e caminho do Windows precisa de tradução.
- Pare só o processo que você iniciou (guarde o objeto de `Start-Process -PassThru` e encerre por ele). Nunca `taskkill /IM chrome.exe`: fecha o navegador do usuário.
