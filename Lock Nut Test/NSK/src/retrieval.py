import os 
from qdrant_client import QdrantClient,models
from fastembed import TextEmbedding 
client=QdrantClient(url="http://localhost:6333")
collection_name="NSK"
dense_encoder=TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")

def embed_query(query):
    dense_embed=next(dense_encoder.query_embed(query))
    return dense_embed

def retrieval(query):
    dense_vector=embed_query(query)
    search_results=client.query_points(
        collection_name=collection_name,
        query=dense_vector,
        using="dense",
        limit=5,
        with_payload=True
    )
    print(search_results)
    return search_results.points


def save_log(query,results):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, "..", "test logs", "retrieval_logs_nsk.txt")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path,"a",encoding="utf-8")as f:
        f.write(f"User query: {query}\n")
        f.write("-"*20 + "\n")

        for rank,result in enumerate(results,start=1):
            score=result.score
            payload=result.payload

            part_number=payload.get("part_number","N/A")
            content=payload.get("chunk","N/A")
            url=payload.get("URL","N/A")

            f.write(f"Rank: {rank} Score: {score: .4f}/n")
            f.write(f"Content: {content}\n")
            f.write(f"URL: {url}\n")
        f.write(f"="*30 +"\n\n")    
if __name__=="__main__":
    user_query="ANL84"
    results=retrieval(user_query)
    save_log(user_query,results)

        