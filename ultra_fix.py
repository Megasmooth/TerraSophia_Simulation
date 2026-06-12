import os

def patch_file(path, search_pattern, replacement):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if search_pattern in content:
            new_content = content.replace(search_pattern, replacement)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ {path} corrigido.")

# 1. Injeta 'id' e 'max_history' como propriedades na classe LLMAgent
agent_path = "core/agents/llm_agent.py"
if os.path.exists(agent_path):
    with open(agent_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Adiciona as propriedades ao final da classe para evitar erros de indentação
    lines.append("\n    @property\n    def id(self):\n        return getattr(self, 'agent_id', 'unknown')\n")
    lines.append("\n    @property\n    def max_history(self):\n        return 10\n")
    
    with open(agent_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"✓ {agent_path}: Propriedades 'id' e 'max_history' injetadas.")

# 2. Corrige a chamada de salvamento no main.py
patch_file("main.py", "runner._save_checkpoint()", "runner._save_checkpoint(ts=0)")

# 3. Impede que o erro de vídeo (FFmpeg) derrube a simulação
patch_file("core/utils/generic.py", "subprocess.run(cmd, check=True)", "subprocess.run(cmd, check=False)")

