# Operar e atualizar

Conferido em 08/11/2026 em docs.docker.com: logging com `json-file`, `volume prune` e boas práticas do WSL2.

## Inventário só de leitura
`docker ps -a`, `docker compose ls -a`, `docker network ls`, `docker volume ls`, `docker info`, `docker system df`. Por container: projeto compose, política de restart, usuário, redes, montagens. Projeto compose vazio quer dizer criado à mão com `docker run`; se tem nome, a mudança é no arquivo compose.

## Falhas silenciosas
1. **Dado que morre com o container.** Ache todo lugar onde o programa escreve (VOLUME do Dockerfile e caminhos da configuração). Prove a persistência recriando e vendo a segunda execução lembrar da primeira.
2. **Containers que não se acham.** Na rede `bridge` padrão, só por IP, que muda; numa rede criada, pelo nome. Teste de dentro do container que chama, nunca da máquina.
3. **Agendamento.** Prove que dispara sem esperar: cópia temporária da linha para dali a 2 minutos, removida num passo separado. Confira o fuso.
4. **Log que cresce para sempre.** O driver padrão `json-file` não rotaciona (`max-size` é ilimitado por padrão). Defina `max-size` e `max-file` por container; mudança no daemon só vale para container novo.
5. **Imagem que não se reproduz.** Tag móvel muda no próximo pull: prefira tag de versão e anote o Id. Leia o Dockerfile de um estranho antes de construir.

## Atualizar é recriar, em seis passos
1. Versão que roda de fato e a mais nova (a tag exata existe?).
2. Leia todas as notas de versão entre as duas ("breaking", "upgrade"; banco que migra sozinho não volta).
3. Duas redes de segurança: snapshot e cópia do volume com o container parado, conferida por hash. Salve o log do container antigo.
4. Prepare antes de parar: `docker compose config -q`, puxe a imagem.
5. Troque mantendo a volta: renomeie o antigo em vez de remover; cópia datada do compose.
6. Prove no lugar de uso, com as mesmas checagens antes e depois. Fixe a versão no arquivo ao terminar.

## Docker Desktop e WSL2
- Guarde o que é montado no sistema de arquivos Linux (`~/projeto` dentro da distro). Evite montar de `/mnt/c`: desempenho bem menor e o container não recebe eventos de arquivo (recarga automática falha).
- `\r\n` em `entrypoint.sh` quebra com "no such file or directory": salve em LF, `.gitattributes` com `*.sh text eol=lf`.
- Caminho do Windows precisa de tradução. Regras em `referencias/windows.md`.
- Alterar o daemon: Docker Desktop, Settings, Docker Engine.

## Liberar espaço: responda com opções por risco
Nada roda antes da resposta. Primeiro `docker system df`.
| Opção | O que remove |
|---|---|
| Containers parados, um a um | só aquele container |
| `docker image prune` | imagens sem tag |
| `docker image prune -a` (prefira com filtro de idade) | toda imagem sem container |
| `docker builder prune` | cache de build |
| `docker system prune` | parados, redes sem uso, imagens sem tag, cache |
| `docker volume prune` | volumes **anônimos** sem uso |
| `docker volume prune --all` | também os **nomeados**: dado de banco |
| `docker compose down -v` | os volumes do projeto |

Lembrete: o mesmo `-f` tem efeitos diferentes conforme o comando.
