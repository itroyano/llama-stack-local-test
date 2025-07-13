# Llama Stack Local Test - Comprehensive ValidatedPatterns RAG Agent

A comprehensive RAG (Retrieval-Augmented Generation) agent built with Llama Stack that provides expert knowledge about Red Hat's ValidatedPatterns ecosystem.

## 📋 Documentation Reference 
https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html

## 🚀 Quick Start

### Prerequisites
- Ollama installed and running
- Python environment set up

### Setup Steps
```bash
# 1. Start Ollama service
ollama serve

# 2. Start Llama Stack server
./run-llama-server.sh

# 3. Set up Python environment
source .venv/bin/activate
which python  # Ensure it points to .venv
uv pip install -r requirements.txt

# 4. Test basic functionality
llama-stack-client inference chat-completion --message "tell me a joke"

# 5. Run the comprehensive ValidatedPatterns RAG agent
uv run python rag_agent.py
```

## 🎯 What the RAG Agent Does

The RAG agent indexes documents from the ValidatedPatterns ecosystem, creating a comprehensive knowledge base that includes:

### 📚 **Core Documentation** (validatedpatterns/docs)
- Getting started guides, pattern documentation
- Learning resources and contributing guidelines  
- Blog posts, workshop materials, and status pages

### 📦 **Major Pattern Repositories**
- **multicloud-gitops** - Multi-cloud GitOps management
- **ansible-edge-gitops** - Edge device management with Ansible
- **multicluster-devsecops** - DevSecOps across clusters

### 🛠️ **Common Utilities** (validatedpatterns/common)
- Shared scripts, deployment tools, and utilities
- Ansible configurations and automation scripts

### 🔧 **Additional Patterns**
- retail-dataset-pattern, medical-diagnosis, industrial-edge
- connected-vehicle-architecture, manufacturing-dev-environment
- autonomous-vehicle-pattern, datacenter-gpu-pattern
- edge-ai-pattern, validated-patterns-operator

### 📋 **Pattern Catalog**
- Metadata definitions and catalog specifications
- Pattern organization and classification

## 📤 Expected Output

The RAG agent demonstrates its knowledge by answering 6 comprehensive questions:

```
user> What are the infrastructure Elements of this Pattern?

The multicloud-gitops pattern is a set of best practices and tools that help organizations manage their GitOps workflow across multiple cloud providers. The key elements of this pattern include:

1. **Git Repository Management**: Centralized management of Git repositories for all applications and services.
2. **CI/CD Pipelines**: Automated build, test, and deployment pipelines for each application.
3. **Infrastructure as Code (IaC)**: Definition of infrastructure using tools like Terraform or CloudFormation.
4. **Cloud Provider Integration**: Integration with multiple cloud providers such as AWS, GCP, Azure, and others.
5. **Monitoring and Logging**: Real-time monitoring and logging of application performance and errors.
6. **Security and Identity Management**: Secure access control and identity management for users and applications.
7. **Continuous Integration and Delivery**: Automated testing and deployment of code changes to production environments.
```

```
user> What patterns are available in the validatedpatterns organization?

multicloud-gitops, ansible-edge-gitops, multicluster-devsecops
```

```
user> How do I install the multicloud-gitops pattern?

To install the `multicloud-gitops` pattern, follow these steps:

1. **Fork the repository**: Fork the `multicloud-gitops` repository from GitHub to your own account.
2. **Update the `values-global.yaml` file**: Update the `values-global.yaml` file with your desired configuration settings, such as cluster names, replicas, and platform types.
3. **Create a `cluster-group-<group-name>.yaml` file**: Create a new file in the same directory as `values-global.yaml`, e.g., `cluster-group-hub.yaml`. Update this file with your desired cluster group configuration.
4. **Run `oc apply -f values-global.yaml`**: Run the command `oc apply -f values-global.yaml` to apply the global configuration settings.
5. **Run `oc apply -f cluster-group-<group-name>.yaml`**: Run the command `oc apply -f cluster-group-hub.yaml` to apply the cluster group configuration.
6. **Verify installation**: Verify that the pattern has been installed successfully by checking the OpenShift console or using the `oc` command-line tool.
```

