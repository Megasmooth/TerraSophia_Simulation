import os

def patch_llm_agent():
    path = "core/agents/llm_agent.py"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        new_lines.append(line)
        # Injeta o atributo 'id' logo após o 'agent_id' no __init__
        if 'self.agent_id = agent_id' in line:
            new_lines.append('        self.id = agent_id  # Atributo exigido pelo llm_utils\n')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("✓ core/agents/llm_agent.py: Atributo 'id' adicionado.")

def patch_main():
    path = "main.py"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corrige a chamada de salvamento de emergência no bloco except do main.py
    # Mudamos para passar o ts=0 ou o ts atual se disponível
    old_call = "runner._save_checkpoint()"
    new_call = "runner._save_checkpoint(ts=0)"
    
    if old_call in content:
        content = content.replace(old_call, new_call)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ main.py: Chamada _save_checkpoint(ts=0) corrigida.")

patch_llm_agent()
patch_main()
