import requests
from config import Config

class SerpProvider:
    def get_serp(self, keyword, country, language, num_results):
        raise NotImplementedError

class ValueSerpProvider(SerpProvider):
    def get_serp(self, keyword, country='es', language='es', num_results=100):
        url = "https://api.valueserp.com/search"
        
        params = {
            'q': keyword,
            'api_key': Config.VALUESERP_API_KEY,
            'location': country,
            'hl': language,
            'gl': country,
            'num': num_results
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

class SerpApiProvider(SerpProvider):
    def get_serp(self, keyword, country='es', language='es', num_results=100):
        url = "https://serpapi.com/search"
        
        params = {
            'q': keyword,
            'api_key': Config.SERPAPI_API_KEY,
            'location': country,
            'hl': language,
            'gl': country,
            'num': num_results,
            'engine': 'google'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

def get_serp_provider():
    """Obtener el proveedor SERP configurado"""
    if Config.SERP_PROVIDER == 'valueserp':
        return ValueSerpProvider()
    elif Config.SERP_PROVIDER == 'serpapi':
        return SerpApiProvider()
    else:
        raise ValueError(f"Proveedor SERP no válido: {Config.SERP_PROVIDER}")