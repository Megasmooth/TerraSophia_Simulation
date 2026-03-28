#!/bin/bash
echo "=== Iniciando TerraLingua por 24 horas ==="
# O timeout -s INT 24h envia o sinal de interrupção segura exatas 24h depois.
timeout -s INT 24h python main.py --grid_size 20 --max_ts 100000 --init_agents 8 --model llama3 --max_parallel_workers 1 --ckpt_interval 5 --save_video --exp_name Pesquisa_TerraSophia_Rodada_05

echo "=== Tempo esgotado! Motor finalizado. Gerando CSVs... ==="
# Extrai os dados assim que o vídeo e o ambiente terminarem de ser salvos.
python extrair_dados.py logs/Pesquisa_TerraSophia_Rodada_05

echo "=== Laboratório Concluído! Seus CSVs e o Vídeo estão prontos. ==="
