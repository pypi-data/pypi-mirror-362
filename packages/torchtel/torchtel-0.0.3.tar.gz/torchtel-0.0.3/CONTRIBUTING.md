# Contributing to torchtel

## Development Workflow

### Environment setup

Running the below from the root of this repository brings [uv](https://docs.astral.sh/uv/), all required development dependencies, and installs torchtel in editable mode:

```bash
make install-dev-requirements
```


### `pre-commit`

We have all linters/formatters/typecheckers integrated into pre-commit, these checks are also running as part of github CI. pre-commit automates part of the changes that will be required to land code on the repo. You can run the below to activate pre-commit in your local env:

```
pre-commit install
```

### Testing Your Changes

Since torchtel provides auto-instrumentation for PyTorch, it's important to test that your changes work correctly and don't break normal PyTorch functionality.

#### Running the Example

The quickest way to test your changes is to run the provided example:

```bash
cd examples
python train.py
```

This will run a simple PyTorch training loop with torchtel instrumentation enabled. You should see training progress printed to console with no errors.

#### Testing with OpenTelemetry Backend

To see the actual telemetry data being collected (traces and metrics), use the complete observability stack, see [docker/README.md](./docker/README.md).

#### Manual Testing Checklist

When making changes to the instrumentation code, verify:

1. **Basic functionality**: The example runs without errors
2. **Instrumentation works**: When connected to a backend, you should see spans for `SimpleModel.forward`, `SGD.step`, `autograd.backward`, and `dataloader.next`
3. **Metrics collection**: Verify training steps, model parameters, and GPU memory metrics are collected
4. **Clean uninstrumentation**: After calling `uninstrument()`, PyTorch should work normally


### Requirements

If you update the requirements, make sure to add it [`pyproject.toml`](./pyproject.toml)'s appropriate section for the dependency. Then you can run the below to update the requirements file:

```
$ make requirements.txt
```

For development dependencies:

```
$ make dev-requirements.txt
```

## Pull Requests
We welcome your pull requests.

1. Fork the repo and create your feature branch from `main`.
1. If you've added code add suitable tests.
1. Ensure the test suite and lint pass.
1. If you haven't already, complete the Contributor License Agreement ("CLA").

## Release

1. Checkout and pull latest main
```
$ git checkout main
$ git pull origin main
```
2. Tag
```
$ git tag -a v0.0.0 -m "Release 0.0.0"
```
3. Push the tag to github
```
$ git push origin v0.0.0
```
4. [Find and run the action related to publishing the branch to PyPI](https://github.com/facebookresearch/torchtel/actions). This requires maintainer approval.

## Contributor License Agreement ("CLA")
In order to accept your pull request, we need you to submit a CLA. You only need to do this once to work on any of Facebook's open source projects.

Complete your CLA here: <https://code.facebook.com/cla>

## Issues
We use GitHub issues to track public bugs. Please ensure your description is clear and has sufficient instructions to be able to reproduce the issue.

Facebook has a [bounty program](https://www.facebook.com/whitehat/) for the safe disclosure of security bugs. In those cases, please go through the process outlined on that page and do not file a public issue.

## License
By contributing to torchtel, you agree that your contributions will be licensed under the LICENSE file in the root directory of this source tree.
