import pickle
from elasticsearch import Elasticsearch

elasticsearch_host = "https://stgelastic.bizmandala.com:443"
print(elasticsearch_host)
es = Elasticsearch(
    elasticsearch_host
)

print(es.ping())
INDEX = "book_indexes"
print('here')
if not es.indices.exists(index=INDEX):
    print('creating index . . . ')
    es.indices.create(index=INDEX,
                    mappings={
                        "properties": {
                            "name": {
                                "type": "dense_vector",
                                "dims": 768,
                                "index": True,
                                'similarity': 'l2_norm'
                            },
                            "description": {
                                "type": "dense_vector",
                                "dims": 768,
                                "index": True,
                                'similarity': 'l2_norm'
                            },
                        }
                    })


with open('book_embeddings.pkl', 'rb') as file:
    loaded_mappings = pickle.load(file)

loaded_mappings = loaded_mappings[6865:]
print('Starting . . .\n\n')
for index, document in enumerate(loaded_mappings):
    print(f'{index} / {len(loaded_mappings)}', end='\r')
    es.index(index=INDEX, document=document, id=document['id'])
