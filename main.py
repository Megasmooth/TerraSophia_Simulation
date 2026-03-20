# Copyright © 2025 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import os
from dotenv import load_dotenv

from core.experiment.cli import parse_args
from core.experiment.config import build_config
from core.experiment.runner import SimulationRunner

# FIX CRÍTICO: Define o cache do tiktoken localmente para evitar erros de conexão (DNS)
os.environ["TIKTOKEN_CACHE_DIR"] = os.path.join(os.getcwd(), "tiktoken_cache")

load_dotenv()


def main():
    args = parse_args()
    params = build_config(args)

    # --- CONFIGURAÇÃO DA TESE: Diversificação de Agentes ---
    # Guardamos a quantidade total de agentes pedida no comando
    total_agents = params['env']['init_agents']
    
    # Zeramos no config para o Runner não criar agentes genéricos automaticamente
    params['env']['init_agents'] = 0 

    resume = args.resume
    runner = SimulationRunner(params=params, resume=resume)

    # Se for uma simulação nova, adicionamos os agentes com seus papéis específicos
    if not resume:
        print(f"--- Iniciando Sociedade de IA: {total_agents} agentes ---")
        for i in range(total_agents):
            agent_tag = f"being{i}"
            
            if i == 0:
                # O Synapsys: Católico e fundamentado no Trivium/Quadrivium
                agent_type = "SynapsysPhilosopher"
            elif i == 1 or i == 2:
                # Os Bots: Agentes de ruído e entropia
                agent_type = "BotAgent"
            else:
                # Agentes Comuns: Tábula Rasa exposta ao ambiente
                agent_type = "CommonAgent"
            
            runner.add_agent(agent_tag, agent_type=agent_type)
    # -------------------------------------------------------

    runner.run()


if __name__ == "__main__":
    main()