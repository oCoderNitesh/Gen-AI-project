from sentence_transformers import SentenceTransformer
import chromadb


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)


with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()


chunks = [
    chunk.strip()
    for chunk in knowledge.split("\n\n")
    if chunk.strip()
]


embeddings = embedding_model.encode(chunks).tolist()


collection.upsert(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings
)


def search_knowledge(question, n_results=3):

    question_embedding = embedding_model.encode(
        [question]
    ).tolist()[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    return results["documents"][0]

