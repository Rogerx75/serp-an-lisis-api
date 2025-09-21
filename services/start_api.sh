# Crear archivo start_api.sh
echo '#!/bin/bash
cd /home/kali/Downloads/
source serp_env/bin/activate
export VALUESERP_API_KEY="8F82C585D7604B85A14A72AE63D2BE07"
export SERP_PROVIDER="valueserp"
python app.py' > start_api.sh

chmod +x start_api.sh

# Usar después de cada corte
./start_api.sh