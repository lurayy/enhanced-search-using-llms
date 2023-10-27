import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer


elasticsearch_host = "https://stgelastic.bizmandala.com:443"
index_name = 'book_indexes'
st.set_page_config(layout="wide")
model = SentenceTransformer('all-mpnet-base-v2')

es = Elasticsearch(
    elasticsearch_host
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
.stDeployButton {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    st.title("Book Search App")

    search_query = st.text_input("Enter search query:")
    if st.button("Using Name"):
        if search_query:
            books = search_books(search_query, 'name')
            with st.container():
                if books:
                    for book in books:
                        display_book_info(book)
                else:
                    st.warning("No books found for the given search query.")

    description_query = st.text_input("Describe the book:")
    if st.button("Using Description"):
        if description_query:
            books = search_books(description_query, 'description')
            with st.container():
                if books:
                    for book in books:
                        display_book_info(book)
                else:
                    st.warning("No books found for the given search query.")

def search_books(query, field):
    query_vector = model.encode(query)
    query = {
        "knn": {
            "field": field,
            "query_vector": query_vector,
            "k": 30,
            "num_candidates": 100
        }
    }
    response = es.search(index=index_name, body=query, fields=['images', 'slug', 'name', 'barcode'])
    return response["hits"]["hits"]

def display_book_info(hit):
    book = hit['_source']
    col1, col2 = st.columns([1, 2])
    col2.subheader(book['slug'])
    if book["images"]:
        with col1:
            st.image(book["images"][0]['url'], width=300)
    with col2:
        st.write(f"ISBN: {book['barcode']}")
        st.write(f"Slug: {book['slug']}")
        st.write(f"Score: {hit['_score']}")
        

if __name__ == "__main__":
    main()
