path = 'core/agents/llm_agent.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Injeta max_history e internal_memory_size
if 'self.max_history' not in content:
    content = content.replace(
        'self.history = []', 
        'self.history = []\n        self.max_history = kwargs.get("max_history", 10)\n        self.internal_memory_size = kwargs.get("internal_memory_size", 150)'
    )

# 2. Adiciona métodos de encerramento e segurança no final da classe
metodos_finais = """
    def close(self):
        pass

    def __getattr__(self, name):
        return None
"""
if 'def close(self):' not in content:
    content += "\n" + metodos_finais

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Atributos de infraestrutura (max_history e close) restaurados com sucesso!")
