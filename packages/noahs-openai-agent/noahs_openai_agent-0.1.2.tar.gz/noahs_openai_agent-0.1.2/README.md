## Usage: `noahs_openai_agent`

This library wraps interactions with a **local Ollama server** and provides tools for:

- Maintaining a conversation history
- Calling a local LLM via the Ollama REST API
- Performing semantic text splitting and search
- Running local SQL-style lookups
- Extracting and analyzing URLs from text

### Getting Started

First, install the library:

```bash
pip install noahs_openai_agent
```

```python
from noahs_openai_agent import ChatAgent

# 1. initialize agent
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
agent = ChatAgent(name="Tomatio", api_key=OPENAI_API_KEY)

# 2. (optional) purge semantic database for fresh start
agent.semantic_db.purge_collection();

# 3. upload txt document of your choosing in chunks of 5 sentences to the semantic database
doc_name = "docs/AliceInWonderland.txt"
agent.upload_document(doc_name, max_sentences_per_chunk=5)

# 4. do a semantic search for 5 relevent passages to a semantic_query and add it to the context window of the agent
semantic_query = "Interactions between Alice and the Mad Hatter"
semantic_contextualize_prompt = f"These are some passages from {doc_name} that should be considered"
agent.discuss_document(semantic_query, doc_name="AliceInWonderland.txt", semantic_top_k=5, semantic_contextualize_prompt=semantic_contextualize_prompt)

# 5. start the chat with a question about the uploaded content.
message = "Tell me about the relationship between Alice and the Mad Hatter. Use examples from the provided passages"
response_stream = agent.chat(message)
print("\n")
print(f"You: {message}")
print(agent.name, end=": ")
agent.print_stream(response_stream)

print("\n")
print("Continue to basic chat...")
print("\n")

while message not in ["bye","goodbye","exit","quit"]:
    message = input("You: ")
    response_stream = agent.chat(message)
    print(agent.name, end=": ")
    agent.print_stream(response_stream)
    print("\n")




```



### Check out Source Code

`https://github.com/jonesnoah45010/openai_agent`




