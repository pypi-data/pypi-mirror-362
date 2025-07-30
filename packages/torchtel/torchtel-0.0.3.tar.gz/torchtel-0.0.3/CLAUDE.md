# TorchTel - AI Agent Guide

This document provides comprehensive context for AI agents working with the TorchTel codebase.

## Project Overview

**TorchTel** is an OpenTelemetry auto-instrumentation library for PyTorch that automatically collects traces and metrics from PyTorch training loops without requiring code changes.

### What it does:
- **Traces**: Captures PyTorch operations (model.forward, optimizer.step, autograd.backward, dataloader.next)
- **Metrics**: Collects training metrics (step counts, model parameters, GPU memory usage)
- **Zero-code instrumentation**: Works by patching PyTorch methods at runtime

### Key Value Proposition:
- Drop-in observability for PyTorch training
- Compatible with any OpenTelemetry backend (Jaeger, Prometheus, etc.)
- Minimal performance overhead

## Architecture

### Core Components

1. **PyTorchInstrumentor** (`torchtel/instrument.py`)
   - Main instrumentation class
   - Patches PyTorch methods to inject OpenTelemetry spans
   - Manages lifecycle (instrument/uninstrument)

2. **OpenTelemetry Setup** (`torchtel/setup.py`)
   - Configures OTLP exporters for traces and metrics
   - Handles resource attributes (job info, cluster details)
   - Sets up tracer and meter providers

3. **Observability Stack** (`docker/`)
   - Complete Docker Compose setup
   - OpenTelemetry Collector, Jaeger, Prometheus, Grafana
   - Production-ready monitoring infrastructure

### Instrumentation Strategy

The library uses **method patching** rather than hooks:

```python
# Patches model.forward directly
self._orig_call = self.model.forward
self.model.forward = _wrapped_call

# Why not hooks?
# - Direct measurement of actual method execution time
```

## Key Files Structure

```
torchtel/
├── torchtel/
│   ├── __init__.py           # Public API exports
│   ├── instrument.py         # Core instrumentation logic
│   └── setup.py             # OpenTelemetry configuration
├── examples/
│   └── train.py             # Example instrumented training script
├── docker/                  # Complete observability stack
│   ├── docker-compose.observability.yml
│   ├── otel-collector-config.yaml
│   ├── prometheus.yml
│   └── README.md            # Visual examples and docker setup of jaeger, prometheus, otel-collector, and grafana
├── CONTRIBUTING.md          # Development workflow
└── README.md               # Main project documentation
```

### Critical Files for Agents

- **`torchtel/instrument.py`**: Core instrumentation logic - modify for new features
- **`torchtel/setup.py`**: OpenTelemetry configuration - modify for new exporters/metrics
- **`examples/train.py`**: Reference implementation - modify for testing
- **`docker/otel-collector-config.yaml`**: Trace/metric routing - modify for new OSS compatible backends

## Development Workflow

### Environment Setup
```bash
make install-dev-requirements  # Sets up uv, dependencies, editable install
pre-commit install            # Enables linting/formatting
```

### Testing Changes
```bash
# Quick test
cd examples && python train.py

# With observability stack
cd docker
docker-compose -f docker-compose.observability.yml up -d
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:11000"
cd ../examples && python train.py

# View results
# Traces: http://localhost:16686 (Jaeger)
# Metrics: http://localhost:9090 (Prometheus)
# Dashboards: http://localhost:3000 (Grafana)
```

### Code Quality
- **pre-commit**: Runs linters, formatters, type checkers
- **mypy**: Type checking enabled
- **flake8**: Code style enforcement

## Observability Stack Details

### Architecture Flow
```
PyTorch Model → OTLP HTTP (localhost:11000) → OpenTelemetry Collector
                                                    ├── Traces → Jaeger
                                                    └── Metrics → Prometheus → Grafana
```

### Key Endpoints
- **OTLP Receiver**: `localhost:11000` (model sends data here)
- **Jaeger UI**: `localhost:16686` (view traces)
- **Prometheus UI**: `localhost:9090` (query metrics)
- **Grafana UI**: `localhost:3000` (dashboards, admin/admin)

