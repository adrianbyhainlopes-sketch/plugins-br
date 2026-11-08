# Acessibilidade: LBI, eMAG e a ponte com a WCAG 2.2

Arquivo de dados com vigência e fonte. Cada item tem o mesmo cabeçalho; o texto da regra é paráfrase, não transcrição. Para decidir um caso, abra a fonte do item.

Como usar:
- Consulte pela **data do fato**. Só vale item "vigente" naquela data; "anunciado" não é "vigente"; "a conferir" não sustenta conclusão.
- Item com `conferido_em` mais velho que 6 meses: avise uma vez e siga.
- Se houver uma cópia mais nova deste arquivo (nos arquivos do Project, na pasta de trabalho ou na camada pessoal), use a de `conferido_em` mais recente e diga qual usou.
- A skill aponta o que a regra pede e o que falta na peça; não dá parecer jurídico. Dúvida sobre obrigação legal de um caso concreto vai para quem responde juridicamente.
- A WCAG é norma técnica internacional, não lei brasileira. A ligação entre ela e a lei está nos itens marcados "ponte", que são leitura de método, não regra.

Lido em 08/11/2026. Fontes:
- [LBI] Lei 13.146/2015 (Lei Brasileira de Inclusão), texto no Planalto: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
- [eMAG] Modelo de Acessibilidade em Governo Eletrônico, versão 3.1: https://emag.governoeletronico.gov.br/
- [WCAG] Web Content Accessibility Guidelines 2.2, Recomendação W3C de 12/12/2024: https://www.w3.org/TR/WCAG22/

---

### ACE-001
- assunto: o que a LBI chama de acessibilidade e de barreira na comunicação
- regra: acessibilidade é a possibilidade e condição de alcance para usar, com segurança e autonomia, espaços, equipamentos, transporte e informação, inclusive sistemas e tecnologias. Barreira nas comunicações e na informação é qualquer entrave, obstáculo, atitude ou comportamento que dificulte ou impossibilite expressar ou receber mensagens e informações por sistemas de comunicação e de tecnologia da informação
- valor: definição
- unidade: definição
- vigencia_inicio: em vigor (180 dias após a publicação de 07/07/2015, art. 127; data exata não calculada)
- vigencia_fim:
- status: vigente
- fonte_norma: LBI
- fonte_artigo: art. 3º, I e IV, d
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
- conferido_em: 2026-11-08
- caso_de_teste: formulário que só funciona com mouse → barreira na comunicação e na informação

### ACE-002
- assunto: sites de empresas e de governo
- regra: é obrigatória a acessibilidade nos sítios da internet mantidos por empresas com sede ou representação comercial no país ou por órgãos de governo, para uso da pessoa com deficiência, garantindo o acesso às informações conforme as melhores práticas e diretrizes de acessibilidade adotadas internacionalmente. Os sítios devem trazer o símbolo de acessibilidade em destaque
- valor: obrigação
- unidade: obrigação
- vigencia_inicio: em vigor (ver ACE-001)
- vigencia_fim:
- status: vigente
- fonte_norma: LBI
- fonte_artigo: art. 63, caput e § 1º
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
- conferido_em: 2026-11-08
- caso_de_teste: site de uma empresa brasileira → a obrigação se aplica; a lei remete às práticas e diretrizes internacionais sem nomear uma norma (ver ACE-010)

### ACE-003
- assunto: formato acessível de documento
- regra: formatos acessíveis são arquivos digitais que possam ser reconhecidos e acessados por softwares leitores de tela ou outras tecnologias assistivas. O artigo trata do incentivo do poder público a livros e artigos científicos nesses formatos
- valor: definição
- unidade: definição
- vigencia_inicio: em vigor (ver ACE-001)
- vigencia_fim:
- status: vigente
- fonte_norma: LBI
- fonte_artigo: art. 68, § 2º (caput e §§ 1º e 3º tratam de livros e artigos científicos)
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
- conferido_em: 2026-11-08
- caso_de_teste: PDF gerado de HTML com texto real, tags e idioma declarado → lido por leitor de tela; PDF feito de imagem escaneada sem texto → não

### ACE-004
- assunto: venda pela internet e publicidade
- regra: os canais de comercialização virtual e os anúncios publicitários devem disponibilizar os recursos de acessibilidade do art. 67 (entre eles legenda oculta, janela de Libras e audiodescrição), às expensas do fornecedor e conforme a compatibilidade do meio. O caput manda informar de forma correta e clara, em qualquer meio, e aplica no que couber os arts. 30 a 41 do CDC
- valor: obrigação
- unidade: obrigação
- vigencia_inicio: em vigor (ver ACE-001)
- vigencia_fim:
- status: a conferir
- fonte_norma: LBI
- fonte_artigo: art. 69, § 1º
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
- conferido_em: 2026-11-08
- caso_de_teste: vídeo de anúncio na internet → prever legenda e audiodescrição. Status "a conferir": o parágrafo foi lido por resumo da página (que veio com os acentos corrompidos), não palavra por palavra; abra a fonte antes de citar

### ACE-005
- assunto: material impresso de fornecedor
- regra: os fornecedores devem disponibilizar, mediante solicitação, exemplares de bulas, prospectos, textos ou qualquer outro tipo de material de divulgação em formato acessível
- valor: obrigação mediante solicitação
- unidade: obrigação
- vigencia_inicio: em vigor (ver ACE-001)
- vigencia_fim:
- status: vigente
- fonte_norma: LBI
- fonte_artigo: art. 69, § 2º
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
- conferido_em: 2026-11-08
- caso_de_teste: folheto em PDF de uma loja → ter versão com texto real e tags para quem pedir

