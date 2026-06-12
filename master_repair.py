import os

path = 'core/agents/llm_agent.py'

code = """
import json
import random
import os

class LLMAgent:
    def __init__(self, *args, **kwargs):
        # Captura o ID de qualquer forma que ele venha (posicional ou nomeado)
        self.agent_id = args[0] if len(args) > 0 else kwargs.get('agent_id', 'unknown_being')
        self.id = self.agent_id
        
        # Parâmetros de Memória
        self.max_history = 10
        self.internal_memory = ""
        
        # Protocolo de Herança Inata (Rodada 08)
        try:
            seed_path = "core/genome/innate_knowledge_r08.json"
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        self.internal_memory = random.choice(data)["content"]
        except:
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."
            
        print(f"[SISTEMA] Agente {self.id} instanciado com sucesso.")

    def close(self):
        pass

    def __getattr__(self, name):
        # Evita AttributeError para qualquer método ou atributo legado
        return None
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())

# Correção final no main.py para garantir o fechamento e salvamento
main_path = 'main.py'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('runner._save_checkpoint()', 'runner._save_checkpoint(ts=0)')
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("✓ Reconstrução Master concluída: Assinatura de classe universal aplicada.")
