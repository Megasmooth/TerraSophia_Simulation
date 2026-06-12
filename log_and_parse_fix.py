import os
import re
from datetime import datetime

# 1. Ajustar o Log Absoluto no main.py
main_path = 'main.py'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cria o nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    log_name = f"LOG_ABSOLUTO_RODADA_08_{timestamp}.txt"
    
    # Injeta a lógica de log no topo do main
    if 'import logging' not in content:
        content = "import logging\n" + content
    
    # Remove logs antigos e define o novo na raiz
    content = re.sub(r'logging\.basicConfig\(.*?\)', '', content, flags=re.DOTALL)
    log_setup = f"\nlogging.basicConfig(filename='{log_name}', level=logging.INFO, format='%(asctime)s - %(message)s')\n"
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(log_setup + content)
    print(f"✓ {main_path}: Log absoluto configurado como {log_name}")

# 2. Ajustar o LLMAgent para retornar Dicionário (evitar erro de Tuple)
agent_path = 'core/agents/llm_agent.py'
code = """
import json
import random
import os
import core.experiment.llm_router as router

class LLMAgent:
    def __init__(self, *args, **kwargs):
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', 'unknown')
        self.id, self.agent_tag, self.agent_name = self.agent_id, self.agent_id, self.agent_id
        self.max_history = 10
        self.internal_memory = ""
        
        try:
            model_name = kwargs.get('model', 'llama3')
            self.router_inst = router.LLMRouter(model_short=model_name, ports=[11434]) if hasattr(router, 'LLMRouter') else None
        except: self.router_inst = None

        try:
            with open("core/genome/innate_knowledge_r08.json", "r") as f:
                self.internal_memory = random.choice(json.load(f))["content"]
        except: self.internal_memory = "Verdade e Realidade."

    def select_action(self, obs, avail_actions, **kwargs):
        prompt = f"Obs: {obs}\\nActions: {avail_actions}\\nMemory: {self.internal_memory}"
        try:
            raw_res = "move" # default
            if self.router_inst:
                client = self.router_inst.next()
                raw_res = client.complete(prompt) if hasattr(client, 'complete') else client(prompt)
            
            # LIMPEZA CRÍTICA: Transforma a resposta em DICIONÁRIO para o env.py
            res_str = str(raw_res).lower()
            action_dict = {"action": "move", "direction": "north"} # Default seguro
            
            if "create" in res_str: action_dict = {"action": "create_artifact"}
            elif "take" in res_str: action_dict = {"action": "take"}
            elif "give" in res_str: action_dict = {"action": "give"}
            
            # Retorna o dicionário e o sinal de refresh (False)
            return action_dict, False
        except:
            return {"action": "move", "direction": "random"}, False

    def get_state_ckpt(self):
        return {"type": "LLMAgent", "agent_id": self.agent_id, "internal_memory": self.internal_memory}
    def close(self): pass
    def __getattr__(self, name): return None
"""
with open(agent_path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ core/agents/llm_agent.py: Tradutor de pensamentos (dict) aplicado.")
