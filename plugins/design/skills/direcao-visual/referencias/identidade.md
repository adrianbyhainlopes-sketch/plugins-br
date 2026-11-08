# Identidade visual: BRAND.md e DESIGN.md

## Duas camadas, dois arquivos
- **BRAND.md** guarda o que sobrevive a um redesenho: estratégia, voz e as primitivas visuais (2 a 5 cores aprovadas, famílias tipográficas, direção de arte). Sem tokens e sem escala.
- **DESIGN.md** guarda a aplicação numa superfície (app, slides, documento, redes): escalas, papéis das cores, espaçamento, componentes, movimento e preferências de saída (formato, pasta, tema). Começa com uma linha apontando para a marca (`brand: ../BRAND.md`).
- Pergunte antes de criar qualquer um dos dois. Se o projeto já tem outro lugar para isso, use o dele.
- O BRAND.md pode já existir com estratégia e voz (feito por uma skill de marca de outro plugin). Então acrescente só a seção "Visual", sem tocar no resto, mostrando o que muda e esperando o sim. A voz continua sendo da skill de marca.

## Formato do BRAND.md (parte visual)
- **Cores-núcleo:** cada uma com valor exato (hex), significado e se é obrigatória ou opcional. Nunca o papel de superfície (isso é do DESIGN.md).
- **Tipos:** família, papel (título, texto) e substituto; licença só como "conferida" se foi conferida.
- **Direção de arte:** um território visual concreto ("papel de arquivo, fotografia documental, sem pessoas posando"), não uma lista de adjetivos. Para cada referência, o traço a emprestar e o traço a não copiar.
- **Logotipo:** variantes, respiro, tamanho mínimo, usos proibidos.

## Coleta
- Pesquise só o que falta e pergunte em blocos pequenos, sempre propondo um padrão.
- Nunca invente cor aprovada, licença de fonte nem alegação. Preserve o que o usuário deu: cores confirmadas, nomes, texto exato.
- O que está em aberto entra como "hipótese criativa", não como decisão.

## Logotipo
- Métodos para gerar o símbolo: monograma, ação do produto, fusão de duas metáforas, espaço negativo, geometria de construção. Combine só o que esclarece o conceito e explique a ligação com a marca.
- 1 ou 2 cores; funciona a 16 px e em uma cor; mostre a linha de variações (símbolo, ícone de aplicativo, assinatura horizontal).
- Respiro em unidades da altura da própria marca (por exemplo, metade da altura); tamanho mínimo definido e testado na menor tela.
- Variantes: cor, uma cor escura, uma cor clara, invertida. Nunca esticar, recolorir fora das variantes, girar, pôr efeito ou aplicar sobre foto movimentada sem película.
- Conceito de logo é proposta, não prova de que o nome ou o desenho estão livres para registro. Quem escolhe a direção é o usuário.

## Cor de marca e cor de interface
- Marca: uma primária, um acento e uma ou duas de apoio, para marketing, slides e redes.
- Interface: papéis (fundo, superfície, texto, borda, primária, destrutiva), mapeados a partir da marca: `marca.primária → interface.primária`, com o passo exato.
- O hex da marca não aparece cru no código: passa por um papel.
- Contrato marca para produto, numa tabela: que passo da cor vira o botão principal; onde a cor da marca não vai (texto corrido, erro); como a tipografia da marca vira papéis; como o logotipo vira tokens de respiro e tamanho mínimo.

## Família de produtos
Compartilham logotipo, paleta, tipografia e ícones; diferem no acento de interface (variação dentro da paleta), nos ícones de domínio e na arte de compartilhamento. O produto filho escreve só o que difere; regras herdadas podem apertar, nunca afrouxar; compromissos de acessibilidade sempre herdam.

## Conflito e deriva
Primitiva obrigatória ausente, ou valor diferente com o mesmo significado: aponte, nunca reconcilie em silêncio. Nunca edite o BRAND.md só para o design "passar". Mudou a marca: liste os DESIGN.md afetados sem editá-los.

## Checagem final da identidade
- Teste da troca: com o nome de um concorrente no lugar, as decisões ainda servem? Se sim, estão genéricas.
- Logo a 16 px e em uma cor.
- Cada cor com papel e contraste conferido nos pares usados.
- Fontes com licença conferida ou marcada como "a conferir".
- Uma página de aplicação (um slide, um post, uma tela) feita com a identidade, vista de fato.
