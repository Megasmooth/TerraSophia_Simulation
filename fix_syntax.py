path = 'core/agents/llm_agent.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Substitui as linhas problemáticas por strings com aspas simples (sem conflito)
linha_velha_1 = 'raw_res = f"PENSAMENTO: Erro interno HTTP. ACAO: {{"action": "move", "args": {{"direction": "stay"}}}}"'
linha_nova_1 = 'raw_res = \'PENSAMENTO: Erro interno HTTP. ACAO: {"action": "move", "args": {"direction": "stay"}}\''

linha_velha_2 = 'raw_res = f"PENSAMENTO: Custo cognitivo excedido (Timeout). ACAO: {{"action": "move", "args": {{"direction": "stay"}}}}"'
linha_nova_2 = 'raw_res = \'PENSAMENTO: Custo cognitivo excedido (Timeout). ACAO: {"action": "move", "args": {"direction": "stay"}}\''

text = text.replace(linha_velha_1, linha_nova_1)
text = text.replace(linha_velha_2, linha_nova_2)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("✓ Erro de Sintaxe curado!")
