<h1 align="center" style="color:#007BFF;"><strong>SoundByte</strong></h1>

## An Academic-friendly DL Toolkit for Accelerated Learning and Prototyping


<p align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+">
  </a>
  <a href="https://pytorch.org/">
    <img src="https://img.shields.io/badge/PyTorch-2.0+-red.svg" alt="PyTorch 2.0+">
  </a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">
    <img src="https://img.shields.io/badge/License-GNU-blue.svg" alt="License: GNU GPLv3">
  </a>
</p>



## Key Features

| Feature                        | Description |
|-------------------------------|-------------|
| **Configuration-Driven Design** | Define entire experiments via simple JSON config files—no hardcoding needed. |
| **Maximum Modularity**         | Swap any model, optimizer, or dataloader without touching core source code. |
| **Plugin Architecture**        | Register and auto-discover custom components with ease. |
| **Custom Minibatch Logic**     | Implement tailored forward/backward passes for specialized training needs. |
| **Type Safety**                | Built-in Pydantic validation ensures safe and correct configurations. |
| **Multiple Paradigms**         | Supports both supervised classification and knowledge distillation out-of-the-box. |
| **Production Ready**           | Includes logging, error handling, and output serialization for robust use. |
| **Extensible**                 | Clean, documented interfaces make it easy to plug in new ideas. |
| **Console Command**            | Run full experiments using the simple `soundbyte` command-line interface. |


---
## Installation 
- Python 3.11 or higher
- conda (for environment management)

```bash
   pip install soundbyte
```
---


## 📝 Changelog — Version `v0.1.3`

---

### Improved Experiment Execution

**Before (`v0.1.2`)**  
To run an experiment, you had to specify the paradigm explicitly:

```bash
soundbyte supervised_classification --json_config /path/to/json
```

**Now (`v0.1.3`)**  
You can run any experiment with a single streamlined command:

#### 🔹 From the Command Line
```bash
soundbyte run examples/configs/classification_example.json
soundbyte run examples/configs/distillation_example.json
soundbyte run examples/configs/custom_logic_example.json
```

#### 🔹 From a Python Script
```bash
python examples/run_classification.py
python examples/run_distillation.py
python examples/run_toy_experiment.py
```

### (+) MTSQ Quantization Algorithm Support 🔗[Paper](https://ieeexplore.ieee.org/abstract/document/10684732)

---

### 🧩 Custom Module Integration Made Easy

**Before (`v0.1.2`)**  
You had to reference custom modules in your JSON config:
```json
{
  ...
  "model": "path/to/custom_model.py"
  ...
}
```

**Now (`v0.1.3`)**  
You can plug in your modules using decorators and registration logic.

#### ✅ Example: Registering a Custom Model

```python
from soundbyte.plugins.registry import register
from soundbyte.core.interfaces import ModelOps
import torch.nn as nn

@register('model_ops', 'my_custom_model')
class MyCustomModel(nn.Module, ModelOps):
    def __init__(self, num_classes=10, hidden_size=128):
        super().__init__()
        self.fc = nn.Linear(784, hidden_size)
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc(x))
        return self.classifier(x)

    def get_model(self):
        return self

    def get_config(self):
        return {
            "num_classes": self.num_classes,
            "hidden_size": self.hidden_size
        }
```

---

You can now register other components similarly:

| Component Type     | Registry Key       | Example Use Case                  |
|--------------------|--------------------|-----------------------------------|
| Loss Functions     | `penalty_ops`      | Custom loss                       |
| Optimizers         | `control_ops`      | Custom optimizer                  |
| Schedulers         | `schedule_ops`     | Custom learning rate scheduler    |
| Training Pipeline  | `train_ops`        | Full custom training logic        |
| Evaluation Logic   | `audit_ops`        | Custom evaluation/reporting       |

---


## Quick Start
### 1. Run a Classification Example

```bash
# Using the command-line interface
soundbyte run examples/configs/classification_example.json

# Using Python script
python examples/run_classification.py
```

### 2. Run a Knowledge Distillation Example

```bash
# Using CLI
soundbyte run examples/configs/distillation_example.json

# Using Python script
python examples/run_distillation.py
```

### 3. Run Custom Logic Example

```bash
# Example with custom minibatch logic
soundbyte run examples/configs/custom_logic_example.json

# Comprehensive toy experiment
python examples/run_toy_experiment.py
```

## Command Line Interface

The toolkit provides a comprehensive CLI through the `soundbyte` command:

