"""
Model configuration presets for different architectures.
This file contains target modules and other architecture-specific settings
for different model families.
"""
from typing import Dict, Any, Optional, List
import re

# Common target modules for different architectures
MODEL_CONFIGS = {
    # GPT Models
    'gpt2': {
        'target_modules': ['c_attn', 'c_proj', 'c_fc'],
        'task_type': 'CAUSAL_LM',
    },
    # LLaMA/Mistral Models
    'llama': {
        'target_modules': ['q_proj', 'v_proj'],
        'task_type': 'CAUSAL_LM',
    },
    # DeepSeek Models
    'deepseek': {
        'target_modules': ['q_proj', 'v_proj'],
        'task_type': 'CAUSAL_LM',
    },
    # MPT Models
    'mpt': {
        'target_modules': ['Wqkv', 'out_proj'],
        'task_type': 'CAUSAL_LM',
    },
    # Default fallback (will try to auto-detect)
    'default': {
        'target_modules': None,  # Will be auto-detected
        'task_type': 'CAUSAL_LM',
    }
}

def get_model_config(model_name: str) -> Dict[str, Any]:
    """
    Get the appropriate configuration for a given model name.
    
    Args:
        model_name: The name or path of the model
        
    Returns:
        Dictionary containing model configuration
    """
    model_name = model_name.lower()
    
    # Check for specific model patterns
    if any(x in model_name for x in ['gpt2', 'gpt3', 'gpt-2', 'gpt-3']):
        return MODEL_CONFIGS['gpt2']
    elif any(x in model_name for x in ['llama', 'vicuna', 'alpaca']):
        return MODEL_CONFIGS['llama']
    elif 'deepseek' in model_name:
        return MODEL_CONFIGS['deepseek']
    elif 'mpt' in model_name:
        return MODEL_CONFIGS['mpt']
    
    # Default to auto-detection
    return MODEL_CONFIGS['default']

def auto_detect_target_modules(model):
    """
    Attempt to automatically detect target modules for LoRA.
    
    Args:
        model: The model to analyze
        
    Returns:
        List of target module names or None if detection fails
    """
    from transformers import PreTrainedModel
    from peft.utils import TRANSFORMERS_MODELS_TO_LORA_TARGET_MODULES_MAPPING
    
    if not isinstance(model, PreTrainedModel):
        return None
        
    # Try to get target modules from PEFT's mapping
    for model_type, modules in TRANSFORMERS_MODELS_TO_LORA_TARGET_MODULES_MAPPING.items():
        if model.__class__.__name__.startswith(model_type):
            return modules
    
    # Fallback: Look for common attention layer patterns
    target_modules = set()
    for name, module in model.named_modules():
        if any(x in name.lower() for x in ['q_proj', 'v_proj', 'c_attn', 'c_proj', 'out_proj']):
            target_modules.add(name.split('.')[-1])
    
    return list(target_modules) if target_modules else None
