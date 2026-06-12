import os
import re

router_path = 'core/experiment/llm_router.py'
agent_path = 'core/agents/llm_agent.py'

# 1. Descobrir o nome da função no roteador
func_name = 'call_llm' # fallback padrão
if os.path.exists(router_path):
    with open(router_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'def\s+(\w+)\s*\(.*prompt', content)
        if match:
            func_name = match.group(1)
            print(f"✓ Função de roteamento detectada: {func_name}")

# 2. Reconstruir o LLMAgent com o import correto
code = f"""
import json
import random
import os
from core.experiment.llm_router import {func_name}

class LLMAgent:
    def __init__(self, *args, **kwargs):
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', 'unknown_being')
        self.id = self.agent_id
        self.max_history = 10
        self.internal_memory = ""
        self.history = []
        
        try:
            seed_path = "core/genome/innate_knowledge_r08.json"
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.internal_memory = random.choice(data)["content"]
        except:
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def select_action(self, obs, avail_actions):
        prompt = f"Obs: {{obs}}\\nActions: {{avail_actions}}\\nMemory: {{self.internal_memory}}\\nDecida a melhor ação."
        # Usa a função detectada automaticamente
        response = {func_name}(prompt, model="llama3", port=11434)
        return response, False

    def close(self):
        pass
"""

with open(agent_path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print(f"✓ {agent_path} reconstruído com sucesso.")
