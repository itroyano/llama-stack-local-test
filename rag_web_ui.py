from flask import Flask, render_template, request, jsonify, stream_template
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.types import Document
import uuid
import threading
import time

app = Flask(__name__)

# Global variables to store the RAG agent and session
rag_agent: Agent = None
session_id = None
vector_db_id = None
initialization_status = {"status": "not_started", "progress": 0, "message": ""}

def initialize_rag_agent():
    """Initialize the RAG agent with all ValidatedPatterns documents"""
    global rag_agent, session_id, vector_db_id, initialization_status
    
    try:
        initialization_status.update({"status": "initializing", "progress": 10, "message": "Connecting to Llama Stack..."})
        
        client = LlamaStackClient(base_url="http://localhost:8321")
        
        # Create a vector database instance
        embed_lm = next(m for m in client.models.list() if m.model_type == "embedding")
        embedding_model = embed_lm.identifier
        vector_db_id = f"v{uuid.uuid4().hex}"
        client.vector_dbs.register(
            vector_db_id=vector_db_id,
            embedding_model=embedding_model,
        )
        
        initialization_status.update({"status": "initializing", "progress": 20, "message": "Creating document index..."})
        
        # Create Documents from all validatedpatterns repositories and key content
        documents = []
        doc_id = 0

        # Core documentation repository content
        docs_content = [
            "README.md", "config.yaml", "Makefile", "LICENSE",
            "content/getting-started.md", "content/patterns/index.md",
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
            "content/learn/index.md", "content/learn/concepts.md", "content/learn/workflows.md",
            "content/contributing/index.md", "content/contributing/development.md",
            "content/contributing/patterns.md", "content/blog/index.md",
            "content/workshop/index.md", "content/status/index.md",
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

        initialization_status.update({"status": "initializing", "progress": 30, "message": "Adding multicloud-gitops pattern..."})

        # Multicloud GitOps pattern repository
        multicloud_gitops_files = [
            "README.md", "pattern-metadata.yaml", "values-global.yaml", "values-hub.yaml",
            "values-secret.yaml.template", "pattern.sh", "Makefile", "ansible.cfg", "LICENSE",
            "charts/hub/values.yaml", "charts/hub/Chart.yaml", "common/scripts/deploy.sh",
            "common/scripts/install.sh", "overrides/README.md", "tests/interop/README.md",
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

        initialization_status.update({"status": "initializing", "progress": 50, "message": "Adding ansible-edge-gitops pattern..."})

        # Ansible Edge GitOps pattern repository
        ansible_edge_gitops_files = [
            "README.md", "pattern-metadata.yaml", "values-global.yaml", "values-hub.yaml",
            "values-secret.yaml.template", "pattern.sh", "Makefile", "ansible.cfg", "LICENSE",
            "Changes.md", "ansible/README.md", "ansible/inventory/group_vars/all.yml",
            "ansible/playbooks/deploy.yml", "common/scripts/deploy.sh", "common/scripts/install.sh",
            "overrides/README.md", "scripts/setup.sh", "diagrams/README.md",
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

        initialization_status.update({"status": "initializing", "progress": 70, "message": "Adding additional patterns and utilities..."})

        # Add more patterns (abbreviated for space)
        other_patterns = ["retail-dataset-pattern", "medical-diagnosis", "industrial-edge"]
        for pattern in other_patterns:
            pattern_files = ["README.md", "values-global.yaml", "values-hub.yaml", "pattern.sh", "LICENSE"]
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

        initialization_status.update({"status": "initializing", "progress": 80, "message": f"Indexing {len(documents)} documents..."})

        # Insert documents
        client.tool_runtime.rag_tool.insert(
            documents=documents,
            vector_db_id=vector_db_id,
            chunk_size_in_tokens=512,
        )

        initialization_status.update({"status": "initializing", "progress": 90, "message": "Creating RAG agent..."})

        # Get the model being served
        llm = next(m for m in client.models.list() if m.model_type == "llm")
        model = llm.identifier

        # Create the RAG agent
        rag_agent = Agent(
            client,
            model=model,
            instructions="You are a helpful assistant specialized in Validated Patterns. Use the RAG tool to answer questions about validated patterns, their architecture, installation, configuration, and usage. You have access to comprehensive documentation from the validatedpatterns organization including all major patterns like multicloud-gitops, ansible-edge-gitops, multicluster-devsecops, and many others. Provide clear, accurate, and helpful responses based on the documentation.",
            tools=[
                {
                    "name": "builtin::rag/knowledge_search",
                    "args": {"vector_db_ids": [vector_db_id]},
                }
            ],
        )

        session_id = rag_agent.create_session(session_name=f"web_session_{uuid.uuid4().hex}")
        
        initialization_status.update({
            "status": "ready", 
            "progress": 100, 
            "message": f"RAG agent ready! Indexed {len(documents)} documents from ValidatedPatterns ecosystem."
        })
        
    except Exception as e:
        initialization_status.update({
            "status": "error", 
            "progress": 0, 
            "message": f"Error initializing RAG agent: {str(e)}"
        })

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/initialize', methods=['POST'])
def initialize():
    """Start the RAG agent initialization in a background thread"""
    global initialization_status
    
    if initialization_status["status"] not in ["not_started", "error"]:
        return jsonify(initialization_status)
    
    # Start initialization in background thread
    thread = threading.Thread(target=initialize_rag_agent)
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "starting", "message": "Initialization started..."})

@app.route('/api/status')
def status():
    """Get the current initialization status"""
    return jsonify(initialization_status)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return RAG agent responses"""
    global rag_agent, session_id
    
    if initialization_status["status"] != "ready":
        return jsonify({"error": "RAG agent not ready. Please initialize first."}), 400
    
    try:
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get response from RAG agent using non-streaming for simpler text extraction
        response = rag_agent.create_turn(
            messages=[{"role": "user", "content": user_message}], 
            session_id=session_id, 
            stream=False
        )
        
        # Extract the response text from the output message
        response_text = response.output_message.content if response.output_message else ""
        
        return jsonify({
            "response": response_text if response_text else "I apologize, but I couldn't generate a response. Please try rephrasing your question.",
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

@app.route('/api/examples')
def examples():
    """Return example questions users can ask"""
    return jsonify({
        "examples": [
            "What are the infrastructure elements of the multicloud-gitops pattern?",
            "How do I install the ansible-edge-gitops pattern?",
            "What Red Hat technologies are used in these patterns?",
            "What patterns are available in the validatedpatterns organization?",
            "How do I customize a validated pattern for my environment?",
            "What is the architecture of the multicluster-devsecops pattern?"
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting ValidatedPatterns RAG Web Interface...")
    print("📋 Navigate to http://localhost:8080 to interact with the RAG agent")
    print("⚠️  Make sure Ollama and Llama Stack server are running first!")
    app.run(debug=True, host='0.0.0.0', port=8080)
