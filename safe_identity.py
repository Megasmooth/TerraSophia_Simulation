path = 'core/agents/llm_agent.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Troca o causador do loop infinito pela busca segura no dicionário
bad_code = "return getattr(self, 'agent_tag', 'Unknown')"
good_code = "return self.__dict__.get('agent_tag', 'Unknown')"

content = content.replace(bad_code, good_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✓ Loop infinito curado. Identidade blindada!")
