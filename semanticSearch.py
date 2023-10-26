from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Initialize the Elasticsearch client
es = Elasticsearch([{
    'host': 'localhost',
    'port': 9200
}])  # Replace with your Elasticsearch server details

# Initialize the Sentence Transformer model
model = SentenceTransformer('all-mpnet-base-v2')

# Define the index name
index_name = 'book_indexes'  # Replace with your Elasticsearch index name


def generate_query_vector(query_text):
    return model.encode(query_text)


def semantic_search(query_text, index_name, field='data', top_k=5):
    query_vector = generate_query_vector(query_text)
    query = {
        "knn": {
            "field": "description",
            "query_vector": query_vector,
            "k": 10,
            "num_candidates": 100
        }
    }
    return es.search(index=index_name, body=query)


# Get user input for the query
user_input = "Business"
# Perform semantic search
search_results = semantic_search(user_input, index_name)

# Print the similar documents
for hit in search_results['hits']['hits']:
    print(f"Document ID: {hit['_id']}, Score: {hit['_score']}")

print(es.count(index=index_name))
