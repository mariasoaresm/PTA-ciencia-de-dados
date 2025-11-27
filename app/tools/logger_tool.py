import logging
import json
from datetime import datetime

# Configura o logger para salvar em um arquivo chamado 'agent_audit.log'
# Isso cria um arquivo físico que você pode abrir e mostrar para o cliente.
logging.basicConfig(
    filename='agent_audit.log',
    level=logging.INFO,
    format='%(message)s'
)

class AuditLogger:
    @staticmethod
    def log_event(request_id: str, agent_name: str, action: str, details: dict):
        """
        Registra cada passo do Agente para auditoria.
        
        Args:
            request_id: O ID único da conversa.
            agent_name: Quem fez a ação (ex: agent_home_decor).
            action: O que ele fez (ex: "SQL_QUERY", "RESPONSE_GENERATED").
            details: O conteúdo (ex: o SQL exato que foi rodado).
        """

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id,
            "agent": agent_name,
            "action": action,
            "details": details
        }

        # Converte para o texto JSON  e salva no arquivo de log
        log_message = json.dumps(log_entry, ensure_ascii=False)
        logging.info(log_message)

        # Mostra no terminal também para ver em tempo real
        print(f"📝 [AuditLogger] {agent_name} -> {action}")