# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mission

Complete the **AI Research Lab Assistant** notebooks with working code. Each notebook should be fully executable in JupyterHub with real platform services.

## Platform: 100% Self-Contained

All AI capabilities run locally on Thinkube - no external API calls:

| Capability | Service | Model |
|------------|---------|-------|
| Chat/Completion | `tkt-tensorrt-llm` → LiteLLM | GPT-OSS 20B, Llama, Qwen, Phi |
| Embeddings | `tkt-text-embeddings` → LiteLLM | nomic-embed-text-v1.5 |

Models are stored in MLflow Model Registry and mounted at runtime.

## Notebook Structure

```
thinkube-ai-examples/
├── 00-platform-validation.ipynb   # Validate 7 platform services
├── 01-register-litellm.ipynb      # Register LLM & embeddings in LiteLLM
└── research-assistant/
    ├── 02-langchain-rag.ipynb     # RAG pipeline for papers
    ├── 03-multi-agent.ipynb       # CrewAI multi-agent system
    └── 04-fine-tuning.ipynb       # Unsloth fine-tuning
```

## Current State

| Notebook | Status |
|----------|--------|
| `00-platform-validation.ipynb` | Educational framework complete |
| `01-register-litellm.ipynb` | Complete - registers models in LiteLLM |
| `02-langchain-rag.ipynb` | Structure only, needs implementation |
| `03-multi-agent.ipynb` | Structure only, needs implementation |
| `04-fine-tuning.ipynb` | Structure only, needs implementation |

## Implementation Priority

1. **00-platform-validation.ipynb** - May need fixes based on actual environment
2. **01-register-litellm.ipynb** - Should work once services are deployed
3. **02-langchain-rag.ipynb** - Core RAG pipeline (most important)
4. **03-multi-agent.ipynb** - Multi-agent with CrewAI
5. **04-fine-tuning.ipynb** - Unsloth fine-tuning (requires `tk-jupyter-fine-tuning` image)

## Platform Services

| Service | Environment Variables |
|---------|----------------------|
| LiteLLM | `LITELLM_ENDPOINT`, `LITELLM_MASTER_KEY` |
| Qdrant | `QDRANT_URL` |
| Langfuse | `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` |
| MLflow | `MLFLOW_TRACKING_URI`, `MLFLOW_AUTH_USERNAME`, `MLFLOW_AUTH_PASSWORD`, `MLFLOW_KEYCLOAK_TOKEN_URL`, `MLFLOW_KEYCLOAK_CLIENT_ID`, `MLFLOW_CLIENT_SECRET` |
| PostgreSQL | `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` |
| Valkey | `VALKEY_HOST`, `VALKEY_PORT` |
| NATS | `NATS_URL` |

## Implementation Rules

1. **No TODO stubs in final code** - Every cell must execute
2. **Use real services** - Connect to actual platform, not mocks
3. **Show real outputs** - Results should be from actual execution
4. **Document issues** - If something doesn't work, document why

## Key Libraries

For `tk-jupyter-agent-dev`:
- `langchain`, `langchain-openai`, `langchain-community`
- `crewai`
- `qdrant-client`
- `langfuse`
- `arxiv` (for paper fetching)
- `openai` (LiteLLM is OpenAI-compatible)

For `tk-jupyter-fine-tuning`:
- `unsloth`
- `peft`
- `trl`
- `mlflow`

## Testing Notebooks

To test, the notebooks need to run in JupyterHub:
1. Open JupyterHub on the Thinkube cluster
2. Select appropriate image (`tk-jupyter-agent-dev` or `tk-jupyter-fine-tuning`)
3. Upload/clone this repository
4. Run notebooks in order

## Related Documentation

- `/home/thinkube/thinkube-platform/thinkube-documentation/guides/thinkube-ai-lab-getting-started.md`
- `/home/thinkube/thinkube-platform/thinkube-documentation/IMPLEMENTATION_PLAN.md`
