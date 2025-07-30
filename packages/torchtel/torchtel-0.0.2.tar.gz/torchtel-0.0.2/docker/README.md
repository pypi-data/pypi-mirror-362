# Observability Setup for TorchTel

This document explains how to set up a complete observability stack to collect and visualize both traces and metrics from your PyTorch models instrumented with TorchTel.

## Problem Statement

The TorchTel model instrumentation (`examples/model.py`) sends both traces and metrics via OpenTelemetry OTLP exporters:
- **Traces**: PyTorch operations, model forward passes, optimizer steps, etc.
- **Metrics**: Training metrics, model parameters, GPU memory usage, etc.

While the CONTRIBUTING.md shows how to set up Jaeger for traces only, you need a complete observability stack to properly collect and visualize both traces and metrics.

## Complete Observability Stack

The repository includes configuration files for a complete Docker-based observability stack:

### Components

- **OpenTelemetry Collector**: Receives both traces and metrics from your model via OTLP HTTP
- **Jaeger**: Stores and visualizes distributed traces
- **Prometheus**: Stores and queries metrics data
- **Grafana**: Creates dashboards for metrics visualization

### Configuration Files

1. **`docker-compose.observability.yml`**: Docker Compose setup for all services
2. **`otel-collector-config.yaml`**: OpenTelemetry Collector configuration
3. **`prometheus.yml`**: Prometheus scraping configuration

### Usage

1. **Start the observability stack**:
```bash
docker-compose -f docker-compose.observability.yml up -d
```

2. **Run your instrumented model**:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:11000"
cd ../examples
python model.py
```

3. **Access the UIs**:
- **Traces**: http://localhost:16686 (Jaeger UI)
- **Metrics**: http://localhost:9090 (Prometheus UI)
- **Dashboards**: http://localhost:3000 (Grafana UI, login: admin/admin)

4. **Stop the stack**:
```bash
docker-compose -f docker-compose.observability.yml down
```

### What You'll See

**In Jaeger (Traces)**:
- `SimpleModel.forward` spans showing model execution
- `SGD.step` spans showing optimizer steps
- `autograd.backward` spans showing backpropagation
- `dataloader.next` spans showing data loading

**In Prometheus (Metrics)**:
- Training step counters
- Model parameter metrics
- GPU memory usage metrics
- Loss values over time

**In Grafana (Dashboards)**:
- Create custom dashboards combining multiple metrics
- Visualize training progress over time
- Monitor resource usage

## Architecture

```
PyTorch Model (examples/model.py)
    ↓ OTLP HTTP (localhost:11000)
OpenTelemetry Collector
    ├── Traces → Jaeger (localhost:16686)
    └── Metrics → Prometheus (localhost:9090) → Grafana (localhost:3000)
```

## Dashboard Setup (Important!)

**Jaeger shows traces, not dashboards.** For actual dashboards with charts and graphs, use Grafana:

1. **Access Grafana**: http://localhost:3000 (admin/admin)
2. **Add Prometheus Data Source**:
   - Go to Configuration → Data Sources → Add data source → Prometheus
   - **Important**: Set URL to: `http://prometheus:9090` (NOT localhost:9090) to ensure Prometheus is reachable from the Docker network
   - Click "Save & Test"
3. **Create Dashboard**: Click "+" → Dashboard → Add panel
4. **Available metrics**: `train_step_count_total`, `model_parameters`, `gpu_memory_bytes`

## Troubleshooting

- Ensure all ports (11000, 16686, 9090, 3000, 8889, 14250) are available
- Check Docker logs: `docker-compose -f docker-compose.observability.yml logs`
- Verify the OTLP endpoint is correctly set: `echo $OTEL_EXPORTER_OTLP_ENDPOINT`
