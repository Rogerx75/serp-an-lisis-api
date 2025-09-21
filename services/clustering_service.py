import networkx as nx
from collections import defaultdict

def cluster_keywords(serp_results, min_common_urls=5):
    """Agrupar keywords en clusters basados en URLs comunes en el top 10"""
    # Crear un grafo donde los nodos son keywords
    G = nx.Graph()
    
    # Añadir todas las keywords como nodos
    keywords = list(serp_results.keys())
    G.add_nodes_from(keywords)
    
    # Para cada par de keywords, verificar si comparten suficientes URLs
    for i, kw1 in enumerate(keywords):
        if kw1 not in serp_results or 'organic_results' not in serp_results[kw1]:
            continue
            
        urls1 = set()
        for result in serp_results[kw1]['organic_results'][:10]:  # Top 10
            if 'link' in result:
                urls1.add(normalize_url(result['link']))
        
        for j, kw2 in enumerate(keywords[i+1:], i+1):
            if kw2 not in serp_results or 'organic_results' not in serp_results[kw2]:
                continue
                
            urls2 = set()
            for result in serp_results[kw2]['organic_results'][:10]:  # Top 10
                if 'link' in result:
                    urls2.add(normalize_url(result['link']))
            
            # Calcular intersección
            common_urls = urls1.intersection(urls2)
            
            # Si comparten suficientes URLs, añadir una arista
            if len(common_urls) >= min_common_urls:
                G.add_edge(kw1, kw2, weight=len(common_urls))
    
    # Encontrar componentes conectados (clusters)
    clusters = []
    for i, component in enumerate(nx.connected_components(G)):
        clusters.append({
            'id': f"cluster_{i+1}",
            'keywords': list(component),
            'size': len(component)
        })
    
    # Keywords que no están en ningún cluster
    all_clustered_keywords = set()
    for cluster in clusters:
        all_clustered_keywords.update(cluster['keywords'])
    
    unclustered = set(keywords) - all_clustered_keywords
    for kw in unclustered:
        clusters.append({
            'id': f"cluster_single_{len(clusters)+1}",
            'keywords': [kw],
            'size': 1
        })
    
    return clusters

def normalize_url(url):
    """Normalizar URL para comparación"""
    # Eliminar protocolo, www y parámetros de consulta
    url = url.lower()
    if '://' in url:
        url = url.split('://')[1]
    if url.startswith('www.'):
        url = url[4:]
    if '?' in url:
        url = url.split('?')[0]
    if '/' in url and url.count('/') > 1:
        url = '/'.join(url.split('/')[:3])
    return url

def analyze_competitors(serp_results, domain):
    """Analizar competidores frecuentes en los resultados"""
    domain_count = defaultdict(int)
    
    for keyword, results in serp_results.items():
        if 'organic_results' not in results:
            continue
            
        for result in results['organic_results'][:20]:  # Top 20
            if 'link' in result:
                url = result['link']
                # Extraer dominio
                competitor_domain = extract_domain(url)
                
                # Ignorar el dominio objetivo y dominios genéricos
                if (competitor_domain and 
                    domain not in competitor_domain and
                    competitor_domain not in ['google.com', 'youtube.com', 'facebook.com']):
                    domain_count[competitor_domain] += 1
    
    # Ordenar por frecuencia
    sorted_competitors = sorted(domain_count.items(), key=lambda x: x[1], reverse=True)
    return [{'domain': domain, 'count': count} for domain, count in sorted_competitors]

def extract_domain(url):
    """Extraer dominio de una URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return None