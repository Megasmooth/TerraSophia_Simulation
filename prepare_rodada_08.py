import os

def patch_file(filepath, changes):
    if not os.path.exists(filepath):
        print(f"Erro: Arquivo {filepath} não encontrado.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for old, new in changes:
        content = content.replace(old, new)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Sucesso: {filepath} atualizado.")
    else:
        print(f"Aviso: Nenhuma alteração necessária em {filepath} (já ajustado ou padrão não encontrado).")

# Definição das mudanças necessárias
adjustments = {
    # 1. Ajustar o Analisador para usar o provedor local (OpenAI-compatible) e o Llama3
    "analysis_scripts/001_llm_agent_analyser.py": [
        ('LLM_PROVIDER = "anthropic"', 'LLM_PROVIDER = "openai"'),
        ('LLM_MODEL = "claude-sonnet-4-5-20250929"', 'LLM_MODEL = "llama3"')
    ],
    
    # 2. Alterar o modelo padrão da simulação na configuração global
    "core/experiment/config.py": [
        ('default="claude-sonnet-4-6"', 'default="llama3"')
    ],
    
    # 3. Corrigir o Cliente LLM para aceitar URLs locais (Ollama) via variável de ambiente
    # Isso permite que o LLMClient do analisador saiba ONDE está o seu Ollama.
    "core/utils/llm_client.py": [
        ('self._openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))', 
         'self._openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=os.environ.get("OPENAI_BASE_URL"))')
    ]
}

if __name__ == "__main__":
    print("Iniciando preparação da Rodada 08...")
    for path, changes in adjustments.items():
        patch_file(path, changes)
    print("\nConfiguração concluída. Verifique seu arquivo .env para garantir que")
    print("OPENAI_BASE_URL=http://localhost:11434/v1 esteja presente.")