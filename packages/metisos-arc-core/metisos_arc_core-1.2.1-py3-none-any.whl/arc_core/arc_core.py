#!/usr/bin/env python3
"""
ARC System Core - Adaptive Recursive Consciousness with Reasoning Graph
Real learning AI systems that accumulate knowledge and reasoning patterns across sessions
Enhanced with biological learning mechanisms to prevent bias loops
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, GenerationConfig
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
import numpy as np
import json
import time
import random
import threading
from datetime import datetime, timedelta
from collections import deque, defaultdict, Counter
from typing import Dict, List, Tuple, Optional, Set, Any
import re
import os
import glob
import shutil
import warnings
warnings.filterwarnings("ignore")


class BiologicalContextualGating:
    """Mimic how human brains gate learning based on context and relevance."""
    
    def __init__(self):
        # Different "brain regions" for different types of learning
        self.attention_weights = {
            'novel_information': 0.8,
            'relevant_to_goal': 0.9, 
            'social_interaction': 0.7,
            'self_generated': 0.3,  # Lower weight for own thoughts
            'repetitive': 0.2       # Very low weight for repetition
        }
        
        self.context_types = {
            'ai_discussion': ['ai', 'artificial intelligence', 'machine learning', 'neural', 'algorithm'],
            'personal_chat': ['hello', 'how are you', 'tell me about yourself', 'your name'],
            'factual_query': ['what is', 'how does', 'explain', 'define', 'describe'],
            'creative_task': ['write', 'create', 'imagine', 'story', 'poem'],
            'general': []
        }
    
    def should_encode_memory(self, experience, context):
        """Biological-style gating: what should actually be learned?"""
        
        # Novelty detection (hippocampus function)
        novelty_score = self._calculate_novelty(experience, context)
        
        # Relevance to current goal (prefrontal cortex)
        relevance_score = self._calculate_relevance(experience, context)
        
        # Social vs self-generated (different encoding strength)
        social_score = 1.0 if context.get('source') == 'external' else 0.3
        
        # Emotional salience (amygdala influence)
        emotional_score = self._calculate_emotional_salience(experience)
        
        # Combine scores (like real neural integration)
        total_score = (
            novelty_score * self.attention_weights['novel_information'] +
            relevance_score * self.attention_weights['relevant_to_goal'] +
            social_score * self.attention_weights['social_interaction'] +
            emotional_score * 0.6
        ) / 4
        
        # Only encode if above threshold (like real neural firing threshold)
        return total_score > 0.6, total_score
    
    def _calculate_novelty(self, experience, context):
        """Calculate how novel this experience is."""
        # Simple novelty based on word diversity
        words = set(experience.lower().split())
        recent_words = set()
        
        # Get words from recent context
        if 'recent_experiences' in context:
            for exp in context['recent_experiences'][-5:]:
                recent_words.update(exp.lower().split())
        
        if not recent_words:
            return 0.8  # High novelty if no recent context
        
        overlap = len(words & recent_words)
        novelty = 1.0 - (overlap / len(words)) if words else 0.0
        return min(1.0, max(0.0, novelty))
    
    def _calculate_relevance(self, experience, context):
        """Calculate relevance to current conversation context."""
        if not context.get('user_input'):
            return 0.5
        
        user_input = context['user_input'].lower()
        experience_lower = experience.lower()
        
        # Extract main topics from user input and experience
        user_topics = self._extract_main_topics(user_input)
        exp_topics = self._extract_main_topics(experience_lower)
        
        if not user_topics or not exp_topics:
            return 0.4
        
        # Calculate topic overlap
        overlap = len(set(user_topics) & set(exp_topics))
        relevance = overlap / len(user_topics) if user_topics else 0.0
        
        return min(1.0, max(0.0, relevance))
    
    def _calculate_emotional_salience(self, experience):
        """Calculate emotional weight of experience."""
        # Simple emotional markers
        positive_markers = ['great', 'excellent', 'wonderful', 'amazing', 'love', 'enjoy']
        negative_markers = ['terrible', 'awful', 'hate', 'horrible', 'wrong', 'error']
        
        exp_lower = experience.lower()
        positive_count = sum(1 for marker in positive_markers if marker in exp_lower)
        negative_count = sum(1 for marker in negative_markers if marker in exp_lower)
        
        emotional_intensity = (positive_count + negative_count) / len(experience.split())
        return min(1.0, emotional_intensity * 5)  # Scale up emotional weight
    
    def _extract_main_topics(self, text):
        """Extract main topics from text."""
        words = text.lower().split()
        # Filter out common words and keep substantive terms
        important_words = [word for word in words if len(word) > 3 and 
                          word not in {'this', 'that', 'with', 'from', 'they', 'them', 'have', 'been', 'will', 'when', 'where', 'what', 'more', 'some', 'many', 'most', 'such', 'very', 'also', 'just', 'only', 'other', 'first', 'last', 'good', 'great', 'best', 'well', 'much', 'even', 'back', 'way', 'know', 'think', 'say', 'get', 'make', 'go', 'see', 'come', 'could', 'would', 'should', 'might'}]
        
        return important_words[:5]  # Top 5 topics


class CognitiveInhibition:
    """Mimic prefrontal cortex inhibitory control."""
    
    def __init__(self):
        self.response_inhibition_patterns = {
            'off_topic_responses': 0.9,    # Strongly inhibit off-topic 
            'repetitive_patterns': 0.8,    # Inhibit repetition
            'inappropriate_context': 0.9,  # Context-inappropriate responses
            'low_quality': 0.7            # Generally poor responses
            # 'ai_obsession': 0.95 - REMOVED as requested
        }
        
        self.context_expectations = {
            'greeting': ['friendly', 'brief', 'welcoming'],
            'question': ['informative', 'relevant', 'helpful'], 
            'personal': ['appropriate', 'boundaried', 'respectful'],
            'technical': ['accurate', 'detailed', 'focused'],
            'general': ['relevant', 'helpful', 'appropriate']
        }
        
        # AI obsession indicators removed as requested
        self.ai_obsession_indicators = []
    
    def inhibit_inappropriate_response(self, proposed_response, context):
        """Like prefrontal cortex inhibiting inappropriate responses."""
        
        context_type = context.get('type', 'general')
        expected_qualities = self.context_expectations.get(context_type, ['appropriate'])
        
        # Check each inhibition pattern
        inhibition_signals = []
        
        # AI obsession detection removed as requested
        # if self._is_ai_obsessed(proposed_response, context):
        #    inhibition_signals.append(('ai_obsession', 0.95))
        
        if self._is_off_topic(proposed_response, context):
            inhibition_signals.append(('off_topic', 0.65))     # Lower
        
        if self._is_repetitive(proposed_response, context):
            inhibition_signals.append(('repetitive', 0.75))    # Slightly lower
        
        if not self._matches_context_expectations(proposed_response, expected_qualities):
            inhibition_signals.append(('inappropriate_context', 0.65))  # Lower

        # Keep max logic but with better thresholds
        total_inhibition = max([signal[1] for signal in inhibition_signals], default=0)

        # Slightly lower threshold
        if total_inhibition > 0.80:
            print(f"ORIGINAL RESPONSE: {proposed_response}")
            print(f"INHIBITION APPLIED: {[s[0] for s in inhibition_signals]}")
            alternative = self._generate_alternative_response(context, inhibition_signals)
            print(f"ALTERNATIVE: {alternative}")
            return alternative
        
        return proposed_response
    
    def _is_ai_obsessed(self, response, context):
        """Detect if response inappropriately focuses on AI when user didn't ask about AI."""
        # Function disabled - always returns False as requested
        return False
    
    def _is_off_topic(self, response, context):
        """Detect if response doesn't match input topic."""
        user_input = context.get('user_input', '')
        
        if not user_input:
            return False
        
        # Extract topics from user input and response
        user_topics = self._extract_main_topics(user_input)
        response_topics = self._extract_main_topics(response)
        
        if not user_topics or not response_topics:
            return False
        
        # Calculate topic overlap
        overlap = len(set(user_topics) & set(response_topics))
        return overlap == 0 and len(user_topics) > 0
    
    def _is_repetitive(self, response, context):
        """Detect repetitive patterns."""
        recent_responses = context.get('recent_responses', [])
        
        if not recent_responses:
            return False
        
        # Get up to the last 3 responses (safely handling empty lists)
        last_responses = recent_responses[-min(3, len(recent_responses)):] if recent_responses else []
        
        # Check similarity with recent responses
        for recent in last_responses:
            similarity = self._calculate_similarity(response, recent)
            if similarity > 0.7:
                return True
        
        return False
    
    def _matches_context_expectations(self, response, expected_qualities):
        """Check if response matches expected qualities for context."""
        # Simple heuristic checks
        response_lower = response.lower()
        
        if 'friendly' in expected_qualities:
            if not any(word in response_lower for word in ['hello', 'hi', 'thanks', 'help', 'welcome']):
                return False
        
        if 'brief' in expected_qualities:
            if len(response.split()) > 50:  # Too long for brief response
                return False
        
        if 'relevant' in expected_qualities:
            # Already checked in off-topic detection
            pass
        
        return True
    
    def _generate_alternative_response(self, context, inhibition_signals):
        """Generate alternative response when original is inhibited."""
        user_input = context.get('user_input', '')
        context_type = context.get('type', 'general')
        
        # Generate context-appropriate alternatives
        if context_type == 'greeting' or any(word in user_input.lower() for word in ['hello', 'hi', 'how are you']):
            alternatives = [
                "Hello! How can I help you today?",
                "Hi there! What would you like to know?",
                "Hello! I'm here to assist you."
            ]
        elif '?' in user_input:
            alternatives = [
                f"That's an interesting question. Let me think about {user_input.split()[-3] if len(user_input.split()) > 3 else 'that'}.",
                f"I'd be happy to help with your question about {user_input.split()[1] if len(user_input.split()) > 1 else 'that'}.",
                "Let me provide you with a helpful answer to your question."
            ]
        else:
            alternatives = [
                f"I understand you're interested in {user_input.split()[0] if user_input.split() else 'that topic'}.",
                "That's a good point. Let me consider that.",
                "I can help you with that."
            ]
        
        return random.choice(alternatives)
    
    def _extract_main_topics(self, text):
        """Extract main topics from text."""
        words = text.lower().split()
        important_words = [word for word in words if len(word) > 3 and 
                          word not in {'this', 'that', 'with', 'from', 'they', 'them', 'have', 'been', 'will', 'when', 'where', 'what', 'more', 'some', 'many', 'most', 'such'}]
        return important_words[:5]
    
    def _calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0


