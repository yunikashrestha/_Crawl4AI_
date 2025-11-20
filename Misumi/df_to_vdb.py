# import os
# import pandas as pd
# import uuid
# from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
# from qdrant_client import QdrantClient, models
# import time

# file_name = "camfollower_cam_follower_with_tapped_hole_for_greasing_cft_type.xlsx"
# collection_name = "camFollower"

# dense_encoder = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
# sparse_encoder = SparseTextEmbedding("Qdrant/bm25")
# late_encoder = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

# df = pd.read_excel(file_name)
# name, extension = os.path.splitext(file_name)
# file_parts = name.split('_')
# category_name = file_parts[0]
# sub_category_name = " ".join(file_parts[1:])

# client = QdrantClient(url="http://localhost:6333")

# NON_SEMANTIC_COLS = [
#     'Part Number URL', 
#     'Price', 
#     'Days to Ship', 
#     'Minimum order Qty', 
#     'Volumn Discount', 
#     'URL'
# ]

# def create_embedding_text(row):
#     """
#     Creates a string optimized for Vector Search.
#     Includes only Part Number, Category, and Technical Specs.
#     """
#     parts = []
    
#     if pd.notna(row.get('Part Number Name')):
#         parts.append(f"Part Number: {row['Part Number Name']}")
#     parts.append(f"Category: {category_name} | Subcategory: {sub_category_name}")

#     for col_name, value in row.items():
#         if col_name in NON_SEMANTIC_COLS or col_name == 'Part Number Name': 
#             continue
        
#         if pd.notna(value) and value != '-':
#             val_str = str(value).strip()
#             parts.append(f"{col_name}: {val_str}")

#     return " | ".join(parts)

# def create_display_text(row):
#     """
#     Creates the full string for the LLM to read later (stored in Payload).
#     Includes Price, Shipping, etc.
#     """
#     parts = []
#     for col_name, value in row.items():
#         if col_name == 'Part Number URL': continue
#         if pd.notna(value):
#             parts.append(f"{col_name}: {value}")
#     return " | ".join(parts)

# df["embedding_text"] = df.apply(create_embedding_text, axis=1)
# df["combined_text"] = df.apply(create_display_text, axis=1)


# def create_collection_payload():
#     if not client.collection_exists(collection_name):
#         client.create_collection(
#             collection_name=collection_name,
#             vectors_config={
#                 "dense": models.VectorParams(
#                     size=dense_encoder.embedding_size,
#                     distance=models.Distance.COSINE
#                 ),
#                 "lateInteraction": models.VectorParams(
#                     size=late_encoder.embedding_size,
#                     distance=models.Distance.COSINE,
#                     multivector_config=models.MultiVectorConfig(
#                         comparator=models.MultiVectorComparator.MAX_SIM
#                     ),
#                 ),
#             },
#             sparse_vectors_config={
#                 "sparse": models.SparseVectorParams(modifier=models.Modifier.IDF)
#             },
#         )
#         client.create_payload_index(collection_name=collection_name,field_name="chunk_id",field_schema="integer")
#         client.create_payload_index(collection_name=collection_name, field_name="product_id", field_schema="integer")
#         client.create_payload_index(collection_name=collection_name, field_name="category_name", field_schema="keyword")
#         client.create_payload_index(collection_name=collection_name, field_name="part_number", field_schema="keyword")

# def to_vectordb():
#     create_collection_payload()
    
#     offset = 0
#     subcategory_offset = 0
#     info = client.get_collection(collection_name=collection_name)
#     if info.points_count != 0:
#         res, _ = client.scroll(
#             collection_name=collection_name,
#             limit=1,
#             with_payload=True,
#             with_vectors=False,
#             order_by={"key": "chunk_id", "direction": "desc"}
#         )
#         if res:
#             offset = res[0].payload.get("chunk_id") + 1
#             subcategory_offset = res[0].payload.get("product_id") + 1

#     num_points = len(df)
#     start_time = time.perf_counter()

#     for i, row in df.iterrows():
#         url_suffix = str(row.get('Part Number URL', ''))
#         url = "https://vn.misumi-ec.com" + url_suffix

#         dense_vec = list(dense_encoder.embed(row["embedding_text"]))[0]
#         sparse_vec = list(sparse_encoder.embed(row["embedding_text"]))[0].as_object()
#         late_vec = list(late_encoder.embed(row["embedding_text"]))[0]

#         client.upsert(
#             collection_name=collection_name,
#             points=[
#                 models.PointStruct(
#                     id=offset,
#                     payload={
#                         "product_id": subcategory_offset,
#                         "category_name": category_name,
#                         "sub_category_name": sub_category_name,
#                         "file_name": file_name,
#                         "part_number": row["Part Number Name"],
#                         "chunk_id": offset,
#                         "chunk": row["combined_text"] + " " + "Url: " + url, 
#                         "URL": url,
#                         "price_raw": row.get("Price", ""),
#                         "days_to_ship": row.get("Days to Ship", "")
#                     },
#                     vector={
#                         "dense": dense_vec,
#                         "sparse": sparse_vec,
#                         "lateInteraction": late_vec
#                     }
#                 )
#             ]
#         )
#         offset += 1

#     end_time = time.perf_counter()
#     elapsed_time = end_time - start_time
#     average_time = elapsed_time / num_points if num_points > 0 else 0

