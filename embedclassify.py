from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a pre-trained SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def relevancy(email_data):
    email_embeddings = model.encode(email_data)

    # Convert email embeddings to a numpy array
    email_embeddings_np = np.array(email_embeddings, dtype='float32')

    # Create an index for the embeddings
    embedding_dimension = email_embeddings_np.shape[1]
    index = faiss.IndexFlatL2(embedding_dimension)

    # Add email embeddings to the index
    index.add(email_embeddings_np)

    # Save the index for future use (optional)
    faiss.write_index(index, 'email_index.faiss')

    query = "Is the coming saturday instructional day?"
    query_embedding = model.encode([query])

    # Search the index for the closest email(s)
    k = 5  # Number of results to retrieve
    distances, indices = index.search(query_embedding, k)

    # Print the most relevant emails
    print("Most relevant emails:")

    
    for idx in indices[0]:
        print(email_data[idx])