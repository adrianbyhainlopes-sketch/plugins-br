<!-- cópia gerada de compartilhado/receita-pdf-windows.md pelo ferramentas/montar.py; edite a fonte, não esta cópia -->

# Receita: HTML para PDF ou PNG no Windows

Usa o Chrome ou o Edge que já estão no computador, sem janela. Nada é instalado. Testada em 08/11/2026 no Windows 10 com o Edge 157 (o Chrome usa o mesmo motor e as mesmas opções). Para as armadilhas gerais do Windows, veja `windows.md`.

Sem execução (chat sem acesso ao computador): entregue o HTML pronto e diga ao usuário para abrir no Chrome ou no Edge, imprimir (Ctrl+P), escolher "Salvar como PDF", desligar cabeçalhos e rodapés do navegador e ligar os gráficos de fundo (os nomes exatos das opções variam com a versão). O PDF fica "Não verificado" até ele conferir.

## 1. Gerar o PDF
Rode o bloco direto no PowerShell (5.1 ou 7). Troque só a primeira linha.

```powershell
$html = "C:\caminho\do\arquivo.html"
$pdf  = [IO.Path]::ChangeExtension($html, ".pdf")
$navegador = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $navegador) { throw "Nem Chrome nem Edge encontrados." }
$perfil = Join-Path $env:TEMP ("pdf-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory $perfil | Out-Null
$hif = @("$env:LOCALAPPDATA\Google\Chrome\User Data\hyphen-data",
         "$env:LOCALAPPDATA\Microsoft\Edge\User Data\hyphen-data") | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($hif) { Copy-Item -Recurse $hif (Join-Path $perfil "hyphen-data") } else { "Aviso: sem dicionário de hifenização" }
if (Test-Path $pdf) { Remove-Item $pdf }
$argumentos = @("--headless", "--disable-gpu", "--user-data-dir=`"$perfil`"", "--no-pdf-header-footer",
  "--generate-pdf-document-outline", "--print-to-pdf=`"$pdf`"", "`"$(([uri]$html).AbsoluteUri)`"")
$p = Start-Process -FilePath $navegador -ArgumentList $argumentos -PassThru -WindowStyle Hidden
if (-not $p.WaitForExit(90000)) { $p.Kill(); "Aviso: o navegador não terminou em 90 s e foi encerrado" }
Start-Sleep -Milliseconds 500
Remove-Item -Recurse -Force $perfil -ErrorAction SilentlyContinue
if (Test-Path $pdf) { "PDF gerado: $pdf" } else { "O PDF não foi gerado" }
```

Por que cada parte:
- **Perfil temporário próprio** (`--user-data-dir`): não mexe no navegador aberto do usuário nem nos dados dele, e é apagado no fim.
- **`hyphen-data` copiado:** com perfil vazio, `hyphens: auto` não hifeniza nada. A pasta que o navegador já baixou traz o dicionário do português (`hyph-pt.hyb`); copiar é só leitura. Sem ela, não justifique o texto: alinhe à esquerda e diga por quê.
- **`--no-pdf-header-footer`:** sem ele o navegador põe data, título e endereço do arquivo no topo e no pé de cada página, por cima das suas margens.
- **`--generate-pdf-document-outline`:** marcadores no PDF a partir dos títulos (navegação no leitor). Não substitui o sumário impresso.
- **Espera com limite e `Kill` só do processo iniciado aqui:** o navegador às vezes não fecha sozinho; nunca feche "todos os Chrome".
- O console pode mostrar linhas "ERROR" do navegador mesmo quando deu certo. Julgue pelo arquivo gerado.
- Rodado de um `.ps1` chamado por outro `powershell -File`, o bloco terminou sem mensagem no teste. Rode direto.
- Fonte e imagem por caminho relativo funcionam porque o arquivo abre como `file:///`. Nada de fonte ou script pela internet: o PDF tem de sair igual sem rede.

## 2. Gerar PNG (post, carrossel, story, capa)
Mesmo começo (navegador e perfil), trocando os argumentos. Um PNG por slide: o HTML mostra o slide pedido no endereço (`arquivo.html#3`).

