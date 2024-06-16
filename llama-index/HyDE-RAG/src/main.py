import logging
import os
import sys
import csv
from rich.pretty import pprint
import modin.pandas as pd
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.readers.file import CSVReader, PandasCSVReader  # noqa
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
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
    json_data = df.to_json(orient="records")
    pprint(json_data[0])
    pprint(df.shape)
    # 1. load the data
    parser = CSVReader()
    file_extractor = {".csv": parser}
    documents = SimpleDirectoryReader(
        file_path, file_extractor=file_extractor
    ).load_data()
    pprint(len(documents))
    # 2. transform the data
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_overlap=20, chunk_size=1024),
            TitleExtractor(nodes=5),
            QuestionsAnsweredExtractor(questions=3),
            KeywordExtractor(keywords=5),
            OpenAIEmbedding(model="text-embedding-3-small"),
        ]
    )
    nodes = pipeline.run(documents)
    pprint(f"Number of nodes: {len(nodes)}")
    # index = VectorStoreIndex(
    #     nodes=nodes, embed_model=OpenAIEmbedding(model="text-embedding-3-small")
    # )
    # store the index in a Vector DB
