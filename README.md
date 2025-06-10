## Documentation reference https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html

TL;DR of steps
```
 > run-llama-server.sh (a script that runs "step 2 using a container")
 > source .venv/bin/activate
 > which python (making sure it points to .venv)
 > uv pip install -r requirements.txt  (the important bit. it's putting llama-stack-client, fire and requests into /.venv)  
 > llama-stack-client inference chat-completion --message "tell me a joke"
 > uv run python rag_agent.py (the rag demo step I will modify and play around with)
```

## Expected result of the simple test
```
inference> Based on the provided knowledge graph, I can infer that the following are the key points about the infrastructure elements of the Ansible Edge GitOps pattern:

1. **Ansible Automation Platform**: A fully functional installation of the Ansible Automation Platform operator is installed on the OpenShift cluster to configure and maintain the VMs for this demo.
2. **OpenShift Virtualization**: OpenShift Virtualization is a Kubernetes-native way to run virtual machine workloads, used in this pattern to host VMs simulating an edge environment.
3. **HashiCorp Vault**: HashiCorp Vault is used as the authoritative source for the Kiosk ssh pubkey via the External Secrets Operator.
4. **Inductive Automation Ignition**: The goal of this pattern is to configure 2 VMs running Firefox in Kiosk mode displaying the demo version of the Ignition application running in a podman container.

These points highlight the key infrastructure elements that are used in the Ansible Edge GitOps pattern, including the use of Ansible Automation Platform, OpenShift Virtualization, HashiCorp Vault, and Inductive Automation Ignition.
```