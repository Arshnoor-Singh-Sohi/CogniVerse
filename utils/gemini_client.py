"""
Enhanced Gemini Client Module

This module provides a sophisticated wrapper around Google's Gemini API.
The design patterns used here demonstrate several important software engineering concepts:

1. Separation of Concerns: API logic is isolated from UI logic
2. Error Handling: Robust error management with retry mechanisms
3. Context Management: Intelligent conversation context handling
4. Performance Optimization: Response caching and request batching

Think of this class as a translator between your application and Google's AI services.
"""

import google.generativeai as genai
from typing import Dict, List, Optional, Any, Union
import json
import time
import logging
from datetime import datetime, timedelta
import base64
from pathlib import Path
import hashlib

from config.settings import AppConfig

# Set up logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Enhanced client for interacting with Google's Gemini API.
    
    This class implements several advanced patterns:
    - Retry logic for handling temporary failures
    - Response caching to improve performance
    - Context-aware conversations
    - File and image processing capabilities
    """
    
    def __init__(self):
        self.config = AppConfig()
        
        # Configure the Gemini API with our key
        genai.configure(api_key=self.config.google_api_key)
        
        # Initialize models dictionary - this creates connections to different AI models
        self.models = {}
        self._initialize_models()
        
        # Response caching system - stores recent responses to avoid redundant API calls
        self.response_cache = {}
        self.cache_expiry = timedelta(minutes=30)  # Cache responses for 30 minutes
        
        # Rate limiting to prevent API quota exhaustion
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Minimum seconds between requests
        
        logger.info("GeminiClient initialized successfully")
    
    def _initialize_models(self):
        """
        Initialize connections to different Gemini models.
        
        This method demonstrates the Factory pattern - we create different
        model instances based on configuration. Each model has different
        capabilities and use cases.
        """
        try:
            for model_name, model_config in self.config.models.items():
                # Create a GenerativeModel instance for each configured model
                self.models[model_name] = genai.GenerativeModel(
                    model_name=model_name,
                    # System instruction helps set the AI's behavior and personality
                    system_instruction=self._get_system_instruction()
                )
                logger.info(f"Initialized model: {model_config.display_name}")
                
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise
    
    def _get_system_instruction(self) -> str:
        """
        Define the AI's personality and behavior guidelines.
        
        System instructions are like giving the AI a job description - they help
        ensure consistent, helpful responses across all interactions.
        """
        return """
        You are an intelligent AI assistant in CogniVerse, designed to be helpful, 
        accurate, and engaging. You excel at:
        
        - Providing clear, well-structured explanations
        - Analyzing documents and extracting key insights
        - Helping with creative writing and problem-solving
        - Writing and explaining code in multiple programming languages
        - Answering questions across diverse domains
        
        Always strive to be informative while maintaining a friendly, professional tone.
        When analyzing files or images, provide detailed observations and actionable insights.
        """
    
    def generate_response(
        self, 
        prompt: str, 
        model: str = "gemini-2.0-flash-exp",
        context: Optional[Dict] = None,
        include_files: bool = True
    ) -> str:
        """
        Generate an AI response with advanced context handling.
        
        This method demonstrates several important concepts:
        - Input validation and sanitization
        - Context preparation and management
        - Error handling with graceful degradation
        - Response caching for performance
        
        Args:
            prompt: The user's input message
            model: Which AI model to use for generation
            context: Additional context like files and conversation history
            include_files: Whether to include uploaded files in the context
        
        Returns:
            The AI's response as a string
        """
        try:
            # Input validation - always validate user inputs
            if not prompt or not prompt.strip():
                return "I'd be happy to help! Please provide a question or message."
            
            # Check if we have a cached response for this exact query
            cache_key = self._generate_cache_key(prompt, model, context)
            cached_response = self._get_cached_response(cache_key)
            if cached_response:
                logger.info("Returning cached response")
                return cached_response
            
            # Rate limiting - prevent overwhelming the API
            self._enforce_rate_limit()
            
            # Prepare the conversation content with context
            conversation_parts = self._prepare_conversation_parts(prompt, context, include_files)
            
            # Get the appropriate model instance
            model_instance = self.models.get(model)
            if not model_instance:
                logger.warning(f"Model {model} not found, using default")
                model_instance = self.models.get("gemini-2.0-flash-exp")
            
            # Generate the response with retry logic
            response = self._generate_with_retry(model_instance, conversation_parts)
            
            # Cache the response for future use
            self._cache_response(cache_key, response)
            
            # Log successful generation for monitoring
            logger.info(f"Generated response using {model} ({len(response)} characters)")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    def _prepare_conversation_parts(
        self, 
        prompt: str, 
        context: Optional[Dict], 
        include_files: bool
    ) -> List[Any]:
        """
        Prepare the conversation content including text, files, and images.
        
        This method demonstrates how to structure complex inputs for AI models.
        We build a list of different content types that the AI can process together.
        """
        parts = []
        
        # Add conversation history for context continuity
        if context and context.get('conversation_history'):
            history_summary = self._summarize_conversation_history(
                context['conversation_history']
            )
            if history_summary:
                parts.append(f"Previous conversation context: {history_summary}\n\n")
        
        # Include uploaded files if requested and available
        if include_files and context and context.get('uploaded_files'):
            file_context = self._prepare_file_context(context['uploaded_files'])
            if file_context:
                parts.extend(file_context)
        
        # Add the main user prompt
        parts.append(prompt)
        
        return parts
    
    def _prepare_file_context(self, uploaded_files: List[Dict]) -> List[Any]:
        """
        Prepare uploaded files for inclusion in the AI conversation.
        
        This method shows how to handle different file types and convert them
        into formats that the AI can understand and analyze.
        """
        file_parts = []
        
        for file_info in uploaded_files[-3:]:  # Include only the 3 most recent files
            try:
                file_name = file_info.get('name', 'Unknown file')
                file_content = file_info.get('content', '')
                file_type = file_info.get('type', '')
                
                # Handle different file types appropriately
                if file_type.startswith('image/'):
                    # For images, we would include them directly if the model supports vision
                    file_parts.append(f"\n[Image file: {file_name}]\n")
                    # Note: Actual image processing would require additional logic
                    
                elif file_type in ['text/plain', 'application/json']:
                    # For text files, include content directly
                    file_parts.append(f"\n[File: {file_name}]\n{file_content}\n")
                    
                else:
                    # For other files, include a summary or description
                    file_parts.append(f"\n[File: {file_name} - {file_type}]\n")
                    
            except Exception as e:
                logger.warning(f"Error preparing file context: {str(e)}")
                continue
        
        return file_parts
    
    def _summarize_conversation_history(self, history: List[Dict]) -> str:
        """
        Create a concise summary of recent conversation history.
        
        This helps maintain context without overwhelming the AI with too much
        previous conversation data. We focus on the most recent and relevant exchanges.
        """
        if not history:
            return ""
        
        # Take the last few exchanges to maintain context
        recent_history = history[-6:]  # Last 6 messages (3 exchanges)
        
        summary_parts = []
        for message in recent_history:
            role = "User" if message.get('role') == 'user' else "Assistant"
            content = message.get('content', '')[:100]  # Limit to 100 characters
            summary_parts.append(f"{role}: {content}...")
        
        return " | ".join(summary_parts)
    
    def _generate_with_retry(self, model_instance, conversation_parts: List[Any]) -> str:
        """
        Generate response with retry logic for handling temporary failures.
        
        This implements the Retry pattern - a common technique for dealing with
        network issues or temporary service unavailability.
        """
        max_retries = 3
        base_delay = 1.0  # Start with 1 second delay
        
        for attempt in range(max_retries):
            try:
                # Generate the response
                response = model_instance.generate_content(conversation_parts)
                
                # Validate the response
                if response and response.text:
                    return response.text
                else:
                    raise ValueError("Empty response received")
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    # Exponential backoff - wait longer between each retry
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
                else:
                    # If all retries failed, raise the exception
                    raise e
    
    def _enforce_rate_limit(self):
        """
        Ensure we don't make requests too frequently.
        
        Rate limiting is crucial for respecting API quotas and maintaining
        good performance for all users.
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _generate_cache_key(self, prompt: str, model: str, context: Optional[Dict]) -> str:
        """
        Generate a unique key for caching responses.
        
        Cache keys help us identify when we've seen the same request before,
        allowing us to return saved responses instead of making new API calls.
        """
        # Create a hash of the prompt, model, and relevant context
        cache_data = {
            'prompt': prompt,
            'model': model,
            'context_hash': self._hash_context(context) if context else None
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _hash_context(self, context: Dict) -> str:
        """Create a hash of the context for cache key generation."""
        # Hash only the relevant parts of context that affect the response
        relevant_context = {
            'files_count': len(context.get('uploaded_files', [])),
            'has_history': bool(context.get('conversation_history'))
        }
        return hashlib.md5(json.dumps(relevant_context, sort_keys=True).encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """Retrieve a cached response if it exists and hasn't expired."""
        if cache_key in self.response_cache:
            cached_data = self.response_cache[cache_key]
            if datetime.now() - cached_data['timestamp'] < self.cache_expiry:
                return cached_data['response']
            else:
                # Remove expired cache entry
                del self.response_cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: str):
        """Store a response in the cache with timestamp."""
        self.response_cache[cache_key] = {
            'response': response,
            'timestamp': datetime.now()
        }
        
        # Prevent cache from growing too large
        if len(self.response_cache) > 100:
            # Remove oldest entries
            oldest_keys = sorted(
                self.response_cache.keys(),
                key=lambda k: self.response_cache[k]['timestamp']
            )[:20]
            for key in oldest_keys:
                del self.response_cache[key]
    
    def analyze_image(self, image_data: bytes, prompt: str = "Describe this image") -> str:
        """
        Analyze an image using Gemini's vision capabilities.
        
        This method demonstrates how to work with multimodal AI models that
        can process both text and images together.
        """
        try:
            # Use a vision-capable model
            vision_model = self.models.get("gemini-2.0-flash-exp")
            
            # Prepare the image for the AI
            image_parts = [
                {
                    "mime_type": "image/jpeg",  # Adjust based on actual image type
                    "data": base64.b64encode(image_data).decode()
                }
            ]
            
            # Combine image and text prompt
            content_parts = [prompt] + image_parts
            
            response = vision_model.generate_content(content_parts)
            return response.text if response and response.text else "Unable to analyze image"
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            return f"Error analyzing image: {str(e)}"
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model's capabilities.
        
        This helps the application understand what each model can do,
        enabling smart model selection based on the task at hand.
        """
        model_config = self.config.get_model_config(model_name)
        if not model_config:
            return {}
        
        return {
            'name': model_config.name,
            'display_name': model_config.display_name,
            'description': model_config.description,
            'max_tokens': model_config.max_tokens,
            'supports_vision': model_config.supports_vision,
            'supports_files': model_config.supports_files
        }
    
    def clear_cache(self):
        """Clear the response cache - useful for testing or memory management."""
        self.response_cache.clear()
        logger.info("Response cache cleared")