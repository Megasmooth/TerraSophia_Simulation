import os
from datetime import datetime

main_path = 'main.py'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove qualquer linha de log mal posicionada
    clean_lines = [line for line in lines if 'import logging' not in line and 'logging.basicConfig' not in line]
    
    # Prepara o cabeçalho correto
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = f"LOG_ABSOLUTO_RODADA_08_{timestamp}.txt"
    
    header = [
        "import logging\n",
        f"logging.basicConfig(filename='{log_name}', level=logging.INFO, format='%(asctime)s - %(message)s')\n"
    ]
    
    # Escreve o arquivo com a ordem perfeita
    with open(main_path, 'w', encoding='utf-8') as f:
        f.writelines(header + clean_lines)
    
    print(f"✓ main.py corrigido! Importações ordenadas. Log: {log_name}")
