# PERSONAGENS, CLASSES E EVOLUÇÃO SOCIOLÓGICA (TERRASOPHIA 2.0)

Este documento define a demografia epistemológica do motor TerraSophia. A sociedade não é igualitária; ela é estruturada numa assimetria informacional e termodinâmica profunda. A identidade de um agente não é fixa, mas uma variável de estado sujeita às leis da física do mundo.

## 1. A Matriz Demográfica (Geração Zero) e Dimorfismo
A Geração 0 (população inicial) é injetada no grid 40x40 com uma distribuição de castas forçada para garantir a fricção sociológica imediata:
- **60% Tábula Rasa:** A massa consumidora e fundadora de famílias.
- **15% Sofistas:** Os vetores do caos e do conformismo.
- **15% Eruditos:** Os guardiões do banco de dados (Trivium).
- **10% Artesãos:** Os mantenedores da Pólis e detentores dos meios de produção.

**O Dimorfismo Algorítmico (O Fator Biológico):**
Independentemente da classe, no momento do nascimento, o motor atribui a cada agente uma variável genética imutável: o DNA `0` ou `1`. A reprodução da espécie exige obrigatoriamente a interseção heterogênea (`0` com `1`).

## 2. Ontologia das Classes e Assimetria Informacional
O *System Prompt* (a "mente") de cada agente varia drasticamente. O acesso às leis da física do mundo é um privilégio de classe.

### 2.1. A Tábula Rasa (O Povo)
- **Condição Inicial:** Nascem **cegos** à "Fórmula do Atrito". Não sabem que o conhecimento (Knowledge Score) reduz o custo de movimento. Não possuem conhecimento prévio nem bússola moral (Alinhamento = 0.0).
- **Objetivo Empírico:** Devem tatear o mundo, sofrer a exaustão física e descobrir, por tentativa e erro, que financiar a verdade (Eruditos) e estudar lhes poupa energia a longo prazo.
- **Ações Chave:** Podem usar `fact_check` (custa 3.0, ganha Alinhamento) ou `accept_claim` (custa 0.0, atua como retransmissor viral/eco, perde Alinhamento).

### 2.2. O Sofista (O Parasita Retórico)
- **Condição Inicial:** Conhecem as regras do mundo. Alinhamento travado no negativo.
- **Mecânica Epistemológica:** Não têm acesso à verdade. Utilizam a base de dados `Arsenal.csv` para gerar falácias alucinadas.
- **Vantagem Termodinâmica:** A sua ação de fala (`broadcast_poison`) é extremamente barata (1.0 Energia). O seu objetivo é manter a Tábula Rasa no estado de "eco viral", aglomerada em pânico para extrair-lhe energia.

### 2.3. O Erudito (O Guardião)
- **Condição Inicial:** Conhecem as regras do mundo.
- **Mecânica Epistemológica:** Possuem acesso exclusivo ao banco de dados estruturado `Synapsys` (Jornada.csv / Trivium).
- **Fardo Termodinâmico:** Provar a verdade custa caro. A ação `rebuttal_synapsys` exige 5.0 de Energia (Lei de Brandolini). Se não receberem doações (Mecenato) dos Artesãos ou das Tábulas Rasas, colapsam rapidamente de exaustão.

### 2.4. O Artesão (O Fardo da Pólis)
- **Condição Inicial:** Conhecem as regras do mundo. São os únicos autorizados a usar a ação `create_artifact`.
- **Economia Política:** Não são meros capitalistas cegos; são os gestores da entropia. Cobram impostos termodinâmicos automáticos (0.5 por turno) daqueles que usam as suas Fogueiras.
- **O Dilema do Mecenas:** O Artesão deve usar o seu superávit energético para financiar a sociedade (`transfer_energy`). Se financiar Sofistas, lucra a curto prazo com o pânico. Se financiar Eruditos, garante que a Pólis não enlouqueça e morra a longo prazo.

## 3. A Mecânica de Conversão (Mobilidade Social e Mutação)
A "Tábula Rasa" é um estado primitivo de transição. O motor físico monitoriza as escolhas destes agentes a cada turno e executa Mutações forçadas ao cruzar limiares matemáticos estritos:

1. **A Queda ao Sofismo (Corrupção):**
   - *Gatilho:* Se a Tábula Rasa agir com conformismo passivo constante (`accept_claim`) ou lucrar com mentiras, afundando o seu `Alinhamento Ético <= -20`.
   - *Efeito:* O agente sofre mutação para **Sofista**. Perde a capacidade de acionar o Juiz Semântico e torna-se um gerador de falácias.

2. **A Ascensão Científica (Erudição):**
   - *Gatilho:* Se a Tábula Rasa investir a sua energia na verificação de fatos (`fact_check`), alcançando um `Knowledge_Score >= 20` E mantendo um `Alinhamento > 0`.
   - *Efeito:* O agente sofre mutação para **Erudito**. Ganha acesso ao banco de dados `Synapsys` para combater a desinformação publicamente.

3. **A Ascensão Burguesa (Capitalismo Termodinâmico):**
   - *Gatilho:* Se a Tábula Rasa focar na exploração eficiente de recursos e na acumulação de capital (negociando Ninhos ou poupando energia) sem se envolver em guerras discursivas, atingindo `Energia >= 250`.
   - *Efeito:* O agente sofre mutação para **Artesão**. Ganha o poder de `create_artifact` e passa a gerir a infraestrutura da Pólis.

## 4. O Ciclo Reprodutivo (Herança Genética Epistemológica)
Quando um casal compatível (`0` e `1`) se encontra num Ninho validado:
- **Sacrifício:** O tempo de vida (Lifespan) dos progenitores sofre um corte para gerar a prole.
- **A Criança:** Nasce invariavelmente como uma Tábula Rasa (classe inicial de consumo), independentemente da classe dos pais.
- **A Herança do Conhecimento:** O único privilégio herdado é informacional (o que reduz o custo de movimento da criança desde o Turno 1). A equação é:
  `Knowledge_filho = ((Knowledge_pai + Knowledge_mae) / 2) * 0.8`
  A entropia geracional de 20% garante que nenhuma linhagem permaneça aristocrática para sempre sem continuar a financiar a sua própria educação (os Eruditos).
