from repo.models import Book
from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('all-mpnet-base-v2')
# Replace with your Elasticsearch server details

books = Book.objects.all()
print(len(books))


def generate_vector_embedding(book, fields):
    document = {}
    for field in fields:
        data = getattr(book, field) or ''
        vector_data = model.encode(data)
        document[f'{field}'] = vector_data.tolist()
    return document


mappings = []
for index, book in enumerate(books):
    print(f'{index} / {len(books)}', end='\r')
    mappings.append(generate_vector_embedding(book, ['name', 'description']))

# Save the mappings to a pickle file
with open('book_embeddings.pkl', 'wb') as file:
    pickle.dump(mappings, file)

print("Mapping saved to book_embeddings.pkl")
