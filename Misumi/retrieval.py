from fastembed import TextEmbedding,SparseTextEmbedding,LateInteractionTextEmbedding
from qdrant_client import QdrantClient,models
client=QdrantClient(url="http://localhost:6333")
collection_name="Misumi parts"
dense_encoder=TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
sparse_encoder=SparseTextEmbedding("Qdrant/bm25")
lateInteraction=LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

def embed_query(query):
    dense_embed=next(dense_encoder.query_embed(query))
    sparse_embed=next(sparse_encoder.query_embed(query))
    late_embed=next(lateInteraction.query_embed(query))
    return dense_embed,sparse_embed,late_embed

def chunk_retrieval(query):
    dense_vectors,sparse_vectors,late_vectors=embed_query(query)
    prefetch=[
        models.Prefetch(query=dense_vectors,using="dense",limit=20,),
        models.Prefetch(query=models.SparseVector(**sparse_vectors.as_object()),using="sparse",limit=20),
    ]
    query_results=client.query_points(
        collection_name=collection_name,
        prefetch=prefetch,
        query=late_vectors,
        using="lateInteraction",
        limit=10,
        with_payload=True,
        with_vectors=False
    ).points

    return query_results
    
def retrieval(query):
    retrieved_docs=chunk_retrieval(query)    
    all_chunks=[]
    for point in retrieved_docs:
            chunk_desc=point.payload.get("chunk")
            all_chunks.append(chunk_desc)
        
    return all_chunks

if __name__=="__main__":
     print("The retrived part numbers are:")
     points =retrieval(query = "cam follower crown hex socket Width=7 ")
     for point in points:
        print(f"{point}\n\n")
    



    
    