# Agroia Backend

Este é o backend da aplicação Agroia, construída com FastAPI.

## Estrutura do Projeto

- `app/`: Contém o código da aplicação.
- `requirements.txt`: Dependências do projeto.
- `.env`: Variáveis de ambiente.
- `docker-compose.yml`: Configuração do Docker Compose.
- `Dockerfile`: Dockerfile para construir a imagem do aplicativo.

## Executando a Aplicação

1. Instale as dependências: `pip install -r requirements.txt`
2. Execute o aplicativo: `uvicorn app.main:app --reload`
3. Acesse a API em `http://localhost:8000`.

## Testes

Para executar os testes, use:

```bash
pytest app/tests/
# nasa-space-apps-back-end
