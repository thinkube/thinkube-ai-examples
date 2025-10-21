# Thinkube Jupyter Examples

Curated Jupyter notebooks for the Thinkube platform, organized by image type.

## Directory Structure

```
jupyter-examples/
├── common/           # Examples for all Jupyter images
├── ml-gpu/          # Machine Learning (GPU) specific examples
├── fine-tuning/     # Fine-tuning specific examples
└── agent-dev/       # Agent development specific examples
```

## Usage

Examples are automatically deployed to JupyterHub:
- **Read-only templates**: `/home/jovyan/thinkube/notebooks/templates/`
- **Editable copies**: `/home/jovyan/thinkube/notebooks/examples/${IMAGE_NAME}/`

## Notebook Cleaning

All notebooks must be cleaned before committing to remove execution output and metadata.

### Setup cleaning tools

```bash
pip install nbstripout
nbstripout --install
```

### Manual cleaning

```bash
# Clean a single notebook
nbstripout notebook.ipynb

# Validate notebook is clean
./scripts/validate_notebooks.sh
```

### Pre-commit hook

The repository uses pre-commit hooks to automatically clean notebooks:

```bash
pip install pre-commit
pre-commit install
```

## Notebook Guidelines

1. **No execution output** - Strip all output before committing
2. **No execution counts** - Remove `execution_count` metadata
3. **Clean metadata** - Remove unnecessary notebook metadata
4. **Fail-fast** - Examples must run without errors on target image
5. **Self-contained** - Include all necessary imports and setup

## Image-Specific Guidelines

### common/
- Basic Thinkube services connection examples
- Platform introduction notebooks
- Storage and environment guides

### ml-gpu/
- CUDA-accelerated training
- Multi-GPU workflows
- Distributed training examples

### fine-tuning/
- Unsloth fine-tuning examples
- QLoRA and LoRA workflows
- Model optimization techniques

### agent-dev/
- LangChain development examples
- CrewAI multi-agent systems
- RAG pipeline implementations

## License

Copyright 2025 Alejandro Martínez Corriá and the Thinkube contributors
SPDX-License-Identifier: Apache-2.0
