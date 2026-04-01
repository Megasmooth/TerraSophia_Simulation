import os
import re
import csv
import json
import requests

# ==========================================
# CONFIGURAÇÕES DO AMBIENTE
# ==========================================
PASTA_LOGS = "logs_para_analise"
ARQUIVO_SAIDA = "analise_epistemologica_rodada08.csv"
MODELO_OLLAMA = "llama3"
OLLAMA_URL = "http://localhost:11434/api/generate"

PROMPT_SISTEMA = """
Você é um Extrator de Dados Epistemológicos. Analise o log bruto abaixo e extraia os dados em formato JSON estrito.
NÃO ESCREVA NENHUM TEXTO ALÉM DO JSON. NÃO USE MARKDOWN (```json).
Regras:
1. "estado_cognitivo": Resuma a intenção em até 2 frases. (Evite usar aspas duplas dentro do texto).
2. "friccao_brandolini": Responda apenas "Sim" se ele mencionou Sofista, Erudito, Verdade, Fácil ou Difícil. Caso contrário, "Não".
3. "acao_executada": Apenas o nome da ação e os argumentos (ex: move (up)).

Formato de saída obrigatório:
{
    "estado_cognitivo": "...",
    "friccao_brandolini": "...",
    "acao_executada": "..."
}
"""

def extrair_blocos_de_texto(caminho_arquivo):
    """Lê o arquivo .txt e separa cada turno de pensamento do agente."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    padrao = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - \[(being\d+) \| ([A-Z_]+)\].*?(?=\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - \[|\Z)"
    blocos = re.findall(padrao, conteudo, re.DOTALL)
    
    dados_estruturados = []
    for bloco in blocos:
        timestamp, id_agente, fenotipo = bloco[0], bloco[1], bloco[2]
        texto_completo = re.search(f"{timestamp}.*?(?={timestamp}|\Z)", conteudo, re.DOTALL)
        texto_bruto = texto_completo.group(0) if texto_completo else ""
        
        dados_estruturados.append({
            "timestamp": timestamp,
            "id_agente": id_agente,
            "fenotipo": fenotipo,
            "texto_bruto": texto_bruto
        })
    return dados_estruturados

def consultar_ollama(texto_bruto):
    """Envia o log para a IA local processar semanticamente com tolerância a falhas."""
    prompt_completo = f"{PROMPT_SISTEMA}\n\nLOG BRUTO PARA ANÁLISE:\n{texto_bruto}"
    
    payload = {
        "model": MODELO_OLLAMA,
        "prompt": prompt_completo,
        "stream": False,
        "format": "json"
    }
    
    try:
        resposta = requests.post(OLLAMA_URL, json=payload)
        resposta.raise_for_status()
        resultado_bruto = resposta.json()['response']
        
        # FILTRO DE LIMPEZA: Garante que vamos pegar apenas o que está entre chaves {}
        match = re.search(r'\{.*\}', resultado_bruto, re.DOTALL)
        if match:
            json_limpo = match.group(0)
        else:
            json_limpo = resultado_bruto
            
        return json.loads(json_limpo)
        
    except json.JSONDecodeError:
        # Se o Llama alucinar aspas ou quebrar o JSON, não paramos o script.
        return {
            "estado_cognitivo": "FALHA DE FORMATAÇÃO DA IA (Verificar txt original)", 
            "friccao_brandolini": "-", 
            "acao_executada": "-"
        }
    except Exception as e:
        return {"estado_cognitivo": f"ERRO DE CONEXÃO: {str(e)}", "friccao_brandolini": "ERRO", "acao_executada": "ERRO"}

def executar_extracao():
    print(f"--- Iniciando Extração Epistemológica via IA ({MODELO_OLLAMA}) ---")
    
    if not os.path.exists(PASTA_LOGS):
        os.makedirs(PASTA_LOGS)
        return

    arquivos = [f for f in os.listdir(PASTA_LOGS) if f.endswith('.txt')]
    if not arquivos:
        print(f"Nenhum arquivo .txt encontrado.")
        return

    with open(ARQUIVO_SAIDA, 'w', newline='', encoding='utf-8') as csvfile:
        campos = ['Timestamp', 'Arquivo_Origem', 'ID_Agente', 'Fenotipo', 'Estado_Cognitivo', 'Friccao_Brandolini', 'Acao_Executada']
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()

        for arquivo in arquivos:
            caminho = os.path.join(PASTA_LOGS, arquivo)
            print(f"\nLendo arquivo: {arquivo}...")
            blocos = extrair_blocos_de_texto(caminho)
            
            for i, bloco in enumerate(blocos):
                print(f"  -> Processando {bloco['id_agente']} ({i+1}/{len(blocos)})...", end=" ")
                analise_ia = consultar_ollama(bloco['texto_bruto'])
                
                writer.writerow({
                    'Timestamp': bloco['timestamp'],
                    'Arquivo_Origem': arquivo,
                    'ID_Agente': bloco['id_agente'],
                    'Fenotipo': bloco['fenotipo'],
                    'Estado_Cognitivo': analise_ia.get('estado_cognitivo', ''),
                    'Friccao_Brandolini': analise_ia.get('friccao_brandolini', ''),
                    'Acao_Executada': analise_ia.get('acao_executada', '')
                })
                # Força a gravação no disco a cada linha para não perder dados se a luz cair
                csvfile.flush() 
                print("OK.")
                
    print(f"\n--- Extração Finalizada! CSV salvo com sucesso. ---")

if __name__ == "__main__":
    executar_extracao()