### Configuration Files
- **`otel-collector-config.yaml`**: Routes traces to Jaeger, metrics to Prometheus
- **`prometheus.yml`**: Scrapes metrics from OpenTelemetry Collector
- **`docker-compose.observability.yml`**: Complete stack definition

## Common Agent Tasks

### Adding New Metrics
1. Modify `torchtel/instrument.py` in `_instrument()` method
2. Create new meter instruments (counter, gauge, histogram)
3. Add callbacks or manual recording in appropriate patches

### Adding New Trace Spans
1. Identify PyTorch method to instrument
2. Add new `_patch_*` method in `PyTorchInstrumentor`
3. Store original method, create wrapped version with span
4. Add cleanup in `_uninstrument()`

### Debugging Instrumentation Issues
1. Check if containers are running: `docker-compose ps`
2. Check collector logs: `docker-compose logs otel-collector`
3. Verify OTLP endpoint: `echo $OTEL_EXPORTER_OTLP_ENDPOINT`
4. Test direct OTLP: `curl -X POST http://localhost:11000/v1/traces`

### Modifying Observability Stack
1. **Add new backend**: Modify `otel-collector-config.yaml` exporters
2. **Change ports**: Update `docker-compose.observability.yml`
3. **Add dashboards**: Create Grafana JSON configs

## Important Technical Concepts

### OpenTelemetry Integration
- **Tracer**: Creates spans for operations
- **Meter**: Creates metrics (counters, gauges)
- **Resource**: Metadata about the service/job
- **Exporters**: Send data to backends (OTLP HTTP)

### Docker Networking
- **Service names**: Containers communicate via service names (`prometheus:9090`)
- **Port mapping**: Host ports (9090) vs container ports
- **Internal vs external**: `localhost:9090` (host) vs `prometheus:9090` (container)

## Common Issues and Solutions

### Traces Not Appearing in Jaeger
1. **Check collector config**: Ensure using OTLP endpoint (`jaeger:4317`)
2. **Verify hostname**: Must be `jaeger`, not `jaegger` (common typo)
3. **Check ports**: Jaeger needs port 4317 exposed for OTLP

### Metrics Not in Prometheus
1. **Check data source**: Grafana must use `http://prometheus:9090`
2. **Verify scraping**: Prometheus should scrape `otel-collector:8889`
3. **Check collector**: Metrics pipeline should export to `prometheus` exporter

### Instrumentation Not Working
1. **Check model passing**: `PyTorchInstrumentor().instrument(model=model)`
2. **Verify OpenTelemetry setup**: Call `setup_opentelemetry()` first
3. **Check uninstrumentation**: Restore methods correctly in `_uninstrument()`

### Docker Issues
1. **Port conflicts**: Ensure ports 11000, 4317, 9090, 3000 are available
2. **File paths**: Config files must be in same directory as docker-compose
3. **Container networking**: Use service names, not localhost, for inter-container communication

## Development Best Practices

### When Modifying Instrumentation
- Always store original methods before patching
- Ensure proper cleanup in `_uninstrument()`
- Test with multiple model instances
- Verify no global state pollution

### When Adding Features
- Follow existing patterns in `instrument.py`
- Update documentation
- Consider performance impact

### When Debugging
- Use collector logs as primary debugging tool
- Test components in isolation
- Verify OpenTelemetry setup before instrumentation
- Check Docker networking issues first

## Quick Reference

### Essential Commands
```bash
# Development setup
make install-dev-requirements && pre-commit install

# Test instrumentation
cd examples && python train.py

# Start observability stack
cd docker && docker-compose -f docker-compose.observability.yml up -d

# Check collector logs
docker-compose -f docker-compose.observability.yml logs otel-collector

# Clean restart
docker-compose -f docker-compose.observability.yml down && docker-compose -f docker-compose.observability.yml up -d
```

### Key Environment Variables
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:11000"  # Required for model
export OTEL_LOG_LEVEL="DEBUG"  # For debugging OpenTelemetry issues
```

This guide should provide comprehensive context for AI agents working with TorchTel. The project focuses on zero-friction PyTorch observability through runtime method patching and a complete Docker-based monitoring stack.
