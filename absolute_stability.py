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
    def __init__(self, *args, **kwargs):
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', 'unknown')
        self.id = self.agent_id
        self.agent_tag = self.agent_id
        self.agent_name = self.agent_id
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

    # A ASSINATURA EXATA QUE O llm_utils.py ESPERA:
    def select_action(self, obs, avail_actions, **kwargs):
        prompt = f"Obs: {obs}\\nActions: {avail_actions}\\nMemory: {self.internal_memory}\\nDecida."
        
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
            
            return action_dict, False
        except Exception as e:
            return {"action": "move", "direction": "random"}, False

    def get_state_ckpt(self):
        return {"type": "LLMAgent", "agent_id": self.agent_id, "internal_memory": self.internal_memory}
    
    def close(self): pass
    
    def __getattr__(self, name): return None
"""
with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ Assinatura exata do select_action() restaurada.")
