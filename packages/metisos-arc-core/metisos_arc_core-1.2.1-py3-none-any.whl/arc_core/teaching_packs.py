"""
ARC Core Teaching Pack System

This module provides complete teaching pack management functionality including:
- Pack installation and uninstallation
- Teaching pack validation and metadata management
- Built-in teaching packs for common use cases
- Pack usage statistics and logging
- CLI integration for seamless pack management

No emojis used for terminal compatibility.
"""

import os
import json
import yaml
import shutil
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PackMetadata:
    """Teaching pack metadata structure."""
    name: str
    version: str
    description: str
    author: str
    category: str
    difficulty: str
    examples_count: int
    format_version: str = "1.0"
    requirements: List[str] = None
    tags: List[str] = None
    created_date: str = None
    
    def __post_init__(self):
        if self.requirements is None:
            self.requirements = []
        if self.tags is None:
            self.tags = []
        if self.created_date is None:
            self.created_date = time.strftime("%Y-%m-%d")

class TeachingPackManager:
    """Complete teaching pack management system."""
    
    def __init__(self, packs_dir: str = None):
        """Initialize the teaching pack manager."""
        if packs_dir is None:
            # Default to user's home directory
            home_dir = Path.home()
            self.packs_dir = home_dir / ".arc" / "teaching_packs"
        else:
            self.packs_dir = Path(packs_dir)
        
        # Create directories if they don't exist
        self.packs_dir.mkdir(parents=True, exist_ok=True)
        self.installed_packs_dir = self.packs_dir / "installed"
        self.installed_packs_dir.mkdir(exist_ok=True)
        
        # Stats and usage tracking
        self.stats_file = self.packs_dir / "usage_stats.json"
        self.load_stats()
        
        # Built-in teaching packs
        self.builtin_packs = self._create_builtin_packs()
    
    def load_stats(self):
        """Load usage statistics."""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            else:
                self.stats = {
                    "total_installations": 0,
                    "total_training_sessions": 0,
                    "pack_usage": {},
                    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            logger.warning(f"Failed to load stats: {e}")
            self.stats = {}
    
    def save_stats(self):
        """Save usage statistics atomically."""
        try:
            self.stats["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
            temp_file = self.stats_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
            temp_file.replace(self.stats_file)
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")
    
    def _create_builtin_packs(self) -> Dict[str, Dict]:
        """Create built-in teaching packs."""
        return {
            "sentiment-basic": {
                "metadata": PackMetadata(
                    name="sentiment-basic",
                    version="1.0.0",
                    description="Basic sentiment analysis training with positive and negative examples",
                    author="ARC Core Team",
                    category="nlp",
                    difficulty="beginner",
                    examples_count=100,
                    tags=["sentiment", "classification", "nlp", "basic"]
                ),
                "examples": [
                    {"input": "I love this product!", "output": "positive", "confidence": 0.95},
                    {"input": "This is amazing quality", "output": "positive", "confidence": 0.90},
                    {"input": "Great value for money", "output": "positive", "confidence": 0.85},
                    {"input": "Excellent customer service", "output": "positive", "confidence": 0.92},
                    {"input": "This is terrible quality", "output": "negative", "confidence": 0.88},
                    {"input": "I hate this product", "output": "negative", "confidence": 0.95},
                    {"input": "Worst purchase ever", "output": "negative", "confidence": 0.90},
                    {"input": "Complete waste of money", "output": "negative", "confidence": 0.87}
                ]
            },
            "dialogue-basic": {
                "metadata": PackMetadata(
                    name="dialogue-basic",
                    version="1.0.0", 
                    description="Basic conversational dialogue patterns and responses",
                    author="ARC Core Team",
                    category="conversation",
                    difficulty="beginner", 
                    examples_count=50,
                    tags=["dialogue", "conversation", "chat", "basic"]
                ),
                "examples": [
                    {"input": "Hello, how are you?", "output": "Hello! I'm doing well, thank you for asking. How are you today?", "confidence": 0.90},
                    {"input": "What's the weather like?", "output": "I don't have access to current weather data, but I'd be happy to help you find weather information if you let me know your location.", "confidence": 0.85},
                    {"input": "Can you help me?", "output": "Of course! I'd be happy to help. What do you need assistance with?", "confidence": 0.92},
                    {"input": "Thank you", "output": "You're welcome! Is there anything else I can help you with?", "confidence": 0.88}
                ]
            },
            "science-facts": {
                "metadata": PackMetadata(
                    name="science-facts",
                    version="1.0.0",
                    description="Scientific facts and explanations for educational training",
                    author="ARC Core Team",
                    category="education",
                    difficulty="intermediate",
                    examples_count=75,
                    tags=["science", "education", "facts", "learning"]
                ),
                "examples": [
                    {"input": "What is photosynthesis?", "output": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen, using chlorophyll as a catalyst.", "confidence": 0.95},
                    {"input": "Explain gravity", "output": "Gravity is a fundamental force that attracts objects with mass toward each other. Earth's gravity pulls objects toward its center at approximately 9.8 m/s².", "confidence": 0.90},
                    {"input": "What is DNA?", "output": "DNA (Deoxyribonucleic Acid) is the hereditary material that contains genetic instructions for all living organisms, structured as a double helix.", "confidence": 0.93}
                ]
            }
        }
    
    def list_packs(self, show_builtin: bool = True, show_installed: bool = True) -> Dict[str, Any]:
        """List available teaching packs."""
        result = {"builtin": [], "installed": [], "total_count": 0}
        
        if show_builtin:
            for pack_name, pack_data in self.builtin_packs.items():
                metadata = pack_data["metadata"]
                result["builtin"].append({
                    "name": metadata.name,
                    "version": metadata.version,
                    "description": metadata.description,
                    "category": metadata.category,
                    "difficulty": metadata.difficulty,
                    "examples_count": metadata.examples_count,
                    "tags": metadata.tags,
                    "type": "builtin"
                })
        
        if show_installed:
            for pack_dir in self.installed_packs_dir.iterdir():
                if pack_dir.is_dir():
                    try:
                        pack_file = pack_dir / "pack.yml"
                        if pack_file.exists():
                            with open(pack_file, 'r') as f:
                                pack_config = yaml.safe_load(f)
                                result["installed"].append({
                                    **pack_config.get("metadata", {}),
                                    "type": "installed",
                                    "location": str(pack_dir)
                                })
                    except Exception as e:
                        logger.warning(f"Failed to read pack {pack_dir.name}: {e}")
        
        result["total_count"] = len(result["builtin"]) + len(result["installed"])
        return result
    
    def install_pack(self, pack_name: str, force: bool = False) -> bool:
        """Install a teaching pack."""
        try:
            # Check if it's a built-in pack
            if pack_name in self.builtin_packs:
                return self._install_builtin_pack(pack_name, force)
            else:
                # For now, only support built-in packs
                # Future: support installing from files or URLs
                logger.error(f"Pack '{pack_name}' not found in built-in packs")
                return False
                
        except Exception as e:
            logger.error(f"Failed to install pack '{pack_name}': {e}")
            return False
    
    def _install_builtin_pack(self, pack_name: str, force: bool = False) -> bool:
        """Install a built-in teaching pack."""
        pack_data = self.builtin_packs[pack_name]
        pack_dir = self.installed_packs_dir / pack_name
        
        # Check if already installed
        if pack_dir.exists() and not force:
            logger.warning(f"Pack '{pack_name}' already installed. Use --force to reinstall.")
            return False
        
        # Create pack directory
        if pack_dir.exists():
            shutil.rmtree(pack_dir)
        pack_dir.mkdir()
        
        # Save metadata as pack.yml
        metadata_dict = asdict(pack_data["metadata"])
        pack_config = {
            "metadata": metadata_dict,
            "format_version": "1.0"
        }
        
        with open(pack_dir / "pack.yml", 'w') as f:
            yaml.dump(pack_config, f, default_flow_style=False)
        
        # Save examples as pack.json
        with open(pack_dir / "pack.json", 'w') as f:
            json.dump({
                "examples": pack_data["examples"],
                "metadata": metadata_dict
            }, f, indent=2)
        
        # Update stats
        self.stats["total_installations"] += 1
        if pack_name not in self.stats["pack_usage"]:
            self.stats["pack_usage"][pack_name] = {
                "installations": 0,
                "training_sessions": 0,
                "last_used": None
            }
        self.stats["pack_usage"][pack_name]["installations"] += 1
        self.save_stats()
        
        logger.info(f"Successfully installed teaching pack: {pack_name}")
        return True
    
    def uninstall_pack(self, pack_name: str) -> bool:
        """Uninstall a teaching pack."""
        try:
            pack_dir = self.installed_packs_dir / pack_name
            if not pack_dir.exists():
                logger.error(f"Pack '{pack_name}' is not installed")
                return False
            
            shutil.rmtree(pack_dir)
            logger.info(f"Successfully uninstalled teaching pack: {pack_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall pack '{pack_name}': {e}")
            return False
    
    def validate_pack(self, pack_name: str) -> Dict[str, Any]:
        """Validate a teaching pack."""
        result = {"valid": False, "errors": [], "warnings": [], "info": {}}
        
        try:
            pack_dir = self.installed_packs_dir / pack_name
            if not pack_dir.exists():
                result["errors"].append(f"Pack '{pack_name}' is not installed")
                return result
            
            # Check required files
            pack_yml = pack_dir / "pack.yml"
            pack_json = pack_dir / "pack.json"
            
            if not pack_yml.exists():
                result["errors"].append("Missing pack.yml file")
            
            if not pack_json.exists():
                result["errors"].append("Missing pack.json file")
            
            if result["errors"]:
                return result
            
            # Validate pack.yml
            with open(pack_yml, 'r') as f:
                pack_config = yaml.safe_load(f)
                
            if "metadata" not in pack_config:
                result["errors"].append("Missing metadata in pack.yml")
            else:
                metadata = pack_config["metadata"]
                required_fields = ["name", "version", "description", "author", "category"]
                for field in required_fields:
                    if field not in metadata:
                        result["errors"].append(f"Missing required metadata field: {field}")
            
            # Validate pack.json
            with open(pack_json, 'r') as f:
                pack_data = json.load(f)
                
            if "examples" not in pack_data:
                result["errors"].append("Missing examples in pack.json")
            else:
                examples = pack_data["examples"]
                if not isinstance(examples, list):
                    result["errors"].append("Examples must be a list")
                elif len(examples) == 0:
                    result["warnings"].append("Pack contains no examples")
                else:
                    result["info"]["example_count"] = len(examples)
                    
                    # Validate example format
                    for i, example in enumerate(examples):
                        if not isinstance(example, dict):
                            result["errors"].append(f"Example {i} is not a dictionary")
                            continue
                        
                        if "input" not in example:
                            result["errors"].append(f"Example {i} missing 'input' field")
                        if "output" not in example:
                            result["errors"].append(f"Example {i} missing 'output' field")
            
            if not result["errors"]:
                result["valid"] = True
                result["info"]["pack_name"] = pack_name
                result["info"]["location"] = str(pack_dir)
                logger.info(f"Pack '{pack_name}' validation successful")
            else:
                logger.warning(f"Pack '{pack_name}' validation failed: {len(result['errors'])} errors")
                
        except Exception as e:
            result["errors"].append(f"Validation error: {e}")
            logger.error(f"Failed to validate pack '{pack_name}': {e}")
        
        return result
    
    def get_pack_info(self, pack_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a teaching pack."""
        try:
            # Check built-in packs first
            if pack_name in self.builtin_packs:
                pack_data = self.builtin_packs[pack_name]
                metadata = asdict(pack_data["metadata"])
                return {
                    **metadata,
                    "type": "builtin",
                    "examples_preview": pack_data["examples"][:3],  # Show first 3 examples
                    "total_examples": len(pack_data["examples"])
                }
            
            # Check installed packs
            pack_dir = self.installed_packs_dir / pack_name
            if pack_dir.exists():
                pack_yml = pack_dir / "pack.yml"
                pack_json = pack_dir / "pack.json"
                
                if pack_yml.exists() and pack_json.exists():
                    with open(pack_yml, 'r') as f:
                        pack_config = yaml.safe_load(f)
                    with open(pack_json, 'r') as f:
                        pack_data = json.load(f)
                    
                    return {
                        **pack_config.get("metadata", {}),
                        "type": "installed",
                        "location": str(pack_dir),
                        "examples_preview": pack_data.get("examples", [])[:3],
                        "total_examples": len(pack_data.get("examples", []))
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get info for pack '{pack_name}': {e}")
            return None
    
    def get_pack_path(self, pack_name: str) -> Optional[str]:
        """Get the file path for a teaching pack."""
        pack_dir = self.installed_packs_dir / pack_name
        if pack_dir.exists():
            return str(pack_dir)
        return None
    
    def record_training_session(self, pack_name: str):
        """Record a training session for statistics."""
        self.stats["total_training_sessions"] += 1
        if pack_name not in self.stats["pack_usage"]:
            self.stats["pack_usage"][pack_name] = {
                "installations": 0,
                "training_sessions": 0,
                "last_used": None
            }
        
        self.stats["pack_usage"][pack_name]["training_sessions"] += 1
        self.stats["pack_usage"][pack_name]["last_used"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_stats()
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get comprehensive usage statistics."""
        return {
            "overview": {
                "total_installations": self.stats.get("total_installations", 0),
                "total_training_sessions": self.stats.get("total_training_sessions", 0),
                "available_builtin_packs": len(self.builtin_packs),
                "installed_packs": len(list(self.installed_packs_dir.iterdir())),
                "last_updated": self.stats.get("last_updated", "Never")
            },
            "pack_usage": self.stats.get("pack_usage", {}),
            "top_packs": self._get_top_packs()
        }
    
    def _get_top_packs(self) -> List[Dict[str, Any]]:
        """Get top used teaching packs."""
        pack_usage = self.stats.get("pack_usage", {})
        sorted_packs = sorted(
            pack_usage.items(),
            key=lambda x: x[1].get("training_sessions", 0),
            reverse=True
        )
        
        return [
            {
                "name": pack_name,
                "training_sessions": data.get("training_sessions", 0),
                "installations": data.get("installations", 0),
                "last_used": data.get("last_used", "Never")
            }
            for pack_name, data in sorted_packs[:5]  # Top 5
        ]

# CLI Integration Functions
def cmd_list_packs():
    """CLI command to list teaching packs."""
    manager = TeachingPackManager()
    packs = manager.list_packs()
    
    print("\n[TEACHING PACKS]")
    print("=" * 50)
    
    if packs["builtin"]:
        print("\n[BUILT-IN PACKS]")
        for pack in packs["builtin"]:
            print(f"  {pack['name']} v{pack['version']}")
            print(f"    {pack['description']}")
            print(f"    Category: {pack['category']} | Difficulty: {pack['difficulty']}")
            print(f"    Examples: {pack['examples_count']} | Tags: {', '.join(pack['tags'])}")
            print()
    
    if packs["installed"]:
        print("[INSTALLED PACKS]")
        for pack in packs["installed"]:
            print(f"  {pack.get('name', 'Unknown')} v{pack.get('version', 'Unknown')}")
            print(f"    {pack.get('description', 'No description')}")
            print(f"    Location: {pack.get('location', 'Unknown')}")
            print()
    
    print(f"Total available packs: {packs['total_count']}")

def cmd_install_pack(pack_name: str, force: bool = False):
    """CLI command to install a teaching pack."""
    manager = TeachingPackManager()
    
    print(f"\n[INSTALLING PACK]: {pack_name}")
    success = manager.install_pack(pack_name, force=force)
    
    if success:
        print(f"[SUCCESS] Pack '{pack_name}' installed successfully")
    else:
        print(f"[ERROR] Failed to install pack '{pack_name}'")
    
    return success

def cmd_uninstall_pack(pack_name: str):
    """CLI command to uninstall a teaching pack."""
    manager = TeachingPackManager()
    
    print(f"\n[UNINSTALLING PACK]: {pack_name}")
    success = manager.uninstall_pack(pack_name)
    
    if success:
        print(f"[SUCCESS] Pack '{pack_name}' uninstalled successfully")
    else:
        print(f"[ERROR] Failed to uninstall pack '{pack_name}'")
    
    return success

def cmd_validate_pack(pack_name: str):
    """CLI command to validate a teaching pack."""
    manager = TeachingPackManager()
    
    print(f"\n[VALIDATING PACK]: {pack_name}")
    result = manager.validate_pack(pack_name)
    
    if result["valid"]:
        print("[SUCCESS] Pack validation passed")
        if result["info"]:
            print("Pack information:")
            for key, value in result["info"].items():
                print(f"  {key}: {value}")
    else:
        print("[ERROR] Pack validation failed")
        if result["errors"]:
            print("Errors:")
            for error in result["errors"]:
                print(f"  - {error}")
        
        if result["warnings"]:
            print("Warnings:")
            for warning in result["warnings"]:
                print(f"  - {warning}")
    
    return result["valid"]

def cmd_pack_info(pack_name: str):
    """CLI command to show teaching pack information."""
    manager = TeachingPackManager()
    
    print(f"\n[PACK INFO]: {pack_name}")
    info = manager.get_pack_info(pack_name)
    
    if info:
        print(f"Name: {info.get('name', 'Unknown')}")
        print(f"Version: {info.get('version', 'Unknown')}")
        print(f"Description: {info.get('description', 'No description')}")
        print(f"Author: {info.get('author', 'Unknown')}")
        print(f"Category: {info.get('category', 'Unknown')}")
        print(f"Difficulty: {info.get('difficulty', 'Unknown')}")
        print(f"Type: {info.get('type', 'Unknown')}")
        print(f"Total Examples: {info.get('total_examples', 0)}")
        
        if info.get('tags'):
            print(f"Tags: {', '.join(info['tags'])}")
        
        if info.get('examples_preview'):
            print("\nExample Preview:")
            for i, example in enumerate(info['examples_preview'], 1):
                print(f"  {i}. Input: {example.get('input', 'N/A')}")
                print(f"     Output: {example.get('output', 'N/A')}")
                if 'confidence' in example:
                    print(f"     Confidence: {example['confidence']}")
                print()
    else:
        print(f"[ERROR] Pack '{pack_name}' not found")
    
    return info is not None

def cmd_usage_stats():
    """CLI command to show usage statistics."""
    manager = TeachingPackManager()
    stats = manager.get_usage_stats()
    
    print("\n[TEACHING PACK STATISTICS]")
    print("=" * 50)
    
    overview = stats["overview"]
    print(f"Total Installations: {overview['total_installations']}")
    print(f"Total Training Sessions: {overview['total_training_sessions']}")
    print(f"Available Built-in Packs: {overview['available_builtin_packs']}")
    print(f"Installed Packs: {overview['installed_packs']}")
    print(f"Last Updated: {overview['last_updated']}")
    
    if stats["top_packs"]:
        print("\n[TOP USED PACKS]")
        for pack in stats["top_packs"]:
            print(f"  {pack['name']}")
            print(f"    Training Sessions: {pack['training_sessions']}")
            print(f"    Installations: {pack['installations']}")
            print(f"    Last Used: {pack['last_used']}")
            print()
    
    return stats