### ACE-006
- assunto: o que é o eMAG e quem segue
- regra: modelo de acessibilidade do governo federal, versão especializada da WCAG para o contexto brasileiro, sem os níveis A, AA e AAA; obrigatório nos sítios e portais do governo federal (Portaria nº 3, de 07/05/2007, no âmbito do SISP). Cada recomendação cita o critério correspondente da WCAG 2.0
- valor: versão 3.1, abril de 2014
- unidade: versão
- vigencia_inicio: 2014-04 (versão 3.1)
- vigencia_fim:
- status: vigente
- fonte_norma: eMAG
- fonte_artigo: seções 1.1, 1.2 e 3
- fonte_url: https://emag.governoeletronico.gov.br/
- conferido_em: 2026-11-08
- caso_de_teste: site de prefeitura ou de órgão federal → eMAG como referência; site de empresa privada → o eMAG não é obrigatório pela portaria, mas serve de guia. Se existe versão posterior à 3.1: a conferir

### ACE-007
- assunto: contraste (eMAG 4.1)
- regra: oferecer contraste mínimo entre plano de fundo e primeiro plano, de no mínimo 4,5:1 (ligado ao critério 1.4.3 da WCAG)
- valor: 4,5
- unidade: razão de contraste (para 1)
- vigencia_inicio: 2014-04
- vigencia_fim:
- status: vigente
- fonte_norma: eMAG
- fonte_artigo: recomendação 4.1
- fonte_url: https://emag.governoeletronico.gov.br/
- conferido_em: 2026-11-08
- caso_de_teste: texto `#999999` sobre branco (cerca de 2,8:1) → falha

### ACE-008
- assunto: apresentação (eMAG 4.2 a 4.4)
- regra: não usar só a cor ou outra característica sensorial para diferenciar elementos (4.2); permitir redimensionar sem perder funcionalidade (4.3); o elemento com foco tem de ser visualmente evidente, e a borda de foco pode ser estilizada, mas não removida (4.4)
- valor: regra
- unidade: regra
- vigencia_inicio: 2014-04
- vigencia_fim:
- status: vigente
- fonte_norma: eMAG
- fonte_artigo: recomendações 4.2, 4.3 e 4.4
- fonte_url: https://emag.governoeletronico.gov.br/
- conferido_em: 2026-11-08
- caso_de_teste: `outline: none` sem substituto → falha 4.4

### ACE-009
- assunto: formulários (eMAG 6.1 a 6.8)
- regra: alternativa em texto para botão de imagem (6.1); etiqueta associada ao campo (6.2); ordem lógica de navegação (6.3); não mudar o contexto automaticamente (6.4); instruções para a entrada de dados (6.5); identificar e descrever erros e confirmar o envio (6.6); agrupar campos (6.7); estratégias de segurança específicas em vez de CAPTCHA (6.8)
- valor: regra
- unidade: regra
- vigencia_inicio: 2014-04
- vigencia_fim:
- status: vigente
- fonte_norma: eMAG
- fonte_artigo: recomendações 6.1 a 6.8
- fonte_url: https://emag.governoeletronico.gov.br/
- conferido_em: 2026-11-08
- caso_de_teste: select que envia o formulário ao mudar de opção → falha 6.4

### ACE-010
- assunto: ponte entre a lei e a norma técnica
- regra: a LBI obriga a acessibilidade conforme práticas e diretrizes internacionais, sem nomear uma (ACE-002), e o eMAG se declara alinhado à WCAG (ACE-006). Como alvo técnico, use a WCAG 2.2 nível AA, que inclui o que o eMAG pede e acrescenta critérios novos (foco não encoberto, alvo mínimo, entrada redundante, autenticação acessível). Isto é leitura de método, não regra legal
- valor: WCAG 2.2 AA
- unidade: alvo técnico
- vigencia_inicio: 2024-12-12 (Recomendação W3C da WCAG 2.2)
- vigencia_fim:
- status: vigente
- fonte_norma: WCAG; eMAG; LBI
- fonte_artigo: ponte
- fonte_url: https://www.w3.org/TR/WCAG22/
- conferido_em: 2026-11-08
- caso_de_teste: relatório diz "atende à WCAG 2.2 AA nos critérios verificados", nunca "está de acordo com a LBI"

### ACE-011
- assunto: tamanho mínimo do alvo (WCAG 2.5.8)
- regra: alvo de toque ou clique com pelo menos 24 por 24 px CSS (nível AA). Exceções: alvo menor espaçado de modo que um círculo de 24 px centrado nele não encoste em outro alvo; função disponível por outro controle que atende; alvo dentro de uma frase; tamanho definido pelo navegador sem mudança do autor; apresentação essencial ou exigida por lei. 44 por 44 é o critério 2.5.5, nível AAA, e 48 não é critério da WCAG
- valor: 24
- unidade: px CSS por lado
- vigencia_inicio: 2024-12-12
- vigencia_fim:
- status: vigente
- fonte_norma: WCAG
- fonte_artigo: 2.5.8 (AA); 2.5.5 (AAA)
- fonte_url: https://www.w3.org/TR/WCAG22/
- conferido_em: 2026-11-08
- caso_de_teste: ícone de 20 px colado a outro ícone → falha AA; ícone de 32 px → passa AA e fica abaixo da meta de 44 em toque (achado baixo, não "falha AA")
