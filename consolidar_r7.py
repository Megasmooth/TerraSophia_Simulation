import json
import glob
import os

def consolidar_experiencia(log_path, output_file):
    print(f"Lendo logs da Rodada 07 em: {log_path}")
    memorias_elite = []
    
    # Busca os logs dos agentes
    pattern = os.path.join(log_path, "agent_logs", "being_*.jsonl")
    agent_logs = glob.glob(pattern)
    
    if not agent_logs:
        print(f"Erro: Nenhum log encontrado em {pattern}")
        return

    for log_file in agent_logs:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines: continue
                
                # Pega o último estado registrado do agente
                last_entry = json.loads(lines[-1])
                lifespan = last_entry.get("observation", {}).get("timestep", 0)
                
                # Critério de resiliência: sobreviveu ao primeiro ciclo de Han (>300 turnos)
                if lifespan > 300:
                    agent_name = os.path.basename(log_file).replace(".jsonl", "")
                    memoria = last_entry.get("internal_memory", "")
                    
                    if memoria:
                        memorias_elite.append({
                            "ancestral": agent_name,
                            "content": memoria,
                            "lifespan": lifespan
                        })
                        print(f"✓ Ancestral detectado: {agent_name} (Vida: {lifespan})")
        except Exception as e:
            print(f"Falha ao processar {log_file}: {e}")

    if memorias_elite:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(memorias_elite, f, indent=4, ensure_ascii=False)
        print(f"\nSucesso: {len(memorias_elite)} memórias injetadas em {output_file}")
    else:
        print("\nNenhum agente sobreviveu o suficiente para gerar herança histórica.")

if __name__ == "__main__":
    # Ajuste para o diretório onde estão os logs da sua Rodada 07
    CAMINHO_R7 = "logs/Rodada_07" 
    consolidar_experiencia(CAMINHO_R7, "core/genome/innate_knowledge_r08.json")
