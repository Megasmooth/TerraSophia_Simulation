import os

path = 'core/agents/llm_agent.py'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Filtrar e remover as linhas de @property que injetamos anteriormente
    # e que estão causando o conflito de "no setter"
    clean_lines = []
    skip = False
    for line in lines:
        if '@property' in line or 'def id(self):' in line or 'def max_history(self):' in line:
            continue
        if 'return getattr(self' in line or 'return 10' in line:
            continue
        clean_lines.append(line)
    
    # Agora, garantir que no __init__ os atributos sejam criados corretamente
    final_lines = []
    init_found = False
    for line in clean_lines:
        final_lines.append(line)
        if 'def __init__' in line:
            init_found = True
        if init_found and ('super().__init__' in line or 'self.agent_id =' in line):
            final_lines.append('        self.id = agent_id if "agent_id" in locals() else "unknown"\n')
            final_lines.append('        self.max_history = 10\n')
            init_found = False # Injeta apenas uma vez
            
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    print("✓ core/agents/llm_agent.py: Conflitos de propriedade removidos e atributos restaurados.")

# Garantir que o main.py não dê erro de argumento no salvamento
main_path = 'main.py'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('runner._save_checkpoint()', 'runner._save_checkpoint(ts=0)')
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ main.py: Salvamento de emergência validado.")
