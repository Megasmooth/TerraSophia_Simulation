import os

path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os
from core.experiment.llm_router import route_to_llm

class LLMAgent:
    def __init__(self, *args, **kwargs):
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', 'unknown_being')
        self.id = self.agent_id
        self.max_history = 10
        self.internal_memory = ""
        self.history = []
        
        # Carregamento da Semente Synapsys (Innate Knowledge)
        try:
            seed_path = "core/genome/innate_knowledge_r08.json"
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.internal_memory = random.choice(data)["content"]
        except:
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def select_action(self, obs, avail_actions):
        # Esta é a função que estava faltando
        prompt = f"Obs: {obs}\\nActions: {avail_actions}\\nMemory: {self.internal_memory}\\nDecida a melhor ação."
        # Roteia para o Llama 3 via Ollama
        response = route_to_llm(prompt, model="llama3", port=11434)
        return response, False

    def close(self):
        pass
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ Cérebro do LLMAgent restaurado com lógica de decisão.")