```bash
# Run experiments
soundbyte run <config.json>

# Validate configurations
soundbyte validate <config.json>

# List available components
soundbyte list-components
soundbyte list-components --type model_ops

# Show experiment information
soundbyte info <config.json>

# Initialize example configurations
soundbyte init --template classification
soundbyte init --template distillation

# Override parameters
soundbyte run config.json --override "train_ops.params.max_epochs=20"
```
---
## Modular Component System
### Plugin Registry
Components are automatically discovered and registered using decorators:

```python
from soundbyte.plugins.registry import register

@register('model_ops')
class MyCustomModel(nn.Module, ModelOps):
    # Implementation
```

### Configuration Management
Experiments are defined through hierarchical JSON configurations with Pydantic validation:

```json
{
  "name": "my_experiment",
  "data_ops": {"name": "cifar10", "params": {"batch_size": 128}},
  "model_ops": {"name": "resnet18", "params": {"num_classes": 10}},
  "control_ops": {"name": "adam", "params": {"lr": 0.001}}
}
```

## Custom Minibatch Logic

SoundByte supports custom forward and backward pass logic through Python files:

### Configuration
```json
{
  "data_ops": {
    "name": "cifar10",
    "params": {"batch_size": 64},
    "train_minibatch_logic": "path/to/custom_logic.py",
    "val_minibatch_logic": "path/to/custom_logic.py"
  }
}
```

### Implementation
```python
def custom_minibatch_logic(idx, minibatch, model, loss_fn, optimizer, scheduler, device):
    """
    Custom training logic for specialized requirements.

    Args:
        idx: Batch index
        minibatch: Data batch (data, targets)
        model: Neural network model
        loss_fn: Loss function
        optimizer: Optimizer
        scheduler: Learning rate scheduler
        device: Device for computation

    Returns:
        tuple: (outputs, loss)
    """
    data, targets = minibatch
    data, targets = data.to(device), targets.to(device)

    optimizer.zero_grad()
    outputs = model(data)
    loss = loss_fn.compute_loss(outputs, targets)

    # Custom logic - skip gradients for every second batch
    if idx % 2 == 0:
        loss.backward()
        optimizer.step()

    return outputs, loss
```
---
## Available Components

SoundByte follows a plugin-based architecture. Each operation type (data, model, loss, optimizer, etc.) supports modular, swappable components.
### Datasets
| Component | Description                          |
|-----------|--------------------------------------|
| `cifar10` | CIFAR-10 dataset with preprocessing  |
| `mnist`   | MNIST dataset with normalization     |

### Models
| Component       | Description                     |
|----------------|---------------------------------|
| `simple_convnet` | Lightweight CNN for CIFAR-10   |
| `mnist_net`     | Specialized network for MNIST   |
| `resnet18`      | ResNet-18 architecture          |
| `vgg16`         | VGG-16 architecture             |
| `densenet121`   | DenseNet-121 architecture       |
| `mobilenet_v2`  | MobileNet V2 architecture       |

### Loss Functions
| Component               | Description                                 |
|-------------------------|---------------------------------------------|
| `cross_entropy`         | Standard cross-entropy loss                 |
| `focal_loss`            | Focal loss for imbalanced datasets          |
| `label_smoothing`       | Cross-entropy with label smoothing          |
| `knowledge_distillation`| KL divergence-based distillation loss       |
| `mse_loss`              | Mean squared error for regression           |
| `huber_loss`            | Robust Huber loss                           |
| `bce_loss`              | Binary cross-entropy                        |
| `bce_with_logits`       | BCE with logits                             |

### Optimizers
| Component   | Description                       |
|------------|-----------------------------------|
| `adam`     | Adam optimizer                    |
| `adamw`    | AdamW with weight decay           |
| `sgd`      | Stochastic gradient descent       |
| `rmsprop`  | RMSprop optimizer                 |
| `adagrad`  | Adagrad optimizer                 |
| `adadelta` | Adadelta optimizer                |
| `nadam`    | NAdam optimizer                   |
| `radam`    | RAdam optimizer                   |

### Schedulers
| Component                        | Description                              |
|----------------------------------|------------------------------------------|
| `step_lr`                        | Step learning rate decay                 |
| `multi_step_lr`                 | Multi-step decay                         |
| `exponential_lr`                | Exponential decay                        |
| `cosine_annealing_lr`          | Cosine annealing                         |
| `cosine_annealing_warm_restarts` | Cosine annealing with warm restarts     |
| `reduce_lr_on_plateau`         | Adaptive reduction on performance plateau|
| `cyclic_lr`                    | Cyclic learning rate                     |
| `linear_lr`                    | Linear learning rate schedule            |
| `polynomial_lr`                | Polynomial decay                         |

### Traininig Paradigms
| Component      | Description                       |
|----------------|-----------------------------------|
| `classification` | Standard supervised training    |
| `distillation`   | Knowledge distillation training |

