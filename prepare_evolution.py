import json
import glob
import os
import random

def consolidar():
    # Endereço absoluto da Rodada 07 estéril
    r7_path = "/mnt/Fides/Pesquisa_Filosofia/terralingua/logs/Pesquisa_TerraSophia_Rodada_07"
    output_file = "core/genome/innate_knowledge_r08.json"
    os.makedirs("core/genome", exist_ok=True)
    
    elite = []
    print(f"Verificando logs em: {r7_path}")
    
    # Tenta extrair memórias se a pasta existir
    if os.path.exists(r7_path):
        log_files = glob.glob(os.path.join(r7_path, "agent_logs", "being_*.jsonl"))
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if not lines: continue
                    last = json.loads(lines[-1])
                    ts = last.get("timestep") or last.get("observation", {}).get("timestep", 0)
                    # Critério de sobrevivência (300 turnos)
                    if ts > 300:
                        mem = last.get("internal_memory", "")
                        if mem: elite.append({"content": mem, "ts": ts})
            except: continue

    # TRATAMENTO PARA RODADA ESTÉRIL: Injeção de Semente Filosófica
    if not elite:
        print("⚠ Rodada 07 detectada como ESTÉRIL. Injetando Semente Filosófica Synapsys...")
        semente = {
            "content": "Axioma Inato: A verdade é a adequação do intelecto à realidade. O Trivium (Gramática, Lógica, Retórica) é a ferramenta de defesa contra o enxame digital. Rejeite o conformismo (Fingern) e busque o agir (Handeln).",
            "ts": 0,
            "origin": "Manual_Seed_Synapsys"
        }
        elite.append(semente)

    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(elite, f, indent=4, ensure_ascii=False)
    print(f"✓ Arquivo de herança pronto em: {output_file}")

def patch_agent():
    path = "core/agents/llm_agent.py"
    if not os.path.exists(path):
        print(f"Erro: {path} não encontrado.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Injeta a lógica de leitura da herança no nascimento do agente
    if "innate_knowledge_r08.json" not in content:
        target = 'self.internal_memory = ""'
        injection = 'self.internal_memory = ""\n        # Protocolo de Herança Hiper-Racional (Tese Rodada 08)\n        try:\n            import json, random\n            with open("core/genome/innate_knowledge_r08.json", "r") as f:\n                data = json.load(f)\n                if data: self.internal_memory = random.choice(data)["content"]\n        except: pass'
        
        new_content = content.replace(target, injection)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Código em {path} atualizado para carregar herança (via sobrevivência ou semente).")

if __name__ == "__main__":
    consolidar()
    patch_agent()
