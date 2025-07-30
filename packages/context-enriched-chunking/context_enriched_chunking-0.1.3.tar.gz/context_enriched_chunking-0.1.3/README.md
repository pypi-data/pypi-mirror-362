# Context-Enriched Chunking

A text chunking strategy that keeps document title and section as headers for each chunk.

```python
from context_enriched_chunking import ContextEnrichedChunking

text = "Any text"
splitter = ContextEnrichedChunking(section_max_words=10, chunk_size=1000, chunk_overlap=100)
splitter.split_text(text, title)
```

Prompt para geração de palavras-chave:

```
Você é um assistente de inteligência artificial que extrai palavras-chave de uma resposta, e essas palavras-chave devem conter as informações mais importantes da resposta, sem as quais a resposta estaria incorreta.
Todas as palavras-chave devem ser substrings contidas na resposta.
É necessário gerar um mínimo de uma e um máximo de quatro palavras-chave.
As palavras-chave devem estar em uma única linha separadas por ;
Pergunta: {question}
Resposta: {answer}
Palavras-chave: 
```

.env

```
OPENAI_API_KEY=
LLM_EVALUATOR=gpt-4o-mini
RAGAS_DO_NOT_TRACK=true
```

python3 evaluate/generate_embeddings.py cec,recursive,token,semantic

python3 evaluate/generate_answers.py gpt-4o-mini-2024-07-18,deepseek-r1:8b,llama3.1:8b [--n_questions=20] [--overwrite]

python3 evaluate/generate_answers.py gpt-4o,llama3-1-8b-instruct-v1,llama3-1-405b-instruct-v1,llama3-1-70b-instruct-v1 => ATENÇÃO REMOVI 70B

gpt, ollama, or evaluate/custom_llm.load_custom_llm(model_name)

python3 evaluate/evaluate.py [--overwrite]

# Publicando

editar pyproject.toml e setup.py com nova versão

pip install -e .

python3 -m build
twine upload dist/*
