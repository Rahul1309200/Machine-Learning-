import pandas as pd
import ollama
import chromadb

# 1. Initialize the vector database
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="movie_dataset")

# 2. Load and clean your Kaggle Dataset
df = pd.read_csv("movies.csv").fillna("")

# Clean the genres column — extract just the genre names from JSON string
import ast
def extract_genres(genre_str):
    try:
        genres = ast.literal_eval(genre_str)
        return ", ".join([g['name'] for g in genres])
    except:
        return genre_str

df['clean_genres'] = df['genres'].apply(extract_genres)

# Extract year from release_date (e.g., "2009-12-10" → "2009")
df['year'] = df['release_date'].apply(lambda x: str(x)[:4] if x else "Unknown")

print("Processing and indexing movies... please wait.")

# Loop through the rows to index them (Limit to 500 for testing speed)
for index, row in df.head(500).iterrows():
    # Combine relevant columns into a single string for context
    movie_info = (
        f"Title: {row['title']}. "
        f"Year: {row['year']}. "
        f"Genre: {row['clean_genres']}. "
        f"Rating: {row['vote_average']}/10. "
        f"Runtime: {row['runtime']} min. "
        f"Plot: {row['overview']}"
    )
    
    # Store text in ChromaDB (it handles embedding generation automatically)
    collection.add(
        documents=[movie_info],
        ids=[str(index)],
        metadatas=[{"title": row['title']}]
    )

print("Indexing complete! Your movie database is ready.")

# 3. Create the Query Function
def ask_movie_bot(user_query):
    # Search the database for relevant movies
    results = collection.query(query_texts=[user_query], n_results=3)
    retrieved_context = "\n\n".join(results['documents'][0])
    
    # Create a prompt combining the user query and retrieved Kaggle data
    system_prompt = (
        "You are an expert movie assistant. Answer the user's question using ONLY the provided movie data. "
        "If you don't know the answer based on the data, say you don't know.\n\n"
        f"Movie Data:\n{retrieved_context}"
    )
    
    # Send the combined prompt to Ollama
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_query}
        ]
    )
    
    return response['message']['content']

# 4. Interactive Test
while True:
    query = input("\nAsk something about movies (or type 'exit'): ")
    if query.lower() == 'exit':
        break
    answer = ask_movie_bot(query)
    print(f"\nAI: {answer}")