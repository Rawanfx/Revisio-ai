from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct
import uuid

client =QdrantClient(host="localhost",port=6333)
COLLECTION_NAME = "lecture_chunks"
VECTOR_SIZE=384

def ensure_collection ():
    collection = client.get_collection().collections
    if not any (c.name == COLLECTION_NAME for c in collection):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(VECTOR_SIZE,Distance=Distance.COSINE)
        )
        client.create_payload_index(collection_name=COLLECTION_NAME,field_name="lecture_id",field_schema="keyword")
        client.create_payload_index(collection_name=COLLECTION_NAME,field_name="user_id",field_schema="keyword")
        client.create_payload_index(collection_name=COLLECTION_NAME,field_name="course_id",field_schema="keyword")


def save_chunk (lecture_id :str,course_id :str,user_id:str,chunk:list[str],embeddings: list[list[float]]):
    points =[]
    for i in range (len(chunk)):
        point = PointStruct(
            id =str(uuid.uuid4()),
            payload={
                "lecture_id": lecture_id,
                "course_id": course_id,
                "user_id": user_id,
                "chunk_index": i,
                "content": chunk[i]
            },
            vector=embeddings[i]
        )
        points.append(point)
    client.upsert(collection_name=COLLECTION_NAME,points=points)
    return len(points)    
