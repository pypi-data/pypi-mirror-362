# Installation and Testing

To get started with the Python CRISPR Analyser, follow the instructions below for prerequisites, installation, and testing.
 
## Prerequisites

The Python CRISPR Analyser requires Python {{requires_python}}. If using the database functionality you should have SQLite3 installed. If using CUDA, you will need to have a compatible Nvidia GPU and the CUDA kernel drivers installed, we have testing with CUDA {{tested_cuda_version}}.

## Installation

To install the Python CRISPR Analyser:

The easiest approach is to install using Pip

```bash
pip install py-crispr-analyser
```

Alternatively the source code can be downloaded from Github:

```bash
git clone git@github.com:sanger-cellular-informatics/py-crispr-analyser.git
```

Make sure you have Python {{requires_python}}.


## Testing

Make sure you have installed the source code and. Pytest need to be installed, this can be done using pip to install the development tools (which includes black, flake8 and pytest):

```bash
pip install '.[dev]'
```

To run the unit tests:

```bash
pytest tests
```
