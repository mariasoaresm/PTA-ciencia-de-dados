import requests
from agno.tools import Toolkit

class ExternalAPIAdapter(Toolkit):
    def __init__(self):
        super().__init__(name="external_api_tool")
        self.register(self.get_data)

    def get_data(self, url: str) -> str:
        """
        Realiza chamadas seguras para APIs externas.
        Útil para validar CEPs, taxas de câmbio ou serviços de terceiros.
        
        Args:
            url (str): O endereço da API.
            
        Returns:
            str: O JSON de resposta ou erro.
        """
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return str(response.json())
            else:
                return f"Erro na API Externa: Status {response.status_code}"
        except Exception as e:
            return f"Falha na conexão externa: {e}"