import os
import re

router_path = 'core/experiment/llm_router.py'
agent_path = 'core/agents/llm_agent.py'

# 1. Descobrir o nome da CLASSE no roteador
class_name = 'LLMRouter' # padrão esperado
if os.path.exists(router_path):
    with open(router_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'class\s+(\w+)', content)
        if match:
            class_name = match.group(1)
            print(f"✓ Classe de roteamento detectada: {class_name}")

# 2. Reconstruir o LLMAgent usando a Classe
code = f"""
import json
import random
import os
from core.experiment.llm_router import {class_name}

class LLMAgent:
    def __init__(self, *args, **kwargs):
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', 'unknown_being')
        self.id = self.agent_id
        self.max_history = 10
        self.internal_memory = ""
        self.history = []
        
        # Instancia o roteador dentro do agente
        # Passamos a porta 11434 que é o seu padrão do Ollama
        self.router = {class_name}(ports=[11434])
        
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
        
        # O método .next() retorna o cliente/conexão
        # O .complete ou .chat envia o prompt
        try:
            client = self.router.next()
            # Tentamos o método complete que é o padrão do TerraSophia
            response = client.complete(prompt)
            return response, False
        except Exception as e:
            return "move random", False

    def close(self):
        pass
"""

with open(agent_path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print(f"✓ {agent_path} sincronizado com a classe {class_name}.")
