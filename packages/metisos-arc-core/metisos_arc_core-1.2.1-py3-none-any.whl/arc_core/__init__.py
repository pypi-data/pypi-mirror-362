"""
ARC Core - Adaptive Recursive Consciousness

A complete implementation of biological learning mechanisms for AI systems.
"""

__version__ = "1.2.1"

# Import core components from arc_core.py
from .arc_core import (
    LearningARCConsciousness,
    LearningARCTransformer,
    RealLearningVocabulary,
    HierarchicalMemory,
    AttractorDetector,
    BiologicalContextualGating,
    SleepLikeConsolidation,
    MultipleLearningSystems,
    CognitiveInhibition,
    MetacognitiveMonitoring,
    ReasoningGraphEngine
)

# Import teaching packs functionality
from .teaching_packs import (
    PackMetadata,
    TeachingPackManager,
    cmd_list_packs,
    cmd_install_pack,
    cmd_uninstall_pack,
    cmd_validate_pack,
    cmd_pack_info,
    cmd_usage_stats
)

# Legacy compatibility - ARCTrainer maps to LearningARCConsciousness
ARCTrainer = LearningARCConsciousness
ARCCore = LearningARCConsciousness  # Another alias

# Compatibility aliases for classes that may be expected
VocabularyExpansion = RealLearningVocabulary
MemorySystem = HierarchicalMemory
SafetySystem = CognitiveInhibition  # Cognitive inhibition is our safety mechanism

# Import CLI module
from .cli import cli as cli_group

# Export all public classes and functions
__all__ = [
    # Core classes
    'LearningARCConsciousness',
    'LearningARCTransformer',
    'RealLearningVocabulary',
    'HierarchicalMemory',
    'AttractorDetector',
    'ReasoningGraphEngine',
    
    # Biological learning components
    'BiologicalContextualGating',
    'CognitiveInhibition',
    'SleepLikeConsolidation',
    'MultipleLearningSystems',
    'MetacognitiveMonitoring',
    
    # Teaching packs
    'TeachingPack',
    'TeachingPackManager',
    'load_teaching_pack',
    'save_teaching_pack',
    'validate_teaching_pack',
    
    # CLI
    'cli_group',
    
    # Legacy/compatibility
    'ARCTrainer',
    'ARCCore',
    'VocabularyExpansion',
    'MemorySystem',
    'SafetySystem',
]
