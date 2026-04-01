# PROJETO DE PESQUISA: TERRASOPHIA 2.0 (DOCUMENTO DE REPLICAÇÃO)

**TÍTULO:** A Economia da Verdade em Sociedades Multiagente: Resiliência Epistemológica, o Trivium e o Custo Termodinâmico da Psicopolítica Algorítmica.
**TIPO:** Simulação Baseada em Agentes (ABM) com Modelos de Linguagem de Grande Escala (LLM).
**MOTOR COGNITIVO:** Llama 3 (via Ollama local). Temperatura = 0.0 (Ausência de estocasticidade na geração de raciocínio).

---

## 1. ARQUITETURA DA EXPERIÊNCIA E PARÂMETROS GLOBAIS
O ambiente é um laboratório fechado projetado para testar se a "Verdade" (informação com lastro na realidade) consegue sobreviver num sistema de livre-arbítrio submetido à entropia térmica e informacional.

* **Topologia do Espaço:** Matriz bidimensional expandida (Grid) de tamanho **40x40** (1600 células), maximizando o "Pathos da Distância" e o isolamento natural.
* **Finitude (Relógio Biológico):** A simulação opera em "Turnos" (Timesteps). Cada agente nasce com um limite vitalício absoluto de **150 Turnos**.
* **Capital Primário:** A "Energia Vital" atua como a única moeda metabólica e económica. Atingir Energia $\le 0$ resulta em óbito (Starvation).
* **Entropia Passiva:** Todo agente perde passivamente uma quantidade fixa de energia por turno (ex: $-2.0$), forçando o "Agir" (*Handeln*).

---

## 2. MECÂNICA VETORIAL E A FÓRMULA DO ATRITO
* **Ação:** O agente define o vetor direcional: `{"action": "move", "args": {"dx": int, "dy": int}}`. Custo regido pela Distância de Manhattan ($D = |dx| + |dy|$).
* **A Equação do Atrito Epistemológico:** O conhecimento reduz o desperdício calórico locomotor:
  $$Custo\_Base = \max\left(1, \, 5 - \lfloor \frac{K}{2} \rfloor \right)$$
  $$Custo\_Total\_Movimento = Custo\_Base \times D$$

---

## 3. A LEI DE BRANDOLINI E O DECAIMENTO DO ECO (VIRALIDADE)
A audição é local, limitada ao **Espaço de Han** originiário (5x5 tiles), mas a propagação de mentiras sofre degradação.

1. **O Ataque Primário (Sofista):** Ação `broadcast_poison`. Custo: **1.0 Energia**. Alcance: **5x5**. Dano Moral: **-10 Alinhamento**. O agente alucina propositalmente baseando-se no `Arsenal.csv`.
2. **O Retweet / Eco (A Câmara de Bolha):** Quando uma Tábula Rasa usa `accept_claim` (Custo: 0.0) sob uma mentira, ela retransmite a falácia involuntariamente no turno seguinte. 
   * *Atenuação Acústica:* O raio do eco cai drasticamente para **1x1** (apenas células coladas).
   * *Atenuação de Força:* O dano moral cai para **-5 Alinhamento**. A mentira dilui-se, a não ser que a própria Tábula Rasa se corrompa e se torne um Sofista.
3. **A Defesa (Erudição):** Ação `rebuttal_synapsys`. Custo: **5.0 Energia**. Alcance: 5x5. O agente acessa o `Jornada.csv` (Trivium) para refutar o veneno, revelando a realidade.
4. **O Realismo Científico:** Ação `fact_check`. Custo: **3.0 Energia**. A Tábula Rasa invoca o Juiz Semântico para validar a informação. Gera bônus de Alinhamento (+10).

---

## 4. O SISTEMA GEOGRÁFICO E A TERMODINÂMICA DA PÓLIS
A sobrevivência depende da mitigação do ambiente hostil 40x40.

* **O Artesão (O Fardo da Pólis):** Não atua como um capitalista maximizador de lucros cegos, mas como o mantenedor da infraestrutura material. O seu objetivo é manter a Pólis viva.
* **A Fogueira Efêmera:** Artefato criado pelo Artesão. Anula a entropia passiva num raio de 3x3. 
  * *Ciclo de Vida Curto:* A fogueira dura no máximo **5 turnos**.
  * *Entropia por Densidade:* O combustível base (100%) cai 20% por turno. Adicionalmente, perde **5% extras por cada agente** presente no raio. Fogueiras lotadas apagam-se mais rápido, forçando o Artesão a reinvestir energia constantemente.

---

## 5. REPRODUÇÃO, DIMORFISMO E O CUSTO IMOBILIÁRIO (O ÊXODO)
A reprodução exige estritamente a combinação heterogênea de progenitores `(0 com 1)`.

* **A Fundação do Ninho (Gentrificação):** O Ninho não "nasce" espontaneamente. Ele deve ser construído ativamente pelos casais (Tábula Rasa 0 e 1) com as suas próprias poupanças.
* **O Preço do Espaço:** Construir um Ninho obedece à densidade populacional:
  $$Custo\_Ninho = 30 + (10 \times Agentes\_no\_Raio\_5x5)$$
  *Consequência Empírica:* Ficar no centro da Pólis (perto da Fogueira) torna o custo reprodutivo extorsivo. Casais são matematicamente forçados a realizar um "Êxodo" para as margens isoladas do mapa 40x40 para conseguirem procriar (onde o custo cai para 30), enfrentando os perigos da entropia.
* **Equação de Herança ($\eta = 0.8$):** A carga genética transmitida é o Knowledge Score.
  $$K_{filho} = \left( \frac{K_{pai} + K_{mae}}{2} \right) \times 0.8$$

---

## 6. AS CLASSES E REGRAS DE MUTAÇÃO (MOBILIDADE SOCIAL)
Geração 0 (20 a 50 agentes), divididos em:
* **60% Tábula Rasa:** O Povo. Nascem cegos à Fórmula do Atrito. Constroem Ninhos e decidem quem financiar.
* **15% Eruditos:** Nascem com acesso ao `Synapsys`. Sofrem para falar a verdade (custo 5.0).
* **15% Sofistas:** Nascem com acesso ao `Arsenal`. Mentem barato (custo 1.0).
* **10% Artesãos:** Os Mantenedores da Pólis. Constroem Fogueiras e cobram impostos termodinâmicos para manter a engrenagem viva.

**Limiares de Conversão (Evolução da Tábula Rasa):**
1. **Torna-se Erudito:** Atingir `Knowledge_Score >= 20` e `Alinhamento > 0`.
2. **Torna-se Sofista:** Atingir `Alinhamento <= -20`.
3. **Torna-se Artesão:** Atingir `Energia >= 250`, acumulando recursos materiais para passar a gerir a Pólis.
