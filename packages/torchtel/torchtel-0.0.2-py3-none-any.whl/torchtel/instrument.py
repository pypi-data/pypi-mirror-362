# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import annotations

import types
from contextlib import ExitStack
from typing import Any, Dict, List, Optional, Sequence, Type

import torch
from opentelemetry import metrics, trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore[attr-defined]
from opentelemetry.metrics import CallbackOptions, Observation
from typing_extensions import Self


class PyTorchInstrumentor(BaseInstrumentor):
    """Auto-instrument PyTorch training loops."""

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
    _train_stack = None

    def instrument(self, model: torch.nn.Module, logging_freq: int = 10, **kwargs: Any) -> Self:
        """Enable instrumentation and return *self* for chaining.

        Example
        -------
        >>> model = Net();
        >>> instr = PyTorchInstrumentor().instrument(model=model, logging_freq=logging_freq)
        """
        self.model = model
        self.logging_freq = logging_freq
        super().instrument(**kwargs)  # BaseInstrumentor.instrument() does the work

        count = sum(p.numel() for p in model.parameters() if p.requires_grad)
        self._param_gauge.callbacks = [lambda _: [Observation(count, {})]]  # type: ignore[attr-defined]
        self._param_gauge_cb_set = True
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

    # ------------------------------------------------------------------
    # Instrument / uninstrument (internal hooks) -----------------------
    # ------------------------------------------------------------------
    def _instrument(self, **kwargs: Any) -> None:
        if self._tracer:
            return  # already active

        # Grab whatever providers the application configured
        self._tracer = trace.get_tracer(__name__)
        self._meter = metrics.get_meter(__name__)

        self.train_stack = ExitStack()
        self.train_stack.enter_context(self._tracer.start_as_current_span("train"))

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
        self._patch_forward_call()
        self._patch_optimizer_steps()
        self._patch_autograd_backward()
        self._patch_dataloader()

    def _uninstrument(self, **kwargs: Any) -> None:
        if not self._tracer:
            return  # nothing to do

        assert self._train_stack is not None, "torchtel self._train_stack should not be None after class initialization"
        # close train span
        self._train_stack.close()

        # restore model.forward
        if self._orig_call:
            self.model.forward = self._orig_call  # type: ignore[assignment]
            self._orig_call = None

        # restore optimizer.step
        for cls, fn in self._orig_opt_step.items():
            cls.step = fn  # type: ignore[assignment, attr-defined]
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
    def _patch_forward_call(self) -> None:
        """
        Instruments the model's forward pass by wrapping it with OpenTelemetry tracing:
            - Preserves the original forward method before replacement
            - Creates spans with naming pattern: "{ModelClass}.forward"
            - Instance-level patching ensures isolation between multiple instrumented models
            - Direct forward method replacement bypasses PyTorch's hook system to measure the real duration of
                the forward pass
        """
        if self._orig_call:
            return

        self._orig_call = self.model.forward

        def _wrapped_call(*args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
            assert self._tracer is not None, "torchtel self._tracer should not be None after class initialization"
            span_name = f"{self.model.__class__.__qualname__}.forward"

            if self._train_stack is None:
                self._train_stack = ExitStack()
                self._train_stack.enter_context(self._tracer.start_as_current_span("train"))

            with self._tracer.start_as_current_span(span_name):
                out = self._orig_call(*args, **kwargs)  # type: ignore[misc]
            return out

        self.model.forward = _wrapped_call

    def _patch_optimizer_steps(self) -> None:
        for name in getattr(torch.optim, "__all__", []):
            cls = getattr(torch.optim, name, None)
            if not isinstance(cls, type) or cls in self._orig_opt_step:
                continue
            self._wrap_optimizer(cls)

    def _wrap_optimizer(self, cls: Type) -> None:
        self._orig_opt_step[cls] = cls.step

        def _step(this, *args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
            assert self._tracer is not None, "torchtel self._tracer should not be None after class initialization"
            assert (
                self._steps_counter is not None
            ), "torchtel self._steps_counter should not be None after class initialization"
            with self._tracer.start_as_current_span(f"{cls.__name__}.step"):
                rv = self._orig_opt_step[cls](this, *args, **kwargs)
                self._steps_counter.add(1)
            return rv

        cls.step = _step  # type: ignore[assignment]

    def _patch_autograd_backward(self) -> None:
        if self._orig_backward:
            return
        self._orig_backward = torch.autograd.backward

        def _backward(*args: Any, **kwargs: Any):  # type: ignore[no-untyped-def]
            assert self._tracer is not None, "torchtel self._tracer should not be None after class initialization"
            with self._tracer.start_as_current_span("autograd.backward"):
                rv = self._orig_backward(*args, **kwargs)  # type: ignore[misc]
            return rv

        torch.autograd.backward = _backward  # type: ignore[assignment]

    def _patch_dataloader(self) -> None:
        import torch.utils.data as torchdata

        if self._orig_iter:
            return
        self._orig_iter = torchdata.DataLoader.__iter__

        def _iter(loader) -> _WrappedIter:  # type: ignore[no-untyped-def]
            assert self._orig_iter is not None, "torchtel self._orig_iter should've been patched"
            it = self._orig_iter(loader)  # type: ignore[call-arg]
            assert self._tracer is not None, "torchtel self._tracer should not be None after class initialization"
            return _WrappedIter(it, self._tracer)

        torchdata.DataLoader.__iter__ = _iter  # type: ignore[assignment]


class _WrappedIter:
    """Iterator proxy that records *dataloader.next* latency."""

    def __init__(self, iterator, tracer: trace.Tracer) -> None:  # type: ignore[no-untyped-def]
        self._it = iterator
        self._tracer = tracer

    def __iter__(self) -> Self:
        return self

    def __next__(self):  # type: ignore[no-untyped-def]
        with self._tracer.start_as_current_span("dataloader.next"):
            batch = next(self._it)
        return batch
