# Desafio MBA Engenharia de Software com IA - Full Cycle

Busca semântica em PDF via CLI usando LangChain, pgVector (PostgreSQL), e OpenAI ou Gemini.

## Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Chave de API da [OpenAI](https://platform.openai.com/) **ou** [Google Gemini](https://aistudio.google.com/)

## Configuração

```bash
# 1. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env e preencha OPENAI_API_KEY ou GOOGLE_API_KEY
```

## Execução

```bash
# 1. Subir o banco de dados (PostgreSQL + pgVector)
docker compose up -d

# 2. Ingerir o PDF
python src/ingest.py

# 3. Iniciar o chat
python src/chat.py
```

## Exemplo de uso

```
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Qual é a capital da França?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Digite `sair` para encerrar o chat.

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `OPENAI_API_KEY` | Chave da OpenAI (use esta **ou** a do Google) |
| `GOOGLE_API_KEY` | Chave do Google Gemini |
| `DATABASE_URL` | String de conexão do PostgreSQL (padrão já definido no `.env.example`) |
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção no pgVector |
| `PDF_PATH` | Caminho para o arquivo PDF |
| `OPENAI_LLM_MODEL` | Modelo LLM da OpenAI (padrão: `gpt-4o-mini`) |
| `GOOGLE_LLM_MODEL` | Modelo LLM do Gemini (padrão: `gemini-2.0-flash-lite`) |
