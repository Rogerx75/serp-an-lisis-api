from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
api = Api(app)

@api.route('/status')
class Status(Resource):
    def get(self):
        return {'status': 'active', 'message': 'API funcionando'}

@api.route('/test-serp')
class TestSERP(Resource):
    def get(self):
        """Probar ValueSerp directamente"""
        try:
            response = requests.get(
                "https://api.valueserp.com/search",
                params={
                    'q': 'zapatos running mujer',
                    'api_key': '8F82C585D7604B85A14A72AE63D2BE07',
                    'location': 'Spain'
                }
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)