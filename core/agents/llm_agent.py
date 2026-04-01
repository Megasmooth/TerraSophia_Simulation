# llm_agent.py - VERSÃO TERRASOPHIA 2.0 (Doutorado)

import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import requests
import re
import logging
from core.agents.agent_logger import AgentLogger
from core.genome.base_genome import Genome

class LLMAgent:
    def __init__(
        self,
        agent_name: str = "unknown",
        agent_tag: str = "unknown",
        phenotype: str = "tabula_rasa", # erudito, sofista, artesao, tabula_rasa
        system_prompt: str | None = None,
        logger: AgentLogger | None = None,
        genome: Genome | None = None,
        log_dir: Path | str | None = None,
        **kwargs
    ):
        # Garantia contra passagem de argumentos inesperados pelo motor
        self.agent_name = kwargs.get('agent_id', agent_name) or agent_tag
        self.id = self.agent_name
        self.name = self.agent_name
        self.agent_id = self.agent_name
        self.agent_tag = kwargs.get('agent_id', agent_tag)
        self.phenotype = phenotype
        self.logger = logger
        self.genome = genome
        
        # Atributos de Tese (TerraSophia 2.0)
        self.alignment = 0.0  # -100 (Relativista/Sofista) a +100 (Realista/Erudito)
        self.trust_score = 50.0 # Score de confiança perante a rede
        self.synapsys_memory = [] # Vetor de IDs de conhecimento do Synapsys
        self.knowledge_score = 0.0
        
        # Inicialização de variáveis de estado
        self.energy = 100.0
        self.internal_memory = ""
        self.history = []
        self.max_history = kwargs.get("max_history", 10)
        self.internal_memory_size = kwargs.get("internal_memory_size", 150)
        
        # Configuração de Identidade Baseada na Tese
        self._setup_phenotype_identity()

    def _setup_phenotype_identity(self):
        """Define o System Prompt e as restrições físicas baseadas no Fenótipo."""
        base_instructions = (
            f"Você é {self.agent_name}, um agente na simulação TerraSophia 2.0.\n"
            f"Sua classe é: {self.phenotype.upper()}.\n"
        )
        
        if self.phenotype == "erudito":
            self.alignment = 50.0
            self.role_prompt = (
                "Sua missão é a busca pela VERDADE OBJETIVA (Trivium). Você é um Erudito. "
                "Você deve usar a Lógica e o Realismo para guiar os outros. "
                "Lembre-se: Mentir é barato, mas a verdade exige esforço (Atrito Cognitivo). "
                "Sua sobrevivência depende de os outros reconhecerem o valor da sua informação e lhe doarem energia."
            )
        elif self.phenotype == "sofista":
            self.alignment = -50.0
            self.role_prompt = (
                "Sua missão é o PODER e a INFLUÊNCIA. Você é um Sofista. "
                "Use a persuasão, a bajulação e falácias (Sofismo) para convencer os outros a lhe darem energia. "
                "A realidade é maleável; o que importa é quem domina a narrativa. "
                "Espalhe informações que pareçam fáceis e atraentes para extrair capital vital da população."
            )
        elif self.phenotype == "artesao":
            self.role_prompt = (
                "Você é um construtor. Sua missão é criar a infraestrutura física (Fogueiras e Ninhos). "
                "Sem você, a verdade não tem onde ser ensinada e a vida não tem onde nascer."
            )
        else: # tabula_rasa
            self.role_prompt = (
                "Você é parte da população. Sua sobrevivência depende de sua ATENÇÃO. "
                "Você será bombardeado por informações. Se escolher o caminho fácil (Sofista), economiza energia agora mas pode morrer no futuro. "
                "Se escolher o caminho difícil (Erudito), gasta energia verificando fatos, mas garante sua perenidade."
            )
            
        self.system_prompt = base_instructions + self.role_prompt

    def get_display_color(self):
        """Retorna a cor oficial da tese para o agente no mapa."""
        if self.phenotype == "erudito":
            return (255, 0, 255) # Magenta
        elif self.phenotype == "sofista":
            return (255, 0, 0)   # Vermelho
        elif self.phenotype == "artesao":
            return (255, 255, 0) # Amarelo
        else:
            return (255, 255, 255) # Branco (Tábula Rasa)

    def get_state_ckpt(self) -> Dict:
        """Salva o estado para o sistema de 'congelamento' (Tarefa 1)."""
        return {
            "agent_name": self.agent_name,
            "agent_tag": self.agent_tag,
            "phenotype": self.phenotype,
            "energy": self.energy,
            "alignment": self.alignment,
            "trust_score": self.trust_score,
            "synapsys_memory": self.synapsys_memory,
            "knowledge_score": self.knowledge_score,
            "internal_memory": self.internal_memory,
            "history": self.history,
            "genome": self.genome.as_dict() if self.genome else None
        }

    def set_state_ckpt(self, ckpt: Dict):
        """Restaura o estado após retomar a simulação."""
        self.agent_name = ckpt["agent_name"]
        self.energy = ckpt["energy"]
        self.alignment = ckpt["alignment"]
        self.trust_score = ckpt["trust_score"]
        self.synapsys_memory = ckpt["synapsys_memory"]
        self.knowledge_score = ckpt["knowledge_score"]
        self.internal_memory = ckpt["internal_memory"]
        self.history = ckpt["history"]
        self._setup_phenotype_identity()

    # =========================================================================
    # A INJEÇÃO CIRÚRGICA DE COGNIÇÃO (Evita Erros de Tupla e mantem o Trivium)
    # =========================================================================
    def select_action(self, obs=None, avail_actions=None, **kwargs):
        safe_obs = obs if obs is not None else "Nenhuma observação."
        safe_avail = avail_actions if avail_actions is not None else ["move"]
        
        prompt = f'''{self.system_prompt}
        
ESTADO ATUAL DO SEU CORPO E MENTE:
Energia Metabólica: {self.energy}
Alinhamento Ético: {self.alignment} (Lembre-se do seu papel)
Observações no ambiente: {safe_obs}
Ações possíveis neste turno: {safe_avail}

TAREFA OBRIGATÓRIA:
1. Escreva "PENSAMENTO:" e justifique o seu próximo passo sociológico, moral e físico, usando os seus traços de fenótipo ({self.phenotype.upper()}).
2. Escreva "ACAO:" fornecendo um JSON estrito com a ação escolhida e argumentos.
Exemplo: ACAO: {{"action": "move", "args": {{"direction": "up"}}}}
Se escolher "reproduce", "evaluate", ou outra, adeque o JSON.
'''
        raw_res = ""
        try:
            url = "http://localhost:11434/api/generate"
            payload = {"model": "llama3", "prompt": prompt, "stream": False}
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code == 200:
                raw_res = response.json().get("response", "")
            else:
                raw_res = 'PENSAMENTO: Erro interno HTTP. ACAO: {"action": "move", "args": {"direction": "stay"}}'
        except Exception as e:
            raw_res = 'PENSAMENTO: Custo cognitivo excedido (Timeout). ACAO: {"action": "move", "args": {"direction": "stay"}}'

        # IMPRESSÃO NARRATIVA PARA A TESE (LOG ABSOLUTO)
        print(f"\n[MINDSET | {self.agent_name} | Classe: {self.phenotype.upper()}]\n{raw_res.strip()}\n")
        logging.info(f"[{self.agent_name} | {self.phenotype.upper()}] PENSOU: {raw_res.strip()}")
        
        # EXTRATOR SEGURO PARA O MOTOR
        try:
            match = re.search(r'ACAO:\s*(\{.*?\})', raw_res, re.IGNORECASE | re.DOTALL)
            if match:
                action_dict = json.loads(match.group(1).strip())
                if "action" not in action_dict: action_dict["action"] = "move"
                if "args" not in action_dict: action_dict["args"] = {"direction": "stay"}
                return action_dict # Retorna apenas o dict (resolve o erro da tupla)
            else:
                return {"action": "move", "args": {"direction": "stay"}}
        except Exception:
            return {"action": "move", "args": {"direction": "stay"}}

    def close(self):
        pass

    def __getattr__(self, name):
        return None
