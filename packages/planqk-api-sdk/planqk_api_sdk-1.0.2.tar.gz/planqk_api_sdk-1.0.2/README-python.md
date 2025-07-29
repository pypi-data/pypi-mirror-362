# PLANQK API SDK

## Installation

The package is published on PyPI and can be installed via `pip`:

```bash
pip install --upgrade planqk-api-sdk
```

## Usage

```python
from planqk.api.client import PlanqkApiClient

# Create a new client
client = PlanqkApiClient(access_token=YOUR_PERSONAL_ACCESS_TOKEN)

# Create a new data pool
data_pool = client.data_pools.create_data_pool(name="Example Data Pool")
```
