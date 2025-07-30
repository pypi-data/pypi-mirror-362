# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
__version__ = "0.0.0"

from torchtel.instrument import PyTorchInstrumentor
from torchtel.setup import setup_opentelemetry

__all__ = ["PyTorchInstrumentor", "setup_opentelemetry"]
