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

# Create Documents from all validatedpatterns repositories and key content
documents = []
doc_id = 0

# Core documentation repository content
docs_content = [
    # Main documentation files
    "README.md",
    "config.yaml",
    "Makefile",
    "LICENSE",
    
    # Content directory - main documentation
    "content/getting-started.md",
    "content/patterns/index.md",
    "content/patterns/multicloud-gitops/index.md",
    "content/patterns/multicloud-gitops/getting-started.md",
    "content/patterns/multicloud-gitops/installation.md",
    "content/patterns/multicloud-gitops/architecture.md",
    "content/patterns/ansible-edge-gitops/index.md",
    "content/patterns/ansible-edge-gitops/getting-started.md",
    "content/patterns/ansible-edge-gitops/installation.md",
    "content/patterns/ansible-edge-gitops/architecture.md",
    "content/patterns/multicluster-devsecops/index.md",
    "content/patterns/multicluster-devsecops/getting-started.md",
    "content/patterns/multicluster-devsecops/installation.md",
    "content/patterns/multicluster-devsecops/architecture.md",
    "content/learn/index.md",
    "content/learn/concepts.md",
    "content/learn/workflows.md",
    "content/contributing/index.md",
    "content/contributing/development.md",
    "content/contributing/patterns.md",
    "content/blog/index.md",
    "content/workshop/index.md",
    "content/status/index.md",
]

# Add docs repository content
for content_path in docs_content:
    documents.append(
        Document(
            document_id=f"doc-{doc_id}",
            content=f"https://raw.githubusercontent.com/validatedpatterns/docs/main/{content_path}",
            mime_type="text/plain",
            metadata={"source": "docs", "type": "documentation", "path": content_path},
        )
    )
    doc_id += 1

# Multicloud GitOps pattern repository
multicloud_gitops_files = [
    "README.md",
    "pattern-metadata.yaml",
    "values-global.yaml",
    "values-hub.yaml",
    "values-secret.yaml.template",
    "pattern.sh",
    "Makefile",
    "ansible.cfg",
    "LICENSE",
    "charts/hub/values.yaml",
    "charts/hub/Chart.yaml",
    "common/scripts/deploy.sh",
    "common/scripts/install.sh",
    "overrides/README.md",
    "tests/interop/README.md",
]

for file_path in multicloud_gitops_files:
    documents.append(
        Document(
            document_id=f"doc-{doc_id}",
            content=f"https://raw.githubusercontent.com/validatedpatterns/multicloud-gitops/main/{file_path}",
            mime_type="text/plain",
            metadata={"source": "multicloud-gitops", "type": "pattern", "path": file_path},
        )
    )
    doc_id += 1

# Ansible Edge GitOps pattern repository
ansible_edge_gitops_files = [
    "README.md",
    "pattern-metadata.yaml",
    "values-global.yaml",
    "values-hub.yaml",
    "values-secret.yaml.template",
    "pattern.sh",
    "Makefile",
    "ansible.cfg",
    "LICENSE",
    "Changes.md",
    "ansible/README.md",
    "ansible/inventory/group_vars/all.yml",
    "ansible/playbooks/deploy.yml",
    "common/scripts/deploy.sh",
    "common/scripts/install.sh",
    "overrides/README.md",
    "scripts/setup.sh",
    "diagrams/README.md",
]

for file_path in ansible_edge_gitops_files:
    documents.append(
        Document(
            document_id=f"doc-{doc_id}",
            content=f"https://raw.githubusercontent.com/validatedpatterns/ansible-edge-gitops/main/{file_path}",
            mime_type="text/plain",
            metadata={"source": "ansible-edge-gitops", "type": "pattern", "path": file_path},
        )
    )
    doc_id += 1

# Multicluster DevSecOps pattern repository
multicluster_devsecops_files = [
    "README.md",
    "values-global.yaml",
    "values-hub.yaml",
    "values-development.yaml",
    "values-production.yaml",
    "values-all-in-one.yaml",
    "values-secret.yaml.template",
    "pattern.sh",
    "Makefile",
    "ansible.cfg",
    "LICENSE",
    "charts/hub/values.yaml",
    "charts/hub/Chart.yaml",
    "common/scripts/deploy.sh",
    "common/scripts/install.sh",
    "overrides/README.md",
    "scripts/setup.sh",
    "containerFiles/README.md",
]

