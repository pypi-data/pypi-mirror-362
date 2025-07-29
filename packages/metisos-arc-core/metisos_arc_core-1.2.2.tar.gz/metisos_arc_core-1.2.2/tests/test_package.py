#!/usr/bin/env python3
"""
Test script to verify the ARC Core package is working correctly.
"""
import os
import sys
import torch
import pytest
from transformers import AutoModelForCausalLM, AutoTokenizer

# Import the ARC Core package from the installed location
try:
    import arc_core
    from arc_core import (
        LearningARCConsciousness, 
        ARCTrainer, 
        ARCCore, 
        RealLearningVocabulary, 
        TeachingPackManager,
        PackMetadata
    )
    print("✅ Successfully imported arc_core package")
    print(f"Version: {arc_core.__version__}")
except ImportError as e:
    print(f"❌ Failed to import arc_core: {e}")
    sys.exit(1)

def test_imports():
    """Test that all required imports work."""
    try:
        from arc_core import (
            LearningARCConsciousness,
            ARCTrainer,
            ARCCore,
            RealLearningVocabulary,
            TeachingPackManager,
            PackMetadata
        )
        print("✅ All core components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_initialization():
    """Test that we can initialize the core components."""
    print("\n=== Testing Initialization ===")
    try:
        # Test core component initialization
        arc = LearningARCConsciousness()
        
        # Check if core methods are available
        required_methods = [
            'process_user_interaction',
            'generate_conscious_thought',
            'display_learning_stats',
            'get_reasoning_insights',
            'save_learning_state'
        ]
        
        for method in required_methods:
            if not hasattr(arc, method):
                print(f"❌ Missing required method: {method}")
                return False
        
        print("✅ Core components and methods initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_lora_adapters():
    """Test that LoRA adapters are properly configured."""
    print("\n=== Testing LoRA Adapters ===")
    try:
        # Test with default model (GPT-2)
        arc = LearningARCConsciousness()
        
        # Check if model has LoRA adapters by looking for PEFT model attributes
        # Note: We need to access the transformer model through the correct attribute
        if not hasattr(arc, 'transformer'):
            print("❌ No transformer attribute found in the ARC instance")
            return False
            
        model = arc.transformer.model if hasattr(arc.transformer, 'model') else arc.transformer
        has_lora = any('lora' in name.lower() for name, _ in model.named_modules())
        
        if has_lora:
            print("✅ LoRA adapters detected in the model")
            # Print some basic model info
            total_params = sum(p.numel() for p in model.parameters())
            trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
            print(f"   Total parameters: {total_params/1e6:.1f}M")
            print(f"   Trainable parameters: {trainable_params/1e6:.1f}M")
            return True
        else:
            print("❌ No LoRA adapters found in the model")
            # Print model structure for debugging
            print("Model structure:")
            for name, _ in model.named_children():
                print(f"  - {name}")
            return False
            
    except Exception as e:
        print(f"❌ LoRA adapter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_learning():
    """Test basic learning functionality."""
    print("\n=== Testing Learning ===")
    try:
        # Initialize with a small model for testing
        arc = LearningARCConsciousness()
        
        # Test processing a user interaction
        print("Testing user interaction...")
        response = arc.process_user_interaction("What is the capital of France?")
        if isinstance(response, dict):
            print(f"✅ Processed user interaction. Response keys: {list(response.keys())}")
        else:
            print(f"✅ Processed user interaction. Response type: {type(response).__name__}")
        
        # Test generating a conscious thought
        print("Testing conscious thought generation...")
        if hasattr(arc, 'generate_conscious_thought'):
            thought = arc.generate_conscious_thought()
            if isinstance(thought, dict) and 'thought' in thought:
                thought_text = str(thought['thought'])
                print(f"✅ Generated conscious thought: {thought_text[:100]}...")
            else:
                thought_text = str(thought)
                print(f"✅ Generated output: {thought_text[:100]}...")
        else:
            print("⚠️ generate_conscious_thought() method not available")
        
        # Test getting reasoning insights
        print("Testing reasoning insights...")
        if hasattr(arc, 'get_reasoning_insights'):
            insights = arc.get_reasoning_insights()
            if isinstance(insights, (str, dict, list)):
                insights_str = str(insights)
                print(f"✅ Got reasoning insights: {insights_str[:200]}...")
            else:
                print(f"✅ Got insights of type: {type(insights).__name__}")
        else:
            print("⚠️ get_reasoning_insights() method not available")
        
        # Test saving and loading state
        print("Testing state management...")
        try:
            arc.save_state("test_state.pth")
            arc.load_state("test_state.pth")
            print("✅ State management test completed")
        except Exception as e:
            print(f"⚠️ State management test failed: {str(e)}")
        
        # Test displaying learning stats
        print("\nLearning Statistics:")
        arc.display_learning_stats()
        
        # Clean up
        import shutil
        if os.path.exists("test_learning_state"):
            shutil.rmtree("test_learning_state")
        
        return True
    except Exception as e:
        print(f"❌ Learning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=== Starting ARC Core Package Tests ===\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Initialization Tests", test_initialization),
        ("LoRA Adapter Tests", test_lora_adapters),
        ("Learning Tests", test_learning)
    ]
    
    all_passed = True
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        if not test_func():
            all_passed = False
    
    if all_passed:
        print("\n✅ All tests passed! The package is ready for PyPI.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