#     output_message = (
#         f"File Inserted: {file_name}\n"
#         f"Total Points: {num_points}\n"
#         f"Total time: {elapsed_time:.4f}s\n"
#         f"Avg time: {average_time:.4f}s\n"
#     )
#     print(output_message)
#     with open("insertion_time.txt", "a") as f:
#         f.write(output_message + "\n")

# if __name__ == "__main__":
#     to_vectordb()
import os
import pandas as pd
import uuid
from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
from qdrant_client import QdrantClient, models
import time

file_name = "camfollower_cam_followers_with_thrust_ball.xlsx"
collection_name = "camFollower"

dense_encoder = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
sparse_encoder = SparseTextEmbedding("Qdrant/bm25")
late_encoder = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

df = pd.read_excel(file_name)
name, extension = os.path.splitext(file_name)
file_parts = name.split('_')
category_name = file_parts[0]
sub_category_name = " ".join(file_parts[1:])

client = QdrantClient(url="http://localhost:6333")

NON_SEMANTIC_COLS = [
    'Part Number URL', 
    'Price', 
    'Days to Ship', 
    'Minimum order Qty', 
    'Volumn Discount', 
    'URL'
]

def create_embedding_text(row):
    """
    Creates a string optimized for Vector Search.
    """
    parts = []
    
    if pd.notna(row.get('Part Number Name')):
        parts.append(f"Part Number: {row['Part Number Name']}")
    parts.append(f"Category: {category_name} | Subcategory: {sub_category_name}")

    for col_name, value in row.items():
        if col_name in NON_SEMANTIC_COLS or col_name == 'Part Number Name': 
            continue
        
        if pd.notna(value) and value != '-':
            val_str = str(value).strip()
            parts.append(f"{col_name}: {val_str}")

    return " | ".join(parts)

def create_display_text(row):
    """
    Creates the full string for the LLM to read.
    FIX: Explicitly excludes 'embedding_text' and 'Part Number URL'
    """
    parts = []
    for col_name, value in row.items():
        # Ignore technical columns and the embedding column to prevent duplication
        if col_name in ['Part Number URL', 'embedding_text']: 
            continue
            
        if pd.notna(value):
            parts.append(f"{col_name}: {value}")
    return " | ".join(parts)

# 1. Create embedding text first
df["embedding_text"] = df.apply(create_embedding_text, axis=1)

# 2. Create display text (The function now knows to ignore the 'embedding_text' column)
df["combined_text"] = df.apply(create_display_text, axis=1)

def create_collection_payload():
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "dense": models.VectorParams(
                    size=dense_encoder.embedding_size,
                    distance=models.Distance.COSINE
                ),
                "lateInteraction": models.VectorParams(
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
        client.create_payload_index(collection_name=collection_name,field_name="chunk_id",field_schema="integer")
        client.create_payload_index(collection_name=collection_name, field_name="product_id", field_schema="integer")
        client.create_payload_index(collection_name=collection_name, field_name="category_name", field_schema="keyword")
        client.create_payload_index(collection_name=collection_name, field_name="part_number", field_schema="keyword")

def to_vectordb():
    create_collection_payload()
    
    offset = 0
    subcategory_offset = 0
    info = client.get_collection(collection_name=collection_name)
    if info.points_count != 0:
        res, _ = client.scroll(
            collection_name=collection_name,
            limit=1,
            with_payload=True,
            with_vectors=False,
            order_by={"key": "chunk_id", "direction": "desc"}
        )
        if res:
            offset = res[0].payload.get("chunk_id") + 1
            subcategory_offset = res[0].payload.get("product_id") + 1

    num_points = len(df)
    start_time = time.perf_counter()

    for i, row in df.iterrows():
        url_suffix = str(row.get('Part Number URL', ''))
        url = "https://vn.misumi-ec.com" + url_suffix

        dense_vec = list(dense_encoder.embed(row["embedding_text"]))[0]
        sparse_vec = list(sparse_encoder.embed(row["embedding_text"]))[0].as_object()
        late_vec = list(late_encoder.embed(row["embedding_text"]))[0]

        # FIX: Construct the final chunk string here to control the order
        # Order: Specs -> Category -> Subcategory -> URL
        final_chunk_text = (
            f"{row['combined_text']} | "
            f"Category: {category_name} | "
            f"Subcategory: {sub_category_name} | "
            f"Url: {url}"
        )

        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=offset,
                    payload={
                        "product_id": subcategory_offset,
                        "category_name": category_name,
                        "sub_category_name": sub_category_name,
                        "file_name": file_name,
                        "part_number": row["Part Number Name"],
                        "chunk_id": offset,
                        "chunk": final_chunk_text, # Uses the ordered string
                        "URL": url,
                        "price_raw": row.get("Price", ""),
                        "days_to_ship": row.get("Days to Ship", "")
                    },
                    vector={
                        "dense": dense_vec,
                        "sparse": sparse_vec,
                        "lateInteraction": late_vec
                    }
                )
            ]
        )
        offset += 1

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    average_time = elapsed_time / num_points if num_points > 0 else 0

    output_message = (
        f"File Inserted: {file_name}\n"
        f"Total Points: {num_points}\n"
        f"Total time: {elapsed_time:.4f}s\n"
        f"Avg time: {average_time:.4f}s\n"
    )
    print(output_message)
    with open("insertion_time.txt", "a") as f:
        f.write(output_message + "\n")

if __name__ == "__main__":
    to_vectordb()