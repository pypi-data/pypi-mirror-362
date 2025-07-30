# OpenRXN Perovskite Optimizer

[Python Version](https://www.python.org/downloads/)
[License](LICENSE)
[Code Style: Black](https://github.com/psf/black)
[Agents: OpenAI SDK](https://github.com/openai/openai-agents-python)

**Author:** Nik Jois (<nikjois@llamasearch.ai>)

Welcome to the OpenRXN Perovskite Optimizer. This platform provides AI-driven materials discovery and optimization for perovskite solar cells using a multi-agent architecture.

## Key Features

- **Multi-Agent Architecture**: Coordinated AI agents for discovery, synthesis, and optimization.
- **Machine Learning**: Advanced property prediction and materials design.
- **Experimental Integration**: Automated synthesis protocols and characterization.
- **Web Interface**: Interactive dashboard and comprehensive REST API.
- **High Performance**: GPU acceleration and distributed computing support.
- **Scientific Rigor**: Comprehensive testing and experimental validation.

## Quick Start

Install the package and start optimizing perovskite materials:

```bash
# Install with automatic setup
curl -sSL https://raw.githubusercontent.com/openrxn/openrxn-perovskite-optimizer/main/scripts/install.sh | bash

# Or install manually
git clone https://github.com/openrxn/openrxn-perovskite-optimizer
cd openrxn-perovskite-optimizer
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[all]"
```

Discover new materials:

```bash
# Discover materials based on MAPbI3
perovskite-optimizer discover materials --composition MAPbI3 --target-efficiency 25.0

# Generate synthesis protocols
perovskite-optimizer synthesize protocol --composition "MA0.8FA0.2PbI3"

# Optimize compositions
perovskite-optimizer optimize composition --base "MAPbI3" --objectives efficiency stability cost
```