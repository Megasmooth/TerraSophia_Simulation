import os
import inspect
import core.experiment.llm_router as router

# Encontra a primeira função no roteador que não seja interna
functions = [name for name, obj in inspect.getmembers(router, inspect.isfunction)]
main_func = functions[0] if functions else None

if main_func:
    print(f"✓ Conector detectado: {main_func}")
    path = 'core/agents/llm_agent.py'
    code = f"""
import json
import random
import os
import core.experiment.llm_router as router

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
        # Chama a função dinamicamente pelo nome detectado
        func = getattr(router, "{main_func}")
        response = func(prompt, model="llama3", port=11434)
        return response, False

    def close(self):
        pass
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code.strip())
    print(f"✓ {path} sincronizado com a função {main_func}.")
else:
    print("✗ Erro: Nenhuma função encontrada em llm_router.py")
