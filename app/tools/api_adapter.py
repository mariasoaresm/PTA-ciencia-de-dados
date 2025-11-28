import json
import requests
from requests.exceptions import Timeout, RequestException
from agno.tools import Toolkit

class ExternalAPIAdapter(Toolkit):
    def __init__(self):
        super().__init__(name="external_api_adapter")
        self.register(self.safe_http_get)

    def safe_http_get(self, url: str) -> str:
        """
        Realiza uma requisição HTTP GET segura para uma URL externa.

        Args:
            url (str): O endpoint da API para consultar.

        Returns:
            str: Uma string JSON contendo o status, código de status e dados (ou mensagem de erro).
        """
        try:
            # Timeout de 5 segundos conforme especificado
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            # Tenta decodificar JSON, fallback para texto se não for JSON
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text

            return json.dumps({
                "status": "SUCCESS",
                "status_code": response.status_code,
                "data": response_data
            })

        except Timeout:
            return json.dumps({
                "status": "ERROR",
                "status_code": 408,
                "data": "A requisição excedeu o tempo limite de 5 segundos."
            })

        except RequestException as e:
            # Captura erros de conexão, erros HTTP (4xx/5xx) levantados por raise_for_status, etc.
            status_code = e.response.status_code if e.response else 500
            return json.dumps({
                "status": "ERROR",
                "status_code": status_code,
                "data": str(e)
            })