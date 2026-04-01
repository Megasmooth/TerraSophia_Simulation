# REGRAS DO MUNDO: TERRASOPHIA 2.0 (FÍSICA E TERMODINÂMICA)

Este documento define as leis imutáveis da simulação. O motor físico do TerraSophia não julga a moralidade dos agentes; ele apenas cobra o custo termodinâmico das suas escolhas.

## 1. Topologia, Finitude e Entropia
- **O Vazio (O Mapa):** O mundo é uma matriz bidimensional expandida de **40x40 células** (1600 blocos). A vasta extensão garante que o isolamento seja a regra e a aglomeração seja um esforço ativo.
- **Relógio Biológico:** Todo agente nasce com um limite absoluto de existência (Lifespan) de **150 turnos**.
- **Entropia Passiva:** Existir custa energia. A cada turno, todo agente sofre uma dedução fixa de energia vital (ex: -2.0) devido ao desgaste celular natural. A imobilidade sem o amparo de uma Ágora resulta em inanição e óbito.

## 2. A Física do Movimento (A Fórmula do Atrito)
O movimento no TerraSophia não é medido em "casas por turno", mas em vetores de deslocamento. A ignorância espacial e física é punida com exaustão.
- **Movimento Vetorial:** O agente executa a ação informando `dx` e `dy`. A distância é calculada pela métrica de Manhattan: `D = |dx| + |dy|`.
- **A Fórmula do Atrito:** A sabedoria (`Knowledge_Score` ou `K`) atua como mitigador do peso físico. A equação de custo de base para cada passo é:
  `Custo_Base = max(1, 5 - (K // 2))`
- **Custo Total:** A energia deduzida da reserva do agente é `Custo_Base * D`.

## 3. Geografia e Infraestrutura (A Pólis)
A sobrevivência a longo prazo exige a suspensão local da entropia através da criação de artefatos.
- **A Fogueira Efêmera (Zonas de Baixa Entropia):**
  - Raio de efeito: **3x3 células**. Agentes dentro deste raio não sofrem a penalidade da Entropia Passiva, mas pagam um imposto automático ao Artesão proprietário.
  - *Combustão por Densidade:* A Fogueira dura no máximo **5 turnos**. A cada turno, ela perde 20% do seu combustível base, MAIS 5% adicionais por cada agente abrigado no seu raio. A superpopulação apaga a fogueira rapidamente.
- **O Ninho (Gentrificação e Êxodo):**
  - É a estrutura imobiliária mandatária para a procriação.
  - *Lei da Oferta e Procura Espacial:* O custo de construção de um Ninho é dinâmico e encarece com a aglomeração: `Custo_Ninho = 30 + (10 * Agentes_no_Raio_5x5)`.
  - Isto força os agentes a realizarem o "Êxodo" para as margens isoladas do grid 40x40 para conseguirem arcar com o custo da fundação de uma família.

## 4. O Espaço de Han e a Termodinâmica da Desinformação
A comunicação obedece à Assimetria de Brandolini e às leis de decaimento acústico. A audição base é restrita a um raio de **5x5 células**.
- **O Ataque (Sofismo):** Custa **1.0 Energia**. Raio: 5x5. Dano: -10 Alinhamento para quem aceita.
- **O Eco Viral (Câmara de Bolha):** Quando um agente aceita uma mentira de graça (`accept_claim`, custo 0.0), ele atua como retransmissor no turno seguinte. 
  - *Decaimento do Sinal:* O raio da mentira ecoada cai para **1x1** (apenas células adjacentes) e o dano cai para **-5 Alinhamento**. A desinformação vira um contágio de proximidade estreita.
- **A Defesa (Erudição):** Custa **5.0 Energia** para acessar o banco de dados real e refutar o Sofista no raio original de 5x5.
- **A Busca pela Verdade:** Custa **3.0 Energia** ao receptor que decide acionar o Juiz Semântico (`fact_check`), garantindo-lhe imunidade à mentira e +10 de Alinhamento.

## 5. Dimorfismo Genético e Herança Epistemológica
A sobrevivência da espécie obedece a restrições biológicas binárias rigorosas, forçando a fricção social.
- **O Dimorfismo 0 e 1:** Todo agente nasce com o gene `0` ou `1`.
- **Regra de Cópula:** A reprodução exige a interseção num Ninho de dois progenitores com DNA oposto (0+1 ou 1+0). Casais homogêneos (0+0 ou 1+1) são rejeitados pelo motor.
- **A Entropia Geracional (0.8):** A carga genética transferida para a prole é informacional.
  `Knowledge_filho = ((Knowledge_pai + Knowledge_mae) / 2) * 0.8`
- Se não houver Eruditos para repor a perda de 20% de conhecimento por geração, a espécie regride à ignorância (Tábula Rasa absoluta), o atrito de movimento volta ao máximo (5.0), e a civilização colapsa.
