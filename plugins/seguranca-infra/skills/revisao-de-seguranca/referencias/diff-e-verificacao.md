# Diff, verificação e correção

## Oito falhas típicas de um diff
Complemento do /security-review. Linhas apagadas pesam mais que as novas.
1. Entrada nova herda o middleware das vizinhas?
2. Checagem removida ou enfraquecida (um `where` que perde o `tenant_id`).
3. Permissão alargada (CORS, SameSite, CSP, bucket, grant, papel).
4. Segredo novo (precisa rotacionar; já está no histórico).
5. Dependência nova.
6. Dado não confiável num destino novo.
7. Padrão de segurança mudado na configuração.
8. Cópia de um padrão que já estava errado (reporte os dois).

Para cada função alterada, descubra quem chama e atrás de quais guardas. Arquivos não rastreados entram: um `.env` novo não aparece no diff.

Veredito: mergear, mergear com pendências, não mergear.

## Verificar um achado: três lentes ao abrir cada linha
- **Explorabilidade:** nomeie o ator. Refute se inalcançável, se exige o maior privilégio ou se o "atacante" é o próprio dono.
- **Correção da afirmação:** a guarda "ausente" costuma estar na rota, no proxy ou numa constraint.
- **Mitigação existente:** cite o `arquivo:linha`.

Cada achado sai com a citação literal e confirme, abrindo o arquivo, que ela existe. Vereditos: Real, Falso positivo, Gravidade exagerada, **Não comprovado: precisa de teste**. No relatório comum, o não comprovado fica fora da contagem principal; no portão de lançamento, bloqueia até ser testado.

**Desqualificações:** controle de base que já neutraliza; "valor fixo poderia ser crítico" (avalie como está implantado); limite ausente com limitador acima; achado sem ter lido o handler e a rota; já fechado em relatório anterior; ramos de desenvolvimento; exaustão de recursos genérica.

## Reproduzir, não raciocinar
Teste que falha no código atual e passaria com a correção, na camada mais baixa que roda. Corrida: teste de intercalação. Documento gerado: gere e inspecione. Data: relógio perto da meia-noite no fuso da implantação. Endpoint público: 404 idêntico byte a byte e tempo que não depende de o registro existir. Teste não rodado nunca é prova: "escrito, não rodado: motivo".

## Doze lentes para achar o que os outros perdem
O predicado sustenta o rótulo? Conta fatos ou artefatos? Quem mais lê o dado depois da regra nova? Onde está o lock em relação à checagem? O portão pergunta o mesmo que a transação? O tempo de resposta denuncia algo? O que acontece no caminho de recuperação? Que dia é (dia local contra UTC; `toISOString().slice(0,10)`)? O par de rotas (página e API) está coberto? A interface espelha o portão do servidor? O que está copiado e deveria ser derivado? O que a guarda não cobre?

## Corrigir e reverificar
Só a pedido, com escopo (`tudo`, `críticos`, números); vazio é perguntar.
- **Ordem:** segredos vivos (rotacionar hoje), críticos, altos alcançáveis sem login, médios rápidos (cabeçalhos, flags de cookie), atualizações agrupadas.
- Em crítico e alto, a causa raiz numa linha, nomeando a entrada não confiável e o mecanismo perigoso.
- Prefira a correção central (helper parametrizado, autorização no router, fetch seguro). Um helper que deixa fácil o caminho seguro elimina a classe.
- Leia o diff inteiro: remove a causa ou só muda o que o scanner vê? Supressão nunca é correção sozinha. Trouxe algo novo? Procure variantes (rotas irmãs, helper copiado).
- Decisões do usuário, sempre com padrão sugerido: tentativas de login, origens de CORS, estratégia de autenticação, tamanho de upload, senha mínima.
- Fecho: tabela de mudanças, dependências novas, variáveis novas, arquivos alterados.

**Reverificar:** rápida (arquivos mudados, achados marcados como corrigidos, rotação dos segredos) durante o ciclo; completa antes da aprovação final ou depois de muita mudança. Corrigido vira verificado só se toda localização resolveu, o código foi lido e o teste passa; volta a aberto se só foi escondido do scanner. O que a correção quebrou? Raio de impacto (chamadores de cada símbolo), super-restrição (o caminho legítimo ainda passa?), teste de dois casos (bloqueia o ataque, deixa o legítimo). Resultado honesto: "o portão passou contra o escopo declarado no commit X".

Comando destrutivo no caminho: `referencias/comandos-destrutivos.md`.

## Regras curtas de confiabilidade
Diff limpo com "sem achados" é válido. Cada achado com local concreto e condição de reprodução; descarte o inferido só pelo nome. No máximo cinco achados menores; o resto vira contagem.
