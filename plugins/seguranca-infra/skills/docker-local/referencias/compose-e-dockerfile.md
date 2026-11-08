# Compose e Dockerfile

Confira a versão do Docker instalada antes de usar opção recente.

## Compose
Editar, não substituir.
- `depends_on` só ordena a partida: todo serviço do qual outro depende tem `healthcheck` e `condition: service_healthy` (`pg_isready`, `redis-cli ping`, `curl -f .../health`).
- Serviços se acham pelo nome; `localhost` dentro do container é o próprio container.
- Publique só as portas que o host precisa, em `127.0.0.1` no desenvolvimento.
- Volume nomeado para o que guarda estado (`down -v` apaga).
- Bind `.:/app` esconde o `node_modules` da imagem: volume anônimo em `/app/node_modules`.
- `environment` vence `env_file`; `$$` para `$` literal.
- Segredo nunca no arquivo; `.env` no `.gitignore` e `.env.example` versionado.
- `restart: unless-stopped`; tag fixa; `init: true` e forma exec; limites de memória; sem a chave `version:`.
- Verifique com `docker compose up -d --wait`.

## Dockerfile
- Meça antes: `docker image ls`, `docker history --no-trunc`.
- Manifesto, install, código, nessa ordem; cache mount do BuildKit.
- Multi-stage, sem ferramenta de build na final.
- Base mínima fixada por tag e por digest do manifesto multi-arquitetura (`docker buildx imagetools inspect`; nunca pull e inspect, que fixa a plataforma local). Sem como conferir: TODO, nunca invente digest.
- Usuário não root antes do CMD.
- Segredo de build só por `--mount=type=secret`. ARG, ENV ou COPY seguido de apagar ficam nas camadas.
- `.dockerignore` com `.git`, `node_modules`, `.env*`.
- `COPY --chown` em vez de `chown -R`.
- HEALTHCHECK; ENTRYPOINT em forma exec (a forma shell engole o SIGTERM).
- Next: `.next/standalone` exige `output: 'standalone'` na configuração.
- Script `.sh` com fim de linha LF.

Saída: o arquivo e o motivo de cada mudança (cache, tamanho ou segurança).
