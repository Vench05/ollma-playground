from embedding import embed_text, list_of_pets, list_of_wild_animals
from sample_chat_request import stream_response

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from uuid import uuid4

import shutil
import asyncio


def add_to_qdrant(client: QdrantClient, collection_name="animals", points=list[PointStruct]):
    return client.upsert(
        collection_name=collection_name,
        points=points
    )

def create_collection(client: QdrantClient, path: str, collection_name="animals", dimensions=1024):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=dimensions, distance=Distance.DOT)
    )

def search_in_qdrant(client: QdrantClient, query, collection_name="animals", top=5):
    search_result = client.query_points(
        collection_name=collection_name,
        query=query,
        with_payload=True,
        limit=top
    ).points
    return search_result

def delete_collection(client: QdrantClient, collection_name="animals"):
    client.delete_collection(collection_name=collection_name)

def point_struct_creation(text, payload):
    print(text, "point_struct_creation")
    embedding = embed_text(text)
    return PointStruct(id=uuid4(), vector=embedding, payload=payload)

def main():
    path = './qdrant_data'
    collection_name = "animals"
    client = QdrantClient(path=path)
    if client.collection_exists(collection_name):
        print("Collection already exists, deleting and creating a new one...")
        delete_collection(client, collection_name)
    create_collection(client, path=path)

    data = []

    for pet in list_of_pets:
        data.append(point_struct_creation(pet, {"type": "pet", "name": pet}))

    for wild_animal in list_of_wild_animals:
        data.append(point_struct_creation(wild_animal, {"type": "wild", "name": wild_animal}))

    add_to_qdrant(client, points=data)
    
    text = "mosquito"
    query = embed_text(text)
    search_result = search_in_qdrant(client, query)
    print(f"Search results for '{text}': ", " ".join([f"{item.payload['name']} ({item.payload['type']})" for item in search_result]))
    
    text = "Tyrannosaurus rex"
    query = embed_text(text)
    search_result = search_in_qdrant(client, query)
    print(f"Search results for '{text}': ", " ".join([f"{item.payload['name']} ({item.payload['type']})" for item in search_result]))

    client.close()

if __name__ == "__main__":
    main()
