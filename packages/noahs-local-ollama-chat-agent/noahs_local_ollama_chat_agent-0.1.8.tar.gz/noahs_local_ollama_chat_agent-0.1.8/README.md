## Usage: `noahs_local_ollama_chat_agent`

This library wraps interactions with a **local Ollama server** and provides tools for:

- Maintaining a conversation history
- Calling a local LLM via the Ollama REST API
- Performing semantic text splitting and search
- Running local SQL-style lookups
- Extracting and analyzing URLs from text

### Getting Started

First, install the library (after uploading to PyPI):

```bash
pip install noahs_local_ollama_chat_agent
```

```python
from noahs_local_ollama_chat_agent import ollama_chat_agent

#  Analyze a document without having to upload entire document into context window

# 1. create agent, ollama api must be running in background and provided model must be installed
agent = ollama_chat_agent(name="Tomatio", model="llama3.2")

# 2. (optional) purge semantic database for fresh start
agent.semantic_db.purge_collection();

# 3. upload txt file of your choosing in chunks of 5 sentences to the semantic database
agent.upload_document("docs/AliceInWonderland.txt", max_sentences_per_chunk=5)

# 4. do a semantic search for 5 relevent passages to a semantic_query and add it to the context window of the agent
semantic_query = "Interactions between Alice and the Mad Hatter"
agent.discuss_document(semantic_query, doc_name="AliceInWonderland.txt", semantic_top_k=5)

# 5. start the chat with a question about the uploaded content.
message = "Tell me about the relationship between Alice and the Mad Hatter. Use examples from the provided passages"
response_stream = agent.chat(message)
print("\n")
print(f"You: {message}")
agent.print_stream(response_stream)



print("\n")
print("Continue to chat...")
print("\n")

while message not in ["bye","goodbye","exit","quit"]:
	message = input("You: ")
	response_stream = agent.chat(message)
	agent.print_stream(response_stream)
```



### Check out Source Code

`https://github.com/jonesnoah45010/local_ollama_chat_agent`




