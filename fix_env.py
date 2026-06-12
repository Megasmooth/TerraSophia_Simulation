import re

path = 'core/environment/env.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def remove_duplicate_agents_ref(match):
    prefix = match.group(1)    # 'def nome_da_funcao('
    args_content = match.group(2) # Todo o conteúdo entre os parênteses
    suffix = match.group(3)    # '):'
    
    if args_content.count('agents_ref') > 1:
        # Divide os argumentos por vírgula
        args = args_content.split(',')
        new_args = []
        found = False
        for a in args:
            if 'agents_ref' in a:
                if not found:
                    # Mantém apenas a primeira ocorrência (que costuma ter o tipo)
                    new_args.append(a)
                    found = True
                # Ignora as ocorrências subsequentes de agents_ref
            else:
                new_args.append(a)
        return prefix + ",".join(new_args) + suffix
    return match.group(0)

# Expressão regular para capturar definições de função multi-linha
# Procura por 'def', nome, '(', conteúdo, e finaliza em '):'
pattern = r'(def\s+\w+\s*\()([\s\S]*?)(\)\s*:)'
fixed_content = re.sub(pattern, remove_duplicate_agents_ref, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)
print("✓ core/environment/env.py: Função limpa de argumentos duplicados.")