```powershell
$largura = 1080; $altura = 1350          # carrossel 4:5; story 1080 x 1920
foreach ($i in 1..$total) {
  $png = Join-Path (Split-Path $html) ("slide-{0:00}.png" -f $i)
  $argumentos = @("--headless", "--disable-gpu", "--user-data-dir=`"$perfil`"", "--hide-scrollbars",
    "--force-device-scale-factor=1", "--window-size=$largura,$altura", "--screenshot=`"$png`"",
    "`"$(([uri]$html).AbsoluteUri)#$i`"")
  $p = Start-Process -FilePath $navegador -ArgumentList $argumentos -PassThru -WindowStyle Hidden
  if (-not $p.WaitForExit(60000)) { $p.Kill() }
}
```

Confira o tamanho de cada PNG (`[Drawing.Image]::FromFile(...)` depois de `Add-Type -AssemblyName System.Drawing`) e abra pelo menos um.

## 3. Sumário com número de página (duas passadas)
O Chrome e o Edge não calculam número de página para o sumário (`target-counter` não funciona). Faça assim:
1. Primeira passada com um marcador no lugar de cada número (`{{p1}}`, `{{p2}}`...).
2. Ache em que página cai cada título (bloco do passo 4, procurando a linha do título só nas páginas depois do sumário, para não achar o próprio sumário nem uma frase do texto).
3. Troque os marcadores pelos números e gere de novo.
4. Confira que os títulos continuam nas mesmas páginas. Se mudou (o sumário cresceu e empurrou o texto), repita os passos 2 e 3.

## 4. Verificar o PDF (sempre, antes de dizer que está pronto)
Um PDF em branco ou cortado também "sai com sucesso". Confira por leitura do arquivo, sem instalar nada:

```powershell
$bruto = [IO.File]::ReadAllText($pdf, [Text.Encoding]::GetEncoding(28591))
"páginas: " + ([regex]::Matches($bruto, '/Type\s*/Page[^s]')).Count
"tamanho em pontos: " + ((([regex]::Matches($bruto, '/MediaBox\s*\[([^\]]+)\]') | ForEach-Object { $_.Groups[1].Value.Trim() }) | Sort-Object -Unique) -join " | ")
"fontes: " + ((([regex]::Matches($bruto, '/FontName\s*/([^\s/>\]]+)') | ForEach-Object { $_.Groups[1].Value }) | Sort-Object -Unique) -join ", ")
"arquivos de fonte embutidos: " + ([regex]::Matches($bruto, '/FontFile[23]?\s')).Count
"idioma: " + ([regex]::Match($bruto, '/Lang\s*\(([^)]*)\)')).Groups[1].Value
```

- **Páginas:** o número esperado (num deck, igual ao de slides).
- **Tamanho:** A4 sai como cerca de 595 × 842 pontos (210 × 297 mm).
- **Fontes:** cada fonte com um arquivo embutido (o prefixo `ABCDEF+` indica subconjunto, normal). Fonte listada sem arquivo embutido depende da máquina de quem abre.
- **Idioma:** `pt-BR` vem do `lang` do HTML e ajuda leitor de tela.
- **Texto:** extraia o texto de cada página e confira o começo e o fim de cada uma, o sumário e o número no pé. Com a skill de PDF ativa, use-a. No Windows com Git, há `pdftotext` em `C:\Program Files\Git\mingw64\bin\`: `& $pdftotext -f 2 -l 2 -layout -enc UTF-8 $pdf -` extrai a página 2; páginas separadas por quebra de página (`` `f ``) dão a contagem.
- **Olhar de fato:** abra o PDF no navegador e veja a primeira página, a última e toda página com figura ou tabela. A contagem pode bater com páginas em branco. Captura de tela de PDF pelo modo sem janela sai em branco: não serve para isso.
- O que não deu para olhar fica em "Não verificado", com o motivo.

## O que funciona e o que não funciona no Chrome e no Edge (testado em 08/11/2026)
| Recurso | Resultado |
|---|---|
| `@page { size: A4; margin: ... }` | funciona |
| Caixas de margem (`@top-left`, `@bottom-center`...) com texto fixo | funciona (desde o Chrome 131) |
| `counter(page)` e `counter(pages)` na margem | funciona ("Página 2 de 5") |
| `@page :first` e páginas nomeadas (`page: abertura`) | funciona: use para tirar cabeçalho da abertura ou mudar o cabeçalho por capítulo |
| `string-set` e `string()` (cabeçalho com o título corrente) | não funciona: use página nomeada por capítulo ou texto fixo |
| `target-counter()` (número de página do sumário) | não funciona: duas passadas (seção 3) |
| `float: footnote` (nota no pé da página) | não funciona: notas no fim do capítulo ou da seção, com link de ida e volta |
| `hyphens: auto` com `lang="pt-BR"` | funciona só com o dicionário no perfil (seção 1) |
| Fonte do sistema ou local (`@font-face` com arquivo ao lado) | é embutida em subconjunto; antes, confira a permissão de embutir da fonte e a licença de uso dela |
