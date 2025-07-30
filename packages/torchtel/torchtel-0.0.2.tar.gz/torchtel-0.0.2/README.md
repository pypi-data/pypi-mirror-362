# torchtel

torchtel provides OpenTelemetry auto instrumentation for pytorch

## Requirements

- Python 3.10 or higher
- PyTorch
- OpenTelemetry API
- OpenTelemetry Instrumentation ≥0.56b0

## Install from pypi

```bash
$ pip install torchtel
```

## Usage

### Instrument PyTorch

To instrument PyTorch, you need to import the `PyTorchInstrumentor` class, call the `instrument()` method, and register your model, see below:

```python
from torchtel import PyTorchInstrumentor

# create your PyTorch model
model = ...

# Registed the model for PyTorch Instrumentation
instrumentor = PyTorchInstrumentor().instrument(model=model)

# Run the model
...

# Uninstrument PyTorch
instrumentor.uninstrument()
```

Check out the [model example](./examples/model.py) to see OpenTelemetry autoinstrumentation in action.

## Observability

To visualize traces and metrics collected by TorchTel, see our [complete observability setup guide](./OBSERVABILITY.md) with Docker Compose configurations for Jaeger, Prometheus, and Grafana.

## Contributing

Read our contributing guide to learn about our development process, how to propose bugfixes and feature requests, and how to build your changes.

### [Code of Conduct](https://code.fb.com/codeofconduct)

Facebook has adopted a Code of Conduct that we expect project participants to adhere to. Please read [the full text](https://code.fb.com/codeofconduct) so that you can understand what actions will and will not be tolerated.

## Mantainers

clusterscope is actively maintained by [Lucca Bertoncini](https://github.com/luccabb), and [Billy Campoli](https://github.com/tooji).

### License

clusterscope is licensed under the [MIT](./LICENSE) license.
