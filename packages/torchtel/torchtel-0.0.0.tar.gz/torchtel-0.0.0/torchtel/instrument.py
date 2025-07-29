# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import annotations

import time
import types
from typing import Any, Dict, List, Optional, Sequence

import torch
from opentelemetry import metrics, trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.metrics import CallbackOptions, Observation
from typing_extensions import Self
from wrapt import function_wrapper

__all__ = ["PyTorchInstrumentor"]


class PyTorchInstrumentor(BaseInstrumentor):
    """Auto‑instrument PyTorch training loops."""

    def instrument(self, **kwargs: Any) -> Self:  # type: ignore[override]
        """Enable instrumentation and return *self* for chaining.

        Example
        -------
        >>> instr = PyTorchInstrumentor().instrument()
        >>> model = Net(); instr.register_model(model)
        """
        super().instrument(**kwargs)  # BaseInstrumentor.instrument() does the work
        return self

    # -------- required by BaseInstrumentor ---------------------------------
    @staticmethod
    def instrumentation_dependencies() -> Sequence[str]:  # noqa: D401
        """Static list of extra PyPI requirements.

        BaseInstrumentor declares this as a ``@staticmethod``. Returning an
        empty tuple tells the bootstrapper that no additional distributions are
        required beyond what the user has already installed.
        """
        return ()

    # ----------------------------------------------------------------------
    # Class‑level state so the patches stay idempotent across instances
    _tracer: Optional[trace.Tracer] = None
    _meter: Optional[metrics.Meter] = None
    _orig_call = None
    _orig_opt_step: Dict[type, types.FunctionType] = {}
    _orig_backward = None
    _orig_iter = None
    _steps_counter: Optional[metrics.Counter] = None
    _param_gauge_cb_set = False

    # ------------------------------------------------------------------
    # Public helper -----------------------------------------------------
    # ------------------------------------------------------------------
    def register_model(self, model: torch.nn.Module):
        """Set the *model.parameters* gauge once the model is built."""
        if self._param_gauge_cb_set or not self._meter:
            return
        count = sum(p.numel() for p in model.parameters() if p.requires_grad)
        self._param_gauge.callbacks = [lambda _: [Observation(count, {})]]
        self._param_gauge_cb_set = True

    # ------------------------------------------------------------------
    # Instrument / uninstrument (internal hooks) -----------------------
    # ------------------------------------------------------------------
    def _instrument(self, **kwargs):  # noqa: D401
        if self._tracer:
            return  # already active

        # Grab whatever providers the application configured
        self._tracer = trace.get_tracer(__name__)
        self._meter = metrics.get_meter(__name__)

        # ---------------- metrics ------------------------------------
        self._steps_counter = self._meter.create_counter(
            "train.step.count", unit="1", description="Optimizer steps (batches)"
        )

        self._param_gauge = self._meter.create_observable_gauge(
            "model.parameters",
            unit="1",
            description="Trainable parameters",
            callbacks=[],
        )

        def _gpu_mem(_: CallbackOptions) -> List[Observation]:
            if not torch.cuda.is_available():
                return []
            return [
                Observation(torch.cuda.memory_allocated(), {"kind": "allocated"}),
                Observation(torch.cuda.memory_reserved(), {"kind": "reserved"}),
            ]

        self._meter.create_observable_gauge(
            "gpu.memory.bytes",
            unit="By",
            description="GPU memory usage",
            callbacks=[_gpu_mem],
        )

        # ---------------- spans --------------------------------------
        self._patch_module_call()
        self._patch_optimizer_steps()
        self._patch_autograd_backward()
        self._patch_dataloader()

    def _uninstrument(self, **kwargs):  # noqa: D401
        if not self._tracer:
            return  # nothing to do

        # restore nn.Module.__call__
        if self._orig_call:
            torch.nn.Module.__call__ = self._orig_call  # type: ignore[assignment]
            self._orig_call = None

        # restore optimizer.step
        for cls, fn in self._orig_opt_step.items():
            cls.step = fn  # type: ignore[assignment]
        self._orig_opt_step.clear()

        # restore autograd.backward
        if self._orig_backward:
            torch.autograd.backward = self._orig_backward  # type: ignore[assignment]
            self._orig_backward = None

        # restore DataLoader iterator
        import torch.utils.data as torchdata

        if self._orig_iter:
            torchdata.DataLoader.__iter__ = self._orig_iter  # type: ignore[assignment]
            self._orig_iter = None

        # reset handles
        self._tracer = self._meter = None
        self._steps_counter = None
        self._param_gauge_cb_set = False

    # ------------------------------------------------------------------
    # Patching helpers --------------------------------------------------
    # ------------------------------------------------------------------
    def _patch_module_call(self):
        if self._orig_call:
            return

        self._orig_call = torch.nn.Module.__call__

        @function_wrapper
        def _wrapped_call(wrapped, instance, args, kwargs):
            span_name = f"{instance.__class__.__qualname__}.forward"
            with self._tracer.start_as_current_span(span_name):  # type: ignore
                start = time.perf_counter()
                out = wrapped(*args, **kwargs)
                trace.get_current_span().set_attribute(  # type: ignore
                    "duration.ms", (time.perf_counter() - start) * 1e3
                )
                return out

        torch.nn.Module.__call__ = _wrapped_call  # type: ignore[assignment]

    def _patch_optimizer_steps(self):
        for name in getattr(torch.optim, "__all__", []):
            cls = getattr(torch.optim, name, None)
            if not isinstance(cls, type) or cls in self._orig_opt_step:
                continue
            self._wrap_optimizer(cls)

    def _wrap_optimizer(self, cls):
        self._orig_opt_step[cls] = cls.step

        def _step(this, *args, **kwargs):
            with self._tracer.start_as_current_span(f"{cls.__name__}.step"):  # type: ignore
                start = time.perf_counter()
                rv = self._orig_opt_step[cls](this, *args, **kwargs)
                trace.get_current_span().set_attribute(  # type: ignore
                    "duration.ms", (time.perf_counter() - start) * 1e3
                )
                self._steps_counter.add(1)
                return rv

        cls.step = _step  # type: ignore[assignment]

    def _patch_autograd_backward(self):
        if self._orig_backward:
            return
        self._orig_backward = torch.autograd.backward

        def _backward(*args, **kwargs):
            with self._tracer.start_as_current_span("autograd.backward"):  # type: ignore
                start = time.perf_counter()
                rv = self._orig_backward(*args, **kwargs)
                trace.get_current_span().set_attribute(  # type: ignore
                    "duration.ms", (time.perf_counter() - start) * 1e3
                )
                return rv

        torch.autograd.backward = _backward  # type: ignore[assignment]

    def _patch_dataloader(self):
        import torch.utils.data as torchdata

        if self._orig_iter:
            return
        self._orig_iter = torchdata.DataLoader.__iter__

        def _iter(loader):
            it = self._orig_iter(loader)
            return _WrappedIter(it, self._tracer)

        torchdata.DataLoader.__iter__ = _iter  # type: ignore[assignment]


class _WrappedIter:
    """Iterator proxy that records *dataloader.next* latency."""

    def __init__(self, iterator, tracer: trace.Tracer):
        self._it = iterator
        self._tracer = tracer

    def __iter__(self):
        return self

    def __next__(self):
        with self._tracer.start_as_current_span("dataloader.next"):
            start = time.perf_counter()
            batch = next(self._it)
            trace.get_current_span().set_attribute(  # type: ignore
                "duration.ms", (time.perf_counter() - start) * 1e3
            )
            return batch
