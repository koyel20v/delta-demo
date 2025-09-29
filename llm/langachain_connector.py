import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from langchain_neo4j import Neo4jGraph

# --- Load environment variables create your own .env file---
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "llm12345")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not found in .env")

# --- Initialize Groq LLM ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # or "mixtral-8x7b-32768"
    temperature=0,
    api_key=GROQ_API_KEY,
)

# --- Initialize Ollama Embeddings (nomic-embed-text) ---
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
print("✅ Using Ollama embeddings: nomic-embed-text:latest")

# --- Neo4j connection ---
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USER,
    password=NEO4J_PASS,
)

# --- Function: query KG using embedding ---
def query_kg_with_embedding(user_query: str):
    # Convert query into embedding
    query_embedding = embeddings.embed_query(user_query)

    # Run Cypher similarity search (make sure embeddings are stored in Neo4j nodes as `e.embedding`)
    cypher = """
    MATCH (e:Entity)
    WITH e, gds.similarity.cosine(e.embedding, $query_embedding) AS score
    ORDER BY score DESC
    LIMIT 3
    RETURN e.name AS name, score
    """
    result = graph.query(cypher, params={"query_embedding": query_embedding})
    return result

# --- Function: full query system ---
def query_system(user_query: str):
    matches = query_kg_with_embedding(user_query)

    if matches and len(matches) > 0:
        entities = [record["name"] for record in matches]
        context = ", ".join(entities)

        prompt = f"""
        The user asked: "{user_query}"
        The knowledge graph returned related entities: {context}.
        Please frame a helpful and natural answer using this context.
        """
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
    else:
        # Fallback to LLM knowledge
        response = llm.invoke(
            f"The knowledge graph has no answer. Based on your knowledge, answer this: {user_query}"
        )
        return response.content if hasattr(response, "content") else str(response)

# --- Chatbot loop ---
def chatbot():
    print("\n🌱 Welcome to Krishi.AI! (Groq LLM + Neo4j + Ollama embeddings) 🌾\n")
    while True:
        user_query = input("🧑 You: ").strip()
        if not user_query or user_query.lower() in ("exit", "quit"):
            print("🌱 KrishiAI: Bye 👋")
            break

        try:
            answer = query_system(user_query)
            print(f"🌱 KrishiAI: {answer}\n")
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    chatbot()
