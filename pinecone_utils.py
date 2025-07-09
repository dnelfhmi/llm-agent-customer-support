import os
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from embedding_utils import get_embedding

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "support-kb"
EMBED_DIM = 1536

pc = Pinecone(api_key=PINECONE_API_KEY)

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

index = pc.Index(INDEX_NAME)

def query_kb(description, top_k=3):
    embedding = get_embedding(description)
    results = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )
    return [match['metadata']['text'] for match in results['matches']]
