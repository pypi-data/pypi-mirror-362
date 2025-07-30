# python-ws-microservico-modulo-verificar-autenticacao-service

This project provides a decorator for FastAPI to verify authentication and authorization via an external service.

## Features

- A FastAPI-compatible decorator for authentication and authorization.
- Easy integration with external authentication services.
- Customizable to fit different authentication flows.

## Installation

You can install the module using pip:

```bash
pip install verifyauth
```

## Usage

This package allows you to add an authentication layer to FastAPI endpoints via a decorator. Example usage:

```python
from verifyauth import AuthDecorator
from fastapi import FastAPI

app = FastAPI()

auth = AuthDecorator(service_url="https://auth.example.com")

@app.get("/protected")
def verifyauth(servico, capacidade, response_tag = 'obterVipCadastroResponse2', result_tag = 'obterVipCadastroResult2'):
@verifyauth(servico='example', capacidade='test', response_tag='capacidadeServicoResponse', result_tag='capacidadeServicoResult')    
def protected_endpoint():
    return {"message": "This is a protected route"}
```

## Build and Deployment

### Build the Package

Before deploying the package to TestPyPI or PyPI, you need to build the distribution files. The build process will create both a source distribution (`.tar.gz`) and a wheel distribution (`.whl`).

To build the package, first ensure the `build` module is installed:

```bash
pip install build
```



Then, run the following command to create the distribution files:

```bash
python -m build
```

This will generate the distribution files in the `dist/` directory.

### Upload to TestPyPI

To upload the package, first ensure the `twine` module is installed:

```bash
pip install twine
```

To upload the package to TestPyPI for testing purposes:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

After uploading, you can install it from TestPyPI using:

```bash
pip install --index-url https://test.pypi.org/simple/ verifyauth
```

### Upload to PyPI

Once you've tested the package on TestPyPI and are ready to publish it, upload it to PyPI:

```bash
twine upload dist/*
```

You can then install it via PyPI using:

```bash
pip install verifyauth
```

