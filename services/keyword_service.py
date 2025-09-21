from config import Config
import requests

def get_related_keywords(topic, max_keywords=20):
    """Obtener keywords relacionadas usando ValueSerp"""
    try:
        # Usar ValueSerp para obtener keywords relacionadas
        url = "https://api.valueserp.com/search"
        params = {
            'q': topic,
            'api_key': "8F82C585D7604B85A14A72AE63D2BE07",
            'location': 'Spain',
            'gl': 'es', 
            'hl': 'es',
            'num': 10
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extraer keywords de las sugerencias y related searches
        keywords = set()
        keywords.add(topic)
        
        # De related searches
        if 'related_searches' in data:
            for item in data['related_searches'][:8]:
                keywords.add(item.get('query', ''))
        
        # De search refinement
        if 'search_refinement' in data:
            for item in data['search_refinement'].get('items', [])[:5]:
                keywords.add(item.get('title', ''))
        
        return list(keywords)[:max_keywords]
        
    except Exception as e:
        print(f"ValueSerp error: {e}, usando keywords realistas")
        # Fallback a keywords realistas
        return get_realistic_keywords(topic, max_keywords)

def get_realistic_keywords(topic, max_keywords):
    """Keywords realistas de alta calidad para fallback"""
    related_map = {
        'zapatos': [
            'zapatillas {keyword} hombre', 'zapatillas {keyword} mujer', 'zapatos {keyword} running',
            'mejores zapatillas {keyword}', '{keyword} outlet', '{keyword} rebajados',
            '{keyword} calidad', '{keyword} marca', 'comprar {keyword} online',
            'ofertas {keyword}', 'precio {keyword}', 'review {keyword}',
            'comparativa {keyword}', '{keyword} baratos', '{keyword} deportivos'
        ],
        'hoteles': [
            'hoteles {keyword} centro', 'reservar hotel {keyword}', 'mejores hoteles {keyword}',
            'hoteles {keyword} baratos', 'hoteles {keyword} lujo', 'ofertas hoteles {keyword}',
            'alojamiento {keyword}', 'apartamentos {keyword}', 'hostales {keyword}',
            'booking {keyword}', 'reservas {keyword}', 'opiniones hoteles {keyword}'
        ],
        'telefonos': [
            'móviles {keyword} baratos', 'smartphones {keyword}', 'mejores móviles {keyword}',
            'teléfonos {keyword} ofertas', '{keyword} última generación', 'comparativa {keyword}',
            'review {keyword}', 'opinión {keyword}', 'precio {keyword}',
            '{keyword} gaming', '{keyword} cámara', '{keyword} 5g'
        ]
    }
    
    # Identificar categoría
    category = 'telefonos'
    for cat in related_map:
        if cat in topic.lower():
            category = cat
            break
    
    # Generar keywords variadas
    keywords = set()
    keywords.add(topic)
    
    for template in related_map[category]:
        keyword_variant = template.format(keyword=topic)
        keywords.add(keyword_variant)
        if len(keywords) >= max_keywords:
            break
    
    return list(keywords)[:max_keywords]