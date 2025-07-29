"""
Test script to verify model configurations work as expected.
"""
import unittest
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.arc_core.model_configs import get_model_config, auto_detect_target_modules

class TestModelConfigs(unittest.TestCase):    
    def test_gpt2_config(self):
        """Test GPT-2 model configuration."""
        config = get_model_config("gpt2")
        self.assertEqual(config['task_type'], 'CAUSAL_LM')
        self.assertIn('c_attn', config['target_modules'])
        
        # Test with actual model
        model = AutoModelForCausalLM.from_pretrained("gpt2")
        detected = auto_detect_target_modules(model)
        self.assertIsNotNone(detected)
        self.assertGreater(len(detected), 0)
        
    def test_llama_config(self):
        """Test LLaMA model configuration."""
        config = get_model_config("llama-7b")
        self.assertEqual(config['task_type'], 'CAUSAL_LM')
        self.assertIn('q_proj', config['target_modules'])
        
    def test_deepseek_config(self):
        """Test DeepSeek model configuration."""
        config = get_model_config("deepseek-coder-6.7b")
        self.assertEqual(config['task_type'], 'CAUSAL_LM')
        self.assertIn('q_proj', config['target_modules'])
        
    def test_mpt_config(self):
        """Test MPT model configuration."""
        config = get_model_config("mpt-7b")
        self.assertEqual(config['task_type'], 'CAUSAL_LM')
        self.assertIn('Wqkv', config['target_modules'])
        
    def test_unknown_model(self):
        """Test with an unknown model name."""
        config = get_model_config("unknown-model-123")
        self.assertEqual(config['task_type'], 'CAUSAL_LM')
        self.assertIsNone(config['target_modules'])  # Should trigger auto-detection

if __name__ == '__main__':
    unittest.main()
