path = 'core/agents/llm_agent.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substitui o escudo cego por um escudo que conhece os nomes
old_getattr = "def __getattr__(self, name): return None"
new_getattr = """def __getattr__(self, name):
        if name in ['id', 'name', 'agent_name', 'agent_id', 'agent_tag']:
            return getattr(self, 'agent_tag', 'Unknown')
        return None"""

content = content.replace(old_getattr, new_getattr)

# Força o mapeamento de ID no __init__
if "self.id = self.agent_name" not in content:
    content = content.replace(
        "self.agent_name = kwargs.get('agent_id', agent_name)",
        "self.agent_name = kwargs.get('agent_id', agent_name) or agent_tag\n        self.id = self.agent_name\n        self.name = self.agent_name\n        self.agent_id = self.agent_name"
    )

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Nomes e identidades restaurados para o logger!")
