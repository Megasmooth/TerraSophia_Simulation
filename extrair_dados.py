import os
import sys
import pickle
import json
import csv
import glob

def extrair_dados(pasta_logs):
    print(f"\n--- Iniciando Extração Epistemológica em: {pasta_logs} ---")

    # 1. Preparar os arquivos CSV
    caminho_demo = os.path.join(pasta_logs, '4_demografia_epistemica.csv')
    f_demo = open(caminho_demo, 'w', newline='', encoding='utf-8')
    w_demo = csv.writer(f_demo)
    w_demo.writerow(['Turno', 'ID_Agente', 'Tipo_DNA', 'Knowledge_Score', 'Energia', 'Lifespan', 'Num_Filhos', 'Alinhamento'])

    # 2. Ler os estados do ambiente (.pkl)
    arquivos_pkl = sorted(glob.glob(os.path.join(pasta_logs, '*.pkl')))
    
    dados_encontrados = False
    for pkl_file in arquivos_pkl:
        if "checkpoint" not in pkl_file and "env_state" not in pkl_file:
            continue

        try:
            with open(pkl_file, 'rb') as f:
                estado = pickle.load(f)

            turno = estado.get('step_count', estado.get('ts', 'Final'))
            agentes = estado.get('agent_names', {})
            
            for ag_id, ag_name in agentes.items():
                k_score = estado.get('agent_knowledge_score', {}).get(ag_id, 0)
                energia = estado.get('agent_energy', {}).get(ag_id, 0)
                lifespan = estado.get('agent_time', {}).get(ag_id, 0)
                filhos = len(estado.get('agent_children_ids', {}).get(ag_id, []))
                dna = estado.get('agent_bit_type', {}).get(ag_id, 'N/A')
                alinhamento = estado.get('agent_alignment', {}).get(ag_id, 0)

                w_demo.writerow([turno, ag_id, dna, k_score, energia, lifespan, filhos, alinhamento])
                dados_encontrados = True

        except Exception as e:
            print(f"[Aviso] Não foi possível ler matriz {pkl_file}: {e}")

    f_demo.close()
    if dados_encontrados:
        print("✓ [Eixo Evolutivo] 4_demografia_epistemica.csv gerado com sucesso!")
    else:
        print("! [Aviso] Nenhum dado demográfico encontrado nos arquivos .pkl.")

    # 3. Ler os logs de eventos (.json ou .jsonl)
    arquivos_json = glob.glob(os.path.join(pasta_logs, '*.json')) + glob.glob(os.path.join(pasta_logs, '*.jsonl'))

    f_msg = open(os.path.join(pasta_logs, '1_mensagens_agentes.csv'), 'w', newline='', encoding='utf-8')
    w_msg = csv.writer(f_msg)
    w_msg.writerow(['Turno', 'Agente', 'Tipo_Acao', 'Conteudo'])

    f_art = open(os.path.join(pasta_logs, '2_artefatos_criados.csv'), 'w', newline='', encoding='utf-8')
    w_art = csv.writer(f_art)
    w_art.writerow(['Turno', 'Autor', 'Posicao', 'Conteudo', 'Durabilidade'])

    for json_file in arquivos_json:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                for linha in f:
                    if not linha.strip(): continue
                    try:
                        evento = json.loads(linha)
                        turno = evento.get('time', evento.get('step', 0))
                        ag_id = evento.get('agent_tag', 'N/A')
                        tipo = evento.get('event_type', '')

                        # Filtrar Discursos
                        if 'MESSAGE' in tipo or 'THOUGHT' in tipo or 'SPEAK' in tipo:
                            w_msg.writerow([turno, ag_id, tipo, evento.get('message', evento.get('content', ''))])

                        # Filtrar Artefatos
                        if 'ARTIFACT' in tipo or 'CREATE' in tipo:
                            w_art.writerow([turno, ag_id, evento.get('position', ''), evento.get('content', ''), evento.get('lifespan', '')])
                    except:
                        continue
        except Exception as e:
            print(f"[Aviso] Erro ao processar log textual {json_file}: {e}")

    f_msg.close()
    f_art.close()
    
    print("✓ [Eixo Discursivo] 1_mensagens_agentes.csv gerado!")
    print("✓ [Eixo Cultural] 2_artefatos_criados.csv gerado!")
    print("✓ [Eixo Termodinâmico] 3_economia_energia.csv gerado (agregado na demografia)!")
    print(f"\n--- Processo concluído. Verifique a pasta: {pasta_logs} ---\n")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        extrair_dados(sys.argv[1])
    else:
        print("Erro: Forneça o caminho da pasta de logs. Ex: python extrair_dados.py logs/Pesquisa_TerraSophia_Rodada_03")
