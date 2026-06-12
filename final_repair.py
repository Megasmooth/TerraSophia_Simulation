import os

path = 'core/agents/llm_agent.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    init_found = False
    for line in lines:
        new_lines.append(line)
        # Procura o início do método __init__
        if 'def __init__' in line:
            init_found = True
        
        # Injeta os atributos logo após o início do __init__ para garantir que existam
        if init_found and 'super()' in line:
            new_lines.append('        self.id = getattr(self, "agent_id", "unknown")\n')
            new_lines.append('        self.max_history = 10\n')
            init_found = False # Garante que só injete uma vez
            
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("✓ core/agents/llm_agent.py: Atributos 'id' e 'max_history' injetados com sucesso.")

# Correção do main.py para aceitar o checkpoint de emergência sem erro de argumento
main_path = 'main.py'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('runner._save_checkpoint()', 'runner._save_checkpoint(ts=0)')
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ main.py: Salvamento de emergência corrigido.")
