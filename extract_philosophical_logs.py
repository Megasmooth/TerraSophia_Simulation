import pickle
import pandas as pd
import argparse
from pathlib import Path
import glob
import os

def extract_logs(exp_name):
    print(f"Iniciando extração de dados para o experimento: {exp_name}")
    log_dir = Path(f"logs/{exp_name}")
    
    if not log_dir.exists():
        print(f"ERRO: Pasta {log_dir} não encontrada.")
        return

    # Busca os arquivos de checkpoint (ignorando o env_state.pkl final se houver duplicidade)
    pkl_files = sorted(glob.glob(f"{log_dir}/checkpoint_*.pkl"))
    if not pkl_files:
        # Tenta pegar qualquer pkl caso o padrao de nome seja diferente
        pkl_files = sorted(glob.glob(f"{log_dir}/*.pkl"))
    
    mensagens = []
    artefatos = []
    transacoes = []
    demografia = [] # NOVO: Rastreamento evolutivo da população

    for file_path in pkl_files:
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                
            # Extrai o timestep do nome do arquivo (ex: checkpoint_5.pkl -> 5)
            filename = os.path.basename(file_path)
            timestep = ''.join(filter(str.isdigit, filename))
            if not timestep:
                timestep = data.get('timestep', 0) if isinstance(data, dict) else 0

            # TerraLingua salva o Runner inteiro ou um dict com 'env' e 'agents'
            env_data = data.get('env') if isinstance(data, dict) else getattr(data, 'env', None)
            agents_data = data.get('agents') if isinstance(data, dict) else getattr(data, 'agents', {})

            if not agents_data and not env_data:
                continue

            # 1. RASTREAMENTO DEMOGRÁFICO E EPISTÊMICO (O Coração da Tese)
            if env_data and agents_data:
                for agent_id, agent_obj in agents_data.items():
                    # Captura atributos dinamicamente (suportando tanto dict quanto objeto)
                    is_dict = isinstance(agent_obj, dict)
                    
                    a_type = agent_obj.get('type', 'Unknown') if is_dict else getattr(agent_obj, 'type', 'Unknown')
                    k_score = agent_obj.get('knowledge_score', 0) if is_dict else getattr(agent_obj, 'knowledge_score', 0)
                    bit_type = agent_obj.get('bit_type', -1) if is_dict else getattr(agent_obj, 'bit_type', -1)
                    children = len(agent_obj.get('children_ids', [])) if is_dict else len(getattr(agent_obj, 'children_ids', []))
                    
                    # Busca a energia e vida atual no environment
                    energia = getattr(env_data, 'agent_energy', {}).get(agent_id, 0)
                    vida = getattr(env_data, 'agent_lifespan', {}).get(agent_id, 0)

                    demografia.append({
                        'Timestep': timestep,
                        'Agent_ID': agent_id,
                        'Type': a_type,
                        'Bit_DNA': bit_type,
                        'Knowledge_Score': k_score,
                        'Energy': energia,
                        'Lifespan_Remaining': vida,
                        'Num_Children': children
                    })

            # 2. EXTRAÇÃO DE MENSAGENS E AÇÕES
            if agents_data:
                for agent_id, agent_obj in agents_data.items():
                    is_dict = isinstance(agent_obj, dict)
                    a_type = agent_obj.get('type', 'Unknown') if is_dict else getattr(agent_obj, 'type', 'Unknown')
                    
                    # Tenta extrair o log de ações/mensagens se o objeto salvar isso
                    last_action = agent_obj.get('last_action', {}) if is_dict else getattr(agent_obj, 'last_action', {})
                    msg = agent_obj.get('last_message', '') if is_dict else getattr(agent_obj, 'last_message', '')
                    
                    # Fallback para o internal_memory se last_message não existir
                    if not msg and not is_dict and hasattr(agent_obj, 'internal_memory'):
                        mem = getattr(agent_obj, 'internal_memory')
                        if mem and isinstance(mem, list):
                            msg = str(mem[-1]) # Pega a última memória

                    if msg or last_action:
                        mensagens.append({
                            'Timestep': timestep,
                            'Agent_ID': agent_id,
                            'Agent_Type': a_type,
                            'Message_Content': msg,
                            'Action_Taken': str(last_action)
                        })

                    # Transações diretas ('give')
                    if isinstance(last_action, dict) and last_action.get('action') == 'give':
                        transacoes.append({
                            'Timestep': timestep,
                            'Donor_ID': agent_id,
                            'Recipient_ID': last_action.get('params', {}).get('target', 'Unknown'),
                            'Energy_Amount': last_action.get('params', {}).get('energy', 0)
                        })

            # 3. EXTRAÇÃO DE ARTEFATOS NO CHÃO
            if env_data:
                artifacts_dict = getattr(env_data, 'artifacts', {})
                artifacts_map = getattr(env_data, 'artifacts_map', {})
                
                for pos, arts in artifacts_map.items():
                    for art_name in arts:
                        payload = artifacts_dict.get(art_name, {})
                        if payload:
                            artefatos.append({
                                'Timestep': timestep,
                                'Artifact_ID': art_name,
                                'Creator_ID': payload.get('creator', 'Unknown'),
                                'Position_X': pos[0],
                                'Position_Y': pos[1],
                                'Artifact_Text': payload.get('payload', '')
                            })
                    
        except Exception as e:
            print(f"Aviso: Não foi possível ler {file_path}. Erro: {e}")

    # Salva os arquivos CSV
    pd.DataFrame(mensagens).to_csv(log_dir / "1_mensagens_agentes.csv", index=False)
    pd.DataFrame(artefatos).to_csv(log_dir / "2_artefatos_criados.csv", index=False)
    pd.DataFrame(transacoes).to_csv(log_dir / "3_economia_energia.csv", index=False)
    
    # O CSV mais importante para os gráficos da tese
    df_demo = pd.DataFrame(demografia)
    if not df_demo.empty:
        df_demo.to_csv(log_dir / "4_demografia_epistemica.csv", index=False)
    
    print(f"Sucesso! Dados extraídos e salvos em {log_dir}")
    print("Arquivos gerados: 1_mensagens, 2_artefatos, 3_economia, 4_demografia_epistemica")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_name", type=str, required=True, help="Nome da pasta do experimento")
    args = parser.parse_args()
    extract_logs(args.exp_name)