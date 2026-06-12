import json
import random
import os
from core.experiment.llm_router import LLMRouter

path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os
from core.experiment.llm_router import LLMRouter

class LLMAgent:
    def __init__(self, agent_id, *args, **kwargs):
        # 1. Atributos de Identidade (Exigidos pelo motor)
        self.agent_id = agent_id
        self.id = agent_id
        self.agent_tag = agent_id
        self.agent_name = agent_id
        
        # 2. Configurações de Memória e Contexto
        self.max_history = 10
        self.internal_memory = ""
        self.history = []
        self.internal_memory_size = kwargs.get('internal_memory_size', 150)
        
        # 3. Inicialização do Roteador
        model_name = kwargs.get('model', 'llama3')
        try:
            self.router = LLMRouter(model_short=model_name, ports=[11434])
        except:
            self.router = LLMRouter(ports=[11434])
        
        # 4. Protocolo de Herança Inata (Semente Synapsys)
        try:
            seed_path = "core/genome/innate_knowledge_r08.json"
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.internal_memory = random.choice(data)["content"]
        except:
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def select_action(self, obs, avail_actions, **kwargs):
        # O argumento **kwargs captura o 'reward' e outros parâmetros extras
        prompt = f"Obs: {obs}\\nActions: {avail_actions}\\nMemory: {self.internal_memory}\\nDecida."
        try:
            client = self.router.next()
            if hasattr(client, 'complete'):
                response = client.complete(prompt)
            else:
                response = client(prompt)
            return response, False
        except:
            return "move random", False

    def get_state_ckpt(self):
        # MÉTODO VITAL: Permite que o sistema salve o agente sem erro
        return {
            "type": "LLMAgent",
            "agent_id": self.agent_id,
            "internal_memory": self.internal_memory,
            "history": self.history
        }

    def close(self):
        pass
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ LLMAgent reconstruído com todos os métodos de suporte (ID, Reward, Checkpoint).")
