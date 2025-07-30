<p align="center">
    <img src="https://raw.githubusercontent.com/Prajjwal2404/NeuralEngine/refs/heads/main/NeuralEngine.webp" alt="NeuralEngine Cover" width="600" />
</p>

<p align="center">
    <a href="https://github.com/Prajjwal2404/NeuralEngine/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/Prajjwal2404/NeuralEngine" /></a>
    <a href="https://github.com/Prajjwal2404/NeuralEngine/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/Prajjwal2404/NeuralEngine" /></a>
    <a href="https://pypi.org/project/NeuralEngine" alt="PyPI">
        <img src="https://img.shields.io/pypi/v/NeuralEngine?color=brightgreen&label=PyPI" /></a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/language-Python-blue">
    </a>
    <a href="mailto:prajjwalpratapshah@outlook.com">
        <img src="https://img.shields.io/badge/-Email-red?style=flat-square&logo=gmail&logoColor=white">
    </a>
    <a href="https://www.linkedin.com/in/prajjwal2404">
        <img src="https://img.shields.io/badge/-Linkedin-blue?style=flat-square&logo=linkedin">
    </a>
</p>


# NeuralEngine

A framework/library for building and training neural networks in Python. NeuralEngine provides core components for constructing, training, and evaluating neural networks, with support for both CPU and GPU (CUDA) acceleration. Designed for extensibility, performance, and ease of use, it is suitable for research, prototyping, and production.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Example Usage](#example-usage)
- [Project Structure](#project-structure)
- [Capabilities & Documentation](#capabilities--documentation)
- [Contribution Guide](#contribution-guide)
- [License](#license)
- [Attribution](#attribution)

## Features
- Custom tensor operations (CPU/GPU support via NumPy and optional CuPy)
- Configurable neural network layers (Linear, Flatten, etc.)
- Built-in loss functions, metrics, and optimizers
- Model class for easy training and evaluation
- Device management (CPU/CUDA)
- Utilities for deep learning workflows
- Autograd capabilities using dynamic computational graphs
- Extensible design for custom layers, losses, and optimizers

## Installation
Install via pip:
```bash
pip install NeuralEngine
```
Or clone and install locally:
```bash
pip install .
```

### Optional CUDA Support
To enable GPU acceleration, Install via pip:
```bash
pip install NeuralEngine[cuda]
```
Or install the optional dependency
```bash
pip install cupy-cuda12x
```

## Example Usage
```python
import neuralengine as ne

# Set device (CPU or CUDA)
ne.set_device(ne.Device.CUDA)

# Load your dataset (example: MNIST)
x_train, y_train, x_test, y_test = load_mnist_data()

y_train = ne.one_hot(y_train)
y_test = ne.one_hot(y_test)

# Build your model
model = ne.Model(
    input_size=(28, 28),
    optimizer=ne.Adam(),
    loss=ne.CrossEntropy(),
    metrics=ne.ClassificationMetrics()
)
model(
    ne.Flatten(),
    ne.Linear(64, activation=ne.RELU()),
    ne.Linear(10, activation=ne.Softmax()),
)

# Train and evaluate
model.train(x_train, y_train, epochs=30, batch_size=10000)
result = model.eval(x_test, y_test)
```

## Project Structure
```
neuralengine/
    __init__.py
    config.py
    tensor.py
    utils.py
    nn/
        __init__.py
        layers.py
        loss.py
        metrics.py
        model.py
        optim.py
setup.py
requirements.txt
pyproject.toml
MANIFEST.in
LICENSE
README.md
```

## Capabilities & Documentation
NeuralEngine offers the following core capabilities:

### Device Management
- `ne.set_device(device)`: Switch between CPU and GPU (CUDA) for computation.
- Device enum: `ne.Device.CPU`, `ne.Device.CUDA`.

### Tensors & Autograd
- Custom tensor implementation supporting NumPy and CuPy backends.
- Automatic differentiation (autograd) using dynamic computational graphs for backpropagation.
- Supports gradients, parameter updates, and custom operations.
- Supported tensor operations:
  - Arithmetic: `+`, `-`, `*`, `/`, `**` (power)
  - Matrix multiplication: `@`
  - Mathematical: `log`, `sqrt`, `exp`, `abs`
  - Reductions: `sum`, `max`, `min`, `mean`, `var`
  - Shape: `transpose`, `reshape`, `concatenate`, `stack`, `slice`, `set_slice`
  - Elementwise: `masked_fill`
  - Comparison: `==`, `!=`, `>`, `>=`, `<`, `<=`
  - Utility: `zero_grad()` (reset gradients)
  - Autograd: `backward()` (compute gradients for the computation graph)

### Layers
- `ne.Flatten()`: Flattens input tensors to 2D (batch, features).
- `ne.Linear(out_features, activation=None)`: Fully connected layer with optional activation.
- `ne.LSTM(...)`: Long Short-Term Memory layer with options for attention, bidirectionality, sequence/state output. You can build deep LSTM networks by stacking multiple LSTM layers. When stacking, ensure that the hidden units for subsequent layers are set correctly:
    - For a standard LSTM, the hidden state shape for the last timestep is `(batch, hidden_units)`.
    - For a bidirectional LSTM, the hidden and cell state shape becomes `(batch, hidden_units * 2)`.
    - If attention is enabled, the hidden state shape is `(batch, hidden_units + input_size[-1])`.
    - If subsequent layers require state initializations from prior layers, set the hidden units accordingly to match the output shape of the previous LSTM (including adjustments for bidirectionality and attention).
- `ne.MultiplicativeAttention(units)`: Dot-product attention mechanism for sequence models.
- `ne.MultiHeadSelfAttention(num_heads=1, in_size=None)`: Multi-head self-attention layer for transformer and sequence models.
- `ne.Embedding(embed_size, vocab_size, n_timesteps=None)`: Embedding layer for mapping indices to dense vectors, with optional positional encoding.
- `ne.LayerNorm(norm_shape, eps=1e-7)`: Layer normalization for stabilizing training.
- `ne.Dropout(prob=0.5)`: Dropout regularization for reducing overfitting.
- All layers inherit from a common base and support extensibility for custom architectures.

### Activations
- `ne.Sigmoid()`: Sigmoid activation function.
- `ne.Tanh()`: Tanh activation function.
- `ne.RELU(alpha=0, parametric=False)`: ReLU, Leaky ReLU, or Parametric ReLU activation.
- `ne.Softmax(axis=-1)`: Softmax activation for classification tasks.
- All activations inherit from a common base and support extensibility for custom architectures.

### Loss Functions
- `ne.CrossEntropy(binary=False, eps=1e-7)`: Categorical and binary cross-entropy loss for classification tasks.
- `ne.MSE()`: Mean Squared Error loss for regression.
- `ne.MAE()`: Mean Absolute Error loss for regression.
- `ne.Huber(delta=1.0)`: Huber loss, robust to outliers.
- `ne.GaussianNLL(eps=1e-7)`: Gaussian Negative Log Likelihood loss for probabilistic regression.
- `ne.KLDivergence(eps=1e-7)`: Kullback-Leibler Divergence loss for measuring distribution differences.
- All loss functions inherit from a common base and support autograd.

### Optimizers
- `ne.Adam(lr=1e-3, betas=(0.9, 0.99), eps=1e-7, reg=0)`: Adam optimizer (switches to RMSProp if only one beta is provided).
- `ne.SGD(lr=1e-2, reg=0, momentum=0, nesterov=False)`: Stochastic Gradient Descent with optional momentum and Nesterov acceleration.
- All optimizers support L2 regularization and gradient reset.

### Metrics
- `ne.ClassificationMetrics(num_classes=None, acc=True, prec=False, rec=False, f1=False, cm=False)`: Computes accuracy, precision, recall, F1 score, and confusion matrix for classification tasks.
- `ne.RMSE()`: Root Mean Squared Error for regression.
- `ne.R2()`: R2 Score for regression.
- All metrics return results as dictionaries and support batch evaluation.

### Model API
- `ne.Model(input_size, optimizer, loss, metrics)`: Create a model specifying input size, optimizer, loss function, and metrics.
- Add layers by calling the model instance: `model(layer1, layer2, ...)` or using `model.build(layer1, layer2, ...)`.
- `model.train(x, y, epochs=10, batch_size=64, random_seed=None)`: Train the model on data, with support for batching, shuffling, and metric/loss reporting per epoch.
- `model.eval(x, y)`: Evaluate the model on data, prints loss and metrics, and returns output tensor. Also prints confusion matrix if enabled in metrics.
- Layers are set to training or evaluation mode automatically during `train` and `eval`.

### Utilities
- Tensor creation: `tensor(data, requires_grad=False)`, `zeros(shape)`, `ones(shape)`, `rand(shape)`, `randn(shape, xavier=False)`, `randint(low, high, shape)` and their `_like` variants for matching shapes.
- Tensor operations: `sum`, `max`, `min`, `mean`, `var`, `log`, `sqrt`, `exp`, `abs`, `concat`, `stack`, `where`, `clip`, `array(data, dtype=...)` for elementwise, reduction, and conversion operations.
- Encoding: `one_hot(labels, num_classes=None)` for converting integer labels to one-hot encoding.

### Extensibility
NeuralEngine is designed for easy extension and customization:
- **Custom Layers**: Create new layers by inheriting from the `Layer` base class and implementing the `forward(self, x)` method. You can add parameters, initialization logic, and custom computations as needed. All built-in layers follow this pattern, making it simple to add your own.
- **Custom Losses**: Define new loss functions by inheriting from the `Loss` base class and implementing the `compute(self, z, y)` method. This allows you to integrate any custom loss logic with autograd support.
- **Custom Optimizers**: Implement new optimization algorithms by inheriting from the `Optimizer` base class and providing your own `step(self)` method. You can manage optimizer state and parameter updates as required.
- **Custom Metrics**: Add new metrics by inheriting from the `Metric` base class and implementing the `compute(self, z, y)` method. Alternatively, you can pass a function of the form `func(x, y) -> dict[str, float | np.ndarray]` directly to the model's metrics argument for flexible evaluation.
- All core components are modular and can be replaced or extended for research, experimentation, or production use.

## Contribution Guide

NeuralEngine is an open-source project, and I warmly welcome all kinds of contributions whether it's code, documentation, bug reports, feature ideas, or sharing cool examples. If you want to help make NeuralEngine better, you're in the right place!

### How to Contribute
- **Fork the repository** and create a new branch for your feature, fix, or documentation update.
- **Keep it clean and consistent**: Try to follow the existing code style, naming conventions, and documentation patterns. Well-commented, readable code is always appreciated!
- **Add tests** for new features or bug fixes if you can.
- **Document your changes**: Update or add docstrings and README sections so others can easily understand your work.
- **Open a pull request** describing what you've changed and why it's awesome.

### What Can You Contribute?
- New layers, loss functions, optimizers, metrics, or utility functions
- Improvements to existing components
- Bug fixes and performance tweaks
- Documentation updates and tutorials
- Example scripts and notebooks
- Feature requests, feedback, and ideas

Every contribution is reviewed for quality and consistency, but don't worry—if you have questions or need help, just open an issue or start a discussion. I'm happy to help and love seeing new faces in the community!

Thanks for making NeuralEngine better, together! 🚀

## License
MIT License with attribution clause. See LICENSE file for details.

## Attribution
If you use this project, please credit the original developer: Prajjwal Pratap Shah.

Special thanks to the Autograd Framework From Scratch project by Eduardo Leitão da Cunha Opice Leão, which served as a reference for tensor operations and autograd implementations.