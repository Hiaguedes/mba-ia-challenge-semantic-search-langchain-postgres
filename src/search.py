from langchain_postgres import PGVector

from config import DATABASE_URL, COLLECTION_NAME, get_embeddings, get_llm

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(question=None):
    try:
        embeddings = get_embeddings()
        llm = get_llm()

        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        )

        def ask(q):
            results = vector_store.similarity_search_with_score(q, k=10)
            context = "\n\n".join([doc.page_content for doc, _ in results])
            prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=q)
            return llm.invoke(prompt).content

        if question:
            return ask(question)

        return ask

    except Exception as e:
        print(f"Erro ao inicializar: {e}")
        return None
