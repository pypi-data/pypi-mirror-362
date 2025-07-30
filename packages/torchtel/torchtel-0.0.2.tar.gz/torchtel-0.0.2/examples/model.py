# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""
Hello World PyTorch example with OpenTelemetry autoinstrumentation.
"""

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader, TensorDataset

# Import the PyTorchInstrumentor from the autoinstrumentation library
from torchtel import PyTorchInstrumentor, setup_opentelemetry


def main():
    """Main function to demonstrate PyTorch with autoinstrumentation."""
    print("Hello World PyTorch with OpenTelemetry Autoinstrumentation!")

    # Set up OpenTelemetry
    tracer_provider, meter_provider = setup_opentelemetry()

    # Create a simple model
    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(10, 5)
            self.fc2 = nn.Linear(5, 1)
            self.relu = nn.ReLU()
            self.sigmoid = nn.Sigmoid()

        def forward(self, x):
            x = self.relu(self.fc1(x))
            x = self.sigmoid(self.fc2(x))
            return x

    # Create model, loss function, and optimizer
    model = SimpleModel()
    criterion = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # Instrument PyTorch with the model
    instrumentor = PyTorchInstrumentor().instrument(model=model)

    # Create some dummy data
    X = torch.randn(100, 10, requires_grad=True)
    y = torch.randint(0, 2, (100, 1)).float()
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=10)

    # Train for a few epochs
    num_epochs = 3
    for epoch in range(num_epochs):
        running_loss = 0.0
        for inputs, labels in dataloader:
            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss = loss.mean()  # Ensure loss is a scalar

            # Backward pass and optimize
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(dataloader):.4f}")

    print("Training complete!")

    # Uninstrument when done
    instrumentor.uninstrument()

    # Shutdown OpenTelemetry
    tracer_provider.shutdown()
    meter_provider.shutdown()


if __name__ == "__main__":
    main()
