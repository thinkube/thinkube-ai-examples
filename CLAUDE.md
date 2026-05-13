# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mission

Maintain the **AI Research Lab Assistant** notebooks — fully executable tutorials that demonstrate thinkube's AI platform capabilities.

## Platform: 100% Self-Contained

All AI capabilities run locally on thinkube — no external API calls:

| Capability | Service | SDK |
|------------|---------|-----|
| Chat/Completion | LLM Gateway (Ollama, vLLM, TensorRT-LLM) | `tk-llm` (`LLMClient`, `get_openai_client()`) |
| Embeddings | LLM Gateway (Text Embeddings Inference) | `tk-llm` (`get_openai_client()`) |
| Vector Search | Qdrant | `qdrant-client` |
| Observability | Langfuse | `langfuse` |
| Experiment Tracking | MLflow | `mlflow` |

Models are stored in MLflow Model Registry and served via the LLM Gateway proxy.

## Repository Structure

```
thinkube-ai-examples/
├── examples/
│   └── research-assistant/
│       ├── 00-platform-validation.ipynb   # Validate platform services
│       ├── 01-working-with-local-llms.ipynb  # Model lifecycle (load/unload/chat/embed)
│       ├── 02-langchain-rag.ipynb         # RAG pipeline with arXiv papers
│       └── 03-multi-agent.ipynb           # AG2 multi-agent debate with tool calling
├── CLAUDE.md
├── README.md
└── LICENSE
```

## How Notebooks Reach JupyterHub

1. **Init container** clones this repo to `templates/` (emptyDir, fresh every pod start)
2. **One-time copy**: `templates/examples/*` → `notebooks/examples/` (JuiceFS persistent)
3. Users work in `notebooks/examples/research-assistant/` (editable)
4. Reference copies always available in `templates/examples/research-assistant/` (read-only)

## Platform Services (Environment Variables)

| Service | Environment Variables |
|---------|----------------------|
| LLM Gateway | `LLM_GATEWAY_URL`, `THINKUBE_API_TOKEN` |
| Qdrant | `QDRANT_URL` |
| Langfuse | `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` |
| MLflow | `MLFLOW_TRACKING_URI`, `MLFLOW_AUTH_USERNAME`, `MLFLOW_AUTH_PASSWORD` |
| PostgreSQL | `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` |
| Valkey | `VALKEY_HOST`, `VALKEY_PORT`, `VALKEY_PASSWORD` |

## Implementation Rules

1. **No TODO stubs** — every cell must execute
2. **Use real services** — connect to actual platform, not mocks
3. **Show real outputs** — results from actual execution, committed with outputs
4. **Dynamic model discovery** — use `LLMClient().list_models()`, never hardcode model names
5. **Educational tone** — explain what each cell does and why

## Key Libraries

For `agent-dev` venv:
- `tk-llm` (thinkube LLM SDK)
- `langchain`, `langchain-openai`, `langchain-qdrant`
- `autogen` (AG2 multi-agent framework)
- `qdrant-client`
- `langfuse`
- `arxiv` (paper fetching)
- `openai` (LLM Gateway is OpenAI-compatible)

For `fine-tuning` venv:
- `unsloth`
- `peft`, `trl`
- `mlflow`
