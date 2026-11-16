#!/usr/bin/env bash
# Deploy da API com Docker: baixa a imagem, troca o container e confere o /health.
# Se a nova versao nao responder, volta para a versao anterior (rollback).
set -euo pipefail

IMAGE="${1:-ghcr.io/marcelo-bernardo/taskflow-devops:latest}"
NAME="taskflow-api"
PORT="${PORT:-5000}"

echo ">> Baixando a imagem $IMAGE"
docker pull "$IMAGE"

PREVIOUS=$(docker inspect --format '{{.Image}}' "$NAME" 2>/dev/null || true)

echo ">> Substituindo o container"
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" --restart unless-stopped -p "$PORT:5000" "$IMAGE" >/dev/null

echo ">> Verificando http://localhost:$PORT/health"
for _ in $(seq 1 10); do
  if curl -fs "http://localhost:$PORT/health" >/dev/null; then
    echo ">> Deploy concluido com sucesso"
    exit 0
  fi
  sleep 3
done

echo ">> A nova versao nao respondeu. Ultimos logs:"
docker logs --tail 30 "$NAME" || true
docker rm -f "$NAME" >/dev/null 2>&1 || true

if [ -n "$PREVIOUS" ]; then
  echo ">> Rollback para a versao anterior"
  docker run -d --name "$NAME" --restart unless-stopped -p "$PORT:5000" "$PREVIOUS" >/dev/null
fi
exit 1
