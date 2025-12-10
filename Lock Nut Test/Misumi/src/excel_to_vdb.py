import os 
from qdrant_client import QdrantClient,models
import pandas as pd
from fastembed import TextEmbedding
client=QdrantClient(url="http://localhost:6333")

filename=r"D:\Internship_Autolabs\Lock Nut Test\Misumi\data\Bearing_lock_nuts_washer_for_rolling_bearings_retaining_and_tightening_washer_series_awl.xlsx" 
collection_name="Misumi Test"

dense_encoder=TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
df=pd.read_excel(filename)

category_name="Bearing lock nuts"
basename=os.path.basename(filename)
name,extension=os.path.splitext(basename)
file_parts=name.split('_')
sub_category_name=" ".join(file_parts[3:])

def combine_parts(row):
    parts=[]
    for col_name, value in row.items():
        if col_name=='Part Number URL':
            continue
        if pd.notna(value):
            parts.append(f"{col_name}: {value}")
    parts.append(f"Category: {category_name}")
    parts.append(f"Sub category: {sub_category_name}")
    parts.append("Website: Misumi")
    return " | ".join(parts)

df["combined_text"]=df.apply(combine_parts,axis=1)

def create_collection_payload():
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "dense":models.VectorParams(size=dense_encoder.embedding_size,distance=models.Distance.COSINE)
            }
        )
    
    client.create_payload_index(collection_name=collection_name,field_name="product_id",field_schema="integer")
    client.create_payload_index(collection_name=collection_name,field_name="chunk_id",field_schema="integer")
    client.create_payload_index(collection_name=collection_name,field_name="part_number",field_schema="keyword")
    client.create_payload_index(collection_name=collection_name,field_name="category_name",field_schema="keyword")
    client.create_payload_index(collection_name=collection_name,field_name="subcategory_name",field_schema="keyword")
    client.create_payload_index(collection_name=collection_name,field_name="website",field_schema="keyword")
    client.create_payload_index(collection_name=collection_name,field_name="chunk",field_schema="keyword")

def to_vector_db():
    create_collection_payload()

    offset=0
    subcategory_offset=0
    info=client.get_collection(collection_name)
    count=info.points_count
    if(count!=0):
        #retrieval from database for chunk_id
        records,_=client.scroll(
            collection_name=collection_name,
            limit=1,
            with_payload=True,
            with_vectors=False,
            order_by={
                "key":"chunk_id",
                "direction":"desc"
            }
        )
        if(records):
            chunk_id_num=records[0].payload.get("chunk_id")
            subcategory_num=records[0].payload.get("product_id")
            offset=chunk_id_num+1
            subcategory_offset=subcategory_num+1
        else:
            offset=0
            subcategory_offset=0
    else:
        offset=0
        subcategory_offset=0

    for i,row in df.iterrows():
        a=str(row.get('Part Number URL',''))
        url="https://vn.misumi-ec.com"+a

        client.upsert(
            collection_name=collection_name,
            points=[models.PointStruct(
                id=offset,
                vector={
                    "dense":list(dense_encoder.embed(row["combined_text"]))[0]
                },
                payload={
                    "product_id":subcategory_offset,
                    "chunk_id":offset,
                    "part_number":row["Part Number Name"],
                    "category_name":category_name,
                    "subcategory_name":sub_category_name,
                    "website":"Misumi",
                    "chunk":row["combined_text"] + " | " + "URL:" +url,
                    "URL":url
                }
            )  
            ]
        )
        offset=offset+1
if __name__=="__main__":
    to_vector_db()



    


    