# Installation

This guide will walk you through installing doteval and setting up your environment for LLM evaluation.

## Prerequisites

doteval requires **Python 3.10** or higher. Check your Python version:

```bash
python --version
```

!!! tip "Python Version Manager"
    We recommend using [pyenv](https://github.com/pyenv/pyenv) or [conda](https://docs.conda.io/en/latest/) to manage Python versions if you need to install a newer version.

## Basic Installation

### Install from PyPI

The simplest way to install doteval is using pip:

```bash
pip install doteval
```

### Install from Source

For the latest development version:

```bash
git clone https://github.com/dottxt-ai/doteval.git
cd doteval
pip install -e .
```

## Development Installation

If you plan to contribute to doteval or need the development dependencies:

```bash
git clone https://github.com/dottxt-ai/doteval.git
cd doteval
pip install -e ".[test,docs]"
```

This installs doteval in editable mode with additional dependencies for:
- **test**: pytest, coverage, and other testing tools
- **docs**: mkdocs, mkdocs-material, and documentation tools


## Next Steps

Now that you have doteval installed, you can:

1. **[Try the quickstart guide](quickstart.md)** - Build your first evaluation
2. **[Explore examples](../cookbook/index.md)** - See real-world evaluation setups
3. **[Learn about the CLI](cli.md)** - Manage evaluation sessions

### Getting Help

If you encounter issues:

1. Check the [troubleshooting section](../reference/troubleshooting.md)
2. Search [existing issues](https://github.com/dottxt-ai/doteval/issues)
3. Create a [new issue](https://github.com/dottxt-ai/doteval/issues/new) with details about your environment and the error
