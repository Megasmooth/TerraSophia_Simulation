import os
import re

print("Procurando variáveis de metabolismo...")
modificado = False

for root, dirs, files in os.walk('core'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Procura por init_agent_energy e aumenta para 500
            if 'init_agent_energy' in content:
                novo_content = re.sub(r"'init_agent_energy':\s*\d+", "'init_agent_energy': 500", content)
                novo_content = re.sub(r"init_agent_energy\s*=\s*\d+", "init_agent_energy = 500", novo_content)
                
                if novo_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(novo_content)
                    print(f"✓ Energia inicial aumentada para 500 em: {path}")
                    modificado = True

if not modificado:
    print("Aviso: Variável de energia não encontrada diretamente, usaremos parâmetros de linha de comando.")
