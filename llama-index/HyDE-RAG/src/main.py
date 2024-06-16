import logging
import os
import sys
import csv
import chromadb
from rich.pretty import pprint
import modin.pandas as pd
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline  # noqa
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,  # noqa
    KeywordExtractor,
)
from llama_index.embeddings.openai import OpenAIEmbedding  # noqa

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
pd.set_option("display.max_columns", None)
csv.field_size_limit(sys.maxsize)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    file_path = "data"
    df = pd.read_csv("data/podcastdata.csv")
    pprint(df.shape)
    df = df.head(1)
    # 1. load the data
    documents = [
        Document(
            text=row["text"],
            metadata={
                "guest": row["guest"],
                "title": row["title"],
            },
        )
        for index, row in df.iterrows()
    ]
    pprint(len(documents))
    pprint(documents[0])
    # 2. transform the data and create the index
    text_splitter = SentenceSplitter(chunk_overlap=20, chunk_size=1024)
    title_extractor = TitleExtractor(nodes=5)
    keywords_extractor = KeywordExtractor(nodes=3)
    index = VectorStoreIndex.from_documents(
        documents=documents,
        transformations=[text_splitter, title_extractor, keywords_extractor],
    )

    # 3. store the index in a vector db of your choice
    db = chromadb.PersistentClient(path="./chroma_db")
