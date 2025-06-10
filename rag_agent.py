from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent, AgentEventLogger
from llama_stack_client.types import Document
import uuid

client = LlamaStackClient(base_url="http://localhost:8321")

# Create a vector database instance
embed_lm = next(m for m in client.models.list() if m.model_type == "embedding")
embedding_model = embed_lm.identifier
vector_db_id = f"v{uuid.uuid4().hex}"
client.vector_dbs.register(
    vector_db_id=vector_db_id,
    embedding_model=embedding_model,
)

# Create Documents
urls = [
    "getting-started.adoc",
]
documents = [
    Document(
        document_id=f"num-{i}",
        content=f"https://raw.githubusercontent.com/validatedpatterns/docs/refs/heads/main/content/patterns/ansible-edge-gitops/{url}",
        mime_type="text/plain",
        metadata={},
    )
    for i, url in enumerate(urls)
]

# Insert documents
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=512,
)

# Get the model being served
llm = next(m for m in client.models.list() if m.model_type == "llm")
model = llm.identifier

# Create the RAG agent
rag_agent = Agent(
    client,
    model=model,
    instructions="You are a helpful assistant. Use the RAG tool to answer questions as needed.",
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {"vector_db_ids": [vector_db_id]},
        }
    ],
)

session_id = rag_agent.create_session(session_name=f"s{uuid.uuid4().hex}")

turns = ["what are the infrastructure Elements of this Pattern?",]

for t in turns:
    print("user>", t)
    stream = rag_agent.create_turn(
        messages=[{"role": "user", "content": t}], session_id=session_id, stream=True
    )
    for event in AgentEventLogger().log(stream):
        event.print()