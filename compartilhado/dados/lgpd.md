# LGPD e regulamentos da ANPD

Arquivo de dados com vigência e fonte. Cada item tem o mesmo cabeçalho; o texto da regra é paráfrase, não transcrição. Para decidir um caso, abra a fonte do item.

Como usar:
- Consulte pela **data do fato**. Só vale item "vigente" naquela data; "anunciado" não é "vigente"; "a conferir" não sustenta conclusão.
- Item com `conferido_em` mais velho que 6 meses: avise uma vez e siga.
- Se houver uma cópia mais nova deste arquivo (nos arquivos do Project, na pasta de trabalho ou na camada pessoal), use a de `conferido_em` mais recente e diga qual usou.
- A skill aponta o que a regra pede e o que falta na prática do usuário; não dá parecer jurídico. Tratamento de dado sensível, de criança ou em larga escala vai para revisão de quem responde juridicamente.

Lido em 08/11/2026. Fontes:
- [LGPD] Lei 13.709/2018, texto compilado: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- [R15] Resolução CD/ANPD nº 15/2024 (Regulamento de Comunicação de Incidente de Segurança): https://bibliotecadigital.mj.gov.br/bitstream/1/12879/2/RES_ANPD_2024_15.html
- [R2] Resolução CD/ANPD nº 2/2022 (agentes de tratamento de pequeno porte): https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022

---

### LGPD-001
- assunto: dado pessoal e dado sensível
- regra: dado pessoal é informação ligada a pessoa natural identificada ou identificável. Dado sensível é o dado pessoal sobre origem racial ou étnica, religião, opinião política, filiação a sindicato ou a organização religiosa, filosófica ou política, saúde, vida sexual, dado genético ou biométrico
- valor: definição
- unidade: definição
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD
- fonte_artigo: art. 5º, I e II
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- conferido_em: 2026-11-08
- caso_de_teste: lista de leads com nome e WhatsApp → dado pessoal; anotação "cliente com diabetes" → dado sensível

### LGPD-002
- assunto: bases legais
- regra: só se trata dado pessoal com uma base: consentimento; obrigação legal ou regulatória; políticas públicas; pesquisa; execução de contrato ou procedimento preliminar a pedido do titular; exercício de direitos em processo; proteção da vida; tutela da saúde; legítimo interesse (salvo se prevalecerem os direitos do titular); proteção do crédito
- valor: 10 bases
- unidade: lista
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD
- fonte_artigo: art. 7º, I a X
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- conferido_em: 2026-11-08
- caso_de_teste: mandar promoção a quem só pediu orçamento → perguntar qual base o usuário usa; sem resposta, apontar a lacuna

### LGPD-003
- assunto: consentimento
- regra: consentimento é manifestação livre, informada e inequívoca para finalidade determinada; autorização genérica é nula; por escrito, fica em cláusula destacada; pode ser revogado a qualquer momento, de graça e de forma fácil
- valor: requisitos
- unidade: princípio
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD
- fonte_artigo: art. 5º, XII; art. 8º, §§ 1º, 4º e 5º
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- conferido_em: 2026-11-08
- caso_de_teste: formulário com "aceito receber comunicações de parceiros" marcado por padrão → não é inequívoco nem determinado; apontar. Mensagem de lista sem forma de sair → falta revogação fácil

### LGPD-004
- assunto: o que informar ao titular
- regra: finalidade específica; forma e duração do tratamento; quem é o controlador e como contatá-lo; com quem o dado é compartilhado e para quê; responsabilidades dos agentes; os direitos do titular
- valor: 7 itens
- unidade: lista
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD
- fonte_artigo: art. 9º, I a VII
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- conferido_em: 2026-11-08
- caso_de_teste: página de captura de lead sem dizer para que o dado será usado → apontar o item que falta

### LGPD-005
- assunto: fim do tratamento e guarda
- regra: o tratamento termina quando a finalidade foi alcançada, o período acabou, o titular pediu (inclusive ao revogar o consentimento) ou a ANPD determinou. Depois, o dado é eliminado; pode ser guardado para obrigação legal, pesquisa, transferência a terceiro dentro da lei ou uso exclusivo do controlador, anonimizado
- valor: regra
- unidade: princípio
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD
- fonte_artigo: arts. 15 e 16
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- conferido_em: 2026-11-08
- caso_de_teste: planilha de leads de uma campanha encerrada há anos, sem uso → perguntar por que ainda existe

### LGPD-006
- assunto: direitos do titular
- regra: confirmação de que há tratamento; acesso; correção; anonimização, bloqueio ou eliminação do desnecessário ou irregular; portabilidade; eliminação do que foi tratado com consentimento; saber com quem foi compartilhado; saber que pode não consentir e o que acontece; revogar o consentimento
- valor: 9 direitos
- unidade: lista
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD
- fonte_artigo: art. 18, I a IX
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- conferido_em: 2026-11-08
- caso_de_teste: cliente pede no direct para apagar os dados dele → há canal e alguém responsável por atender?

