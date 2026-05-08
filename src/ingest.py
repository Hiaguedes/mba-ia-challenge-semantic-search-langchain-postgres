from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

from config import DATABASE_URL, COLLECTION_NAME, PDF_PATH, get_embeddings


def ingest_pdf():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    print(f"{len(documents)} páginas carregadas, {len(chunks)} chunks gerados.")

    embeddings = get_embeddings()

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    vector_store.add_documents(chunks)
    print(f"{len(chunks)} chunks armazenados no pgVector.")


if __name__ == "__main__":
    ingest_pdf()
