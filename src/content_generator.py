"""Content generation module using OpenAI GPT"""

import openai
import logging
import json
from typing import Dict, List, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generate educational content using OpenAI GPT API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize content generator with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.max_tokens = 2000
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.api_key
    
    def generate(self, topic: str, language: str = 'en', depth: str = 'intermediate') -> Dict:
        """Generate educational content for a given topic"""
        try:
            logger.info(f"Generating content for topic: {topic}")
            
            # Create prompt
            prompt = self._create_prompt(topic, language, depth)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator. Create comprehensive, engaging, and accurate learning materials."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=self.max_tokens,
                top_p=0.9
            )
            
            # Extract content
            content_text = response['choices'][0]['message']['content']
            
            # Parse content
            structured_content = self._parse_content(content_text, topic)
            
            return {
                'id': hash(topic + datetime.now().isoformat()),
                'topic': topic,
                'title': structured_content['title'],
                'description': structured_content['description'],
                'sections': structured_content['sections'],
                'key_points': structured_content['key_points'],
                'language': language,
                'depth': depth,
                'created_at': datetime.utcnow().isoformat(),
                'status': 'completed',
                'tokens_used': response['usage']['total_tokens']
            }
        
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise
    
    def _create_prompt(self, topic: str, language: str, depth: str) -> str:
        """Create a detailed prompt for content generation"""
        
        depth_instructions = {
            'basic': 'Cover fundamentals only, simple language suitable for beginners',
            'intermediate': 'Cover key concepts with some depth, suitable for learners with basic knowledge',
            'advanced': 'Provide comprehensive coverage with advanced concepts and technical details'
        }
        
        prompt = f"""
Create comprehensive educational content for the topic: "{topic}"

Depth Level: {depth_instructions.get(depth, depth_instructions['intermediate'])}
Language: {'English' if language == 'en' else language}

Provide content in the following JSON format:
{{
    "title": "Topic Title",
    "description": "2-3 sentence overview",
    "sections": [
        {{
            "title": "Section 1",
            "content": "Detailed explanation",
            "key_points": ["point1", "point2", "point3"]
        }},
        {{
            "title": "Section 2",
            "content": "Detailed explanation",
            "key_points": ["point1", "point2"]
        }},
        {{
            "title": "Key Takeaways",
            "content": "Summary of main learnings",
            "key_points": ["takeaway1", "takeaway2"]
        }}
    ],
    "key_points": ["main_point_1", "main_point_2", "main_point_3"],
    "learning_objectives": ["objective_1", "objective_2"],
    "fun_facts": ["fact_1", "fact_2"]
}}

Ensure the content is:
- Accurate and factually correct
- Well-structured with clear sections
- Engaging and easy to understand
- Suitable for video narration
- Contains practical examples where applicable
"""
        return prompt
    
    def _parse_content(self, content_text: str, topic: str) -> Dict:
        """Parse the GPT response into structured content"""
        try:
            # Try to extract JSON from the response
            json_start = content_text.find('{')
            json_end = content_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content_text[json_start:json_end]
                parsed = json.loads(json_str)
            else:
                # Fallback if no JSON found
                parsed = {
                    'title': f'Learning {topic}',
                    'description': content_text[:200],
                    'sections': [{'title': 'Content', 'content': content_text, 'key_points': []}],
                    'key_points': [],
                    'learning_objectives': []
                }
            
            return parsed
        
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback")
            return {
                'title': f'Learning {topic}',
                'description': content_text[:200],
                'sections': [{'title': 'Content', 'content': content_text, 'key_points': []}],
                'key_points': [],
                'learning_objectives': []
            }
    
    def generate_script(self, content: Dict) -> str:
        """Generate a video script from the content"""
        script = f"""
{content['title']}

{content['description']}

"""
        
        for section in content.get('sections', []):
            script += f"""
Section: {section['title']}
{section['content']}

Key Points:
"""
            for point in section.get('key_points', []):
                script += f"  - {point}\n"
        
        return script
    
    def generate_summary(self, content: Dict, max_length: int = 500) -> str:
        """Generate a summary of the content"""
        summary_parts = [
            content['description'],
            "Key Points:"
        ]
        
        for point in content.get('key_points', [])[:5]:
            summary_parts.append(f"  - {point}")
        
        summary = "\n".join(summary_parts)
        
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary


class ContentCache:
    """Simple cache for generated content"""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str) -> Optional[Dict]:
        """Get cached content"""
        return self.cache.get(key)
    
    def set(self, key: str, value: Dict) -> None:
        """Set cached content"""
        self.cache[key] = value
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
