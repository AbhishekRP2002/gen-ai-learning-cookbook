import os
import sys
import logging
import nest_asyncio
from dotenv import load_dotenv
import tiktoken
from pprint import pprint
from firecrawl import FirecrawlApp
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.core import Settings
from llama_index.core import Document, VectorStoreIndex


load_dotenv()
nest_asyncio.apply()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
Settings.tokenizer = tiktoken.encoding_for_model("gpt-4-turbo").encode
token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)
Settings.callback_manager = CallbackManager([token_counter])



def website_scrape_firecrawl():
    # Initialize FireCrawlWebReader to crawl a website
    app = FirecrawlApp( api_key = os.getenv("FIRECRAWL_API_KEY"))
    # firecrawl_reader = FireCrawlWebReader(
    #     api_key = os.getenv("FIRECRAWL_API_KEY"), 
    #     mode="crawl", 
    #     params={
    #         'crawlerOptions': {
    #             'excludes': ['blog/*'],
    #             'includes': [], # leave empty for all pages
    #             'limit': 100,
    #             'generateImgAltText': True,
    #             'returnOnlyUrls': True,
    #             'maxDepth': 2,
    #         },
    #         'pageOptions': {
    #             'onlyMainContent': True,
    #             "includeHtml":False
    #         }
    #             }
    # )
    
    crawl_url = "http://paulgraham.com/"
    params={
            'crawlerOptions': {
                'excludes': ['blog/*'],
                'includes': [], # leave empty for all pages
                'limit': 100,
                'generateImgAltText': True,
                'returnOnlyUrls': True,
                'maxDepth': 2,
            }
                }
    crawl_result = app.crawl_url(crawl_url, params=params, wait_until_done=True, timeout=5)
    pprint(crawl_result)
    # documents = firecrawl_reader.load_data(url="http://paulgraham.com/")
    documents = [Document(text=t) for t in list(crawl_result)]
    # for idx, doc in enumerate(documents):
    #     pprint(doc['sourceURL'])
    index = VectorStoreIndex.from_documents(documents)

    # Set Logging to DEBUG for more detailed outputs
    query_engine = index.as_query_engine()
    response = query_engine.query("List all the urls in which the author talks about Lisp.")
    print("\nThe answer is :", response)
    
    
if __name__ == "__main__":
    website_scrape_firecrawl()
