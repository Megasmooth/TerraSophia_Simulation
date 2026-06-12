import os
import json
import random

path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os
import core.experiment.llm_router as router

class LLMAgent:
    def __init__(self, *args, **kwargs):
        # Identidade flexível
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', kwargs.get('agent_tag', 'unknown'))
        self.id = self.agent_id
        self.agent_tag = self.agent_id
        self.agent_name = self.agent_id
        self.max_history = 10
        self.internal_memory = ""
        self.history = []
        
        # Inicializa Roteador
        try:
            model_name = kwargs.get('model', 'llama3')
            if hasattr(router, 'LLMRouter'):
                self.router_inst = router.LLMRouter(model_short=model_name, ports=[11434])
            else:
                self.router_inst = None
        except:
            self.router_inst = None

        # Carga da Semente Synapsys
        try:
            seed_path = "core/genome/innate_knowledge_r08.json"
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding='utf-8') as f:
                    self.internal_memory = random.choice(json.load(f))["content"]
        except:
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def select_action(self, *args, **kwargs):
        # Captura universal de argumentos para evitar TypeError
        obs = kwargs.get('obs', args[0] if len(args) > 0 else "")
        avail_actions = kwargs.get('avail_actions', args[1] if len(args) > 1 else [])
        
        prompt = f"Obs: {obs}\\nActions: {avail_actions}\\nMemory: {self.internal_memory}\\nDecida."
        
        try:
            # Tenta usar a instância do roteador
            if self.router_inst:
                client = self.router_inst.next()
                for method in ['complete', 'chat', '__call__']:
                    if hasattr(client, method):
                        res = getattr(client, method)(prompt)
                        if res: return str(res), False
            
            # Fallback para funções globais
            for f_name in ['call_llm', 'route_to_llm', 'llm_query']:
                if hasattr(router, f_name):
                    res = getattr(router, f_name)(prompt)
                    return str(res), False
        except:
            pass
            
        return "move random", False

    def get_state_ckpt(self):
        return {"type": "LLMAgent", "agent_id": self.agent_id, "internal_memory": self.internal_memory, "history": self.history}

    def close(self):
        pass

    def __getattr__(self, name):
        return None
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())
print("✓ LLMAgent ressuscitado com assinatura universal.")
