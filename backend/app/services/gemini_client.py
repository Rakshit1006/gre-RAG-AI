"""Gemini API client wrapper with mocking support."""
import json
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import google.generativeai as genai
from app.config import settings


class GeminiClientInterface(ABC):
    """Abstract interface for Gemini client."""
    
    @abstractmethod
    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Gemini."""
        pass
    
    @abstractmethod
    def generate_json(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate JSON response."""
        pass
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for text."""
        pass
    
    @abstractmethod
    def function_call(
        self, 
        prompt: str, 
        functions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute function calling."""
        pass


class GeminiClient(GeminiClientInterface):
    """Real Gemini API client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client."""
        self.api_key = api_key or settings.gemini_api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model_name = settings.gemini_model
        self.embedding_model_name = settings.gemini_embedding_model
    
    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Gemini."""
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature
            )
        )
        return response.text
    
    def generate_json(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate JSON response."""
        text = self.generate_text(prompt, temperature)
        # Try to extract JSON from response
        try:
            # Look for JSON in code blocks
            if "```json" in text:
                json_str = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                json_str = text.split("```")[1].split("```")[0].strip()
            else:
                json_str = text.strip()
            
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError) as e:
            raise ValueError(f"Failed to parse JSON from response: {e}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for text."""
        result = genai.embed_content(
            model=f"models/{self.embedding_model_name}",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
    def function_call(
        self, 
        prompt: str, 
        functions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute function calling."""
        model = genai.GenerativeModel(
            self.model_name,
            tools=functions
        )
        response = model.generate_content(prompt)
        
        if response.candidates[0].content.parts[0].function_call:
            fc = response.candidates[0].content.parts[0].function_call
            return {
                "name": fc.name,
                "arguments": dict(fc.args)
            }
        
        return {"name": None, "arguments": {}}


class MockGeminiClient(GeminiClientInterface):
    """Mock Gemini client for testing."""
    
    def __init__(self):
        """Initialize mock client."""
        self.responses = {}
        self.embeddings = {}
    
    def set_response(self, key: str, response: Any):
        """Set mock response for a key."""
        self.responses[key] = response
    
    def set_embedding(self, text: str, embedding: List[float]):
        """Set mock embedding for text."""
        self.embeddings[text] = embedding
    
    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate mock text response."""
        return self.responses.get("text", "Mock response")
    
    def generate_json(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate mock JSON response."""
        # Check if prompt is for mnemonic generation
        if "mnemonic generator" in prompt.lower() or '"word"' in prompt:
            # Try to extract word from prompt
            word = "test"
            if '"word":' in prompt:
                try:
                    import re
                    match = re.search(r'"word":\s*"([^"]+)"', prompt)
                    if match:
                        word = match.group(1)
                except:
                    pass
            
            return {
                "word": word,
                "pos": "adjective",
                "gre_definition": f"Mock definition for {word}",
                "pithy_definition": f"Brief definition for {word}",
                "base_word": word,
                "associations": ["assoc1", "assoc2", "assoc3", "assoc4", "assoc5"],
                "examples": ["Example 1", "Example 2", "Example 3"],
                "easy_synonyms": ["syn1", "syn2", "syn3"],
                "gre_synonyms": ["gresyn1", "gresyn2", "gresyn3"],
                "story": f"A memorable story about {word} to help you remember it."
            }
        
        return self.responses.get("json", {"mock": "data"})
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate mock embedding."""
        if text in self.embeddings:
            return self.embeddings[text]
        # Generate consistent mock embedding based on text hash
        import hashlib
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        return [(hash_val >> i) % 100 / 100.0 for i in range(768)]
    
    def function_call(
        self, 
        prompt: str, 
        functions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute mock function calling."""
        return self.responses.get("function_call", {"name": None, "arguments": {}})


# Global client instance
_client: Optional[GeminiClientInterface] = None


def get_gemini_client() -> GeminiClientInterface:
    """Get Gemini client instance."""
    global _client
    if _client is None:
        # Check if we should use mock client
        if os.getenv("USE_MOCK_GEMINI", "false").lower() == "true":
            _client = MockGeminiClient()
        else:
            _client = GeminiClient()
    return _client


def set_gemini_client(client: GeminiClientInterface):
    """Set custom Gemini client (useful for testing)."""
    global _client
    _client = client
