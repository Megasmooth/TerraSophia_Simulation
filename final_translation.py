import os
import json
import random

path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os
import core.experiment.llm_router as router
import logging

class LLMAgent:
    def __init__(self, agent_id="unknown", *args, **kwargs):
        self.agent_id = agent_id
        self.id = agent_id
        self.agent_tag = agent_id
        self.agent_name = agent_id
        self.max_history = 10
        self.internal_memory = ""
        self.history = []
        
        try:
            model_name = kwargs.get('model', 'llama3')
            self.router_inst = router.LLMRouter(model_short=model_name, ports=[11434]) if hasattr(router, 'LLMRouter') else None
        except: 
            self.router_inst = None

        try:
            with open("core/genome/innate_knowledge_r08.json", "r", encoding='utf-8') as f:
                self.internal_memory = random.choice(json.load(f))["content"]
        except: 
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def select_action(self, obs=None, avail_actions=None, **kwargs):
        safe_obs = obs if obs is not None else "Nenhuma."
        safe_avail = avail_actions if avail_actions is not None else ["move"]
        
        prompt = f"Obs: {safe_obs}\\nActions: {safe_avail}\\nMemory: {self.internal_memory}\\nResponda apenas com a acao desejada e uma direcao (up, down, left, right)."
        
        try:
            raw_res = ""
            if self.router_inst:
                client = self.router_inst.next()
                if hasattr(client, 'complete'):
                    raw_res = client.complete(prompt)
                elif hasattr(client, '__call__'):
                    raw_res = client(prompt)
            
            res_str = str(raw_res).lower()
            
            # --- LOG NARRATIVO PARA A TESE ---
            print(f"\\n[DIÁLOGO] {self.agent_id} pensou: {raw_res.strip()}")
            logging.info(f"{self.agent_id} DECIDIU: {raw_res.strip()}")
            # ---------------------------------
            
            # --- TRADUÇÃO ESTRITA PARA O MOTOR ---
            # O motor exige: {'action': 'move', 'args': {'direction': 'down'}}
            action_name = "move"
            direction = "stay"
            
            if "create" in res_str: action_name = "create_artifact"
            elif "take" in res_str: action_name = "take"
            elif "give" in res_str: action_name = "give"
            
            if "up" in res_str or "cima" in res_str or "north" in res_str: direction = "up"
            elif "down" in res_str or "baixo" in res_str or "south" in res_str: direction = "down"
            elif "left" in res_str or "esquerda" in res_str or "west" in res_str: direction = "left"
            elif "right" in res_str or "direita" in res_str or "east" in res_str: direction = "right"
            
            action_dict = {"action": action_name, "args": {"direction": direction}}
            return action_dict, False
            
        except Exception as e:
            print(f"[ERRO TRADUÇÃO] {self.agent_id}: {e}")
            return {"action": "move", "args": {"direction": "stay"}}, False

    def get_state_ckpt(self):
        return {"type": "LLMAgent", "agent_id": self.agent_id, "internal_memory": self.internal_memory}
    
    def close(self): pass
    def __getattr__(self, name): return None
"""
with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ Tradutor Perfeito e Log de Diálogo aplicados.")