### Evaluation Paradigms
| Component      | Description                                               |
|----------------|-----------------------------------------------------------|
| `classification` | Accuracy, precision, recall, F1                         |
| `distillation`   | Evaluation with agreement and KL-divergence metrics     |
| `regression`     | MSE, MAE, R² for regression tasks                       |

```json
Additional components are currently under development and will be added soon.
```

---

## Supported Training Paradigms

### 1. Supervised Classification

Standard supervised learning with comprehensive evaluation metrics.

**Example Configuration:**
```json
{
  "name": "cifar10_classification",
  "data_ops": {"name": "cifar10", "params": {"batch_size": 128}},
  "model_ops": {"name": "simple_convnet", "params": {"num_classes": 10}},
  "penalty_ops": {"name": "cross_entropy", "params": {}},
  "control_ops": {"name": "adam", "params": {"lr": 0.001}},
  "train_ops": {"name": "classification", "params": {"max_epochs": 50}},
  "audit_ops": {"name": "classification", "params": {"metrics": ["accuracy", "f1"]}}
}
```

### 2. Knowledge Distillation

Teacher-student training with configurable temperature and loss combination.

**Example Configuration:**
```json
{
  "name": "knowledge_distillation",
  "data_ops": {"name": "cifar10", "params": {"batch_size": 128}},
  "teacher_model_ops": {"name": "resnet18", "params": {"num_classes": 10}},
  "student_model_ops": {"name": "simple_convnet", "params": {"num_classes": 10}},
  "distillation_penalty_ops": {
    "name": "knowledge_distillation", 
    "params": {"temperature": 4.0, "alpha": 0.5}
  },
  "train_ops": {"name": "distillation", "params": {"max_epochs": 50}},
  "audit_ops": {"name": "distillation", "params": {"compute_agreement": true}}
}
```

## Programmatic Usage

### Basic Experiment Execution

```python
from soundbyte import run_experiment, load_config

# Load and run experiment
config = load_config("my_experiment.json")
results = run_experiment("my_experiment.json")

print(f"Test Accuracy: {results['test_metrics']['accuracy']:.2f}%")
```

### Advanced Usage with ExperimentRunner

```python
from soundbyte import ExperimentRunner
from soundbyte.config.experiment import ExperimentConfig

# Create configuration programmatically
config_dict = {
    "name": "programmatic_experiment",
    "data_ops": {"name": "mnist", "params": {"batch_size": 64}},
    "model_ops": {"name": "mnist_net", "params": {"num_classes": 10}},
    # ... other configuration
}

config = ExperimentConfig(**config_dict)
runner = ExperimentRunner(config)
results = runner.run()
```

### Custom Component Registration

```python
from soundbyte.plugins.registry import register
from soundbyte.core.interfaces import ModelOps
import torch.nn as nn

@register('model_ops', 'my_custom_model')
class MyCustomModel(nn.Module, ModelOps):
    def __init__(self, num_classes=10, hidden_size=128):
        super().__init__()
        self.fc = nn.Linear(784, hidden_size)
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc(x))
        return self.classifier(x)

    def get_model(self):
        return self

    def get_config(self):
        return {"num_classes": self.num_classes, "hidden_size": self.hidden_size}
```

---
## Extending the Toolkit

### Adding New Components

1. **Create Component Class**
   ```python
   from soundbyte.core.interfaces import ModelOps
   from soundbyte.plugins.registry import register

   @register('model_ops', 'my_new_model')
   class MyNewModel(ModelOps):
       # Implement required methods
   ```

2. **Update Configuration**
   ```json
   {
     "model_ops": {"name": "my_new_model", "params": {"custom_param": 42}}
   }
   ```

### Adding New Training Paradigms

1. **Implement Trainer Interface**
   ```python
   from soundbyte.core.interfaces import TrainOps
   from soundbyte.plugins.registry import register

   @register('train_ops', 'my_new_paradigm')
   class MyNewParadigmTrainer(TrainOps):
       def train(self, model, data_ops, control_ops, penalty_ops, audit_ops, device, **kwargs):
           # Implement training logic
   ```

2. **Create Specialized Components**
3. **Update Configuration Schema if Needed**

## Custom Logic Examples

The toolkit includes several custom minibatch logic examples:

- **Gradient Skipping**: Skip gradients for specific batches
- **Gradient Accumulation**: Accumulate gradients over multiple batches
- **Mixup**: Data augmentation with sample mixing
- **Cutout**: Random masking augmentation
- **Label Smoothing**: Custom label smoothing implementation
- **Focal Loss**: Custom focal loss for class imbalance
- **Adversarial Training**: FGSM-based adversarial examples
---
## Experiment Tracking
Update in progress