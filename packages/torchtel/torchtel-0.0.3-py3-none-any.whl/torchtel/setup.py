# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
import getpass
import os
import socket
from typing import Mapping, Optional, Tuple, Union

from clusterscope import cluster

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.metrics import NoOpMeterProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import NoOpTracerProvider

# TODO: move the below to clusterscope
# from clusterscope.lib import (
#     cluster,
#     global_rank,
#     job_id,
#     job_name,
#     local_node_gpu_generation_and_count,
#     local_rank,
#     world_size,
# )


OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")


# TODO: move the below to clusterscope
class JobInfo:
    from functools import lru_cache  # type: ignore[misc]

    def __init__(self) -> None:
        self.is_torch_run = os.environ.get("LOCAL_RANK") is not None
        self.is_slurm_job = "SLURM_JOB_ID" in os.environ and not self.is_torch_run
        self.job_id = self.get_job_id()
        self.job_name = self.get_job_name()
        self.global_rank = self.get_global_rank()
        self.local_rank = self.get_local_rank()
        self.world_size = self.get_world_size()

    @lru_cache(maxsize=1)
    def get_job_id(self) -> int:
        if self.is_slurm_job:
            return int(os.environ.get("SLURM_JOB_ID", -1))
        return 0

    @lru_cache(maxsize=1)
    def get_job_name(self) -> str:
        if self.is_slurm_job:
            return os.environ.get("SLURM_JOB_NAME", "")
        return "local"

    @lru_cache(maxsize=1)
    def get_global_rank(self) -> int:
        if self.is_slurm_job:
            return int(os.environ["SLURM_PROCID"])
        if self.is_torch_run:
            return int(os.environ["RANK"])
        return 0

    @lru_cache(maxsize=1)
    def get_local_rank(self) -> int:
        if self.is_slurm_job:
            return int(os.environ["SLURM_LOCALID"])
        if self.is_torch_run:
            return int(os.environ["LOCAL_RANK"])
        return 0

    @lru_cache(maxsize=1)
    def get_world_size(self) -> int:
        if self.is_slurm_job:
            return int(os.environ["SLURM_NTASKS"])
        if self.is_torch_run:
            return int(os.environ["WORLD_SIZE"])
        return 1


# TODO: move the below to clusterscope
job_info = JobInfo()


def setup_opentelemetry(
    resource_attributes: Optional[Mapping[str, Union[str, int]]] = None,
    init_tracer_provider: bool = True,
    init_meter_provider: bool = True,
    service_name: str = "torchtel",
) -> Tuple[TracerProvider, MeterProvider]:
    """Set up OpenTelemetry SDK with OTLP HTTP exporters."""
    final_resource_attributes = {
        # TODO: move the below to clusterscope
        # "job_id": job_id,
        # "job_name": job_name,
        # "user": getpass.getuser(),
        # "cluster": cluster(),
        # "local_rank": local_rank,
        # "global_rank": global_rank,
        # "world_size": world_size,
        # "host": socket.gethostname(),
        # "gpu_type": local_node_gpu_generation_and_count(),
        SERVICE_NAME: service_name,
        "job_id": job_info.job_id,
        "job_name": job_info.job_name,
        "user": getpass.getuser(),
        "cluster": cluster(),
        "local_rank": job_info.local_rank,
        "global_rank": job_info.global_rank,
        "world_size": job_info.world_size,
        "host": socket.gethostname(),
        # TODO: fix the below to return empty instead of failing
        # "gpu_type": list(local_node_gpu_generation_and_count().keys()),
        **(resource_attributes or {}),
    }
    resource = Resource(attributes=final_resource_attributes)

    if init_tracer_provider:
        # Set up tracing with OTLP HTTP exporter
        tracer_provider = TracerProvider(resource=resource)
        otlp_span_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT + "/v1/traces", timeout=60)
        span_processor = BatchSpanProcessor(otlp_span_exporter)
        tracer_provider.add_span_processor(span_processor)
    else:
        tracer_provider = NoOpTracerProvider()  # type: ignore[assignment]
    trace.set_tracer_provider(tracer_provider)

    if init_meter_provider:
        # Set up metrics with OTLP HTTP exporter
        otlp_metric_exporter = OTLPMetricExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT + "/v1/metrics", timeout=60)
        metric_reader = PeriodicExportingMetricReader(
            otlp_metric_exporter,
            export_interval_millis=60000,
            export_timeout_millis=30000,
        )
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader], shutdown_on_exit=True)
    else:
        meter_provider = NoOpMeterProvider()  # type: ignore[assignment]
    metrics.set_meter_provider(meter_provider)

    return tracer_provider, meter_provider