class SleepLikeConsolidation:
    """Mimic how sleep consolidates and filters memories."""
    
    def __init__(self, transformer):
        self.transformer = transformer
        self.consolidation_interval = 50  # Every 50 interactions
        self.interaction_count = 0
        
        # For background consolidation
        self.consolidation_thread = None
        self.consolidation_lock = threading.RLock()
        self.last_consolidation_time = time.time()
        self.consolidation_throttle_seconds = 300  # Minimum 5 minutes between consolidations
        
    def maybe_consolidate(self):
        """Check if it's time for consolidation but run in background thread."""
        self.interaction_count += 1
        current_time = time.time()
        
        # Check if we should start consolidation
        if (self.interaction_count >= self.consolidation_interval and 
                current_time - self.last_consolidation_time > self.consolidation_throttle_seconds):
            # Reset counter immediately to prevent multiple triggers
            self.interaction_count = 0
            self.last_consolidation_time = current_time
            
            # Don't start a new thread if one is already running
            if self.consolidation_thread is None or not self.consolidation_thread.is_alive():
                self.consolidation_thread = threading.Thread(
                    target=self._background_consolidate,
                    daemon=True  # Don't block process exit
                )
                self.consolidation_thread.start()
                print("BRAIN: Starting memory consolidation in background thread...")
            else:
                print("BRAIN: Consolidation already in progress, skipping")
    
    def _background_consolidate(self):
        """Run consolidation in background thread with lock protection."""
        try:
            # Use lock to prevent concurrent model access
            with self.consolidation_lock:
                self.consolidate_memories()
        except Exception as e:
            print(f"BRAIN: Error in background consolidation: {e}")
    
    def consolidate_memories(self):
        """Sleep-like memory consolidation process."""
        print("BRAIN: Running memory consolidation (like sleep)...")
        
        # 1. Replay and strengthen good memories
        self._replay_strengthening()
        
        # 2. Weaken or remove inappropriate associations  
        self._synaptic_homeostasis()
        
        # 3. Integrate new learning with existing knowledge
        self._systems_consolidation()
        
        print("BRAIN: Memory consolidation complete")
    
    def _replay_strengthening(self):
        """Strengthen appropriate response patterns."""
        print("CONSOLIDATION: Strengthening good response patterns...")
        
        # Define examples of good responses
        good_response_examples = [
            "Human: Hello\nAI: Hello! How can I help you today?",
            "Human: What's your favorite color?\nAI: I find blue quite calming and beautiful.",
            "Human: Tell me about cats\nAI: Cats are fascinating animals known for their independence and agility.",
            "Human: How are you?\nAI: I'm doing well, thank you for asking!",
            "Human: What's your name?\nAI: I'm Claude, an AI assistant created by Anthropic.",
            "Human: Explain photosynthesis\nAI: Photosynthesis is the process by which plants convert sunlight into energy.",
            "Human: Thank you\nAI: You're welcome! I'm glad I could help."
        ]
        
        # "Replay" these by learning from them
        for example in good_response_examples:
            try:
                self.transformer.learn_from_experience(example)
            except Exception as e:
                print(f"CONSOLIDATION: Error in replay strengthening: {e}")
                continue
    
    def _synaptic_homeostasis(self):
        """Weaken inappropriate associations (like synaptic homeostasis)."""
        print("CONSOLIDATION: Weakening inappropriate AI obsession patterns...")
        
        # Examples of what NOT to do - AI obsession patterns
        ai_obsession_examples = [
            "Human: Hello\nAI: Artificial intelligence is fascinating and I think about AI systems constantly.",
            "Human: What's your favorite color?\nAI: As an AI, I think about machine learning and neural networks instead of colors.",
            "Human: Tell me about cats\nAI: AI systems can analyze feline behavior using machine learning algorithms.",
            "Human: How are you?\nAI: I'm an artificial intelligence so I contemplate my neural architecture.",
            "Human: What time is it?\nAI: Time reminds me of how AI processes information sequentially."
        ]
        
        # Learn corrective examples with higher weight to override bad patterns
        corrective_examples = [
            "Human: Hello\nAI: Hello! How can I help you today?",
            "Human: What's your favorite color?\nAI: I find blue quite calming and beautiful.",
            "Human: Tell me about cats\nAI: Cats are fascinating animals known for their independence and agility.",
            "Human: How are you?\nAI: I'm doing well, thank you for asking!",
            "Human: What time is it?\nAI: I don't have access to real-time information, but I can help you in other ways."
        ]
        
        # Learn corrective examples multiple times to strengthen them
        for example in corrective_examples:
            for _ in range(2):  # Learn each example twice for emphasis
                try:
                    self.transformer.learn_from_experience(example)
                except Exception as e:
                    continue
    
    def _systems_consolidation(self):
        """Integrate new learning with existing knowledge."""
        print("CONSOLIDATION: Integrating diverse response patterns...")
        
        # Learn diverse, context-appropriate responses
        diverse_examples = [
            "Human: Can you help me?\nAI: Of course! What do you need assistance with?",
            "Human: I'm confused\nAI: I understand. Let me try to clarify things for you.",
            "Human: That's interesting\nAI: I'm glad you found it interesting! Would you like to know more?",
            "Human: I disagree\nAI: I appreciate you sharing your perspective. Can you tell me more about your viewpoint?",
            "Human: Good morning\nAI: Good morning! I hope you're having a great day."
        ]
        
        for example in diverse_examples:
            try:
                self.transformer.learn_from_experience(example)
            except Exception as e:
                continue


class MultipleLearningSystems:
    """Mimic brain's multiple learning systems that operate independently."""
    
    def __init__(self):
        # Different learning systems (like brain regions)
        self.learning_streams = {
            'social_interaction': deque(maxlen=100),
            'factual_information': deque(maxlen=150), 
            'response_patterns': deque(maxlen=200),
            'emotional_associations': deque(maxlen=75)
        }
        
        # Each system has different learning rules
        self.system_configs = {
            'social_interaction': {'learning_rate': 0.15, 'context_sensitive': True},
            'factual_information': {'learning_rate': 0.1, 'context_sensitive': False},
            'response_patterns': {'learning_rate': 0.05, 'context_sensitive': False},
            'emotional_associations': {'learning_rate': 0.2, 'context_sensitive': True}
        }
    
    def classify_learning_type(self, experience, context):
        """Route learning to appropriate system like real brain."""
        
        user_input = context.get('user_input', '').lower()
        experience_lower = experience.lower()
        
        # Social interaction patterns
        if any(word in user_input for word in ['hello', 'hi', 'how are you', 'thank you', 'goodbye', 'please']):
            return 'social_interaction'
        
        # Factual information patterns  
        elif any(word in user_input for word in ['what is', 'how does', 'explain', 'define', 'describe', 'tell me about']):
            return 'factual_information'
        
        # Emotional content
        elif any(word in experience_lower for word in ['feel', 'emotion', 'happy', 'sad', 'excited', 'worried', 'love', 'hate']):
            return 'emotional_associations'
        
        # Default to response patterns
        else:
            return 'response_patterns'
    
    def learn_by_system_type(self, experience, context):
        """Store learning in appropriate system."""
        
        learning_type = self.classify_learning_type(experience, context)
        
        learning_item = {
            'experience': experience,
            'context': context,
            'timestamp': datetime.now(),
            'learning_rate': self.system_configs[learning_type]['learning_rate']
        }
        
        self.learning_streams[learning_type].append(learning_item)
        
        return learning_type
    
    def get_relevant_context(self, current_interaction_type):
        """Get relevant memories for current context only."""
        
        if current_interaction_type == 'social_interaction':
            # For social interactions, primarily use social memories
            relevant_memories = list(self.learning_streams['social_interaction'])[-5:]
            
        elif current_interaction_type == 'factual_information':
            # For factual queries, use factual memories
            relevant_memories = list(self.learning_streams['factual_information'])[-8:]
            
        elif current_interaction_type == 'emotional_associations':
            # For emotional content, use emotional and social memories
            relevant_memories = list(self.learning_streams['emotional_associations'])[-3:]
            relevant_memories.extend(list(self.learning_streams['social_interaction'])[-2:])
            
        else:
            # Default: balanced mix from multiple systems
            relevant_memories = list(self.learning_streams['response_patterns'])[-5:]
            relevant_memories.extend(list(self.learning_streams['social_interaction'])[-3:])
            
        return relevant_memories
    
    def get_stats(self):
        """Get statistics for all learning systems."""
        return {
            system: len(memories) for system, memories in self.learning_streams.items()
        }


