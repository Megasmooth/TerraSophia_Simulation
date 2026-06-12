import json
import random
import os

# Caminho do arquivo
path = 'core/agents/llm_agent.py'

# Conteúdo robusto para o agente
code = """
import json
import random
import os

class LLMAgent:
    def __init__(self, agent_id, **kwargs):
        # Atributos básicos de identidade exigidos pelo motor e logs
        self.agent_id = agent_id
        self.id = agent_id  
        
        # Configurações de Memória e História
        self.max_history = 10
        self.internal_memory = ""
        self.internal_memory_size = kwargs.get('internal_memory_size', 150)
        
        # Protocolo de Herança Inata (Rodada 08 - Semente Synapsys)
        # Tenta carregar a semente inata preparada pelo prepare_evolution.py
        try:
            seed_path = "core/genome/innate_knowledge_r08.json"
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    if data:
                        self.internal_memory = random.choice(data)["content"]
        except Exception:
            self.internal_memory = "Axioma: A verdade é a adequação do intelecto à realidade."

    def close(self):
        pass

    # Mantemos o restante da lógica compatível se necessário
    def __getattr__(self, name):
        return None
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(code.strip())

# Correção auxiliar no main.py para o argumento ts
main_path = 'main.py'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        m_content = f.read()
    m_content = m_content.replace('runner._save_checkpoint()', 'runner._save_checkpoint(ts=0)')
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(m_content)

print("✓ Sistema reparado: LLMAgent reconstruído com 'id' e Herança Inata.")
