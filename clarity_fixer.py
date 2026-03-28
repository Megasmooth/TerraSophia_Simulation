import os

def patch_env():
    path = "core/environment/env.py"
    if not os.path.exists(path):
        print(f"Erro: {path} não encontrado.")
        return

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 1. Ajuste do Construtor para aceitar agents_ref
    for i, line in enumerate(lines):
        if "def __init__" in line:
            # Procura o final dos argumentos do init
            for j in range(i, i + 30):
                if "):" in lines[j]:
                    lines[j] = lines[j].replace("):", "    agents_ref: dict = None\n    ):")
                    lines.insert(j + 2, "        self.agents = agents_ref or {}\n")
                    break
            break

    # 2. Injeção da Lei de Brandolini no Step
    for i, line in enumerate(lines):
        if "def step(self, actions):" in line:
            injection = [
                "\n        # --- INJEÇÃO TERRASOPHIA: LEI DE BRANDOLINI ---\n",
                "        for agent_id, act in actions.items():\n",
                "            if agent_id not in self.agent_registry: continue\n",
                "            agent_obj = self.agents.get(agent_id)\n",
                "            phenotype = getattr(agent_obj, 'phenotype', 'tabula_rasa')\n",
                "            action_name = act.get('action', 'move')\n",
                "            move_mult = 2.0 if phenotype == 'erudito' else 1.0\n",
                "            costs = {'move': 1.0*move_mult, 'broadcast_poison': 1.0, 'rebuttal_synapsys': 5.0, 'fact_check': 3.0, 'accept_claim': 0.0}\n",
                "            self.agent_energy[agent_id] -= costs.get(action_name, 1.0)\n",
                "            if action_name in ['broadcast_poison', 'rebuttal_synapsys']:\n",
                "                self._apply_spatial_broadcast(agent_id, act.get('message', ''), radius=5)\n"
            ]
            lines[i+1:i+1] = injection
            break

    # 3. Funções de Apoio no final
    support_funcs = [
        "\n    def _apply_spatial_broadcast(self, origin_id, message, radius=5):\n",
        "        origin_pos = self.agent_pos.get(origin_id)\n",
        "        if not origin_pos: return\n",
        "        for target_id, target_pos in self.agent_pos.items():\n",
        "            if origin_id == target_id: continue\n",
        "            dist = np.linalg.norm(np.array(origin_pos) - np.array(target_pos))\n",
        "            if dist <= radius:\n",
        "                target_agent = self.agents.get(target_id)\n",
        "                if target_agent: target_agent.internal_memory += f'\\n[RÁDIO]: {message}'\n"
    ]
    lines.extend(support_funcs)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("✓ env.py corrigido com sucesso.")

def patch_runner():
    path = "core/experiment/runner.py"
    if not os.path.exists(path): return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Import Pandas
    content = content.replace("import numpy as np", "import numpy as np\nimport pandas as pd")

    # Injeção de Dados no Loop
    search_str = 'for ts in range(self.start_ts, max_ts):'
    injection = """
                    # Injeção Synapsys
                    for tag, agent in self.agents.items():
                        ph = getattr(agent, 'phenotype', 'tabula_rasa')
                        if ph == "sofista" and self.df_arsenal is not None:
                            agent.internal_memory += f"\\n[ARSENAL]: {self.df_arsenal.sample(1).iloc[0]['afirmacao_veneno']}"
                        elif ph == "erudito" and self.df_jornada is not None:
                            agent.internal_memory += f"\\n[TRIVIUM]: {self.df_jornada.sample(1).iloc[0]['content'][:300]}"
    """
    content = content.replace(search_str, search_str + injection)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ runner.py corrigido com sucesso.")

if __name__ == "__main__":
    patch_env()
    patch_runner()