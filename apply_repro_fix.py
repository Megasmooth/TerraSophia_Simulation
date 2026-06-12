import os

def patch_env():
    filepath = "core/environment/env.py"
    if not os.path.exists(filepath):
        print("Erro: Arquivo core/environment/env.py não encontrado.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inserção da trava física de Ninho no bloco de reprodução
    old_repro = '            elif action_name == "reproduce":\n    \n                creator = agent\n                \n                # 1. Encontrar um parceiro adjacente'
    new_repro = '''            elif action_name == "reproduce":
    
                creator = agent
                
                # 0. Verificar Infraestrutura (Ninho) - Requisito da Tese
                if not self._check_nearby_artifact(creator, "ninho", radius=3):
                    infos[creator]["reproduction"] = {"status": "failed", "reason": "No Ninho nearby"}
                    if self.agent_energy[creator] >= 1: self.agent_energy[creator] -= 1
                    continue

                # 1. Encontrar um parceiro adjacente'''
    
    # Ajuste de quebras de linha para o replace funcionar no ambiente Unix/Linux
    content = content.replace(old_repro.replace('\\n', '\n'), new_repro)

    # 2. Correção de bugs técnicos no método _check_nearby_artifact
    # art.type não existe na classe Artifact (é art_type) e position é pose
    content = content.replace("if art.type == art_type:", "if art.art_type == art_type:")
    content = content.replace("np.array(art.position)", "np.array(art.pose)")

    # 3. Limpeza do lixo duplicado ao final do arquivo
    # Remove a declaração solta de _apply_spatial_broadcast detectada após o env.close()
    if "    env.close()\n    def _apply_spatial_broadcast" in content:
        content = content.split("    env.close()\n    def _apply_spatial_broadcast")[0] + "    env.close()"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Sucesso: core/environment/env.py atualizado.")
    print("✓ Mecânica de 'Ninho' ativada (Raio: 3).")
    print("✓ Bugs de atributos de artefatos corrigidos.")

if __name__ == "__main__":
    patch_env()
