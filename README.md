# plugins-br

> **In English:** Claude plugins written in Brazilian Portuguese, built around Brazilian rules (LGPD, consumer and advertising law, Simples Nacional, MEI, NF-e, OFX, Pix, accessibility law). 7 plugins, 36 skills, condensed from the community catalog. Apache-2.0. The skills themselves are in Portuguese.

Plugins para o Claude em português do Brasil, com as regras daqui: LGPD, CDC, CONAR, Simples Nacional, MEI, NF-e, OFX, Pix e acessibilidade pela LBI. Cada um foi condensado do melhor que existe no catálogo da comunidade, traduzido, corrigido e sem scripts de terceiros.

São 7 plugins, 36 skills e 3 agentes.

## Os plugins

| Plugin | O que faz | Skills | Onde funciona |
|---|---|---|---|
| `escrita` | Escrever e revisar sem mudar o que o autor disse | redigir, revisar-texto, criticar, voz, metodo-de-pesquisa | Chat, Cowork, Claude Code |
| `escritorio-contabil` | Rotina de escritório contábil: números, planilhas, documentos, extratos, notas e fechamento | confere-numeros, planilhas, documento-oficial, pops-e-guias, extratos-e-conciliacao, notas-fiscais, contabilidade-do-mes | Chat, Cowork, Claude Code |
| `pequeno-negocio` | Marca, Instagram, copy, anúncios e números do pequeno negócio, sem inventar fato | marca, instagram, copy, anuncios, financas-gerenciais | Chat, Cowork, Claude Code |
| `design` | Direção visual, telas, apresentações e impressos, com acessibilidade | direcao-visual, telas, apresentacoes, impressos-e-imagens | Chat, Cowork, Claude Code |
| `memoria-e-contexto` | Manter memória, instruções e continuidade entre sessões | memoria, continuidade, cofre, instrucoes | Chat, Cowork, Claude Code |
| `engenharia` | Código com prova: planejar, testar, revisar, depurar, Next.js 16 com Supabase, automações | planejar, testar-e-verificar, revisar-e-refatorar, depurar, next-supabase, automacoes | Claude Code |
| `seguranca-infra` | Revisão de segurança, RLS, segredos, publicação, deploy e Docker local | revisao-de-seguranca, supabase, segredos-e-publicacao, deploy-e-lancamento, docker-local | Claude Code |

Os agentes `explorador`, `revisor-independente` (engenharia) e `verificador-cetico` (seguranca-infra) só leem; nenhum altera arquivo. O chat ignora agentes, por isso esses dois plugins ficam no Claude Code.

Nenhum plugin traz hook ativo, comando ou servidor MCP.

## Como instalar

**No chat e no Cowork:** gere os pacotes com `python -I ferramentas/montar.py --zip` e envie o zip de cada plugin em Customize > Plugins > Adicionar > Upload plugin.

**No Claude Code, pelo terminal:** adicione a pasta deste repositório como marketplace e instale o plugin:

```
/plugin marketplace add /caminho/para/este/repositorio
/plugin install engenharia@plugins-br
```

**No Claude Code, pelo app para computador:** registre o marketplace em `~/.claude/settings.json` (caminho absoluto, com `/`) e instale pelo botão **+** ao lado da caixa de mensagem, em **Add plugins**:

```json
{
  "extraKnownMarketplaces": {
    "plugins-br": {
      "source": { "source": "directory", "path": "C:/caminho/para/este/repositorio" }
    }
  }
}
```

Instale só o que for usar: cada skill ativa soma a descrição dela ao que o Claude lê.

## Pasta `extras/`

Coisas opcionais que não fazem parte de plugin nenhum e não se ligam sozinhas. Hoje há a `extras/guarda-git/`, um hook que barra comandos destrutivos de git e de sistema nas ferramentas Bash e PowerShell. O README dela diz como ligar, o que ela não pega e como desligar.

## O que foi testado, e o que não foi

- **Cada plugin passou por 2 pedidos sintéticos**, comparando a resposta com e sem a skill, por agentes separados. Isso exercitou 14 das 36 skills. As outras 22 tiveram só a forma conferida pelo build e as fontes conferidas na documentação.
- **A escolha da skill foi simulada:** um agente recebeu nomes e descrições e indicou qual usaria em frases soltas. Isso mostra que as descrições se separam bem, não que a skill entra sozinha numa conversa real.
- **Os scripts** de extrato, OFX e XML, e a guarda opcional, têm testes com dados sintéticos. Nenhum viu arquivo real de banco ou de nota.
- **Os testes rodaram em Sonnet**, com pedidos e armadilhas escritos por quem escreveu as skills. Medem se elas travam o erro previsto, não o que ninguém previu.

## Regras brasileiras

As regras fiscais, de publicidade, de proteção de dados e de acessibilidade ficam em `compartilhado/dados/`, com vigência e fonte por linha. Só linha "vigente" sustenta número; "anunciado" e "a conferir" não. Confira a coluna `conferido_em`: lei muda e este repositório pode ficar para trás.

Estes plugins apoiam o trabalho. Não substituem contador, advogado nem o encarregado de dados, e a responsabilidade pelo que for entregue, declarado ou publicado continua sendo de quem usa.

## Como manter

As peças comuns moram em `compartilhado/` e são copiadas para cada skill pelo build. Nunca edite a cópia dentro de `referencias/`.

```
python -I ferramentas/montar.py            # monta e confere
python -I ferramentas/montar.py --conferir # só confere
python -I ferramentas/montar.py --zip      # gera os pacotes em dist/
```

O build precisa só de Python 3. Ele avisa se a lista opcional de termos internos não existir.

## Licença e créditos

Apache-2.0: veja `LICENSE` e `NOTICE`. Tudo que inspirou cada skill, com repositório, versão e licença, está em `CREDITS.md`; os textos originais das licenças estão em `licencas/terceiros/`.
