![CI](https://github.com/marcelo-bernardo/taskflow-devops/actions/workflows/ci.yml/badge.svg)

# taskflow-devops

API REST de tarefas (TaskFlow) em Python/Flask, usada como projeto da disciplina **DevOps na Prática** (PUCRS). O foco é o fluxo DevOps: integração contínua, entrega contínua com containers, infraestrutura como código e deploy com rollback.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Verificação de saúde |
| GET | `/tasks` | Lista as tarefas |
| POST | `/tasks` | Cria uma tarefa (`{"title": "..."}`) |
| PUT | `/tasks/<id>` | Marca a tarefa como concluída |
| DELETE | `/tasks/<id>` | Exclui a tarefa |

## Rodando localmente

Com Python:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest --cov=app
flask --app app run
```

Com Docker:

```bash
docker compose up --build
curl http://localhost:5000/health
```

## Pipeline CI/CD (`.github/workflows/ci.yml`)

Roda a cada push e pull request:

1. **Lint e testes**: flake8, pip-audit e pytest com cobertura mínima de 80%.
2. **Validar Terraform**: `fmt -check`, `init -backend=false` e `validate` (em paralelo com o job 1).
3. **Build e teste do container**: constrói a imagem, sobe o container e testa `/health` e `POST /tasks`.
4. **Publicação** (somente push na `main`): envia a imagem para `ghcr.io/marcelo-bernardo/taskflow-devops` com as tags `latest` e SHA do commit.

## Infraestrutura (`infra/`)

Terraform para AWS: VPC, sub-rede pública, security group, EC2 `t3.micro` (o `user_data` instala o Docker e sobe a imagem) e bucket S3 versionado.

```bash
cd infra
terraform init
terraform plan
terraform apply
```

## Deploy (`scripts/deploy.sh`)

```bash
./scripts/deploy.sh ghcr.io/marcelo-bernardo/taskflow-devops:<sha-do-commit>
```

Baixa a imagem, troca o container e confere o `/health`. Se a nova versão não responder, volta automaticamente para a versão anterior.

## Fluxo de contribuição

A `main` só recebe mudanças por pull request a partir de branches `feature/*`, depois que o pipeline passa.
