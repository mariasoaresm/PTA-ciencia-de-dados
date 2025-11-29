import json
import os
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from agno.tools import Toolkit

class LoggerTool(Toolkit):
    def __init__(self, base_evidence_path: str = "evidence"):
        super().__init__(name="logger_tool")
        
        # Garante caminho absoluto seguro
        cwd = os.getcwd()
        if cwd.endswith("app") or cwd.endswith("tools"):
            cwd = os.path.dirname(os.path.dirname(cwd))
        
        self.base_path = os.path.join(cwd, "evidence")
        self.register(self.log_execution)

    def log_execution(self, 
                      agent_name: str, 
                      user_query: str, 
                      response_text: str, 
                      sources: Optional[Union[List[Dict], List[str], str]] = None,
                      inconsistency_flag: bool = False,
                      latency_ms: float = 0.0) -> str:
        """
        Registra a execução do agente de forma defensiva e estruturada.
        
        Args:
            sources: Aceita formatos variados para evitar crash (List[Dict], List[str] ou str).
        """
        try:
            # 1. Geração de IDs e Timestamp
            request_id = str(uuid.uuid4())
            now = datetime.now()
            timestamp = now.isoformat()

            # 2. Definição do Caminho (S3 Style)
            folder_path = os.path.join(
                self.base_path,
                str(now.year),
                f"{now.month:02d}",
                f"{now.day:02d}",
                request_id
            )
            os.makedirs(folder_path, exist_ok=True)

            # 3. Sanitização Defensiva de Sources
            safe_sources: List[Dict[str, Any]] = []
            
            if sources:
                if isinstance(sources, list):
                    for s in sources:
                        if isinstance(s, dict):
                            safe_sources.append(s)
                        elif isinstance(s, str):
                            # Se vier string solta na lista, encapsula
                            safe_sources.append({"type": "UNKNOWN", "content": s})
                elif isinstance(sources, str):
                    # Se o agente enviou uma string em vez de lista
                    safe_sources.append({"type": "TEXT", "content": sources})

            # 4. Lógica de QA (Inconsistency Flag)
            inconsistency_flag = False
            source_types = [str(s.get('type', '')).upper() for s in safe_sources]
            if 'DW' in source_types and 'PDF' in source_types:
                inconsistency_flag = True

            # 5. Payload Estruturado
            log_payload = {
                "metadata": {
                    "id": request_id,
                    "timestamp": timestamp,
                    "agent": agent_name,
                    "latency_ms": latency_ms,
                    "environment": os.getenv("ENV", "dev"),
                    "model": "llama-3.3-70b-versatile" # Metadado exigido
                },
                "interaction": {
                    "input": user_query,
                    "output": response_text
                },
                "evidence": {
                    "raw_sources": safe_sources,
                    "qa_flags": {
                        "inconsistency_detected": inconsistency_flag,
                        "source_count": len(safe_sources)
                    }
                }
            }

            # 6. Persistência Atômica
            file_path = os.path.join(folder_path, "log.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(log_payload, f, indent=2, ensure_ascii=False)
            
            print(f"📝 [AUDIT SUCCESS] Log ID: {request_id} | Path: {file_path}")
            return f"Log registrado com sucesso. ID de auditoria: {request_id}"

        except Exception as e:
            # Fallback de emergência: Nunca deixa o agente falhar por causa de log
            error_msg = f"Falha interna no Logger: {str(e)}"
            print(f"❌ [LOG CRASH] {error_msg}")
            return json.dumps({"status": "LOGging_FAILED", "error": error_msg})