```
user> What is the architecture of the ansible-edge-gitops pattern?

The Ansible Edge GitOps pattern is an OpenShift-based solution that uses Ansible for automation and configuration management. The architecture consists of:

1. **Hub**: The central component providing centralized location for managing Ansible configurations and workflows.
2. **Compute**: The compute layer providing underlying infrastructure for running Ansible workloads.
3. **Control Plane**: Management and orchestration capabilities including cluster creation, scaling, and monitoring.
4. **Ansible Automation Platform (AAP)**: Centralized platform for managing Ansible configurations and workflows.
5. **OpenShift Virtualization**: Virtual machines and containers for running Ansible workloads.

Key features include:
- **Configuration-as-Code**: Ansible configurations stored in version control
- **Modular Architecture**: Customizable and extensible solution
- **OpenShift Support**: Supports OpenShift 4.12 and later versions
```

```
user> What Red Hat technologies are used in these patterns?

Based on the patterns, the following Red Hat technologies are used:

1. **Red Hat Advanced Cluster Management**: Managed platform for managing clusters across multiple clouds
2. **Red Hat OpenShift GitOps**: Open-source tool for managing GitOps workflows in Kubernetes
3. **OpenShift Serverless**: Serverless computing platform for building and deploying applications
4. **OpenDataHub**: Open-source data management platform for centralized data repository
5. **Hashicorp Vault**: Secrets management tool for secure storage of sensitive data
6. **Red Hat OpenShift**: Container application platform with comprehensive Kubernetes tools
```

```
user> How do I customize a validated pattern for my environment?

To customize a validated pattern for your environment, follow these steps:

1. **Understand the pattern**: Study the documentation, code, and configuration files
2. **Identify customization points**: Look for areas to customize (configuration parameters, resource types, service templates)
3. **Create a fork**: Clone the pattern repository and create a new branch
4. **Modify configuration files**: Edit values.yaml, configmap.yaml, and template files
5. **Update clusterGroup configuration**: Modify cluster names, node types, and service configurations
6. **Test and validate**: Run the pattern in a test environment
7. **Push changes**: Push to your forked repository
8. **Submit pull request**: Request maintainers review and merge changes

**Example customization:**
- Edit `values.yaml` to change cloud provider from GCP to AWS
- Update `clusterGroup` configuration with AWS-specific settings
- Modify node types and regional settings
```

## 🎨 Features

- **147 Documents Indexed**: Comprehensive coverage of the ValidatedPatterns ecosystem
- **Semantic Search**: Intelligent RAG-based question answering
- **Real-time Responses**: Interactive Q&A with contextual understanding
- **Expert Knowledge**: Deep insights into installation, architecture, and customization
- **Multi-Pattern Support**: Knowledge spanning all major validated patterns

## 🛠️ Technical Details

- **Vector Database**: FAISS with SQLite backend for efficient similarity search
- **Embedding Model**: `all-minilm:latest` for document vectorization
- **LLM**: `llama3.2:3b` for response generation
- **Chunk Size**: 512 tokens for optimal context retrieval
- **Document Sources**: Direct GitHub raw file URLs for up-to-date content

## 📈 Performance Metrics

- **Document Ingestion**: ~2 minutes for 147 documents
- **Query Response Time**: 5-30 seconds depending on complexity
- **Context Retrieval**: Top 5 relevant chunks per query
- **Memory Usage**: ~2GB for full knowledge base

## 🔧 Customization

To modify the questions or add new patterns:

1. Edit the `turns` array in `rag_agent.py`
2. Add new document sources to the respective content arrays
3. Adjust chunk size or retrieval parameters as needed
4. Restart the agent to apply changes

## 🤝 Contributing

This RAG agent demonstrates comprehensive knowledge management for the ValidatedPatterns ecosystem. It serves as a foundation for building production-ready pattern recommendation and support systems.