### LGPD-007
- assunto: encarregado e pequeno porte
- regra: o controlador indica um encarregado, com identidade e contato públicos. O agente de tratamento de pequeno porte não é obrigado a indicar encarregado, mas tem de manter um canal de comunicação com o titular; indicar mesmo assim conta como boa prática
- valor: dispensa com canal obrigatório
- unidade: princípio
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD; Resolução CD/ANPD nº 2/2022
- fonte_artigo: LGPD art. 41; R2 art. 11, caput e §§ 1º e 2º
- fonte_url: https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022
- conferido_em: 2026-11-08
- caso_de_teste: MEI sem encarregado e sem e-mail ou canal para o titular → falta o canal

### LGPD-008
- assunto: quem é pequeno porte
- regra: microempresa, empresa de pequeno porte (incluído o MEI, enquadrados na LC 123/2006), startup e pessoa natural ou ente privado que trate dados como controlador ou operador. Ficam fora do regime diferenciado quem faz tratamento de alto risco, quem tem receita bruta acima do limite da empresa de pequeno porte e quem pertence a grupo econômico acima desse limite. Alto risco pede ao mesmo tempo um critério geral (larga escala ou afetar significativamente direitos fundamentais) e um específico (por exemplo, tecnologia emergente, vigilância de área pública, decisão automatizada, dado sensível ou de criança, adolescente ou idoso)
- valor: critérios
- unidade: princípio
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: Resolução CD/ANPD nº 2/2022
- fonte_artigo: arts. 2º, 3º e 4º
- fonte_url: https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-2-de-27-de-janeiro-de-2022
- conferido_em: 2026-11-08
- caso_de_teste: clínica pequena com prontuário de muitos pacientes → pode cair em alto risco (dado de saúde e escala); não presumir o regime diferenciado

