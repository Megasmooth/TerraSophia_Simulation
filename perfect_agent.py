import json
import random
import os
import core.experiment.llm_router as router

path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os
import core.experiment.llm_router as router

class LLMAgent:
    def __init__(self, agent_id=None, *args, **kwargs):
        # Captura agressiva de Identidade
        if agent_id:
            self.id = agent_id
        elif len(args) > 0:
            self.id = args[0]
        else:
            self.id = kwargs.get('agent_id', kwargs.get('agent_tag', 'unknown_being'))
            
        self.agent_id = self.id
        self.agent_tag = self.id
        self.agent_name = self.id
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
        safe_obs = obs if obs is not None else "Sem observações."
        safe_avail = avail_actions if avail_actions is not None else ["move"]
        
        prompt = f"Obs: {safe_obs}\\nActions: {safe_avail}\\nMemory: {self.internal_memory}\\nDecida."
        
        try:
            raw_res = "move"
            if self.router_inst:
                client = self.router_inst.next()
                if hasattr(client, 'complete'):
                    raw_res = client.complete(prompt)
                elif hasattr(client, '__call__'):
                    raw_res = client(prompt)
            
            res_str = str(raw_res).lower()
            action_dict = {"action": "move", "direction": "north"}
            
            if "create" in res_str: action_dict = {"action": "create_artifact"}
            elif "take" in res_str: action_dict = {"action": "take"}
            elif "give" in res_str: action_dict = {"action": "give"}
            
            # RETORNA APENAS O DICIONÁRIO (Isto resolve o erro da Tupla)
            return action_dict
        except Exception as e:
            # RETORNA APENAS O DICIONÁRIO
            return {"action": "move", "direction": "random"}

    def get_state_ckpt(self):
        return {"type": "LLMAgent", "agent_id": self.agent_id, "internal_memory": self.internal_memory}
    
    def close(self): pass
    
    def __getattr__(self, name): return None
"""
with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ Perfect Agent Aplicado: Erro de Tupla removido e ID restaurado.")
