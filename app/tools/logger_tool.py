import logging
import json
from datetime import datetime
from agno.tools import Toolkit

# Configuração global do logging conforme especificado
logging.basicConfig(
    filename='agent_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LoggerTool(Toolkit):
    def __init__(self):
        super().__init__(name="logger_tool")
        self.register(self.log_agent_activity)

    def log_agent_activity(self, agent_name: str, action: str, details: str) -> str:
        """
        Registra uma atividade de um agente no log de auditoria local.

        Args:
            agent_name (str): O nome do agente realizando a ação.
            action (str): O tipo de ação realizada (ex: "CONSULTA_API", "RESPOSTA_USUARIO").
            details (str): Detalhes específicos da ação.

        Returns:
            str: Confirmação de registro.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "action": action,
            "details": details
        }

        # Serializa para JSON para manter a estrutura dentro da mensagem de log
        logging.info(json.dumps(log_entry, ensure_ascii=False))

        return "Log registrado com sucesso."