### LGPD-009
- assunto: segurança
- regra: os agentes adotam medidas técnicas e administrativas para proteger os dados contra acesso não autorizado e contra situação acidental ou ilícita, desde a concepção do produto ou serviço
- valor: obrigatória
- unidade: princípio
- vigencia_inicio: em vigor (data de início não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD
- fonte_artigo: art. 46, caput e §§ 1º e 2º
- fonte_url: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- conferido_em: 2026-11-08
- caso_de_teste: planilha de leads num link aberto a qualquer pessoa → apontar

### LGPD-010
- assunto: incidente de segurança: comunicação à ANPD
- regra: incidente que possa causar risco ou dano relevante é comunicado à ANPD e ao titular. A lei remete o prazo à ANPD; o regulamento fixa 3 dias úteis, contados de quando o controlador soube que o incidente afetou dados pessoais, com 20 dias úteis para complementar, justificando. Conteúdo: natureza dos dados, titulares envolvidos, medidas de segurança usadas, riscos, motivo da demora se houver, medidas para reverter ou reduzir os efeitos
- valor: 3
- unidade: dias úteis
- vigencia_inicio: 2024-04 (vigor na publicação; data do Diário Oficial não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: LGPD; Resolução CD/ANPD nº 15/2024
- fonte_artigo: LGPD art. 48, caput e § 1º; R15 art. 6º, caput e §§ 1º e 3º
- fonte_url: https://bibliotecadigital.mj.gov.br/bitstream/1/12879/2/RES_ANPD_2024_15.html
- conferido_em: 2026-11-08
- caso_de_teste: soube na segunda-feira, sem feriado na semana → prazo comum até quinta-feira (conferir o calendário de dias úteis)

### LGPD-011
- assunto: incidente de segurança: comunicação ao titular
- regra: 3 dias úteis, com a mesma contagem. A comunicação diz: natureza e categoria dos dados afetados; medidas de segurança; riscos e impactos possíveis; motivo da demora, se houver; medidas de reversão ou mitigação, quando couber; data em que soube do incidente; contato para informações (o do encarregado, quando houver)
- valor: 3
- unidade: dias úteis
- vigencia_inicio: 2024-04 (vigor na publicação; data do Diário Oficial não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: Resolução CD/ANPD nº 15/2024
- fonte_artigo: art. 9º, caput e incisos I a VII
- fonte_url: https://bibliotecadigital.mj.gov.br/bitstream/1/12879/2/RES_ANPD_2024_15.html
- conferido_em: 2026-11-08
- caso_de_teste: rascunho de aviso aos clientes sem a data de conhecimento → falta o item

### LGPD-012
- assunto: prazo em dobro para pequeno porte
- regra: o agente de pequeno porte tem prazo em dobro para comunicar incidente à ANPD e ao titular e para complementar, salvo quando houver risco à integridade física ou moral dos titulares ou à segurança nacional. Também tem prazo em dobro para atender pedidos do titular, nos termos de regulamento próprio
- valor: dobro
- unidade: prazo
- vigencia_inicio: 2024-04 (redação dada pela Resolução nº 15/2024; data do Diário Oficial não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: Resolução CD/ANPD nº 15/2024; Resolução CD/ANPD nº 2/2022
- fonte_artigo: R15 art. 6º, § 8º, e art. 9º, § 6º; R2 art. 14, I e II
- fonte_url: https://bibliotecadigital.mj.gov.br/bitstream/1/12879/2/RES_ANPD_2024_15.html
- conferido_em: 2026-11-08
- caso_de_teste: MEI com vazamento de lista de clientes, sem risco à integridade → 6 dias úteis

### LGPD-013
- assunto: registro do incidente
- regra: o controlador guarda o registro do incidente, inclusive do que não foi comunicado à ANPD nem aos titulares, por no mínimo 5 anos a partir da data do registro. O registro traz ao menos: data em que soube, circunstâncias gerais, natureza e categorias dos dados, número de titulares, avaliação de risco e possíveis danos, medidas de correção e mitigação, forma e conteúdo de eventual comunicação e, se não comunicou, os motivos
- valor: 5
- unidade: anos
- vigencia_inicio: 2024-04 (vigor na publicação; data do Diário Oficial não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: Resolução CD/ANPD nº 15/2024
- fonte_artigo: art. 10, caput e § 1º
- fonte_url: https://bibliotecadigital.mj.gov.br/bitstream/1/12879/2/RES_ANPD_2024_15.html
- conferido_em: 2026-11-08
- caso_de_teste: incidente comunicado em 2026 → registro guardado ao menos até 2031; incidente avaliado e não comunicado → também registrado, com o motivo

### LGPD-014
- assunto: incidente: quando há risco ou dano relevante
- regra: precisa valer ao mesmo tempo: (a) poder afetar significativamente interesses e direitos fundamentais dos titulares e (b) envolver ao menos um destes: dados sensíveis; de crianças, adolescentes ou idosos; financeiros; de autenticação em sistemas; protegidos por sigilo legal, judicial ou profissional; em larga escala. A ANPD só espera comunicação quando o incidente foi confirmado, envolve dados pessoais e pode causar risco ou dano relevante. Vulnerabilidade sozinha não é incidente; dado só anonimizado não se comunica
- valor: critério cumulativo
- unidade: princípio
- vigencia_inicio: 2024-04 (vigor na publicação; data do Diário Oficial não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: Resolução CD/ANPD nº 15/2024; orientação da ANPD
- fonte_artigo: R15 art. 5º; página de comunicado de incidente da ANPD, modificada em 26/08/2026
- fonte_url: https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis
- conferido_em: 2026-11-08
- caso_de_teste: lista de senhas de clientes exposta → dado de autenticação; avaliar o critério (a) e tratar como comunicável na dúvida. Falha corrigida sem acesso indevido a dado pessoal → vulnerabilidade, não incidente

### LGPD-015
- assunto: incidente: como comunicar
- regra: à ANPD, pelo encarregado ou representante legal, por processo no SEI!ANPD (login gov.br), tipo de comunicado de incidente, com formulário preliminar ou completo e comprovante de representação; o complemento vai como peticionamento no mesmo processo. A comunicação à ANPD traz os doze itens do art. 6º, § 2º: natureza e categoria dos dados; número de titulares, com crianças, adolescentes e idosos à parte; medidas antes e depois; riscos e impactos; motivo da demora; providências; data do incidente e data em que soube; encarregado ou representante; controlador e declaração de pequeno porte, se for o caso; operador; descrição e causa principal; total de titulares tratados na atividade afetada. Ao titular: linguagem simples e, se possível, direta e individual, pelos meios de costume; se inviável, divulgação em site, aplicativo, redes ou canais de atendimento por no mínimo 3 meses; depois, declaração no processo em até 3 dias úteis após o prazo
- valor: canal e conteúdo
- unidade: procedimento
- vigencia_inicio: 2024-04 (vigor na publicação; data do Diário Oficial não conferida)
- vigencia_fim:
- status: vigente
- fonte_norma: Resolução CD/ANPD nº 15/2024; orientação da ANPD
- fonte_artigo: R15 art. 6º, § 2º, e art. 9º, §§ 1º a 4º; página de comunicado de incidente da ANPD
- fonte_url: https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis
- conferido_em: 2026-11-08
- caso_de_teste: rascunho à ANPD sem o número de titulares → falta o inciso II; dizer o que falta e seguir como preliminar, a complementar
