##### Tabular Data or Structured Data Understanding and Reasoning with LLMs

- how do llms interpret tabular or structured data ?

  - llms cannot handle tabular data inherently.
  - linearization issues - column positioning / localization

    ![1716121756268](image/notes/1716121756268.png)
  - ![1716121908586](image/notes/1716121908586.png)
  - use hybrid method - textual + symbolic reasoning

  1. convert the table to markdown format or any other textual format and then feed into the llms
  2. convert the structured data into semi-structured data formats like json
  3. to improve the reasoning, we can leverage few-shot samples or cot reasoning
- implement multi-reasoning in multiple finite steps to leverage the structural tabular format in reasoning.
- two types of reasoning that can be deduced from Tabular data:

  1. generic reasoning : leverage textual understanding to get the final response
  2. program-aided reasoning : leverage a programmatic approach ( text-2-sql or text-2-pandas or PandasQueryEngine in llama-index , binder)

     ![1716120951448](image/notes/1716120951448.png)
  3. ![1716121165763](image/notes/1716121165763.png)
- **QA Over Tabular Data**
