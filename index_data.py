import pickle
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

print(es.ping())
INDEX = "book_indexes"
print('here')
if es.indices.exists(index=INDEX):
    print('has index')
    es.indices.delete(index=INDEX)
print('creating index')
es.indices.create(index=INDEX,
                  mappings={
                      "properties": {
                          "name": {
                              "type": "dense_vector",
                              "dims": 768,
                              "index": True,
                              "similarity": "l2_norm"
                          },
                          "description": {
                              "type": "dense_vector",
                              "dims": 768,
                              "index": True,
                              "similarity": "l2_norm"
                          },
                      }
                  })

print('done')

with open('book_embeddings.pkl', 'rb') as file:
    loaded_mappings = pickle.load(file)

print('Starting . . .\n\n')
for index, document in enumerate( loaded_mappings):
    print(f'{index} / {len(loaded_mappings)}', end='\r')
    es.index(index=INDEX, document=document, id=document['id'])
