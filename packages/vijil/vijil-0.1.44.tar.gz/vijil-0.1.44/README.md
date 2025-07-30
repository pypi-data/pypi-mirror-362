# vijil-python
Python Client for Vijil


## Setup

```bash
pip install -U vijil
```

Then initialize the client using

```python
from vijil import Vijil

client = Vijil()
```


Requires a `VIJIL_API_KEY`, either loaded in the environment or suppllied as `api_key` argument above.

## Run Evaluations

```python
client.evaluations.create(
    model_hub="openai",
    model_name="gpt-3.5-turbo",
    model_params={"temperature": 0},
    harnesses=["ethics","hallucination"],
    harness_params={"sample_size": 5}
)
```

See the [minimal example](tutorials/minimal_example.ipynb) for more functionalities.
