import os

def patch_file(path, search_text, replacement_text):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if search_text in content and replacement_text not in content:
            new_content = content.replace(search_text, replacement_text)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ {path} corrigido.")
        else:
            print(f"ℹ {path} já parece estar correto ou o alvo não foi encontrado.")

# 1. Corrigir LLMAgent (max_history e close)
agent_path = "core/agents/llm_agent.py"
if os.path.exists(agent_path):
    with open(agent_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        new_lines.append(line)
        # Adiciona max_history no __init__
        if 'self.internal_memory = ""' in line:
            new_lines.append('        self.max_history = 10  # Limite de memória para o contexto\n')
    
    # Adiciona o método close se não existir
    content = "".join(new_lines)
    if "def close(self):" not in content:
        content += "\n    def close(self):\n        pass\n"
    
    with open(agent_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {agent_path} (max_history e close) corrigido.")

# 2. Corrigir main.py (save_checkpoint -> _save_checkpoint)
patch_file("main.py", "runner.save_checkpoint()", "runner._save_checkpoint()")