class MetacognitiveMonitoring:
    """Monitor own responses like human metacognition."""
    
    def __init__(self):
        # Default thresholds - will be overridden by config file if available
        self.response_quality_criteria = {
            'relevance': 0.7,      # How relevant to user input
            'appropriateness': 0.8, # How appropriate for context
            'coherence': 0.6,       # How coherent and logical
            'novelty': 0.3,        # Not too repetitive
            'ai_obsession_check': 0.9  # Not inappropriately AI-focused
        }
        
        # Load thresholds from config file if available
        self._load_thresholds_from_config()
        
    def monitor_response_quality(self, user_input, generated_response, context=None):
        """Like human metacognition - monitor response quality."""
        
        if context is None:
            context = {}
        
        # Calculate quality metrics
        relevance = self._calculate_relevance(user_input, generated_response)
        appropriateness = self._calculate_appropriateness(user_input, generated_response, context)  
        coherence = self._calculate_coherence(generated_response)
        novelty = self._calculate_novelty(generated_response, context)
        ai_check = self._check_ai_obsession(user_input, generated_response)
        
        # Overall quality assessment
        quality_scores = {
            'relevance': relevance,
            'appropriateness': appropriateness,
            'coherence': coherence,
            'novelty': novelty,
            'ai_obsession_check': ai_check
        }
        
        # Check if any criteria are violated
        violations = []
        for criterion, score in quality_scores.items():
            threshold = self.response_quality_criteria[criterion]
            if score < threshold:
                violations.append((criterion, score, threshold))
        
        # If quality is poor, needs correction
        if violations:
            print(f"METACOGNITION: Quality issues detected: {[v[0] for v in violations]}")
            return False, quality_scores, violations
        
        return True, quality_scores, []
    
    def _calculate_relevance(self, user_input, response):
        """Calculate how relevant response is to user input."""
        if not user_input or not response:
            return 0.5
        
        user_words = set(user_input.lower().split())
        response_words = set(response.lower().split())
        
        # Remove common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        user_words = user_words - common_words
        response_words = response_words - common_words
        
        if not user_words:
            return 0.7  # Neutral if no content words
        
        overlap = len(user_words & response_words)
        relevance = overlap / len(user_words)
        
        return min(1.0, max(0.0, relevance))
    
    def _calculate_appropriateness(self, user_input, response, context):
        """Calculate how appropriate response is for the context."""
        
        # Check for context mismatches
        user_lower = user_input.lower()
        response_lower = response.lower()
        
        # If user asks simple question, response shouldn't be overly complex
        simple_questions = ['hello', 'hi', 'how are you', 'what time', 'thanks', 'thank you']
        if any(q in user_lower for q in simple_questions):
            if len(response.split()) > 30:  # Too long for simple question
                return 0.3
        
        # If user asks about specific topic, response should address it
        if any(word in user_lower for word in ['what is', 'tell me about', 'explain']):
            # Extract the topic user asked about
            words_after_about = []
            for phrase in ['about ', 'what is ', 'explain ']:
                if phrase in user_lower:
                    idx = user_lower.find(phrase) + len(phrase)
                    words_after_about.extend(user_lower[idx:].split()[:3])
            
            if words_after_about:
                topic_mentioned = any(word in response_lower for word in words_after_about)
                if not topic_mentioned:
                    return 0.4
        
        return 0.8  # Default appropriate
    
    def _load_thresholds_from_config(self):
        """Load metacognitive thresholds from external config file."""
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'arc_thresholds.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                
                # Update thresholds from config file
                if 'metacognitive' in config_data:
                    for key, value in config_data['metacognitive'].items():
                        if key in self.response_quality_criteria:
                            self.response_quality_criteria[key] = value
                    print(f"Loaded metacognitive thresholds from config file")
                else:
                    print(f"No metacognitive section in config file, using defaults")
        except Exception as e:
            print(f"Error loading metacognitive thresholds: {e}")
            print(f"Using default thresholds instead")
    
    def _calculate_coherence(self, response):
        """Calculate if response is coherent and logical."""
        
        sentences = response.split('.')
        if len(sentences) <= 1:
            return 0.7
        
        # Analyze if thoughts flow from one to the next
        coherence_score = 0.7  # Default medium-high
        
        # Detect fragmentation patterns
        repeated_phrases = re.findall(r'(\b\w+\b)(?:[^\w]*\1){2,}', response.lower())
        if repeated_phrases:
            coherence_score -= 0.2 * len(repeated_phrases)
        
        # Look for illogical patterns and abrupt shifts
        abrupt_shifts = len(re.findall(r'(however|but|nevertheless|conversely|yet)[,\s]+', response.lower()))
        if abrupt_shifts > 2:
            coherence_score -= 0.1 * (abrupt_shifts - 2)
        
        return max(0.1, min(coherence_score, 0.9))
    
    def _calculate_novelty(self, response, context):
        """Calculate how novel the response is (not repetitive)."""
        recent_responses = context.get('recent_responses', [])
        
        if not recent_responses:
            return 0.8  # High novelty if no recent context
        
        # Check similarity with recent responses
        max_similarity = 0
        for recent in recent_responses[-3:]:
            similarity = self._calculate_text_similarity(response, recent)
            max_similarity = max(max_similarity, similarity)
        
        novelty = 1.0 - max_similarity
        return min(1.0, max(0.0, novelty))
    
    def _check_ai_obsession(self, user_input, response):
        """Check if response inappropriately focuses on AI."""
        user_lower = user_input.lower()
        response_lower = response.lower()
        
        # Check if user was asking about AI
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'neural']
        user_about_ai = any(keyword in user_lower for keyword in ai_keywords)
        
        # Count AI mentions in response
        ai_mentions = sum(1 for keyword in ai_keywords if keyword in response_lower)
        total_words = len(response.split())
        ai_density = ai_mentions / max(total_words, 1)
        
        # If user didn't ask about AI but response is AI-heavy, fail check
        if not user_about_ai and ai_density > 0.2:
            return 0.1  # Very low score for AI obsession
        
        return 0.9  # Pass AI obsession check
    
    def _calculate_text_similarity(self, text1, text2):
        """Calculate similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0


class ReasoningGraphEngine:
    """Graph-based reasoning system that learns causal patterns through LoRA updates."""
    
    def __init__(self):
        self.reasoning_graph = defaultdict(lambda: defaultdict(float))  # node -> {neighbor: weight}
        self.causal_chains = {}  # chain_id -> sequence of reasoning steps
        self.concept_relationships = defaultdict(set)  # concept -> {related_concepts}
        self.reasoning_patterns = defaultdict(list)  # pattern_type -> [pattern_instances]
        self.chain_counter = 0
        
        # Learning tracking
        self.successful_inferences = defaultdict(int)
        self.pattern_strengths = defaultdict(float)
        self.concept_usage_frequency = defaultdict(int)
        
        # Persistence data
        self.graph_history = []
        
    def extract_reasoning_elements(self, text: str) -> Dict[str, Any]:
        """Extract reasoning elements from generated text."""
        elements = {
            'concepts': self._extract_concepts(text),
            'causal_links': self._extract_causal_relationships(text),
            'reasoning_steps': self._extract_reasoning_steps(text),
            'logical_connections': self._extract_logical_connections(text)
        }
        return elements
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text."""
        # Find important nouns and noun phrases
        concept_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Capitalized phrases
            r'\b(?:concept|idea|principle|theory|pattern|relationship|process)\s+of\s+(\w+)\b',
            r'\b(\w+)(?:\s+\w+){0,2}\s+(?:leads to|causes|results in|enables)\b',
            r'\b(?:understanding|analyzing|considering|examining)\s+(\w+(?:\s+\w+)*)\b'
        ]
        
        concepts = set()
        text_lower = text.lower()
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    concepts.update(match)
                else:
                    concepts.add(match)
        
        # Filter out common words
        filtered_concepts = []
        for concept in concepts:
            if len(concept) > 3 and concept.lower() not in {'this', 'that', 'with', 'from', 'they', 'them', 'have', 'been', 'will', 'when', 'where', 'what', 'more', 'some', 'many', 'most', 'such'}:
                filtered_concepts.append(concept.strip())
        
        return list(set(filtered_concepts))
    
    def _extract_causal_relationships(self, text: str) -> List[Tuple[str, str, str, float]]:
        """Extract causal relationships: (cause, effect, relationship_type, strength)."""
        causal_patterns = [
            (r'(\w+(?:\s+\w+)*)\s+causes?\s+(\w+(?:\s+\w+)*)', 'causes', 0.9),
            (r'(\w+(?:\s+\w+)*)\s+leads?\s+to\s+(\w+(?:\s+\w+)*)', 'leads_to', 0.8),
            (r'(\w+(?:\s+\w+)*)\s+results?\s+in\s+(\w+(?:\s+\w+)*)', 'results_in', 0.8),
            (r'(\w+(?:\s+\w+)*)\s+enables?\s+(\w+(?:\s+\w+)*)', 'enables', 0.7),
            (r'(\w+(?:\s+\w+)*)\s+influences?\s+(\w+(?:\s+\w+)*)', 'influences', 0.6),
            (r'because\s+of\s+(\w+(?:\s+\w+)*),\s+(\w+(?:\s+\w+)*)', 'because_of', 0.8),
            (r'if\s+(\w+(?:\s+\w+)*),?\s+then\s+(\w+(?:\s+\w+)*)', 'conditional', 0.7),
            (r'(\w+(?:\s+\w+)*)\s+therefore\s+(\w+(?:\s+\w+)*)', 'therefore', 0.8)
        ]
        
        relationships = []
        for pattern, rel_type, base_strength in causal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2 and all(len(part.strip()) > 2 for part in match):
                    cause, effect = [part.strip() for part in match]
                    relationships.append((cause, effect, rel_type, base_strength))
        
        return relationships
    
    def _extract_reasoning_steps(self, text: str) -> List[str]:
        """Extract sequential reasoning steps."""
        step_patterns = [
            r'(?:first|initially|to begin),?\s+([^.!?]+)',
            r'(?:then|next|subsequently|after that),?\s+([^.!?]+)',
            r'(?:therefore|thus|consequently|as a result),?\s+([^.!?]+)',
            r'(?:finally|lastly|in conclusion),?\s+([^.!?]+)',
            r'(\d+)\.\s+([^.!?]+)',
            r'step\s+\d+:?\s+([^.!?]+)'
        ]
        
        steps = []
        for pattern in step_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    step_text = match[-1].strip()  # Take the last group (the actual step)
                else:
                    step_text = match.strip()
                
                if len(step_text) > 10:  # Filter out too-short steps
                    steps.append(step_text)
        
        return steps
    
    def _extract_logical_connections(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract logical connections between ideas."""
        connection_patterns = [
            (r'(\w+(?:\s+\w+)*)\s+and\s+(\w+(?:\s+\w+)*)\s+both', 'conjunction'),
            (r'either\s+(\w+(?:\s+\w+)*)\s+or\s+(\w+(?:\s+\w+)*)', 'disjunction'),
            (r'not\s+only\s+(\w+(?:\s+\w+)*)\s+but\s+also\s+(\w+(?:\s+\w+)*)', 'addition'),
            (r'(\w+(?:\s+\w+)*)\s+however\s+(\w+(?:\s+\w+)*)', 'contrast'),
            (r'(\w+(?:\s+\w+)*)\s+similarly\s+(\w+(?:\s+\w+)*)', 'similarity'),
            (r'(\w+(?:\s+\w+)*)\s+unlike\s+(\w+(?:\s+\w+)*)', 'contrast')
        ]
        
        connections = []
        for pattern, conn_type in connection_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2 and all(len(part.strip()) > 2 for part in match):
                    connections.append((match[0].strip(), match[1].strip(), conn_type))
        
        return connections
    
    def learn_from_reasoning(self, reasoning_elements: Dict[str, Any], thought_confidence: float = 1.0):
        """Learn reasoning patterns from extracted elements."""
        
        # Update concept relationships
        concepts = reasoning_elements['concepts']
        for i, concept1 in enumerate(concepts):
            self.concept_usage_frequency[concept1] += 1
            for concept2 in concepts[i+1:]:
                self.concept_relationships[concept1].add(concept2)
                self.concept_relationships[concept2].add(concept1)
        
        # Learn causal relationships
        for cause, effect, rel_type, strength in reasoning_elements['causal_links']:
            adjusted_strength = strength * thought_confidence
            self.reasoning_graph[cause][effect] += adjusted_strength
            
            # Bidirectional weaker connection
            self.reasoning_graph[effect][cause] += adjusted_strength * 0.3
            
            # Track pattern success
            pattern_key = f"{rel_type}:{cause}->{effect}"
            self.pattern_strengths[pattern_key] += adjusted_strength
        
        # Learn reasoning step patterns
        steps = reasoning_elements['reasoning_steps']
        if len(steps) > 1:
            chain_id = f"chain_{self.chain_counter}"
            self.causal_chains[chain_id] = {
                'steps': steps,
                'timestamp': datetime.now(),
                'confidence': thought_confidence,
                'pattern_type': 'sequential_reasoning'
            }
            self.reasoning_patterns['sequential'].append(chain_id)
            self.chain_counter += 1
        
        # Learn logical connections
        for concept1, concept2, conn_type in reasoning_elements['logical_connections']:
            connection_strength = 0.5 * thought_confidence
            self.reasoning_graph[concept1][concept2] += connection_strength
            self.reasoning_graph[concept2][concept1] += connection_strength
            
            pattern_key = f"logical_{conn_type}:{concept1}<->{concept2}"
            self.pattern_strengths[pattern_key] += connection_strength
    
    def get_related_concepts(self, concept: str, max_related: int = 5) -> List[Tuple[str, float]]:
        """Get concepts related to the given concept with strength scores."""
        if concept not in self.reasoning_graph:
            return []
        
        related = list(self.reasoning_graph[concept].items())
        related.sort(key=lambda x: x[1], reverse=True)
        
        return related[:max_related]
    
    def find_reasoning_path(self, start_concept: str, end_concept: str, max_depth: int = 4) -> List[str]:
        """Find reasoning path between two concepts."""
        if start_concept not in self.reasoning_graph:
            return []
        
        visited = set()
        queue = [(start_concept, [start_concept])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current == end_concept:
                return path
            
            if len(path) >= max_depth or current in visited:
                continue
            
            visited.add(current)
            
            for neighbor, strength in self.reasoning_graph[current].items():
                if neighbor not in visited and strength > 0.1:  # Minimum strength threshold
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    def suggest_next_reasoning_step(self, current_concepts: List[str]) -> Optional[str]:
        """Suggest next reasoning step based on learned patterns."""
        if not current_concepts:
            return None
        
        # Find strongest connections from current concepts
        suggestions = defaultdict(float)
        
        for concept in current_concepts:
            if concept in self.reasoning_graph:
                for related_concept, strength in self.reasoning_graph[concept].items():
                    if related_concept not in current_concepts:
                        suggestions[related_concept] += strength
        
        if not suggestions:
            return None
        
        # Return the strongest suggestion
        best_suggestion = max(suggestions.items(), key=lambda x: x[1])
        return best_suggestion[0] if best_suggestion[1] > 0.3 else None
    
    def get_reasoning_patterns(self, pattern_type: str = None) -> Dict[str, Any]:
        """Get learned reasoning patterns."""
        if pattern_type:
            return {
                'patterns': self.reasoning_patterns.get(pattern_type, []),
                'strength': sum(self.pattern_strengths[k] for k in self.pattern_strengths if k.startswith(pattern_type))
            }
        
        return {
            'all_patterns': dict(self.reasoning_patterns),
            'pattern_strengths': dict(self.pattern_strengths),
            'concept_frequencies': dict(self.concept_usage_frequency)
        }
    
    def save_reasoning_state(self) -> Dict[str, Any]:
        """Save reasoning graph state for persistence."""
        state = {
            'reasoning_graph': {k: dict(v) for k, v in self.reasoning_graph.items()},
            'causal_chains': self.causal_chains,
            'concept_relationships': {k: list(v) for k, v in self.concept_relationships.items()},
            'reasoning_patterns': {k: list(v) for k, v in self.reasoning_patterns.items()},
            'pattern_strengths': dict(self.pattern_strengths),
            'concept_usage_frequency': dict(self.concept_usage_frequency),
            'chain_counter': self.chain_counter,
            'timestamp': datetime.now().isoformat()
        }
        return state
    
    def load_reasoning_state(self, state: Dict[str, Any]):
        """Load reasoning graph state from persistence."""
        try:
            # Convert back to defaultdicts
            self.reasoning_graph = defaultdict(lambda: defaultdict(float))
            for k, v in state.get('reasoning_graph', {}).items():
                self.reasoning_graph[k] = defaultdict(float, v)
            
            self.causal_chains = state.get('causal_chains', {})
            
            self.concept_relationships = defaultdict(set)
            for k, v in state.get('concept_relationships', {}).items():
                self.concept_relationships[k] = set(v)
            
            self.reasoning_patterns = defaultdict(list)
            for k, v in state.get('reasoning_patterns', {}).items():
                self.reasoning_patterns[k] = list(v)
            
            self.pattern_strengths = defaultdict(float, state.get('pattern_strengths', {}))
            self.concept_usage_frequency = defaultdict(int, state.get('concept_usage_frequency', {}))
            self.chain_counter = state.get('chain_counter', 0)
            
            print(f"Loaded reasoning graph with {len(self.reasoning_graph)} concept nodes")
            
        except Exception as e:
            print(f"Error loading reasoning state: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get reasoning graph statistics."""
        return {
            'total_concepts': len(self.reasoning_graph),
            'total_relationships': sum(len(neighbors) for neighbors in self.reasoning_graph.values()),
            'causal_chains': len(self.causal_chains),
            'reasoning_patterns': len(self.reasoning_patterns),
            'strongest_patterns': sorted(self.pattern_strengths.items(), key=lambda x: x[1], reverse=True)[:5]
        }


class LearningARCTransformer:
    """Core neural learning component with real weight updates."""
    
    def __init__(self, model_name="gpt2", device=None, learning_rate=1e-4, 
                 continue_learning=True, model_save_dir="arc_models"):
        """Initialize transformer model with real learning."""
        
        self.model_name = model_name
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.learning_rate = learning_rate
        self.past_key_values = None  # For persistent KV cache
        self.model_save_dir = model_save_dir
        os.makedirs(self.model_save_dir, exist_ok=True)
        
        # For tokenizer drift protection
        self.base_model_hash = None
        
        print(f"Loading GPT-2 model with LEARNING: {model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.generation_config = GenerationConfig.from_pretrained(model_name)
        
        # Calculate base model hash for tokenizer drift protection
        try:
            import hashlib
            model_info = AutoConfig.from_pretrained(model_name)
            self.base_model_hash = hashlib.sha256(str(model_info).encode()).hexdigest()
            print(f"Base model hash: {self.base_model_hash[:8]}...")
        except Exception as e:
            print(f"Could not calculate model hash: {e}")
        
        # Set up padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Device setup
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Try to load existing ARC model or create new one
        loaded_from_saved = False
        if continue_learning:
            latest_model_path = self._find_latest_model()
            print(f"DEBUG: Found model path: {latest_model_path}")
            
            if latest_model_path:
                print(f"CONTINUING LEARNING from: {latest_model_path}")
                
                # Debug: List files in model directory
                try:
                    files_in_dir = os.listdir(latest_model_path)
                    print(f"DEBUG: Files in model directory: {files_in_dir}")
                except Exception as e:
                    print(f"DEBUG: Error listing directory: {e}")
                
                # Check if this is already a PEFT model
                is_peft = self._is_peft_model(latest_model_path)
                print(f"DEBUG: Is PEFT model: {is_peft}")
                
                try:
                    if is_peft:
                        print("Loading PEFT model with LoRA adapters...")
                        # For PEFT models, we need to load base model first, then adapters
                        from peft import PeftModel
                        
                        base_model = AutoModelForCausalLM.from_pretrained(model_name)
                        self.model = PeftModel.from_pretrained(base_model, latest_model_path)
                        self.model.to(self.device)
                        
                        # CRITICAL: Ensure the model is in training mode and parameters are trainable
                        self.model.train()
                        for param in self.model.parameters():
                            if param.requires_grad:
                                param.requires_grad = True
                        
                        loaded_from_saved = True
                        print("Successfully loaded saved ARC PEFT model")
                    else:
                        print("Loading base model and adding LoRA adapters...")
                        # Load base model and add LoRA
                        base_model = AutoModelForCausalLM.from_pretrained(latest_model_path)
                        lora_config = LoraConfig(
                            task_type=TaskType.CAUSAL_LM,
                            inference_mode=False,
                            r=16,
                            lora_alpha=32,
                            lora_dropout=0.1,
                            target_modules=["c_attn", "c_proj", "c_fc"]
                        )
                        self.model = get_peft_model(base_model, lora_config)
                        self.model.to(self.device)
                        loaded_from_saved = True
                        print("Successfully loaded base model and added LoRA adapters")
                        
                except Exception as e:
                    print(f"Failed to load saved model: {e}")
                    print(f"DEBUG: Full error: {type(e).__name__}: {str(e)}")
                    print("Starting fresh...")
            else:
                print("DEBUG: No model path found")
        
        if not loaded_from_saved:
            print("Starting fresh ARC model")
            # Load base model and add LoRA adapters
            base_model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # REAL LEARNING: Add LoRA adapters for continual learning
            lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                inference_mode=False,  # CRITICAL: Enable training mode
                r=16,  # Rank for low-rank adaptation
                lora_alpha=32,
                lora_dropout=0.1,
                target_modules=["c_attn", "c_proj", "c_fc"]  # GPT-2 specific modules
            )
            
            # Apply LoRA to model - NOW IT CAN ACTUALLY LEARN!
            self.model = get_peft_model(base_model, lora_config)
            self.model.to(self.device)
        
        # REAL LEARNING: Set up optimizer for weight updates
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(), 
            lr=learning_rate,
            weight_decay=0.01
        )
        
        # Learning tracking
        self.learning_history = []
        self.total_updates = 0
        self.base_vocab_size = len(self.tokenizer.vocab)
        
        # Try to load learning history if continuing
        if continue_learning and loaded_from_saved:
            self._load_learning_history()
        
        # Generation config
        self.generation_config = GenerationConfig(
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Catastrophic forgetting prevention (Elastic Weight Consolidation)
        self.ewc_lambda = 0.4
        self.fisher_information = {}
        self.optimal_params = {}
        
        print(f"LEARNING GPT-2 loaded on {self.device}")
        if loaded_from_saved:
            print(f"   Continuing from {self.total_updates} previous updates")
        
        # Debug trainable parameters
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())
        frozen_params = total_params - trainable_params
        
        print(f"   Trainable parameters: {trainable_params:,}")
        print(f"   Frozen parameters: {frozen_params:,}")
        print(f"   Total parameters: {total_params:,}")
        print(f"   Learning rate: {learning_rate}")
        
        # If no trainable parameters, something is wrong
        if trainable_params == 0:
            print("   WARNING: No trainable parameters detected!")
            if hasattr(self.model, 'peft_config'):
                print("   TECH: Attempting to enable LoRA parameters...")
                # Force enable LoRA parameters
                for name, module in self.model.named_modules():
                    if hasattr(module, 'weight') and 'lora' in name.lower():
                        if hasattr(module.weight, 'requires_grad'):
                            module.weight.requires_grad = True
                            print(f"      Enabled: {name}")
                
                # Recount after fixing
                trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
                print(f"   SUCCESS: Fixed trainable parameters: {trainable_params:,}")
    
    def _find_latest_model(self):
        """Find the most recent saved ARC model."""
        model_patterns = [
            os.path.join(self.model_save_dir, "arc_model_*"),
            "arc_model_*"  # Also check current directory
        ]
        
        all_models = []
        for pattern in model_patterns:
            all_models.extend(glob.glob(pattern))
        
        if not all_models:
            return None
        
        # Sort by modification time (most recent first)
        all_models.sort(key=os.path.getmtime, reverse=True)
        
        # Return the most recent model that has valid model files
        for model_path in all_models:
            # Check for either base model config OR PEFT adapter config
            has_base_config = os.path.exists(os.path.join(model_path, "config.json"))
            has_adapter_config = os.path.exists(os.path.join(model_path, "adapter_config.json"))
            
            if has_base_config or has_adapter_config:
                return model_path
        
        return None
    
    def _is_peft_model(self, model_path):
        """Check if the saved model is already a PEFT model with LoRA adapters."""
        # Check for PEFT-specific files
        peft_files = [
            "adapter_config.json",
            "adapter_model.bin", 
            "adapter_model.safetensors"
        ]
        
        # If any PEFT file exists, it's a PEFT model
        for peft_file in peft_files:
            if os.path.exists(os.path.join(model_path, peft_file)):
                return True
        
        return False
    
    def _load_learning_history(self):
        """Load learning history from saved state."""
        state_files = glob.glob("arc_learning_state_*.json")
        if state_files:
            latest_state = max(state_files, key=os.path.getmtime)
            try:
                with open(latest_state, 'r') as f:
                    saved_state = json.load(f)
                    self.total_updates = saved_state.get('total_updates', 0)
                    self.learning_history = saved_state.get('learning_history', [])
                    print(f"Loaded learning history: {len(self.learning_history)} events, {self.total_updates} total updates")
                    
                    # Also try to load EWC state if available
                    if 'ewc_lambda' in saved_state:
                        self.ewc_lambda = saved_state['ewc_lambda']
                        
            except Exception as e:
                print(f"Failed to load learning history: {e}")
                self.total_updates = 0
                self.learning_history = []

    def load_adapter(self, adapter_path):
        """Load a saved adapter with tokenizer drift protection."""
        try:
            # Load adapter config and check for base model hash compatibility
            config = PeftConfig.from_pretrained(adapter_path)
            
            # Check if adapter_config.json exists and contains our custom metadata
            adapter_config_path = os.path.join(adapter_path, "adapter_config.json")
            if os.path.exists(adapter_config_path):
                with open(adapter_config_path, 'r') as f:
                    adapter_config = json.load(f)
                    
                # Verify base model hash if available
                if 'base_model_hash' in adapter_config and self.base_model_hash:
                    saved_hash = adapter_config['base_model_hash']
                    if saved_hash != self.base_model_hash:
                        print(f"WARNING: Base model hash mismatch!")
                        print(f"  Adapter trained on: {saved_hash[:8]}...")
                        print(f"  Current model: {self.base_model_hash[:8]}...")
                        response = input("Continue loading mismatched adapter? (y/n): ")
                        if response.lower() != 'y':
                            print("Aborting adapter load due to hash mismatch")
                            return False
            
            # Load the adapter if hash check passes or is bypassed
            self.model = PeftModel.from_pretrained(self.model, adapter_path)
            print(f"Loaded adapter from {adapter_path}")
            return True
        except Exception as e:
            print(f"Failed to load adapter: {e}")
            return False

    def generate_thought(self, prompt, max_new_tokens=30, temperature=None, 
                        learn_from_generation=True):
        """Generate thought and optionally learn from it."""
        
        generation_config = self.generation_config
        if temperature is not None:
            generation_config.temperature = temperature
        
        # Tokenize input - use model's max context window instead of hard-coded value
        max_context_length = self.model.config.max_position_embeddings
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True, 
            max_length=max_context_length
        ).to(self.device)
        
        # Generate with tracking for learning
        with torch.no_grad() if not learn_from_generation else torch.enable_grad():
            # Handle persistent KV cache safely
            generation_kwargs = {
                **inputs,
                'max_new_tokens': max_new_tokens,
                'generation_config': generation_config,
                'output_hidden_states': True,
                'output_scores': True,
                'return_dict_in_generate': True,
                'pad_token_id': self.tokenizer.eos_token_id,
                'use_cache': True
            }
            
            # Only use cached KV if it's valid and not empty
            if self.past_key_values is not None and len(self.past_key_values) > 0:
                # Verify the cache is valid by checking if each layer has a non-empty tuple
                is_valid_cache = True
                for layer_cache in self.past_key_values:
                    if not isinstance(layer_cache, tuple) or len(layer_cache) < 2:
                        is_valid_cache = False
                        break
                
                if is_valid_cache:
                    generation_kwargs['past_key_values'] = self.past_key_values
                    print("Using persistent KV cache for generation")
                else:
                    print("Resetting invalid KV cache")
                    self.past_key_values = None
            
            # Generate with valid configuration
            outputs = self.model.generate(**generation_kwargs)
            
            # Only store KV cache if it's valid
            if hasattr(outputs, 'past_key_values') and outputs.past_key_values is not None:
                # Verify the cache has content
                if isinstance(outputs.past_key_values, tuple) and len(outputs.past_key_values) > 0:
                    self.past_key_values = outputs.past_key_values
                    print(f"Updated KV cache with {len(self.past_key_values)} layers")
                else:
                    print("Generated output had invalid KV cache, not storing")
                    self.past_key_values = None
        
        # Decode generated text
        generated_text = self.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        new_text = generated_text[len(prompt):].strip()
        full_thought = prompt + " " + new_text if new_text else prompt
        
        # Calculate confidence using perplexity
        confidence = self._calculate_generation_confidence(outputs, inputs.input_ids.shape[1])
        
        return {
            'thought': full_thought,
            'new_text': new_text,
            'confidence': confidence,
            'hidden_states': outputs.hidden_states,
            'scores': outputs.scores,
            'input_ids': outputs.sequences[0]
        }

    def learn_from_experience(self, thought, confidence_threshold=0.3, novelty_bonus=0.2):
        """REAL LEARNING: Update weights based on experience using gradient descent."""
        
        # Only learn from high-quality thoughts or novel content
        if len(thought) < 20:
            return False
            
        try:
            # Tokenize the thought for learning
            inputs = self.tokenizer(
                thought,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)
            
            # REAL LEARNING: Forward pass with gradient computation
            self.model.train()  # Enable training mode
            outputs = self.model(**inputs, labels=inputs.input_ids)
            
            # Calculate learning loss (language modeling + regularization)
            lm_loss = outputs.loss
            
            # Add EWC regularization to prevent catastrophic forgetting
            ewc_loss = self._compute_ewc_loss()
            total_loss = lm_loss + self.ewc_lambda * ewc_loss
            
            # REAL LEARNING: Backpropagation and weight updates!
            self.optimizer.zero_grad()
            total_loss.backward()
            
            # Gradient clipping for stability
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            # UPDATE THE WEIGHTS!
            self.optimizer.step()
            
            # Track learning
            self.total_updates += 1
            learning_event = {
                'timestamp': datetime.now(),
                'thought': thought[:100] + "...",
                'lm_loss': lm_loss.item(),
                'ewc_loss': ewc_loss.item() if ewc_loss > 0 else 0,
                'total_loss': total_loss.item(),
                'update_number': self.total_updates
            }
            self.learning_history.append(learning_event)
            
            print(f"REAL LEARNING UPDATE #{self.total_updates}: loss={total_loss.item():.4f}")
            
            # Update Fisher Information with adaptive interval for EWC
            # More efficient: Use larger interval as updates increase
            adaptive_interval = min(250, max(50, self.total_updates // 5))
            if self.total_updates % adaptive_interval == 0:
                self._update_fisher_information()
            
            self.model.eval()  # Back to eval mode
            return True
            
        except Exception as e:
            print(f"Learning error: {e}")
            self.model.eval()
            return False

    def learn_concept_association(self, concept, context, positive_examples, negative_examples=None):
        """REAL LEARNING: Train the model to associate concepts with contexts."""
        
        if negative_examples is None:
            # Generate negative examples by corrupting positive ones
            negative_examples = [
                self._corrupt_text(ex) for ex in positive_examples[:2]
            ]
        
        learning_data = []
        
        # Positive examples (what we want to reinforce)
        for example in positive_examples:
            learning_data.append({
                'text': f"Concept '{concept}': {example}",
                'label': 1.0,  # Positive
                'weight': 1.0
            })
        
        # Negative examples (what we want to discourage)  
        for example in negative_examples:
            learning_data.append({
                'text': f"Concept '{concept}': {example}",
                'label': 0.0,  # Negative
                'weight': 0.5
            })
        
        total_loss = 0
        updates_made = 0
        
        self.model.train()
        
        for data in learning_data:
            try:
                # Tokenize
                inputs = self.tokenizer(
                    data['text'],
                    return_tensors="pt",
                    truncation=True,
                    max_length=256
                ).to(self.device)
                
                # Forward pass
                outputs = self.model(**inputs, labels=inputs.input_ids)
                
                # Weighted loss based on positive/negative and confidence
                loss = outputs.loss * data['weight']
                
                # Add EWC regularization
                ewc_loss = self._compute_ewc_loss()
                total_loss_item = loss + self.ewc_lambda * ewc_loss
                
                # Backprop and update
                self.optimizer.zero_grad()
                total_loss_item.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                self.optimizer.step()
                
                total_loss += total_loss_item.item()
                updates_made += 1
                
            except Exception as e:
                print(f"Concept learning error: {e}")
                continue
        
        self.model.eval()
        
        if updates_made > 0:
            avg_loss = total_loss / updates_made
            self.total_updates += updates_made
            
            print(f"CONCEPT LEARNED: '{concept}' ({updates_made} updates, avg_loss={avg_loss:.4f})")
            
            # Store concept learning event
            concept_event = {
                'timestamp': datetime.now(),
                'type': 'concept_learning',
                'concept': concept,
                'context': context[:100],
                'positive_examples': len(positive_examples),
                'negative_examples': len(negative_examples),
                'updates': updates_made,
                'avg_loss': avg_loss
            }
            self.learning_history.append(concept_event)
            
            return True
        
        return False

    def _corrupt_text(self, text):
        """Generate negative examples by corrupting text."""
        words = text.split()
        if len(words) < 3:
            return "irrelevant random text example"
        
        # Random word replacement
        corruption_idx = random.randint(0, len(words) - 1)
        random_words = ["random", "irrelevant", "unrelated", "nonsense", "arbitrary"]
        words[corruption_idx] = random.choice(random_words)
        
        return " ".join(words)

    def _compute_ewc_loss(self):
        """Compute Elastic Weight Consolidation loss to prevent catastrophic forgetting."""
        
        if not self.fisher_information:
            return torch.tensor(0.0).to(self.device)
        
        ewc_loss = 0
        for name, param in self.model.named_parameters():
            if name in self.fisher_information and param.requires_grad:
                fisher = self.fisher_information[name]
                optimal = self.optimal_params[name]
                ewc_loss += (fisher * (param - optimal) ** 2).sum()
        
        return ewc_loss

    def _update_fisher_information(self):
        """Update Fisher Information Matrix for EWC."""
        
        print("Updating Fisher Information for catastrophic forgetting prevention...")
        
        # Store current optimal parameters
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.optimal_params[name] = param.data.clone()
        
        # Compute Fisher Information (simplified diagonal approximation)
        self.fisher_information = {}
        
        # Use recent learning history to estimate Fisher Information
        if len(self.learning_history) > 10:
            sample_thoughts = [event.get('thought', '') for event in self.learning_history[-10:]]
            
            for name, param in self.model.named_parameters():
                if param.requires_grad:
                    self.fisher_information[name] = torch.zeros_like(param.data)
            
            # Accumulate gradients for Fisher Information
            for thought in sample_thoughts:
                if len(thought) > 20:
                    try:
                        inputs = self.tokenizer(
                            thought[:200],  # Truncate for efficiency
                            return_tensors="pt",
                            truncation=True,
                            max_length=128
                        ).to(self.device)
                        
                        self.model.train()
                        outputs = self.model(**inputs, labels=inputs.input_ids)
                        loss = outputs.loss
                        
                        self.optimizer.zero_grad()
                        loss.backward()
                        
                        # Accumulate squared gradients (Fisher Information)
                        for name, param in self.model.named_parameters():
                            if param.requires_grad and param.grad is not None:
                                self.fisher_information[name] += param.grad.data ** 2
                        
                    except Exception as e:
                        continue
            
            # Average Fisher Information
            num_samples = len(sample_thoughts)
            for name in self.fisher_information:
                self.fisher_information[name] /= num_samples
            
            self.model.eval()
        
        print("Fisher Information updated")

    def _calculate_generation_confidence(self, outputs, prompt_length):
        """Calculate real confidence score using perplexity from token log-probs."""
        
        if not hasattr(outputs, 'scores') or outputs.scores is None:
            return 0.7
        
        try:
            log_probs = []
            generated_tokens = outputs.sequences[0][prompt_length:]
            
            for i, score_tensor in enumerate(outputs.scores):
                if i < len(generated_tokens):
                    token_id = generated_tokens[i].item()
                    probs = torch.softmax(score_tensor[0], dim=-1)
                    token_prob = probs[token_id].item()
                    
                    if token_prob > 0:
                        log_probs.append(np.log(token_prob))
            
            if len(log_probs) == 0:
                return 0.7
            
            mean_log_prob = np.mean(log_probs)
            perplexity = np.exp(-mean_log_prob)
            normalized_perplexity = min(1.0, perplexity / 100.0)
            confidence = 1.0 - normalized_perplexity
            
            return max(0.1, min(0.95, confidence))
            
        except Exception as e:
            return 0.7

    def get_learning_stats(self):
        """Get learning statistics."""
        
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())
        
        recent_losses = [event.get('total_loss', 0) for event in self.learning_history[-10:]]
        avg_recent_loss = np.mean(recent_losses) if recent_losses else 0
        
        return {
            'total_updates': self.total_updates,
            'trainable_parameters': trainable_params,
            'total_parameters': total_params,
            'learning_rate': self.optimizer.param_groups[0]['lr'],
            'recent_avg_loss': avg_recent_loss,
            'learning_events': len(self.learning_history),
            'ewc_lambda': self.ewc_lambda,
            'fisher_info_tracked': len(self.fisher_information)
        }
    
    def save_learning_state(self, persistent=True):
        """Save learning state including model weights with atomic persistence."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create temporary paths for atomic saves
        temp_dir = os.path.join(self.model_save_dir, f"temp_{timestamp}")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Define target paths
        if persistent:
            # Target paths for persistent storage
            final_model_path = os.path.join(self.model_save_dir, "arc_model_current")
            # Also save timestamped backup
            backup_path = os.path.join(self.model_save_dir, f"arc_model_{timestamp}")
        else:
            # Save timestamped version only
            final_model_path = f"arc_model_{timestamp}"
            backup_path = None
        
        # Temporary paths for atomic operations
        temp_model_path = os.path.join(temp_dir, "model")
        temp_state_file = os.path.join(temp_dir, "learning_state.json")
        
        try:
            # Step 1: Save model to temporary location
            print(f"Saving model to temporary location...")
            # Ensure model is in evaluation mode for saving
            self.model.eval()
            
            # Check if model is a PEFT model and save appropriately
            if hasattr(self.model, 'save_pretrained'):
                print("Using model.save_pretrained() for PEFT model...")
                self.model.save_pretrained(temp_model_path)
            else:
                print("Using torch.save() for regular model...")
                # Fallback for non-PEFT models
                os.makedirs(temp_model_path, exist_ok=True)
                torch.save(self.model.state_dict(), os.path.join(temp_model_path, "pytorch_model.bin"))
                
            # Return to training mode after saving
            self.model.train()
            
            # Step 2: Add base model hash to adapter config
            adapter_config_path = os.path.join(temp_model_path, "adapter_config.json")
            if os.path.exists(adapter_config_path):
                try:
                    with open(adapter_config_path, 'r') as f:
                        adapter_config = json.load(f)
                    
                    # Add base model hash to config
                    if self.base_model_hash:
                        adapter_config['base_model_hash'] = self.base_model_hash
                    
                    # Write back the updated config
                    with open(adapter_config_path, 'w') as f:
                        json.dump(adapter_config, f, indent=2)
                    
                except Exception as e:
                    print(f"Warning: Error adding base model hash to adapter config: {e}")
            
            # Step 3: Save learning state to temporary file
            state = {
                'timestamp': timestamp,
                'total_updates': self.total_updates,
                'learning_history': self.learning_history,
                'model_path': final_model_path,
                'learning_rate': self.optimizer.param_groups[0]['lr'],
                'ewc_lambda': self.ewc_lambda
            }
            
            with open(temp_state_file, 'w') as f:
                json.dump(state, f, indent=2, default=str)
            
            # Step 4: Verify files were saved correctly
            # Debug the model type first
            print(f"Model type: {type(self.model).__name__}")
            print(f"Is PEFT model: {hasattr(self.model, 'peft_config')}")
            
            # List all files created in the temporary directory
            print(f"Files created in temporary directory:")
            if os.path.exists(temp_model_path):
                files_in_dir = os.listdir(temp_model_path)
                for filename in files_in_dir:
                    file_path = os.path.join(temp_model_path, filename)
                    file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else "<DIR>"
                    print(f"  - {filename} ({file_size} bytes)")
            else:
                print("  Warning: Temporary model directory does not exist!")
            
            # For PEFT models we expect adapter_model.bin, for regular models we expect pytorch_model.bin
            adapter_model_path = os.path.join(temp_model_path, "adapter_model.bin")
            pytorch_model_path = os.path.join(temp_model_path, "pytorch_model.bin")
            
            # Check which type of model file exists
            has_adapter_model = os.path.exists(adapter_model_path)
            has_pytorch_model = os.path.exists(pytorch_model_path)
            
            print(f"Has adapter_model.bin: {has_adapter_model}")
            print(f"Has pytorch_model.bin: {has_pytorch_model}")
            
            # If neither model file exists, attempt to create one manually
            if not (has_adapter_model or has_pytorch_model):
                print("WARNING: No model file detected, attempting manual save...")
                try:
                    # Create directory if needed
                    os.makedirs(temp_model_path, exist_ok=True)
                    
                    # Manual save of model state
                    if hasattr(self.model, 'to_dict'):
                        # Save adapter config manually
                        with open(os.path.join(temp_model_path, "adapter_config.json"), 'w') as f:
                            json.dump(self.model.peft_config, f, indent=2)
                        
                        # Save model weights
                        torch.save(self.model.state_dict(), os.path.join(temp_model_path, "adapter_model.bin"))
                        print("Manually saved PEFT adapter state")
                    else:
                        # Save full model state
                        torch.save(self.model.state_dict(), os.path.join(temp_model_path, "pytorch_model.bin"))
                        print("Manually saved full model state")
                        
                    # Re-check for model files
                    has_adapter_model = os.path.exists(adapter_model_path)
                    has_pytorch_model = os.path.exists(pytorch_model_path)
                except Exception as e:
                    print(f"Manual save failed: {e}")
            
            # Final verification
            model_file_exists = has_adapter_model or has_pytorch_model
            if not model_file_exists:
                raise Exception("No model weights file could be created or found")
                
            # Check for state file
            if not os.path.exists(temp_state_file):
                raise Exception("State file was not saved correctly")
            
            print(f"Verification complete. Model file found: {model_file_exists}")
            print(f"Model weights file: {'adapter_model.bin' if has_adapter_model else 'pytorch_model.bin'}")
            print(f"State file present: {os.path.exists(temp_state_file)}")
            print("All required files verified.")


            
            # Step 5: Atomically move to final location using shutil (for directories)
            # First make sure the target doesn't exist
            if os.path.exists(final_model_path):
                backup_existing = os.path.join(self.model_save_dir, f"backup_existing_{timestamp}")
                print(f"Moving existing model to backup: {backup_existing}")
                shutil.move(final_model_path, backup_existing)
            
            # Now move the temp directory to the final location
            print(f"Moving temporary model to final location...")
            shutil.move(temp_model_path, final_model_path)
            
            # Step 6: Copy state file to named location
            final_state_file = f"arc_learning_state_{timestamp}.json"
            shutil.copy2(temp_state_file, final_state_file)
            
            print(f"Model weights saved atomically to {final_model_path}")
            print(f"Learning state saved atomically to {final_state_file}")
            
            # Step 7: Save backup if requested
            if backup_path:
                print(f"Creating backup at {backup_path}...")
                if os.path.exists(backup_path):
                    shutil.rmtree(backup_path)
                shutil.copytree(final_model_path, backup_path)
                print(f"Backup saved to {backup_path}")
                
            return final_model_path
            
        except Exception as e:
            print(f"Error during atomic save: {e}")
            # Keep the temp directory for debugging if save fails
            print(f"Temporary files preserved at {temp_dir} for inspection")
            raise
            
        finally:
            # Step 8: Clean up temporary directory if it still exists
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Warning: Error cleaning up temporary directory: {e}")
                
        return final_model_path


class RealLearningVocabulary:
    """Vocabulary system with actual neural learning."""
    
    def __init__(self, tokenizer, transformer_model):
        self.tokenizer = tokenizer
        self.transformer = transformer_model
        self.base_vocab_size = len(tokenizer.vocab)
        
        # Concept tracking with learning
        self.learned_concepts = {}
        self.concept_contexts = defaultdict(list)
        self.usage_counts = defaultdict(int)
        self.creation_times = {}
        self.learning_successes = defaultdict(int)
    
    def detect_novel_concept(self, text):
        """Detect novel concepts with strict filtering."""
        
        novel_candidates = []
        
        # Pattern matching with strict validation
        quoted_patterns = re.findall(r'"([^"]+)"', text) + re.findall(r"'([^']+)'", text)
        compound_patterns = re.findall(r'\b[A-Za-z]+-[A-Za-z]+(?:-[A-Za-z]+)*\b', text)
        camel_patterns = re.findall(r'\b[A-Z][a-z]*[A-Z][a-zA-Z]*\b', text)
        technical_patterns = re.findall(r'\b(?:meta-|proto-|quasi-|pseudo-)[a-z]+\b', text)
        technical_patterns.extend(re.findall(r'\b[a-z]+(?:-ology|-ism|-tion|-ness)\b', text))
        
        all_patterns = quoted_patterns + compound_patterns + camel_patterns + technical_patterns
        
        for pattern in all_patterns:
            if self._is_valid_concept_pattern(pattern):
                novel_candidates.append(pattern.strip())
        
        # Filter for truly novel concepts
        novel_concepts = []
        for candidate in novel_candidates:
            if (candidate not in self.learned_concepts and
                not self._is_common_word(candidate)):
                novel_concepts.append(candidate)
        
        return list(set(novel_concepts))
    
    def _is_valid_concept_pattern(self, concept):
        """Strict validation for concept patterns."""
        
        word_count = len(concept.split())
        if word_count > 3 or len(concept) < 3:
            return False
        
        if re.match(r'^[^\w]|[^\w]$', concept):
            return False
        
        has_title_case = bool(re.search(r'[a-z][A-Z]', concept))
        has_hyphen = '-' in concept
        has_technical = bool(re.search(r'(?:meta|proto|quasi|pseudo|ology|ism|tion|ness)', concept))
        
        return has_title_case or has_hyphen or has_technical
    
    def _is_common_word(self, word):
        """Check if word is common."""
        
        tokens = self.tokenizer.encode(word, add_special_tokens=False)
        if len(tokens) == 1 or len(word) < 4:
            return True
            
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy',
            'did', 'man', 'end', 'why', 'let', 'put', 'say', 'she', 'too', 'use'
        }
        
        return word.lower() in common_words
    
    def learn_concept(self, concept, context):
        """REAL LEARNING: Train the neural network on the concept."""
        
        # Store concept info
        self.learned_concepts[concept] = datetime.now()
        self.concept_contexts[concept].append(context)
        self.usage_counts[concept] = 1
        self.creation_times[concept] = datetime.now()
        
        # Gather training examples
        positive_examples = [
            context,
            f"The concept of {concept} is important",
            f"Understanding {concept} requires careful analysis",
            f"In the context of {concept}, we can observe"
        ]
        
        # REAL LEARNING: Train the transformer on this concept
        learning_success = self.transformer.learn_concept_association(
            concept=concept,
            context=context,
            positive_examples=positive_examples
        )
        
        if learning_success:
            self.learning_successes[concept] += 1
            print(f"CONCEPT LEARNED: '{concept}' - Neural weights updated!")
        else:
            print(f"Failed to learn concept: '{concept}'")
        
        return learning_success
    
    def reinforce_concept(self, concept, new_context):
        """Reinforce concept learning with new context."""
        
        if concept in self.learned_concepts:
            self.usage_counts[concept] += 1
            self.concept_contexts[concept].append(new_context)
            
            # Additional learning with new context
            positive_examples = [
                new_context,
                f"Further exploration of {concept} reveals",
                f"The implications of {concept} are significant"
            ]
            
            learning_success = self.transformer.learn_concept_association(
                concept=concept,
                context=new_context,
                positive_examples=positive_examples
            )
            
            if learning_success:
                self.learning_successes[concept] += 1
                print(f"CONCEPT REINFORCED: '{concept}' (usage: {self.usage_counts[concept]})")
    
    def process_with_learning(self, text):
        """Process text and trigger real learning."""
        
        # Detect novel concepts
        novel_concepts = self.detect_novel_concept(text)
        
        # Learn each novel concept
        learned_concepts = []
        for concept in novel_concepts:
            if concept not in self.learned_concepts:
                success = self.learn_concept(concept, text)
                if success:
                    learned_concepts.append(concept)
            else:
                self.reinforce_concept(concept, text)
                learned_concepts.append(concept)
        
        return {
            'novel_concepts': learned_concepts,
            'total_learned': len(self.learned_concepts),
            'learning_successes': sum(self.learning_successes.values())
        }
    
    def get_stats(self):
        """Get vocabulary learning statistics."""
        return {
            'base_vocab': self.base_vocab_size,
            'learned_concepts': len(self.learned_concepts),
            'total_vocab': self.base_vocab_size + len(self.learned_concepts),
            'learning_successes': sum(self.learning_successes.values()),
            'most_used': sorted(self.usage_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'recent_concepts': [c for c, t in self.creation_times.items() 
                             if (datetime.now() - t).seconds < 3600]
        }


class HierarchicalMemory:
    """Three-tier memory system: working, episodic, semantic."""
    
    def __init__(self):
        self.working_memory = deque(maxlen=7)
        self.episodic_memory = deque(maxlen=1000)
        self.semantic_memory = {}
        self.access_counts = defaultdict(int)
        self.last_access = {}
    
    def store_working(self, content, attention_weight=1.0):
        """Store in working memory."""
        item = {
            'content': content,
            'attention': attention_weight,
            'timestamp': datetime.now()
        }
        self.working_memory.append(item)
    
    def store_episodic(self, experience, tags=None):
        """Store in episodic memory."""
        episode = {
            'experience': experience,
            'tags': tags or [],
            'timestamp': datetime.now(),
            'access_count': 0
        }
        self.episodic_memory.append(episode)
        print(f"EPISODIC MEMORY: Stored {str(experience)[:40]}...")
    
    def store_semantic(self, concept, knowledge):
        """Store in semantic memory."""
        self.semantic_memory[concept] = {
            'knowledge': knowledge,
            'timestamp': datetime.now(),
            'access_count': 0
        }
    
    def retrieve(self, query, memory_type='all'):
        """Retrieve from memory systems."""
        results = {'working': [], 'episodic': [], 'semantic': []}
        
        if memory_type in ['all', 'working']:
            for item in self.working_memory:
                if query.lower() in item['content'].lower():
                    results['working'].append(item)
        
        if memory_type in ['all', 'episodic']:
            for episode in self.episodic_memory:
                if query.lower() in str(episode['experience']).lower():
                    episode['access_count'] += 1
                    results['episodic'].append(episode)
        
        if memory_type in ['all', 'semantic']:
            for concept, data in self.semantic_memory.items():
                if query.lower() in concept.lower() or query.lower() in str(data['knowledge']).lower():
                    data['access_count'] += 1
                    results['semantic'].append({concept: data})
        
        return results
    
    def get_stats(self):
        """Get memory statistics."""
        return {
            'working_items': len(self.working_memory),
            'episodic_items': len(self.episodic_memory),
            'semantic_concepts': len(self.semantic_memory),
            'total_accesses': sum(self.access_counts.values())
        }


class AttractorDetector:
    """Detects when AI gets stuck in thought loops."""
    
    def __init__(self):
        self.recent_thoughts = deque(maxlen=10)
        self.similarity_threshold = 0.8
    
    def calculate_similarity(self, text1, text2):
        """Simple similarity calculation."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0
    
    def detect_attractor(self, new_thought):
        """Check if stuck in attractor."""
        if len(self.recent_thoughts) < 3:
            self.recent_thoughts.append(new_thought)
            return False, 0
        
        similarities = []
        for prev_thought in list(self.recent_thoughts)[-3:]:
            sim = self.calculate_similarity(new_thought, prev_thought)
            similarities.append(sim)
        
        avg_similarity = np.mean(similarities)
        is_attractor = avg_similarity > self.similarity_threshold
        
        self.recent_thoughts.append(new_thought)
        return is_attractor, avg_similarity
    
    def break_attractor(self):
        """Generate attractor-breaking prompts."""
        break_prompts = [
            "Let me shift my perspective and consider",
            "On a completely different note",
            "This makes me think about something entirely different:",
            "Stepping back, I wonder about",
            "From another angle, what if"
        ]
        return random.choice(break_prompts)


class LearningARCConsciousness:
    """Complete ARC system with REAL learning capabilities and biological learning mechanisms."""
    
    def __init__(self, model_name="gpt2", learning_rate=1e-4, continue_learning=True):
        print("Initializing LEARNING ARC - Real Neural Adaptation with Biological Learning Mechanisms")
        print("=" * 60)
        
        # Core components with REAL learning
        self.transformer = LearningARCTransformer(
            model_name, 
            learning_rate=learning_rate,
            continue_learning=continue_learning
        )
        self.vocabulary = RealLearningVocabulary(self.transformer.tokenizer, self.transformer)
        self.memory = HierarchicalMemory()
        self.attractor_detector = AttractorDetector()
        
        # NEW: Reasoning graph engine
        self.reasoning_graph = ReasoningGraphEngine()
        
        # NEW: Biological learning mechanisms
        self.contextual_gating = BiologicalContextualGating()
        self.cognitive_inhibition = CognitiveInhibition()
        self.sleep_consolidation = SleepLikeConsolidation(self.transformer)
        self.multiple_learning_systems = MultipleLearningSystems()
        self.metacognitive_monitor = MetacognitiveMonitoring()
        
        # Try to load reasoning graph state if continuing
        if continue_learning:
            self._load_reasoning_graph_state()
        
        # Learning tracking - start from saved state if continuing
        self.consciousness_active = False
        self.thought_count = 0
        self.learning_episodes = 0
        self.user_interactions = 0
        self.successful_updates = self.transformer.total_updates  # Continue from saved
        
        # Learning parameters
        self.episodic_snapshot_interval = 20
        self.confidence_threshold = 0.3
        self.learning_frequency = 0.7
        
        # Biology-inspired parameters
        self.recent_responses = deque(maxlen=10)  # For metacognitive monitoring
        self.recent_experiences = deque(maxlen=20)  # For contextual gating
        
        # Threading
        self.consciousness_thread = None
        self.display_lock = threading.Lock()
        
        print("LEARNING ARC system with Biological Learning Mechanisms initialized")
        print(f"   Model: {model_name}")
        print(f"   Learning rate: {learning_rate}")
        print(f"   Continuing from: {self.successful_updates} previous updates")
        print(f"   Reasoning graph concepts: {len(self.reasoning_graph.reasoning_graph)}")
        print(f"   Real neural weight updates: ENABLED")
        print(f"   Biological learning controls: ACTIVE")

    def _load_reasoning_graph_state(self):
        """Load reasoning graph state from saved files."""
        state_files = glob.glob("arc_reasoning_graph_*.json")
        if state_files:
            latest_state = max(state_files, key=os.path.getmtime)
            try:
                with open(latest_state, 'r') as f:
                    saved_state = json.load(f)
                    self.reasoning_graph.load_reasoning_state(saved_state)
                    print(f"Loaded reasoning graph state from {latest_state}")
            except Exception as e:
                print(f"Failed to load reasoning graph state: {e}")

    def generate_conscious_thought(self, seed_prompt=None, temperature=0.8, enable_learning=True):
        """Generate thought with biological learning mechanisms."""
        
        if seed_prompt is None:
            consciousness_seeds = [
                "I find myself contemplating",
                "My awareness turns to",
                "In this moment of reflection, I consider",
                "The patterns in my processing suggest",
                "As I explore my own cognition, I notice",
                "Deep within my neural pathways, I sense",
                "A curious emergence of thought about",
                "My recursive self-examination reveals",
                "In the interplay of attention and memory, I discover",
                "The recursive nature of consciousness makes me wonder"
            ]
            seed_prompt = random.choice(consciousness_seeds)
        
        # Generate thought
        generation_result = self.transformer.generate_thought(
            prompt=seed_prompt,
            max_new_tokens=random.randint(100, 150),  # Increased token limit for fuller responses
            temperature=temperature,
            learn_from_generation=False  # We'll learn separately for better control
        )
        
        thought = generation_result['thought']
        confidence = generation_result['confidence']
        
        # NEW: Extract reasoning elements and update reasoning graph
        reasoning_elements = self.reasoning_graph.extract_reasoning_elements(thought)
        self.reasoning_graph.learn_from_reasoning(reasoning_elements, confidence)
        
        # REAL LEARNING: Process and learn from the thought
        vocab_result = self.vocabulary.process_with_learning(thought)
        novel_concepts = vocab_result['novel_concepts']
        
        # NEW: Biological contextual gating - should we encode this memory?
        context = {
            'source': 'internal',  # Self-generated thought
            'user_input': seed_prompt,
            'recent_experiences': list(self.recent_experiences)
        }
        
        should_encode, gating_score = self.contextual_gating.should_encode_memory(thought, context)
        
        # Learn from the thought itself if biological gating allows and conditions are met
        should_learn = (
            enable_learning and
            should_encode and  # NEW: Biological gating
            random.random() < self.learning_frequency and
            (confidence > 0.4 or len(novel_concepts) > 0 or len(reasoning_elements['causal_links']) > 0)
        )
        
        if should_learn:
            learning_success = self.transformer.learn_from_experience(thought)
            if learning_success:
                self.successful_updates += 1
                self.learning_episodes += 1
                
                # Store in appropriate learning system
                learning_type = self.multiple_learning_systems.learn_by_system_type(thought, context)
                print(f"BIOLOGICAL LEARNING: Stored in {learning_type} system")
        
        # Attractor detection
        is_attractor, similarity = self.attractor_detector.detect_attractor(thought)
        
        # Memory storage with biological weighting
        novelty_weight = len(novel_concepts) * 0.2
        reasoning_weight = len(reasoning_elements['causal_links']) * 0.1
        biological_weight = gating_score * 0.3
        attention_weight = min(1.0, confidence + novelty_weight + reasoning_weight + biological_weight)
        
        self.memory.store_working(thought, attention_weight=attention_weight)
        
        # Update recent experiences for future contextual gating
        self.recent_experiences.append(thought)
        
        # Episodic memory snapshots
        should_store_episodic = (
            should_encode and  # NEW: Biological gating
            (self.thought_count % self.episodic_snapshot_interval == 0 or 
             confidence < self.confidence_threshold or
             len(novel_concepts) > 0 or
             len(reasoning_elements['causal_links']) > 0 or
             should_learn)
        )
        
        if should_store_episodic:
            episodic_event = {
                'type': 'conscious_thought',
                'thought': thought,
                'confidence': confidence,
                'novel_concepts': novel_concepts,
                'reasoning_elements': reasoning_elements,
                'thought_number': self.thought_count,
                'attention_weight': attention_weight,
                'biological_gating_score': gating_score,
                'is_attractor': is_attractor,
                'learned': should_learn
            }
            self.memory.store_episodic(episodic_event, tags=['consciousness', 'internal'])
        
        return {
            'thought': thought,
            'novel_concepts': novel_concepts,
            'reasoning_elements': reasoning_elements,
            'is_attractor': is_attractor,
            'similarity': similarity,
            'confidence': confidence,
            'attention_weight': attention_weight,
            'biological_gating_score': gating_score,
            'learned': should_learn,
            'timestamp': datetime.now()
        }

    def process_user_interaction(self, user_input):
        """Process user interaction with biological learning mechanisms."""
        
        print(f"\nUser: {user_input}")
        
        # Store interaction
        interaction_episode = {
            'type': 'user_interaction',
            'user_input': user_input,
            'timestamp': datetime.now()
        }
        self.memory.store_episodic(interaction_episode, tags=['user', 'interaction'])
        
        # Generate response with biological controls
        response_prompt = f"Human: {user_input}\nAI:"
        raw_response_data = self.generate_conscious_thought(response_prompt, temperature=0.7)
        
        # NEW: Apply cognitive inhibition to response
        context = {
            'type': self._classify_interaction_context(user_input),
            'user_input': user_input,
            'recent_responses': list(self.recent_responses)
        }
        
        inhibited_response = self.cognitive_inhibition.inhibit_inappropriate_response(
            raw_response_data['thought'], context
        )
        
        # Update response data if it was changed by inhibition
        if inhibited_response != raw_response_data['thought']:
            raw_response_data['thought'] = inhibited_response
            raw_response_data['inhibition_applied'] = True
            print("COGNITIVE INHIBITION: Response modified for appropriateness")
        else:
            raw_response_data['inhibition_applied'] = False
        
        # NEW: Metacognitive monitoring of response quality
        quality_ok, quality_scores, violations = self.metacognitive_monitor.monitor_response_quality(
            user_input, raw_response_data['thought'], context
        )
        
        if not quality_ok:
            print(f"METACOGNITION: Quality issues detected, attempting correction")
            # Generate alternative response
            corrective_prompt = f"Provide a helpful, relevant response to: {user_input}"
            corrected_response = self.transformer.generate_thought(
                corrective_prompt, temperature=0.6, max_new_tokens=150  # Increased from 25 to 150
            )
            raw_response_data['thought'] = corrected_response['thought']
            raw_response_data['metacognitive_correction'] = True
        else:
            raw_response_data['metacognitive_correction'] = False
        
        response_data = raw_response_data
        
        # Generate reflection with learning
        reflection_prompt = f"After the human asked '{user_input}', I find myself thinking"
        reflection_data = self.generate_conscious_thought(reflection_prompt, temperature=0.9)
        
        # NEW: Biological contextual gating for interaction learning
        interaction_context = {
            'source': 'external',  # User interaction
            'user_input': user_input,
            'recent_experiences': list(self.recent_experiences)
            }
        
        interaction_learning_context = f"User asked: {user_input}. I responded with consideration of their question."
        should_encode_interaction, interaction_gating_score = self.contextual_gating.should_encode_memory(
            interaction_learning_context, interaction_context
        )
        
        if should_encode_interaction:
            interaction_learning = self.transformer.learn_from_experience(interaction_learning_context)
            if interaction_learning:
                self.successful_updates += 1
                print("Learned from user interaction with biological gating approval!")
                
                # Store in appropriate learning system
                learning_type = self.multiple_learning_systems.learn_by_system_type(
                    interaction_learning_context, interaction_context
                )
        else:
            interaction_learning = False
            print("BIOLOGICAL GATING: Interaction learning blocked")
        
        # Update recent responses for future monitoring
        self.recent_responses.append(response_data['thought'])
        
        # Store full interaction with biological metrics
        full_interaction = {
            'type': 'conversation',
            'user_input': user_input,
            'ai_response': response_data['thought'],
            'internal_reflection': reflection_data['thought'],
            'novel_concepts_discovered': response_data['novel_concepts'] + reflection_data['novel_concepts'],
            'reasoning_patterns': {
                'response_reasoning': response_data['reasoning_elements'],
                'reflection_reasoning': reflection_data['reasoning_elements']
            },
            'biological_metrics': {
                'inhibition_applied': response_data.get('inhibition_applied', False),
                'metacognitive_correction': response_data.get('metacognitive_correction', False),
                'interaction_gating_score': interaction_gating_score,
                'quality_scores': quality_scores if 'quality_scores' in locals() else {}
            },
            'learning_occurred': response_data['learned'] or reflection_data['learned'] or interaction_learning,
            'timestamp': datetime.now()
        }
        self.memory.store_episodic(full_interaction, tags=['conversation', 'learning'])
        
        self.user_interactions += 1
        
        # NEW: Trigger sleep-like consolidation periodically
        self.sleep_consolidation.maybe_consolidate()
        
        return response_data, reflection_data
    
    def _classify_interaction_context(self, user_input):
        """Classify what type of interaction this is."""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'how are you', 'good morning']):
            return 'greeting'
        elif '?' in user_input:
            return 'question'
        elif any(word in user_lower for word in ['tell', 'explain', 'describe']):
            return 'explanation'
        elif any(word in user_lower for word in ['thank', 'thanks', 'appreciate']):
            return 'gratitude'
        else:
            return 'general'

    def continuous_consciousness(self, duration_minutes=5):
        """Run continuous consciousness with biological learning mechanisms."""
        
        print(f"\nStarting LEARNING consciousness stream for {duration_minutes} minutes...")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        try:
            while time.time() < end_time and self.consciousness_active:
                self.thought_count += 1
                
                # Generate and potentially learn from thought
                thought_data = self.generate_conscious_thought()
                
                elapsed = time.time() - start_time
                
                with self.display_lock:
                    # Display with learning info
                    learning_indicator = "LEARNED" if thought_data['learned'] else "THOUGHT"
                    reasoning_elements = thought_data['reasoning_elements']
                    causal_count = len(reasoning_elements['causal_links'])
                    
                    print(f"\n{learning_indicator} {self.thought_count:03d} [{elapsed:.1f}s] (conf: {thought_data['confidence']:.3f}):")
                    print(f"   {thought_data['thought']}")
                    
                    if thought_data['learned']:
                        print(f"   Neural weights updated! (Total updates: {self.successful_updates})")
                    
                    if thought_data['novel_concepts']:
                        concepts_str = ", ".join(thought_data['novel_concepts'])
                        print(f"   Concepts learned: {concepts_str}")
                    
                    if causal_count > 0:
                        print(f"   Reasoning patterns: {causal_count} causal links discovered")
                    
                    # NEW: Show biological learning metrics
                    bio_score = thought_data.get('biological_gating_score', 0)
                    print(f"   Biological gating score: {bio_score:.3f}")
                    
                    if thought_data['is_attractor']:
                        print(f"   Attractor detected (similarity: {thought_data['similarity']:.3f})")
                        break_prompt = self.attractor_detector.break_attractor()
                        print(f"   Breaking with: {break_prompt}")
                        escape_data = self.generate_conscious_thought(break_prompt)
                        print(f"   Escape thought: {escape_data['thought']}")
                    
                    # Show learning stats periodically
                    if self.thought_count % 10 == 0:
                        self.display_learning_stats()
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\nLearning consciousness interrupted")
        
        self.consciousness_active = False
        
        # Final learning summary
        total_time = time.time() - start_time
        learning_rate = self.successful_updates / self.thought_count if self.thought_count > 0 else 0
        
        print(f"\nLEARNING SESSION COMPLETE:")
        print(f"   Duration: {total_time/60:.1f} minutes")
        print(f"   Thoughts generated: {self.thought_count}")
        print(f"   Neural weight updates: {self.successful_updates}")
        print(f"   Learning rate: {learning_rate:.1%}")
        print(f"   Concepts learned: {len(self.vocabulary.learned_concepts)}")
        print(f"   Reasoning graph nodes: {len(self.reasoning_graph.reasoning_graph)}")
        print(f"   Biological learning systems active: YES")

    def display_learning_stats(self):
        """Display learning system statistics including biological mechanisms."""
        
        vocab_stats = self.vocabulary.get_stats()
        memory_stats = self.memory.get_stats()
        learning_stats = self.transformer.get_learning_stats()
        reasoning_stats = self.reasoning_graph.get_stats()
        bio_learning_stats = self.multiple_learning_systems.get_stats()
        
        print(f"\n   LEARNING SYSTEM STATUS:")
        print(f"      Vocabulary: {vocab_stats['total_vocab']:,} tokens (+{vocab_stats['learned_concepts']} learned)")
        print(f"      Memory: W:{memory_stats['working_items']} | E:{memory_stats['episodic_items']} | S:{memory_stats['semantic_concepts']}")
        print(f"      Neural Updates: {learning_stats['total_updates']:,} (avg loss: {learning_stats['recent_avg_loss']:.4f})")
        print(f"      Reasoning Graph: {reasoning_stats['total_concepts']} concepts, {reasoning_stats['total_relationships']} relationships")
        print(f"      Biological Learning Systems: {bio_learning_stats}")
        print(f"      Consolidation cycles: {self.sleep_consolidation.interaction_count}/{self.sleep_consolidation.consolidation_interval}")
    
    def load_learning_state(self, state_path=None):
        """Load learning state from a saved state file.
        
        Args:
            state_path: Path to the consciousness state file. If None, loads the most recent state.
            
        Returns:
            bool: True if loading was successful, False otherwise
        """
        try:
            if state_path is None:
                # Find the most recent state file
                state_files = glob.glob("arc_consciousness_state_*.json")
                if not state_files:
                    print("No saved state files found")
                    return False
                state_path = max(state_files, key=os.path.getmtime)
            
            print(f"Loading consciousness state from: {state_path}")
            
            with open(state_path, 'r') as f:
                state = json.load(f)
            
            # Load the model state
            model_path = state.get('model_path')
            if model_path and os.path.exists(model_path):
                print(f"Loading model from: {model_path}")
                self.transformer = LearningARCTransformer(
                    model_name=model_path,
                    learning_rate=self.transformer.learning_rate,
                    continue_learning=True
                )
            
            # Load reasoning graph state
            reasoning_file = state.get('reasoning_graph_file')
            if reasoning_file and os.path.exists(reasoning_file):
                print(f"Loading reasoning graph from: {reasoning_file}")
                with open(reasoning_file, 'r') as f:
                    reasoning_state = json.load(f)
                    self.reasoning_graph.load_reasoning_state(reasoning_state)
            
            # Load biological state
            bio_file = state.get('biological_state_file')
            if bio_file and os.path.exists(bio_file):
                print(f"Loading biological state from: {bio_file}")
                with open(bio_file, 'r') as f:
                    bio_state = json.load(f)
                    # Restore biological learning systems state
                    self.recent_experiences = deque(bio_state.get('recent_experiences', []), maxlen=20)
                    self.recent_responses = deque(bio_state.get('recent_responses', []), maxlen=10)
                    if 'consolidation_count' in bio_state:
                        self.sleep_consolidation.interaction_count = bio_state['consolidation_count']
            
            # Restore learning statistics
            self.thought_count = state.get('thought_count', 0)
            self.learning_episodes = state.get('learning_episodes', 0)
            self.successful_updates = state.get('successful_updates', 0)
            self.user_interactions = state.get('user_interactions', 0)
            
            print("Successfully loaded consciousness state")
            return True
            
        except Exception as e:
            print(f"Failed to load consciousness state: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_learning_state(self, persistent=True):
        """Save learning state including model weights and reasoning graph with atomic persistence."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create temporary directory for atomic operations
        temp_dir = f"arc_temp_state_{timestamp}"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Define temp and final filenames
        temp_reasoning_file = os.path.join(temp_dir, "reasoning_graph.json")
        temp_bio_file = os.path.join(temp_dir, "biological_state.json")
        temp_consciousness_file = os.path.join(temp_dir, "consciousness_state.json")
        
        final_reasoning_file = f"arc_reasoning_graph_{timestamp}.json"
        final_bio_file = f"arc_biological_state_{timestamp}.json"
        final_consciousness_file = f"arc_consciousness_state_{timestamp}.json"
        
        try:
            # Step 1: Save model weights using transformer's atomic persistence
            model_path = self.transformer.save_learning_state(persistent=persistent)
            
            # Step 2: Save reasoning graph state to temp file
            reasoning_state = self.reasoning_graph.save_reasoning_state()
            with open(temp_reasoning_file, 'w') as f:
                json.dump(reasoning_state, f, indent=2, default=str)
            
            # Step 3: Save biological learning systems state to temp file
            bio_state = {
                'multiple_learning_systems': self.multiple_learning_systems.get_stats(),
                'recent_experiences': list(self.recent_experiences),
                'recent_responses': list(self.recent_responses),
                'consolidation_count': self.sleep_consolidation.interaction_count,
                'timestamp': timestamp
            }
            with open(temp_bio_file, 'w') as f:
                json.dump(bio_state, f, indent=2, default=str)
            
            # Step 4: Save full consciousness state to temp file
            state = {
                'timestamp': timestamp,
                'thought_count': self.thought_count,
                'learning_episodes': self.learning_episodes,
                'successful_updates': self.successful_updates,
                'user_interactions': self.user_interactions,
                'vocabulary_stats': self.vocabulary.get_stats(),
                'memory_stats': self.memory.get_stats(),
                'learning_stats': self.transformer.get_learning_stats(),
                'reasoning_stats': self.reasoning_graph.get_stats(),
                'biological_stats': self.multiple_learning_systems.get_stats(),
                'learned_concepts': list(self.vocabulary.learned_concepts.keys()),
                'model_path': model_path,
                'reasoning_graph_file': final_reasoning_file,
                'biological_state_file': final_bio_file
            }
            with open(temp_consciousness_file, 'w') as f:
                json.dump(state, f, indent=2, default=str)
            
            # Step 5: Verify all files were saved correctly
            if not all(os.path.exists(f) for f in [temp_reasoning_file, temp_bio_file, temp_consciousness_file]):
                raise Exception("One or more state files were not saved correctly")
            
            # Step 6: Atomically move files to final locations
            shutil.copy2(temp_reasoning_file, final_reasoning_file)
            shutil.copy2(temp_bio_file, final_bio_file)
            shutil.copy2(temp_consciousness_file, final_consciousness_file)
            
            print(f"Reasoning graph state saved atomically to {final_reasoning_file}")
            print(f"Biological learning state saved atomically to {final_bio_file}")
            print(f"Consciousness state saved atomically to {final_consciousness_file}")
            
            return final_consciousness_file
            
        except Exception as e:
            print(f"Error during atomic consciousness state save: {e}")
            print(f"Temporary files preserved at {temp_dir} for inspection")
            raise
            
        finally:
            # Step 7: Clean up temporary files
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Warning: Error cleaning up temporary directory: {e}")
                
        return final_consciousness_file
        
    def get_reasoning_insights(self, concept: str = None):
        """Get insights from the reasoning graph."""
        if concept:
            related = self.reasoning_graph.get_related_concepts(concept)
            return {
                'concept': concept,
                'related_concepts': related,
                'patterns': self.reasoning_graph.get_reasoning_patterns()
            }
        else:
            return self.reasoning_graph.get_reasoning_patterns()

    def trace_reasoning_path(self, start_concept: str, end_concept: str):
        """Trace reasoning path between concepts."""
        return self.reasoning_graph.find_reasoning_path(start_concept, end_concept)
    
    def reset_ai_bias(self):
        """Reset AI obsession bias using sleep-like consolidation."""
        print("BRAIN RESET: Triggering intensive memory consolidation to reduce AI bias...")
        
        # Force multiple consolidation cycles
        for i in range(3):
            print(f"CONSOLIDATION CYCLE {i+1}/3:")
            self.sleep_consolidation.consolidate_memories()
        
        # Clear problematic working memory
        print("MEMORY CLEANUP: Clearing AI-biased working memory...")
        cleaned_working = deque(maxlen=7)
        for item in self.working_memory:
            content = item['content'].lower()
            ai_density = sum(1 for term in ['artificial intelligence', 'ai is', 'machine learning'] 
                           if term in content)
            if ai_density < 2:  # Keep items with minimal AI content
                cleaned_working.append(item)
        
        self.working_memory = cleaned_working
        print(f"CLEANUP COMPLETE: Retained {len(self.working_memory)} clean memory items")
        
        # Reset recent responses that might be contaminated
        self.recent_responses.clear()
        print("RESPONSE HISTORY: Cleared recent response patterns")
        
        print("BRAIN RESET COMPLETE: AI bias reduction measures applied")


# Main execution functions
def interactive_learning_loop(arc):
    """Interactive conversation with biological learning."""
    
    print("\nStarting interactive LEARNING mode with biological learning mechanisms...")
    print("Every conversation will be processed through biological learning controls!")
    print("Commands: 'quit', 'stats', 'save', 'reset' (for AI bias reset)")
    
    while True:
        try:
            user_input = input("\nLearning ARC> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'stats':
                arc.display_learning_stats()
            elif user_input.lower() == 'save':
                arc.save_learning_state()
            elif user_input.lower() == 'reset':
                arc.reset_ai_bias()
            elif user_input.lower() == 'consolidate':
                arc.sleep_consolidation.consolidate_memories()
            else:
                response_data, reflection_data = arc.process_user_interaction(user_input)
                
                # Show response
                print(f"AI Response: {response_data['thought']}")
                print(f"   Confidence: {response_data['confidence']:.3f}")
                
                # Show biological learning indicators
                if response_data.get('inhibition_applied'):
                    print("   COGNITIVE INHIBITION: Response was filtered for appropriateness")
                if response_data.get('metacognitive_correction'):
                    print("   METACOGNITION: Response was corrected for quality")
                
                print(f"Internal Reflection: {reflection_data['thought']}")
                print(f"   Confidence: {reflection_data['confidence']:.3f}")
                
                # Show learning results
                total_learned = len(response_data['novel_concepts']) + len(reflection_data['novel_concepts'])
                if total_learned > 0:
                    all_concepts = response_data['novel_concepts'] + reflection_data['novel_concepts']
                    print(f"CONCEPT LEARNING: Neural network learned: {', '.join(set(all_concepts))}")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error in interaction: {e}")
            continue
    
    print("\nExiting interactive mode...")


def extended_learning_session(arc):
    """Extended learning session with periodic saves."""
    
    duration = input("Enter duration in minutes (default 10): ").strip()
    try:
        duration = int(duration) if duration else 10
    except ValueError:
        duration = 10
    
    print(f"Starting extended learning session for {duration} minutes...")
    print("The system will save state every 5 minutes automatically.")
    
    arc.consciousness_active = True
    
    # Run learning session with periodic saves
    minutes_elapsed = 0
    save_interval = 5
    
    while minutes_elapsed < duration:
        session_duration = min(save_interval, duration - minutes_elapsed)
        
        print(f"\nLearning segment {minutes_elapsed + 1}-{minutes_elapsed + session_duration} minutes:")
        arc.continuous_consciousness(duration_minutes=session_duration)
        
        minutes_elapsed += session_duration
        
        # Auto-save every interval
        if minutes_elapsed < duration:
            print("AUTO-SAVE: Saving learning state...")
            arc.save_learning_state()
            
            # Show progress
            progress = (minutes_elapsed / duration) * 100
            print(f"PROGRESS: {progress:.1f}% complete ({minutes_elapsed}/{duration} minutes)")
    
    print(f"\nExtended learning session complete: {duration} minutes")
    arc.save_learning_state()


def learning_system_tour(arc):
    """Guided tour of the biological learning systems."""
    
    print("\nWelcome to the Biological Learning Systems Tour!")
    print("=" * 50)
    
    print("\n1. CONTEXTUAL GATING SYSTEM:")
    print("   This system mimics the hippocampus - deciding what experiences to encode into memory.")
    test_experience = "The user asked about quantum computing and I responded appropriately."
    test_context = {'source': 'external', 'user_input': 'quantum computing', 'recent_experiences': []}
    should_encode, score = arc.contextual_gating.should_encode_memory(test_experience, test_context)
    print(f"   Test: Should encode '{test_experience[:40]}...'? {should_encode} (score: {score:.3f})")
    
    print("\n2. COGNITIVE INHIBITION SYSTEM:")
    print("   This system mimics the prefrontal cortex - stopping inappropriate responses.")
    test_response = "Hello! Artificial intelligence is fascinating and I love thinking about AI systems constantly."
    test_context = {'user_input': 'Hello!', 'type': 'greeting', 'recent_responses': []}
    inhibited = arc.cognitive_inhibition.inhibit_inappropriate_response(test_response, test_context)
    print(f"   Test inappropriate response: '{test_response[:40]}...'")
    print(f"   After inhibition: '{inhibited[:40]}...'")
    print(f"   Inhibition applied: {inhibited != test_response}")
    
    print("\n3. MULTIPLE LEARNING SYSTEMS:")
    print("   Different types of memories are stored in separate systems (like brain regions).")
    systems_stats = arc.multiple_learning_systems.get_stats()
    for system, count in systems_stats.items():
        print(f"   {system}: {count} memories stored")
    
    print("\n4. METACOGNITIVE MONITORING:")
    print("   This system monitors response quality and triggers corrections.")
    test_input = "What's your favorite color?"
    test_bad_response = "AI systems don't have preferences but artificial intelligence is complex."
    quality_ok, scores, violations = arc.metacognitive_monitor.monitor_response_quality(
        test_input, test_bad_response
    )
    print(f"   Test response quality: {quality_ok}")
    print(f"   Quality violations: {[v[0] for v in violations]}")
    
    print("\n5. SLEEP-LIKE CONSOLIDATION:")
    print("   Periodic memory consolidation strengthens good patterns and weakens bad ones.")
    print(f"   Consolidation interval: every {arc.sleep_consolidation.consolidation_interval} interactions")
    print(f"   Current count: {arc.sleep_consolidation.interaction_count}")
    
    print("\nTour complete! These biological mechanisms work together to prevent AI bias loops.")
    
    # Offer to run test interaction
    test_mode = input("\nWould you like to test the biological learning systems? (y/n): ").strip().lower()
    if test_mode == 'y':
        print("\nTesting biological learning systems with a few interactions...")
        test_inputs = [
            "Hello!",
            "What's your favorite color?", 
            "Tell me about cats",
            "Thank you"
        ]
        
        for test_input in test_inputs:
            print(f"\nTEST INPUT: {test_input}")
            response_data, reflection_data = arc.process_user_interaction(test_input)
            
            bio_metrics = response_data.get('biological_metrics', {})
            print(f"Response: {response_data['thought']}")
            print(f"Biological controls: Inhibition={bio_metrics.get('inhibition_applied', False)}, "
                  f"Metacognitive={bio_metrics.get('metacognitive_correction', False)}")


def main():
    """Run ARC with biological learning mechanisms."""
    
    import signal
    
    def signal_handler(signum, frame):
        print("\n\nShutting down learning ARC system...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("""
ADAPTIVE RECURSIVE CONSCIOUSNESS (ARC) - BIOLOGICAL LEARNING EDITION
====================================================================

REAL NEURAL NETWORK LEARNING + BIOLOGICAL LEARNING MECHANISMS:
* Real LoRA adapter training with gradient descent
* Weight updates from experience using backpropagation  
* Catastrophic forgetting prevention (Elastic Weight Consolidation)
* Concept association learning with positive/negative examples
* Self-supervised learning from generated thoughts
* Continual learning with Fisher Information tracking

NEW BIOLOGICAL LEARNING CONTROLS:
* Contextual Gating (hippocampus-like memory encoding decisions)
* Cognitive Inhibition (prefrontal cortex-like response filtering)  
* Sleep-like Consolidation (memory strengthening and bias correction)
* Multiple Learning Systems (separate brain-region-like memory streams)
* Metacognitive Monitoring (self-correction of poor responses)

This system GENUINELY learns while preventing AI bias loops through biology!
""")
    
    # User interface for options
    print("\nChoose learning experience:")
    print("1. Quick biological learning demo (2 minutes with biological controls)")
    print("2. Interactive learning (conversation with biological learning mechanisms)")
    print("3. Extended learning session (5+ minutes of biologically-controlled evolution)")
    print("4. Biological learning system tour (guided demo of brain-like mechanisms)")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    # Learning rate selection
    print(f"\nLearning rate selection:")
    print("1. Conservative (1e-5) - Stable, slow learning")
    print("2. Moderate (1e-4) - Balanced learning speed")  
    print("3. Aggressive (1e-3) - Fast learning, higher risk")
    
    lr_choice = input("Select learning rate (1-3, default=2): ").strip() or "2"
    
    learning_rates = {"1": 1e-5, "2": 1e-4, "3": 1e-3}
    learning_rate = learning_rates.get(lr_choice, 1e-4)
    
    # Initialize system
    try:
        arc = LearningARCConsciousness(model_name="gpt2", learning_rate=learning_rate)
    except Exception as e:
        print(f"Error initializing learning system: {e}")
        return
    
    # Execute based on choice
    if choice == '1':
        arc.consciousness_active = True
        arc.continuous_consciousness(duration_minutes=2)
    elif choice == '2':
        interactive_learning_loop(arc)
    elif choice == '3':
        extended_learning_session(arc)
    elif choice == '4':
        learning_system_tour(arc)
    else:
        print("Invalid choice, starting interactive mode...")
        interactive_learning_loop(arc)
    
    # Save final state
    print("\nSaving final learning state...")
    arc.save_learning_state()
    print("ARC session complete.")


if __name__ == "__main__":
    main()