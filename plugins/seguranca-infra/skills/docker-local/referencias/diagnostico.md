# Diagnóstico de dentro para fora

Estado e código de saída, últimas linhas do log, `inspect` de rede e montagens, teste de dentro do container, só então mudar algo, uma coisa por vez. Só leitura até aí: peça antes de `rm`, `restart`, `up`, `down` ou apagar volume.

## Códigos de saída
| Código | Significado |
|---|---|
| 0 num serviço longo | o comando terminou: um override trocou o processo |
| 1 | erro da aplicação |
| 126 e 127 | comando não executável ou não encontrado |
| 137 | SIGKILL ou falta de memória (veja `OOMKilled` no inspect) |
| 139 | falha de segmentação |

## Sintomas
| Sintoma | Causa provável |
|---|---|
| Porta ocupada | outro container ou programa |
| Responde dentro e não fora | app escuta em `127.0.0.1`, precisa de `0.0.0.0`; ou `localhost` resolvendo para IPv6 |
| Log vazio | falhou antes de abrir a saída, loga em arquivo, ou driver `none` |
| Bind mount esconde arquivos | origem inexistente vira pasta vazia |
| Permissão negada | usuário do container contra dono dos arquivos |
| `exec format error` | arquitetura errada |
| `no such file or directory` no entrypoint | fim de linha CRLF no script |
| Imagem não encontrada | tag não existe ou falta login no registry |
| Serviço não acha o outro | `localhost` dentro do container é o próprio container; use o nome do serviço na mesma rede |
| Fica reiniciando | leia os logs entre reinícios com `docker logs --tail 50` |

`docker compose config -q` valida. Para ver os valores resolvidos, filtre o campo que precisa: sem `-q`, os segredos saem na tela.

Formato da resposta em `SKILL.md`. Afirmar a causa só com a saída na mão; sem ela, "hipótese" e o comando que confirma.
