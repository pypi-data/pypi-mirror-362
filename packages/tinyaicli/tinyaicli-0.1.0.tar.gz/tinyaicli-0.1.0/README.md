# Tiny AI

A powerful CLI tool for training small Language Models (LLMs) and Vision models using custom YAML configurations for reproducible research.

## Features

-  **Multi-Model Support**: Train both LLMs and Vision models
-  **Hydra Configuration**: YAML-based configs for reproducible experiments
-  **Experiment Tracking**: Integrated wandb logging and TensorBoard support
-  **Modular Architecture**: Easy to extend and customize
-  **Rich Logging**: Beautiful CLI output with progress tracking
-  **Reproducible Research**: Deterministic training with seed management


### Installation

```bash
# Clone the repository
git clone https://github.com/nheinstein/TinyAI.git
cd TinyAI

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Basic Usage

```bash
# Train an LLM with default config
python -m tinyai.train model=llm

# Train a vision model with custom config
python -m tinyai.train model=vision config=vision_custom

# Override config parameters
python -m tinyai.train model=llm training.batch_size=32 training.learning_rate=1e-4

# Run with wandb logging
python -m tinyai.train model=llm logging.wandb=true logging.project_name=my_experiment
```

## Configuration

The trainer uses Hydra for configuration management. Configs are stored in `configs/` directory:

```
configs/
├── model/
│   ├── llm.yaml
│   └── vision.yaml
├── training/
│   ├── default.yaml
│   └── custom.yaml
└── logging/
    └── default.yaml
```

### Example Config Structure

```yaml
# configs/model/llm.yaml
defaults:
  - training: default
  - logging: default

model:
  type: "transformer"
  vocab_size: 50257
  hidden_size: 768
  num_layers: 12
  num_heads: 12

training:
  batch_size: 16
  learning_rate: 1e-4
  num_epochs: 10
  warmup_steps: 1000

data:
  train_path: "data/train.txt"
  val_path: "data/val.txt"
  max_length: 512

logging:
  wandb: true
  project_name: "tiny-llm"
  log_interval: 100
```

## Project Structure

```
TinyAI/
├── tinyai/
│   ├── __init__.py
│   ├── train.py              # Main training script
│   ├── models/               # Model implementations
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   └── vision.py
│   ├── data/                 # Data loading utilities
│   │   ├── __init__.py
│   │   ├── datasets.py
│   │   └── tokenizers.py
│   ├── training/             # Training utilities
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   └── optimizer.py
│   └── utils/                # Utility functions
│       ├── __init__.py
│       ├── logging.py
│       └── metrics.py
├── configs/                  # Hydra configurations
├── scripts/                  # Utility scripts
├── requirements.txt
├── setup.py
└── README.md
```

## Advanced Usage

### Custom Model Implementation

```python
# tinyai/models/custom_model.py
from tinyai.models.base import BaseModel

class CustomModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        # Your model implementation

    def forward(self, x):
        # Forward pass
        return output
```

### Custom Training Loop

```python
# Override training behavior
class CustomTrainer(Trainer):
    def training_step(self, batch):
        # Custom training logic
        pass
```

## License

MIT License - see LICENSE file for details.
