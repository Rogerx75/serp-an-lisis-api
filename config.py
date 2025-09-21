
import os

class Config:
    # API Keys REALES (reemplaza con las tuyas)
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'ebc1395d1emsh69528501ee78f5ap19c2cfjsnbb649c147b38')
    RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', 'google-keyword-insight1.p.rapidapi.com')
    
    # ValueSerp REAL
    SERP_PROVIDER = os.getenv('SERP_PROVIDER', 'valueserp')
    VALUESERP_API_KEY = os.getenv('VALUESERP_API_KEY', '8F82C585D7604B85A14A72AE63D2BE07')
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '')