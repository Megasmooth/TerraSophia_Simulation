import logging
logging.basicConfig(filename='LOG_ABSOLUTO_RODADA_08_20260328_181143.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

import os
import sys
import signal
import time
from datetime import datetime
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
    resume = args.resume

    # Gerenciador de interrupção (Blindagem contra perda de dados)
    def signal_handler(sig, frame):
        print(f"\n[SISTEMA] Interrupção detectada (Ctrl+C). Salvando estado crítico...")
        if 'runner' in locals():
            # Tenta salvar o checkpoint antes de fechar
            try:
                # O runner salvará o estado de todos os agentes e do ambiente
                checkpoint_path = runner._save_checkpoint(ts=0)
                print(f"[SISTEMA] Checkpoint salvo com sucesso em: {checkpoint_path}")
                print(f"[SISTEMA] LOG ABSOLUTO atualizado. GPU e RAM liberadas.")
            except Exception as e:
                print(f"[ERRO] Falha ao salvar checkpoint: {e}")
        sys.exit(0)

    # Registra o capturador de interrupção no sistema
    signal.signal(signal.SIGINT, signal_handler)

    # O Runner lerá a configuração e instanciará o mundo
    print(f"[INÍCIO] Instanciando TerraSophia 2.0...")
    runner = SimulationRunner(params=params, resume=resume)

    # FIX DE EXPANSÃO TEMPORAL (RESUME)
    if resume:
        print(f"[RETOMADA] Carregando progresso anterior. Novo limite: {args.max_ts} turnos.")
        runner.params.run.max_ts = args.max_ts
        if hasattr(runner, 'max_ts'):
            runner.max_ts = args.max_ts

    # Inicia a simulação dentro de um bloco de segurança
    try:
        print(f"[EXECUÇÃO] Rodada iniciada em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        runner.run()
    except Exception as e:
        print(f"[CRÍTICO] Erro durante a execução: {e}")
        # Tenta salvar mesmo em caso de erro inesperado
        runner._save_checkpoint(ts=0)
        raise e

if __name__ == "__main__":
    main()