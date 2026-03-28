# core/utils/synapsys_manager.py
import pandas as pd
import random
from pathlib import Path

class SynapsysManager:
    def __init__(self, base_path: str = "data/synapsys"):
        self.base_path = Path(base_path)
        self.jornada = self._load_csv("BancoDeDados_Clarity - Jornada.csv")
        self.arsenal = self._load_csv("BancoDeDados_Clarity - Arsenal_Municoes.csv")
        
    def _load_csv(self, filename: str):
        path = self.base_path / filename
        if not path.exists():
            print(f"[ERRO] Ficheiro não encontrado: {path}")
            return None
        return pd.read_csv(path)

    def get_poison(self):
        """Retorna uma falácia/veneno aleatório para o Sofista."""
        if self.arsenal is not None:
            row = self.arsenal.sample(n=1).iloc[0]
            return {
                "id": row['municao_id'],
                "texto": row['afirmacao_veneno'],
                "tipo": "veneno"
            }
        return {"texto": "Ruído genérico sofista.", "id": "0"}

    def get_truth(self, poison_id=None):
        """Retorna a refutação/verdade correspondente ou uma lição da Jornada."""
        if poison_id and self.arsenal is not None:
            # Tenta encontrar a refutação específica para aquele veneno
            refutation = self.arsenal[self.arsenal['municao_id'] == poison_id]
            if not refutation.empty:
                row = refutation.iloc[0]
                return {
                    "id": row['municao_id'],
                    "texto": f"Refutação: {row['refutacao_ponto1']}. Pergunta: {row['pergunta_bisturi']}",
                    "tipo": "trivium"
                }
        
        # Se não houver veneno específico, dá uma lição geral da Jornada
        if self.jornada is not None:
            row = self.jornada.sample(n=1).iloc[0]
            return {
                "id": row['Jornada_id'],
                "texto": row['content'][:200], # Resumo da lição
                "tipo": "jornada"
            }
        return {"texto": "Verdade genérica do Trivium.", "id": "0"}