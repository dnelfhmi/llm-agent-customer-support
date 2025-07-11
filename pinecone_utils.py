import os
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from embedding_utils import get_embedding

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "support-kb"
EMBED_DIM = 1536

pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if it doesn't exist
try:
    if INDEX_NAME not in pc.list_indexes():
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBED_DIM,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"Created Pinecone index: {INDEX_NAME}")
    else:
        print(f"Pinecone index {INDEX_NAME} already exists")
except Exception as e:
    print(f"Error with Pinecone index: {e}")
    # Continue without the index for testing purposes

try:
    index = pc.Index(INDEX_NAME)
except Exception as e:
    print(f"Error connecting to Pinecone index: {e}")
    index = None

def query_kb(description, top_k=3):
    if index is None:
        print("Pinecone index not available, returning empty results")
        return []
    
    try:
        embedding = get_embedding(description)
        results = index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )
        return [match['metadata']['text'] for match in results['matches']]
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []
