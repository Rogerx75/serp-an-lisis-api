import os
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import concurrent.futures
import time
import json

# === CONFIGURACIÓN REAL === 
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'ebc1395d1emsh69528501ee78f5ap19c2cfjsnbb649c147b38')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', 'google-keyword-insight1.p.rapidapi.com')
SERP_PROVIDER = os.getenv('SERP_PROVIDER', 'valueserp')  # 'valueserp' o 'serpapi'
VALUESERP_API_KEY = os.getenv('VALUESERP_API_KEY', '8F82C585D7604B85A14A72AE63D2BE07')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', 'ebc1395d1emsh69528501ee78f5ap19c2cfjsnbb649c147b38')

from services.keyword_service import get_related_keywords
from services.serp_service import get_serp_results
from services.clustering_service import cluster_keywords, analyze_competitors

app = Flask(__name__)

CORS(app)
api = Api(app, version='1.0', title='SERP Analysis API',
          description='API para análisis de keywords y SERP')

ns = api.namespace('api', description='Operaciones de análisis SERP')

# Modelos de datos para la API
analysis_request = api.model('AnalysisRequest', {
    'topic': fields.String(required=True, description='Keyword principal'),
    'domain': fields.String(required=True, description='Dominio a analizar'),
    'country': fields.String(default='es', description='País para la búsqueda'),
    'language': fields.String(default='es', description='Idioma para la búsqueda'),
    'max_keywords': fields.Integer(default=20, description='Número máximo de keywords relacionadas')
})

@ns.route('/analyze')
class Analysis(Resource):
    @api.expect(analysis_request)
    def post(self):
        """Realizar análisis completo de keywords y SERP"""
        start_time = time.time()
        
        data = request.json
        topic = data.get('topic')
        domain = data.get('domain')
        country = data.get('country', 'es')
        language = data.get('language', 'es')
        max_keywords = data.get('max_keywords', 20)
        
        if not topic or not domain:
            return {'error': 'Se requieren topic y domain'}, 400
        
        # Paso 1: Obtener keywords relacionadas
        try:
            keywords = get_related_keywords(topic, max_keywords)
            if not keywords:
                return {'error': 'No se pudieron obtener keywords relacionadas'}, 500
        except Exception as e:
            return {'error': f'Error obteniendo keywords: {str(e)}'}, 500
        
        # Paso 2: Obtener resultados SERP para cada keyword
        serp_results = {}
        
        # Usamos threads para paralelizar las peticiones SERP
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_keyword = {
                executor.submit(get_serp_results, keyword, country, language): keyword 
                for keyword in keywords
            }
            
            for future in concurrent.futures.as_completed(future_to_keyword):
                keyword = future_to_keyword[future]
                try:
                    result = future.result()
                    serp_results[keyword] = result
                except Exception as e:
                    serp_results[keyword] = {'error': str(e)}
        
        # Paso 3: Clusterizar keywords por intención de búsqueda
        clusters = cluster_keywords(serp_results)
        
        # Paso 4: Analizar presencia del dominio y competidores
        domain_analysis = analyze_domain_presence(serp_results, domain, clusters)
        competitors = analyze_competitors(serp_results, domain)
        
        # Preparar respuesta
        response = {
            'topic': topic,
            'domain': domain,
            'keywords_analyzed': list(serp_results.keys()),
            'clusters': clusters,
            'domain_analysis': domain_analysis,
            'top_competitors': competitors[:3],
            'processing_time': round(time.time() - start_time, 2)
        }
        
        return response

def analyze_domain_presence(serp_results, domain, clusters):
    """Analizar la presencia del dominio en los resultados"""
    present_intents = []
    missing_intents = []
    
    for cluster in clusters:
        cluster_domain_present = False
        cluster_info = {
            'intent_id': cluster['id'],
            'keywords': cluster['keywords'],
            'domain_appearances': []
        }
        
        for keyword in cluster['keywords']:
            if keyword in serp_results and 'organic_results' in serp_results[keyword]:
                for result in serp_results[keyword]['organic_results'][:20]:  # Top 20
                    if domain in result.get('link', '') or domain in result.get('displayed_link', ''):
                        cluster_domain_present = True
                        cluster_info['domain_appearances'].append({
                            'keyword': keyword,
                            'position': result.get('position', 0),
                            'url': result.get('link', ''),
                            'title': result.get('title', '')
                        })
        
        if cluster_domain_present:
            present_intents.append(cluster_info)
        else:
            missing_intents.append(cluster_info)
    
    return {
        'present': present_intents,
        'missing': missing_intents
    }

@ns.route('/status')
class Status(Resource):
    def get(self):
        """Verificar estado de la API"""
        return {'status': 'active', 'message': 'SERP Analysis API is running'}

if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0', port=5001)  # debug=False y port=5001

  