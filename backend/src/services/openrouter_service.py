import requests
import os

class OpenRouterService:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or os.environ.get('OPENROUTER_API_KEY')
        self.base_url = base_url or os.environ.get('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.model = model or os.environ.get('OPENROUTER_MODEL', 'meta-llama/llama-3.1-8b-instruct:free')
    
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://ai-interviewer.local',
            'X-Title': 'AI Interviewer'
        }
    
    def generate_content(self, prompt, system_prompt=None, temperature=0.7, max_tokens=2000):
        """Generate content using OpenRouter API"""
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f'{self.base_url}/chat/completions',
            headers=self.get_headers(),
            json=payload,
            timeout=60
        )
        
        if not response.ok:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            raise Exception(f"OpenRouter API error: {response.status_code} - {error_data.get('error', {}).get('message', response.text)}")
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    def get_free_models(self):
        """Fetch free models from OpenRouter"""
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured")
        
        response = requests.get(
            f'{self.base_url}/models',
            headers=self.get_headers(),
            timeout=10
        )
        
        if not response.ok:
            raise Exception(f"Failed to fetch models: {response.status_code}")
        
        data = response.json()
        models = data.get('data', [])
        
        free_models = []
        for model in models:
            pricing = model.get('pricing', {})
            prompt_price = float(pricing.get('prompt', '0'))
            completion_price = float(pricing.get('completion', '0'))
            
            if prompt_price == 0 and completion_price == 0:
                free_models.append({
                    'id': model.get('id'),
                    'name': model.get('name'),
                    'description': model.get('description', ''),
                    'context_length': model.get('context_length', 0),
                    'pricing': pricing
                })
        
        return free_models
    
    def test_key(self):
        """Test if the API key is valid"""
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured")
        
        response = requests.get(
            f'{self.base_url}/auth/key',
            headers=self.get_headers(),
            timeout=10
        )
        
        return response.ok


def get_openrouter_service(user=None):
    """Factory function to create OpenRouterService from user settings or environment"""
    if user:
        return OpenRouterService(
            api_key=user.openrouter_api_key,
            base_url=user.openrouter_base_url,
            model=user.selected_model
        )
    return OpenRouterService()