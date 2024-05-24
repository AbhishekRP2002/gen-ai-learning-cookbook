**Advanced Agentic RAG steps (high level):**

- *Routing* - add descision making to route requests to multiple tools
- *Tool Use* - create an interface for agents to select the tool and generate the right arguments for that tool
- *LLM Reasoning and Inference* - use an LLM to perform multi-step reasoning with the tools, while retaining the memory throughout the process, and finally generating the qualified response

**Notes:**

- given a data, first read the data with core functions like  `SimpleDirectoryReader`
- then split the data, into chunks or nodes with an appropriate chunking strategy using `node_parser` module from `llama-index`
- after chunking, we are expected to create vector embeddings of the chunks with an embedding model, It can be finetuned or pre-trained one.
  1. eg. `from llama_index.embeddings.openai                                                                                                                                                                    import OpenAIEmbedding`
- now comes the main part, we have to define custom functions which will eventually be acting as functions in support for a given tool.
  There are two ways to create Tools in llama-index, generally:
  1. FunctionTool --> use this if we have an user-defined function in place or if the underlying logic does not include LLM-generated response as the final response
  2. QueryEngineTool -> used as a wrapper on top of the QueryEngine by llama-index
- Usually, Create index --> create a query engine which will act as interface between the index and rest of the world --> create a tool on top of the query engine using `QueryEngineTool` class
- instead of the llm choosing the tool in a single shot setting, we can also define an agent reasoning loop which will help to reason tools in multiple steps. --> this is basically using multi-step reasoning to identify the right tool to use
  1. ![1716177419940](image/notes/1716177419940.png)
  2.
