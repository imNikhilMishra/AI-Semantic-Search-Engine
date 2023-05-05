import openai
import pinecone

# Initialize OpenAI's latest text embeddings model
openai.api_key = "YOUR_OPENAI_API_KEY"
model_engine = "text-8.0.0"
model_prompt = f"embed:{model_engine}:"

# Initialize Pinecone vector database
pinecone.init(api_key="YOUR_PINECONE_API_KEY")
pinecone_index_name = "my_index"
pinecone_index = pinecone.Index(index_name= pinecone_index_name)

# Define a function to create the index with LSH
def create_index():
    # Example text documents to be added to the index
    text_docs = {
        "en": [
            "This is the first document.",
            "This is the second document.",
            "Third document. Document number three.",
            "Number four. This is the fourth document.",
            "And finally, the fifth document."
        ],
        "es": [
            "Este es el primer documento.",
            "Este es el segundo documento.",
            "Tercer documento. Documento número tres.",
            "Número cuatro. Este es el cuarto documento.",
            "Y finalmente, el quinto documento."
        ],
        "fr": [
            "Ceci est le premier document.",
            "Ceci est le deuxième document.",
            "Troisième document. Document numéro trois.",
            "Numéro quatre. Ceci est le quatrième document.",
            "Et enfin, le cinquième document."
        ]
    }
    # Encode text documents using OpenAI's text embeddings model
    encoded_docs = {lang: [] for lang in text_docs}
    for lang, docs in text_docs.items():
        for text in docs:
            prompt = f"{model_prompt}{lang}:{text}"
            result = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024)
            encoded_doc = result.choices[0].text.strip()
            encoded_docs[lang].append(encoded_doc)
    # Add encoded documents to the Pinecone index with LSH
    pinecone_index.upsert(ids=list(range(len(text_docs["en"]))), embeddings=encoded_docs["en"])
    pinecone_index.create_index(metric="cosine_similarity", shards=1, engine="lsh", num_replicas=1)

# Define a function to perform a similarity search with LSH and document ranking
def perform_search(query, language):
    # Encode query using OpenAI's text embeddings model
    prompt = f"{model_prompt}{language}:{query}"
    result = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024)
    encoded_query = result.choices[0].text.strip()
    # Perform similarity search with LSH
    results = pinecone_index.query(queries=[encoded_query], top_k=5)
    # Rank search results based on relevance to query
    ranked_results = []
    for idx, score in zip(results["ids"][0], results["scores"][0]):
        doc = {"id": idx, "score": score, "language": language}
        ranked_results.append(doc)
    ranked_results = sorted(ranked_results, key=lambda x: x["score"], reverse=True)
    return ranked_results

# Create the index
create_index()

# Perform a search and print the results
query = "fifth"
language = "en"
results = perform_search(query, language)
print(f"Search results for query '{query}' in {language}:")
for i, result in enumerate(results):
    print(f"{i+1}. Document {result['id']+1} (score: {result['score']:.
