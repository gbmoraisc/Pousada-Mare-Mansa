import json
import os
from datetime import datetime

class LoggerJSON:
    def __init__(self, caminho_arquivo="logs.json"):
        self.caminho = caminho_arquivo
        # Garante que o arquivo exista
        if not os.path.exists(self.caminho):
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def registrar(self, usuario, acao, tela, tipo="INFO"):
        """Adiciona uma nova entrada de log"""
        novo_log = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usuario": usuario,
            "acao": acao,
            "tela": tela,
            "tipo": tipo
        }

        logs = self._carregar_logs()
        logs.append(novo_log)
        self._salvar_logs(logs)

    def _carregar_logs(self):
        """Lê todos os logs existentes"""
        with open(self.caminho, "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar_logs(self, logs):
        """Salva todos os logs no arquivo"""
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)

    def listar_logs(self):
        """Retorna todos os logs (pode ser usado para exibição no sistema)"""
        return self._carregar_logs()
    