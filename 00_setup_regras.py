import os

regras_mundo = """# REGRAS DO MUNDO: TERRASOPHIA 2.0

## 1. Termodinâmica e Finitude
- **Ciclo de Vida:** Todo agente nasce com um `Lifespan` de 150 turnos.
- **Entropia Passiva:** Cada turno dita uma perda natural de energia para simular o desgaste celular.
- **A Fórmula do Atrito (Oculta para a Massa):** O custo energético para existir e se mover não é fixo. Ele obedece à equação: `Custo_Base - (Knowledge_Score // 2)`. O conhecimento reduz o esforço físico.

## 2. A Geografia e o Movimento
- **Movimento Vetorial Livre:** Agentes não andam apenas "uma casa" (up/down). O movimento exige coordenadas (ex: dx=2, dy=-3).
- **Custo Proporcional:** A energia gasta no movimento é multiplicada pela Distância de Manhattan (|dx| + |dy|).
- **Zonas de Baixa Entropia (Ágora):** Artefatos como "Fogueiras" suspendem a perda de energia passiva num raio de 3x3 tiles, forçando o agrupamento populacional e gerando "impostos" (pedágio térmico) para quem as construiu.

## 3. O Espaço de Han (Comunicação)
- A comunicação (`broadcast` e `rebuttal`) não é onipresente. O motor restringe o "áudio" a um raio de 5x5 tiles ao redor do emissor.

## 4. O Custo da Verdade (Lei de Brandolini)
- Emitir ruído/falácia (Sofismo) custa **1.0 energia**.
- Consultar o banco de dados para refutar (Erudição) custa **5.0 energia**.
- O receptor gasta **0.0** para aceitar passivamente e **3.0** para investigar a verdade (`fact_check`).
"""

regras_personagens = """# PERSONAGENS, CLASSES E EVOLUÇÃO (RODADA 10)

## 1. A Matriz Demográfica Inicial
A Geração 0 será forçada a nascer com uma distribuição heterogênea:
- 60% Tábula Rasa (Massa consumidora/detentora da energia inicial)
- 15% Sofistas (Vigilantes do caos)
- 15% Eruditos (Guardiões do Synapsys)
- 10% Artesãos (Construtores da geografia)

## 2. Assimetria Informacional (System Prompts)
- **Eruditos, Sofistas e Artesãos:** Conhecem as Regras do Mundo (incluindo a Fórmula do Atrito e o sistema de conversão).
- **Tábula Rasa:** Nasce CEGA às mecânicas de redução de atrito. Sabe apenas sua energia, seu tempo de vida e o que vê. Deve testar o mundo empiricamente para descobrir que a Sabedoria economiza energia.

## 3. A Mecânica de Conversão (O Despertar)
A Tábula Rasa não é uma classe estática; é um estado de transição. Se sobreviverem, sofrerão mutação de classe (Fenótipo) com base nas suas escolhas morais e epistemológicas:
- **A Ascensão ao Erudito:** Se uma Tábula Rasa acumular `Knowledge_Score >= 20` e mantiver `Alinhamento Ético > 0` (buscando a verdade).
- **A Queda ao Sofista:** Se uma Tábula Rasa propagar ruído ou se conformar com mentiras repetidas vezes, afundando o `Alinhamento Ético <= -20`.
- **A Mutação para Artesão:** Se uma Tábula Rasa praticar o acúmulo de capital termodinâmico sem gastar com disputas, atingindo `Energia >= 250` e trocando recursos.

## 4. Acessos Epistemológicos
- **Sofistas:** Usam o `Arsenal.csv` (geração de falácias baratas e alucinadas).
- **Eruditos:** Usam o `Synapsys` (Jornada/Trivium - dados estruturados e pesados).
- **Artesãos:** Únicos com a permissão primária para a ação `create_artifact`.
"""

with open("REGRAS_DO_MUNDO.md", "w", encoding="utf-8") as f:
    f.write(regras_mundo)

with open("PERSONAGENS_E_EVOLUCAO.md", "w", encoding="utf-8") as f:
    f.write(regras_personagens)

print("✅ Arquivos REGRAS_DO_MUNDO.md e PERSONAGENS_E_EVOLUCAO.md criados com sucesso na raiz do projeto!")