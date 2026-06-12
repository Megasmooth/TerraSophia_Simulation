import os
import re

agent_path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os
from core.experiment.llm_router import LLMRouter

class LLMAgent:
    def __init__(self, *args, **kwargs):
        # Captura de Identidade
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', 'unknown_being')
        self.id = self.agent_id
        
        # Configurações de Memória
        self.max_history = 10
        self.internal_memory = ""
        self.history = []
        
        # RESOLUÇÃO DO ERRO: Passando 'model_short' para o LLMRouter
        # O SimulationRunner passa o modelo dentro de kwargs
        model_name = kwargs.get('model', 'llama3')
        try:
            self.router = LLMRouter(model_short=model_name, ports=[11434])
        except TypeError:
            # Fallback caso a classe use argumento posicional em vez de nomeado
            self.router = LLMRouter(model_name, ports=[11434])
        
        # Protocolo de Herança Inata (Rodada 08)
        try:
            seed_path = "core/genome/innate_knowledge_r08.json"
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.internal_memory = random.choice(data)["content"]
        except:
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def select_action(self, obs, avail_actions):
        prompt = f"Obs: {obs}\\nActions: {avail_actions}\\nMemory: {self.internal_memory}\\nDecida a melhor ação."
        
        try:
            # O roteador retorna a instância do cliente via .next()
            client = self.router.next()
            # O motor do TerraSophia costuma usar .complete ou .chat
            if hasattr(client, 'complete'):
                response = client.complete(prompt)
            elif hasattr(client, 'chat'):
                response = client.chat(prompt)
            else:
                # Fallback genérico de chamada
                response = client(prompt)
            return response, False
        except Exception as e:
            return "move random", False

    def close(self):
        pass
"""

with open(agent_path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print(f"✓ {agent_path} ajustado com model_short e instanciamento de roteador.")
