import requests
import time
from config import Config
from utils.serp_providers import get_serp_provider

def get_serp_results(keyword, country='es', language='es', num_results=100):
    """Obtener resultados SERP para una keyword"""
    provider = get_serp_provider()
    return provider.get_serp(keyword, country, language, num_results)

def process_batch_serp_requests(keywords, country='es', language='es'):
    """Procesar múltiples solicitudes SERP en lote"""
    results = {}
    
    for keyword in keywords:
        try:
            results[keyword] = get_serp_results(keyword, country, language)
            time.sleep(1)  # Respeta los límites de rate limiting
        except Exception as e:
            results[keyword] = {'error': str(e)}
    
    return results