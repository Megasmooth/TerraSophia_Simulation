import os
import re

def fix_agent():
    path = "core/agents/llm_agent.py"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Garante o atributo 'id' e 'max_history' no init
    if "self.id =" not in content:
        content = re.sub(r"(self\.agent_id\s*=\s*agent_id)", r"\1\n        self.id = agent_id\n        self.max_history = 10", content)
    
    # Garante o método close
    if "def close" not in content:
        content += "\n    def close(self):\n        pass\n"
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ LLMAgent: id, max_history e close reparados.")

def fix_main():
    path = "main.py"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Conserta a chamada de salvamento no erro
    content = content.replace("runner._save_checkpoint()", "runner._save_checkpoint(ts=0)")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ main.py: Salvamento de emergência reparado.")

def fix_ffmpeg():
    path = "core/utils/generic.py"
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Evita que o FFmpeg mate o processo se não houver imagens
    if "check=True" in content:
        content = content.replace("check=True", "check=False")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ generic.py: FFmpeg blindado contra pastas vazias.")

fix_agent()
fix_main()
fix_ffmpeg()
