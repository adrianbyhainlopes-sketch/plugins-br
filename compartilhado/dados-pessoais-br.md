# Dados pessoais brasileiros em varredura

Como achar, validar e mascarar identificadores brasileiros em código, arquivo, log e planilha. Conferido em 08/11/2026; as fontes estão no fim. O padrão acha candidatos; quem decide é a leitura do contexto.

## Regras
- Nunca repita o número no relatório: arquivo:linha, o tipo e o espaço reservado (`[CPF]`). Para distinguir dois casos, no máximo os 2 últimos dígitos (`[CPF ..34]`).
- Dígito verificador certo não prova que o documento existe, e errado quase sempre descarta o candidato. Número de 11 dígitos ao acaso passa no teste do CPF cerca de 1 vez em 100 (medido em 200 mil números sintéticos).
- Sintético também passa. Antes de chamar de vazamento, veja onde está: fixture, teste, exemplo ou dado real. Em repositório público, prefira exemplo com dígito propositalmente errado.
- Falso positivo comum: 11 ou 14 dígitos seguidos dentro de hash hexadecimal (sha, lockfile, catálogo): olhe o caractere antes e depois do número. Também caem os formatos de exemplo (`000.000.000-00`, `00.000.000/0000-00`) e e-mail tipo `pacote@hash.json`.
- Documento de pessoa jurídica também pede cuidado: CNPJ de MEI e de empresário individual leva a uma pessoa natural.
- Dado pessoal achado não se "rotaciona". Se saiu para onde não devia, vai para o fluxo de incidente no mesmo dia.

## Tabela de busca
| Dado | Como achar | Como validar | Observação |
|---|---|---|---|
| CPF | `\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b` | dígito verificador (abaixo); recusar os 11 dígitos iguais | fora de formatação, aparece como 11 dígitos colados: exija contexto (`cpf`, `documento`, coluna) ou o DV |
| CNPJ numérico | `\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b` | dígito verificador (abaixo) | os números já emitidos não mudam |
| CNPJ alfanumérico | `\b[0-9A-Z]{2}\.?[0-9A-Z]{3}\.?[0-9A-Z]{3}/?[0-9A-Z]{4}-?\d{2}\b` | dígito verificador (abaixo) | só para inscrições novas, a partir de julho de 2026 (IN RFB 2.229/2024). Sem pontuação, o padrão pega qualquer código em maiúsculas: exija DV e contexto |
| Chave Pix, CPF | `^[0-9]{11}$` | como CPF | sem ponto nem traço |
| Chave Pix, CNPJ | `^[A-Z0-9]{12}[0-9]{2}$` | como CNPJ | já aceita o formato alfanumérico |
| Chave Pix, celular | `^\+[1-9]\d{1,14}$` | formato E.164 | com contexto (`pix`, `chave`); telefone sozinho é só telefone |
| Chave Pix, e-mail | e-mail em minúsculas, até 77 caracteres | formato | com contexto; e-mail sozinho é só e-mail |
| Chave Pix aleatória (EVP) | `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$` | formato de UUID | todo UUID casa: só conta com contexto (`pix`, `chave`, `evp`) |
| PIS, NIS, NIT, Pasep | 11 dígitos perto da palavra `pis`, `nis`, `nit`, `pasep` | a conferir: o cálculo do dígito não foi achado em fonte primária | só por contexto; não afirme "inválido" |
| RG | número perto de `rg`, `identidade`, `órgão emissor` | nenhuma: não há formato nacional único | a Carteira de Identidade Nacional usa o próprio CPF como número |
| Telefone | `(?:\+?55[\s-]?)?\(?\d{2}\)?[\s-]?9?\d{4}[\s-]?\d{4}` | formato | muito falso positivo: use com contexto |
| Agência e conta | números perto de `agência`, `conta`, `ag`, `cc`, `banco` | nenhuma: varia por banco | só por contexto |
| Certificado digital A1 | por nome de arquivo: `*.pfx`, `*.p12` | não abrir | trate como segredo de alto risco: quem tem o arquivo e a senha assina em nome da pessoa ou da empresa. Procure também a senha em script ou `.env` vizinho |

## Dígito verificador
Módulo 11. Testado em 08/11/2026 com o exemplo oficial da Receita (`12.ABC.345/01DE-35`) e, no CPF, comparando as duas formas publicadas em 200 mil bases sintéticas (nenhuma divergência). Rode com `python -I`, num arquivo temporário fora do repositório, e nunca imprima o número.

```python
def _dv(valores, pesos):
    resto = sum(v * p for v, p in zip(valores, pesos)) % 11
    return 0 if resto < 2 else 11 - resto

def cpf_valido(texto):
    d = [c for c in texto if c.isdigit()]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    v = [int(c) for c in d]
    a = _dv(v[:9], range(10, 1, -1))
    b = _dv(v[:9] + [a], range(11, 1, -1))
    return v[9:] == [a, b]

def cnpj_valido(texto):
    c = [x for x in texto.upper() if x.isalnum()]
    if len(c) != 14 or len(set(c)) == 1 or not all(x.isdigit() for x in c[12:]):
        return False
    v = [ord(x) - 48 for x in c]   # '0' a '9' valem 0 a 9; 'A' vale 17, 'B' vale 18
    a = _dv(v[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    b = _dv(v[:12] + [a], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return v[12:] == [a, b]
```

## O que procurar além do número
Nome junto de data de nascimento, endereço, filiação, dado de saúde, placa, foto de documento (`rg_frente.jpg`), planilha com lista de clientes, exportação de banco (`.csv`, `.sql`, `.dump`), e-mails nos commits e log com corpo de requisição.

## Fontes (lidas em 08/11/2026)
- CNPJ alfanumérico: Receita Federal, https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/cnpj-alfanumerico ; manual do DV em https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/documentos-tecnicos/cnpj (o PDF não pôde ser aberto aqui: método e exemplo vieram do trecho indexado e foram conferidos rodando o exemplo).
- Chaves Pix: API do DICT, versão 2.13.0, https://www.bcb.gov.br/content/estabilidadefinanceira/pix/API-DICT.html
- CPF: anexo de regras de validação publicado no portal do SPED (gov.br), módulo 11.
- NIS com 11 dígitos, incluído o dígito verificador: Manual de Orientação do eSocial, https://www.gov.br/esocial/pt-br/documentacao-tecnica/manuais
- Carteira de Identidade Nacional: https://www.gov.br/governodigital/pt-br/identificacao-do-cidadao
