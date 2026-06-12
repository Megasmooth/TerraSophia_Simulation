import os

path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os
import logging
import requests

class LLMAgent:
    def __init__(self, agent_id="unknown", *args, **kwargs):
        if agent_id and agent_id != "unknown": self.id = agent_id
        elif len(args) > 0: self.id = args[0]
        else: self.id = kwargs.get('agent_id', kwargs.get('agent_tag', 'unknown_being'))
            
        self.agent_id, self.agent_tag, self.agent_name = self.id, self.id, self.id
        self.max_history = 10
        self.internal_memory = ""
        self.history = []

        try:
            with open("core/genome/innate_knowledge_r08.json", "r", encoding='utf-8') as f:
                self.internal_memory = random.choice(json.load(f))["content"]
        except: 
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def select_action(self, obs=None, avail_actions=None, **kwargs):
        safe_obs = obs if obs is not None else "Nenhuma."
        safe_avail = avail_actions if avail_actions is not None else ["move"]
        
        prompt = f"Obs: {safe_obs}\\nActions: {safe_avail}\\nMemory: {self.internal_memory}\\nResponda APENAS com uma acao (move, take, give, create) e uma direcao (up, down, left, right)."
        
        raw_res = ""
        try:
            url = "http://localhost:11434/api/generate"
            payload = {"model": "llama3", "prompt": prompt, "stream": False}
            
            # --- A MÁGICA ACONTECE AQUI: 120 Segundos de Tolerância ---
            response = requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 200:
                raw_res = response.json().get("response", "")
            else:
                raw_res = f"Erro HTTP {response.status_code}"
        except Exception as e:
            raw_res = f"Erro de API: {e}"

        res_str = str(raw_res).lower()
        
        print(f"\\n[DIÁLOGO] {self.id} pensou: {raw_res.strip() if raw_res else 'Vazio.'}")
        logging.info(f"[{self.id}] PENSAMENTO: {raw_res.strip()}")
        
        action_name = "move"
        direction = "stay"
        
        if "create" in res_str: action_name = "create_artifact"
        elif "take" in res_str: action_name = "take"
        elif "give" in res_str: action_name = "give"
        
        if "up" in res_str or "north" in res_str: direction = "up"
        elif "down" in res_str or "south" in res_str: direction = "down"
        elif "left" in res_str or "west" in res_str: direction = "left"
        elif "right" in res_str or "east" in res_str: direction = "right"
        
        return {"action": action_name, "args": {"direction": direction}}

    def get_state_ckpt(self):
        return {"type": "LLMAgent", "agent_id": self.agent_id, "internal_memory": self.internal_memory}
    
    def close(self): pass
    def __getattr__(self, name): return None
"""
with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ Cérebro Expandido: Timeout de 120s aplicado com sucesso.")
