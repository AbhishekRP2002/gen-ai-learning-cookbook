import pandas as pd
from rich.pretty import pprint
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


#TODO: Test other embeddings models
def create_embeddings(df: pd.DataFrame):
    global encoder_model
    encoder_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    try:
        text = df["Sentence"]
        embeddings = encoder_model.encode(text)
    except Exception as e:
        print(e)
        return None
    
    return embeddings
    

#TODO: Understand the different type of indexes in FAISS and how they affect the results
def create_index(embeddings, type: str = "L2"):
    index = None
    if type == "L2":
        index = faiss.IndexFlatL2(embeddings.shape[1])
    elif type == "IP":
        index = faiss.IndexFlatIP(embeddings.shape[1])
    
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    return index


#TODO: What is an index, how does it work and how it helps in effective search results
# Check all variables data type to understand the return types
def search_index(index, search_vector, k=10):
    _vector = np.array([search_vector])
    faiss.normalize_L2(_vector)
    distances, ann = index.search(_vector, k)
    results_df = pd.DataFrame(
        {
            "Distance": distances[0],
            "Index": ann[0]
        }
    
    )
    return results_df

if __name__ == "__main__":
    df = pd.read_excel("openai/dataset/test_data.xlsx")
    pprint(df.columns)
    pprint(df.shape)
    embeddings = create_embeddings(df)
    pprint(embeddings.shape)
    # create the FAISS index
    index = create_index(embeddings=embeddings, type="L2")
    search_query = "FAISS Library research paper introduces an efficient semantic search algorithm for dense vectors"
    search_vector = encoder_model.encode(search_query)
    # search the index
    results_df = search_index(index, search_vector, k=index.ntotal)
    merged_df = pd.merge(results_df, df, left_on='Index', right_index=True)
    pprint(merged_df)
    pprint(merged_df.iloc[0].Sentence)
    exit()