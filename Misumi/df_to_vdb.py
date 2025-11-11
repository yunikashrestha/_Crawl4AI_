import os
import pandas as pd
import uuid
from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
from qdrant_client import QdrantClient, models

file_name = "camfollower_cam_followers_flat_hex_socket.xlsx"
collection_name = "Misumi parts"
dense_encoder = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
sparse_encoder = SparseTextEmbedding("Qdrant/bm25")
late_encoder = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

df = pd.read_excel(file_name)
name,extension=os.path.splitext(file_name)
file_parts=name.split('_')
category_name=file_parts[0]
sub_category_name="".join(file_parts[1:])

def combine_row_parts(row):
    parts = []
   
    for col_name, value in row.items():
        if col_name == 'Part Number URL':
            continue
        if pd.notna(value):
            parts.append(f"{col_name}: {value}")
    parts.append(f"Category: {category_name}")
    parts.append(f"Sub Category: {sub_category_name}")
    return " | ".join(parts)

df["combined_text"] = df.apply(combine_row_parts, axis=1)

client = QdrantClient(url="http://localhost:6333")

def create_collection_payload():
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "dense": models.VectorParams(
                    size=dense_encoder.embedding_size,
                    distance=models.Distance.COSINE
                ),
                "lateInteraction":models.VectorParams(
                    size=late_encoder.embedding_size,
                    distance=models.Distance.COSINE,
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM
                    ),
                ),
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(modifier=models.Modifier.IDF)
            },
        )
        client.create_payload_index(collection_name=collection_name,field_name="product_id",field_schema="integer")
        client.create_payload_index(collection_name=collection_name,field_name="category_name",field_schema="keyword")
        client.create_payload_index(collection_name=collection_name,field_name="subcategory_name",field_schema="keyword")
        client.create_payload_index(collection_name=collection_name,field_name="file_name",field_schema="keyword")
        client.create_payload_index(collection_name=collection_name,field_name="chunk_id",field_schema="integer")
        client.create_payload_index(collection_name=collection_name,field_name="chunk",field_schema="keyword")
        

def to_vectordb():
     
    name,extension=os.path.splitext(file_name)
    file_parts=name.split('_')
    category_name=file_parts[0]
    subcategory_name=" ".join(file_parts[1:])

    create_collection_payload()
    texts=df["combined_text"].tolist()

    offset = 0
    subcategory_offset = 0
    info = client.get_collection(collection_name=collection_name)
    count = info.points_count
    if(count != 0):
        res,_ = client.scroll(
            collection_name = collection_name,
            limit = 1,
            with_payload = True,
            with_vectors = False,
            order_by={
                "key" : "chunk_id",
                "direction" : "desc"
            }
        )
        if(res):
            chunk_id_num= res[0].payload.get("chunk_id")
            subcategory_id_num=res[0].payload.get("product_id")
            offset = chunk_id_num + 1
            subcategory_offset=subcategory_id_num+1

        else:
            offset = 0
            subcategory_offset = 0
    else:
        offset = 0
        subcategory_offset = 0
    for i,row in df.iterrows():
        a=str(row.get('Part Number URL', ''))
        url="https://vn.misumi-ec.com" + a
        client.upsert(
            collection_name = collection_name,
            points = [
                models.PointStruct(
                    id = offset,
                    payload = {
                            "product_id" :subcategory_offset,
                            "category_name" : category_name,
                            "sub_category_name":subcategory_name,
                            "file_name" : file_name,
                            "chunk_id" : offset,
                            "chunk" : row["combined_text"],
                            "URL":url
                        },
                    vector = {
                            "dense" : list(dense_encoder.embed(row["combined_text"]))[0],
                            "sparse" : list(sparse_encoder.embed(row["combined_text"]))[0].as_object(),
                            "lateInteraction" : list(late_encoder.embed(row["combined_text"]))[0]
                        }
                    )
                ]
            )
          
        offset=offset+1


def query_rag_database(query:str,limit:int=5):
    """
    Performs hybrid search on Qdrant, reranked by lateinteraction 
    """
    
    dense_query=next(dense_encoder.query_embed(query))
    sparse_query=next(sparse_encoder.query_embed(query))
    late_query=next(late_encoder.query_embed(query))

    # Hybrid Search 
    prefetch=[
        models.Prefetch(query=dense_query,using="dense",limit=20),
        models.Prefetch(query=models.SparseVector(**sparse_query.as_object()),using="sparse",limit=20)
    ]

    #Query using late-interaction vector for reranking
    query_results = client.query_points(
        collection_name = collection_name,
        prefetch=prefetch,
        query = late_query,
        using = "lateInteraction",
        limit = 10,
        with_payload = True,
        with_vectors = False
    ).points

    return query_results

# to_vectordb()
search_query="crown hex socket"
retrieved_points=query_rag_database(search_query)
print("The retrieved points are:")
for point in retrieved_points:
    payload = point.payload
    
    
    part_number = payload.get('chunk_id', 'N/A')
    url = payload.get('URL', 'URL Missing')
    
    print(f"\nID: {point.id}, Score: {point.score:.4f}")
    print(f"  **Part Number**: {part_number}")
    print(f"  **Chunk**: {payload.get('chunk', 'Chunk Missing')}")
    print(f"  **Source URL**: {url}")