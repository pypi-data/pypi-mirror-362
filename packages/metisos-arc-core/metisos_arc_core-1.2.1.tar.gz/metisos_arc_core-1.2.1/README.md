# ARC Core

Adaptive Recursive Consciousness (ARC) Core is a framework for building continual learning AI systems that can learn and reason over time. It features:

- **Continual Learning**: Real-time learning with LoRA adapters
- **Reasoning Engine**: Graph-based reasoning and pattern recognition
- **Biological Learning**: Implements biological learning mechanisms
- **Model Agnostic**: Works with various transformer architectures

## Installation

```bash
pip install arc-core
```

## Quick Start

```python
from arc_core import LearningARCConsciousness, ARCCore, ARCTrainer  # All aliases for the same class

# Initialize with a base model
arc = LearningARCConsciousness(model_name="gpt2")

# Learn from interactions
arc.learn_from_experience("The sky appears blue due to Rayleigh scattering")

# Generate responses
response = arc.generate("Why is the sky blue?")
print(response)
```

## Features

- **Dynamic LoRA Adapters**: Automatically adapts to different model architectures
- **Reasoning Graph**: Maintains a knowledge graph of learned concepts
- **Biological Learning**: Implements contextual gating and cognitive inhibition
- **Persistence**: Saves learning progress between sessions

## Documentation

For detailed documentation, see [ARC Core Documentation](https://github.com/yourusername/arc-core).

## License

MIT
