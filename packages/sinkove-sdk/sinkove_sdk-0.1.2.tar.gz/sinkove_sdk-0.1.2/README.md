# Sinkove SDK

[![PyPI version](https://badge.fury.io/py/sinkove-sdk.svg)](https://badge.fury.io/py/sinkove-sdk)

The Sinkove SDK is a Python library designed to facilitate interaction with Sinkove's AI dataset generation API. This library allows seamless integration with Sinkove's services, enabling organizations to create, manage, and download datasets programmatically.

## Features

- Create and manage datasets
- Download datasets with customizable strategies
- Monitor dataset generation status

## Getting Started

### Installation

You can install the SDK via pip:

```bash
pip install sinkove-sdk
```

### Usage

To use the SDK, you need to set your API key and API URL in the environment variables. Here's a basic example of how to create and download a dataset:

```python
import uuid
from sinkove import Client

def main():
    organization_id = uuid.UUID("your-organization-id")
    model_id = uuid.UUID("your-model-id")

    dataset = Client(organization_id).datasets.create(
        model_id, num_samples=2, args={"prompt": "cardiomegaly"}
    )

    dataset.download("dataset.zip", strategy="skip", wait=True)

if __name__ == "__main__":
    main()
```

### API Documentation

For complete API details, visit the [API documentation](https://api.sinkove.com/docs).

### Official Documentation

Find more detailed documentation about the Sinkove services at [Sinkove Docs](https://docs.sinkove.com).

### Sinkove Console

Access your Sinkove dashboard at the [Sinkove Console](https://cloud.sinkove.com).

## Contributing

Contributions are welcome! Please read the contribution guidelines first. You can start by running the project locally using:

```bash
just build
just test
```
