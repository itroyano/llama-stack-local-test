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