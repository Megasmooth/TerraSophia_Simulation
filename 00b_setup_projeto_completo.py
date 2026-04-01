import os

documento_completo = """# PROJETO DE PESQUISA: TERRASOPHIA 2.0 (DOCUMENTO DE REPLICAÇÃO)

**TÍTULO:** A Economia da Verdade em Sociedades Multiagente: Resiliência Epistemológica, o Trivium e o Custo Termodinâmico da Psicopolítica Algorítmica.
**TIPO:** Simulação Baseada em Agentes (ABM) com Modelos de Linguagem de Grande Escala (LLM).
**MOTOR COGNITIVO:** Llama 3 (via Ollama local). Temperatura = 0.0 (Ausência de estocasticidade na geração de raciocínio).

---

## 1. ARQUITETURA DA EXPERIÊNCIA E PARÂMETROS GLOBAIS
O ambiente é um laboratório fechado projetado para testar se a "Verdade" (informação com lastro na realidade) consegue sobreviver em um sistema de livre-arbítrio submetido à entropia térmica e informacional.

* **Topologia do Espaço:** Matriz bidimensional (Grid) de tamanho $N \\times N$ (padrão: 20x20).
* **Finitude (Relógio Biológico):** A simulação opera em "Turnos" (Timesteps). Cada agente nasce com um limite máximo vitalício absoluto de **150 Turnos**, após o qual sofre falência sistêmica (simulando envelhecimento incondicional), forçando a necessidade urgente de reprodução.
* **Capital Primário:** A "Energia Vital" atua como a única moeda metabólica e econômica do sistema. Atingir Energia $\\le 0$ resulta em óbito instantâneo (Starvation).
* **Entropia Passiva:** Todo agente perde passivamente uma quantidade fixa de energia por turno (ex: $-2.0$ de Energia) simplesmente por existir, forçando o "Agir" (*Handeln*).

---

## 2. MECÂNICA VETORIAL E A FÓRMULA DO ATRITO
Diferente de ABMs tradicionais onde agentes movem-se 1 tile por turno a custo fixo, o TerraSophia implementa movimentação por vetores regida pela "Economia do Conhecimento".

* **Ação:** O agente define o vetor direcional nos eixos X e Y: `{"action": "move", "args": {"dx": int, "dy": int}}`.
* **Cálculo da Distância:** Baseado na Distância de Manhattan: $D = |dx| + |dy|$.
* **A Equação do Atrito Epistemológico:** O atrito não é constante. Agentes com maior *Knowledge_Score* ($K$) compreendem o ambiente e reduzem o desperdício calórico locomotor através da equação:
  $$Custo\\_Base = \\max\\left(1, \\, 5 - \\lfloor \\frac{K}{2} \\rfloor \\right)$$
  $$Custo\\_Total\\_Movimento = Custo\\_Base \\times D$$
* *Conclusão Empírica Esperada:* A sabedoria torna-se uma vantagem mecânica literal. A longo prazo, agentes que ignoram a busca pela verdade colapsam devido à ineficiência de deslocamento.

---

## 3. A LEI DE BRANDOLINI E A MECÂNICA DE COMUNICAÇÃO
A simulação abole a omnisciência. A audição é local, limitada ao **Espaço de Han** (Vizinhança de Moore com raio de 5x5 tiles). Mensagens emitidas fora desse raio não entram no *prompt* de observação do agente.

A refutação da Desinformação obedece rigidamente à Assimetria Termodinâmica de Brandolini:
1. **O Ataque (Sofismo):** Ação `broadcast_poison`. Custo: **1.0 Energia**. O agente alucina propositalmente com base em um *dataset* de falácias (`Arsenal.csv`). Requer baixo processamento.
2. **A Defesa (Erudição):** Ação `rebuttal_synapsys`. Custo: **5.0 Energia**. O agente acessa o banco vetorial estruturado Trivium (`Jornada.csv`). Requer busca intensiva em banco de dados e custa 5x mais caro que a mentira.
3. **A Recepção Passiva (Conformismo):** Ação `accept_claim`. Custo: **0.0 Energia**. A Tábula Rasa aceita a informação sem validação. Risco de seguir coordenadas para o vazio (dano moral e desperício termodinâmico).
4. **A Recepção Ativa (Realismo Científico):** Ação `fact_check`. Custo: **3.0 Energia**. O agente invoca o Juiz Semântico (SBERT) para validar a informação. Gera bônus de Alinhamento e revela o mundo material real.

---

## 4. O SISTEMA GEOGRÁFICO DE INCENTIVOS (MECENATO)
Para evitar que a população perambule eternamente até a morte, a geografia deve ser moldada pela ação `create_artifact` (Exclusiva da classe Artesão, custo elevado: **30.0 Energia**).

* **A Fogueira (Ágora/Mercado):** Cria um raio térmico de 3x3 tiles.
  * *Mitigação:* Agentes dentro do raio têm sua entropia passiva suspensa.
  * *Rent-Seeking (Pedágio Térmico):* A cada turno que um agente se beneficia da fogueira, o sistema debita automaticamente $0.5$ de energia do beneficiário e credita na conta do Artesão proprietário. Isso gera o "Superávit do Mecenas", necessário para financiar o alto custo da ação dos Eruditos.
* **O Ninho (Berçário):** Artefato fixo mandatário para a ocorrência da ação `reproduce`.

---

## 5. REPRODUÇÃO