for file_path in multicluster_devsecops_files:
    documents.append(
        Document(
            document_id=f"doc-{doc_id}",
            content=f"https://raw.githubusercontent.com/validatedpatterns/multicluster-devsecops/main/{file_path}",
            mime_type="text/plain",
            metadata={"source": "multicluster-devsecops", "type": "pattern", "path": file_path},
        )
    )
    doc_id += 1

# Common utilities repository
common_files = [
    "README.md",
    "Changes.md",
    "LICENSE",
    "Makefile",
    "requirements.yml",
    "scripts/README.md",
    "scripts/deploy.sh",
    "scripts/install.sh",
    "scripts/pattern-util.sh",
    "scripts/utilities.sh",
    ".ansible-lint",
    ".gitleaks.toml",
]

for file_path in common_files:
    documents.append(
        Document(
            document_id=f"doc-{doc_id}",
            content=f"https://raw.githubusercontent.com/validatedpatterns/common/main/{file_path}",
            mime_type="text/plain",
            metadata={"source": "common", "type": "utilities", "path": file_path},
        )
    )
    doc_id += 1

# Other pattern repositories - add key files from additional patterns
other_patterns = [
    "retail-dataset-pattern",
    "medical-diagnosis", 
    "industrial-edge",
    "connected-vehicle-architecture",
    "manufacturing-dev-environment",
    "autonomous-vehicle-pattern",
    "datacenter-gpu-pattern",
    "edge-ai-pattern",
    "validated-patterns-operator",
]

# Add key files from other patterns
for pattern in other_patterns:
    pattern_files = [
        "README.md",
        "values-global.yaml",
        "values-hub.yaml",
        "pattern.sh",
        "Makefile",
        "LICENSE",
    ]
    
    for file_path in pattern_files:
        documents.append(
            Document(
                document_id=f"doc-{doc_id}",
                content=f"https://raw.githubusercontent.com/validatedpatterns/{pattern}/main/{file_path}",
                mime_type="text/plain",
                metadata={"source": pattern, "type": "pattern", "path": file_path},
            )
        )
        doc_id += 1

# Patterns catalog
catalog_files = [
    "README.md",
    "catalog.yaml",
    "default-patterncatalogsource.yaml",
]

for file_path in catalog_files:
    documents.append(
        Document(
            document_id=f"doc-{doc_id}",
            content=f"https://raw.githubusercontent.com/validatedpatterns-sandbox/patterns-catalog/main/{file_path}",
            mime_type="text/plain",
            metadata={"source": "patterns-catalog", "type": "catalog", "path": file_path},
        )
    )
    doc_id += 1

print(f"Created {len(documents)} documents for ingestion")

# Insert documents
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=512,
)

print(f"Inserted {len(documents)} documents into vector database")

# Get the model being served
llm = next(m for m in client.models.list() if m.model_type == "llm")
model = llm.identifier

# Create the RAG agent
rag_agent = Agent(
    client,
    model=model,
    instructions="You are a helpful assistant specialized in Validated Patterns. Use the RAG tool to answer questions about validated patterns, their architecture, installation, configuration, and usage. You have access to comprehensive documentation from the validatedpatterns organization including all major patterns like multicloud-gitops, ansible-edge-gitops, multicluster-devsecops, and many others.",
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {"vector_db_ids": [vector_db_id]},
        }
    ],
)

session_id = rag_agent.create_session(session_name=f"s{uuid.uuid4().hex}")

turns = [
    "What are the infrastructure Elements of this Pattern?",
    "What patterns are available in the validatedpatterns organization?",
    "How do I install the multicloud-gitops pattern?",
    "What is the architecture of the ansible-edge-gitops pattern?",
    "What Red Hat technologies are used in these patterns?",
    "How do I customize a validated pattern for my environment?",
]

for t in turns:
    print("user>", t)
    stream = rag_agent.create_turn(
        messages=[{"role": "user", "content": t}], session_id=session_id, stream=True
    )
    for event in AgentEventLogger().log(stream):
        event.print()
    print("\n" + "="*80 + "\n")