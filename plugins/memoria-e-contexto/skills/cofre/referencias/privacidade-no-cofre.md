# Privacidade no cofre

Vale para o que o Claude escreve (resumo, conceito, resposta gravada). O material bruto que o usuário trouxe fica como está. Padrões, dígito verificador e máscara: `dados-pessoais-br.md`. Bases legais, direitos e incidente: `dados/lgpd.md`.

## Três níveis
| Nível | O quê | O que fazer |
|---|---|---|
| Sempre remover | chave de API, senha, token, chave privada, conexão de banco com usuário e senha, credencial de nuvem | fora do texto; `[segredo removido]` |
| Remover por padrão | CPF, CNPJ de pessoa física (MEI, empresário individual), RG, PIS, agência e conta, chave Pix, e-mail não público, telefone, IP interno, caminho com nome de usuário | espaço reservado (`[CPF]`, `[user]`) |
| Só sinalizar | URL interna, nome junto de dado sensível | marca e pergunta |

Não filtre: informação pública, identificador técnico (porta, versão, nome de chave sem valor), espaço reservado. CNPJ de empresa, se a nota é sobre a empresa, é informação pública; o de pessoa natural, não.

Registre quantos itens saíram e de qual fonte, sem repetir o valor. Usuário pediu para não filtrar: respeite e marque a página como privada (`visibilidade: privada`). Página derivada com remoção do primeiro nível fica privada.

## Nunca abrir
`.env*`, `*.pfx`, `*.p12`, `*.key`, `*.pem` e nomes com chave, senha, segredo, token, credencial, contrato, holerite. Um link para eles já é achado: só confira se o caminho existe. `.pfx` inclui o certificado digital A1.

## Dados de terceiros
Cofre pessoal não é cadastro. Não crie ficha de pessoa com trivialidade. Cliente ou funcionário só o necessário para o trabalho, e pelo papel quando bastar. Material sob sigilo não entra em cofre nenhum.

Publicar um trecho do cofre é outra operação: passe a varredura antes de ele sair da pasta, e nunca publique do cofre direto.

Regra sobre condição pessoal: escreva pelo efeito, sem citar a condição.
