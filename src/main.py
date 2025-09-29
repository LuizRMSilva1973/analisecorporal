import os
import sys
import logging

# Adiciona o diretório src ao Python path para permitir importações diretas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import LOGGING_CONFIG
from processing import process_point_cloud
from measurement import extract_circumferences

def setup_logging():
    """Configura o sistema de logging para salvar em arquivo e exibir no console."""
    logging.basicConfig(
        level=LOGGING_CONFIG['level'],
        format=LOGGING_CONFIG['format'],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG['file']),
            logging.StreamHandler(sys.stdout)
        ]
    )

def find_input_file(data_dir="data"):
    """Encontra o primeiro arquivo .ply no diretório de dados."""
    for f in sorted(os.listdir(data_dir)):
        if f.endswith(".ply"):
            return os.path.join(data_dir, f)
    return None

def main():
    """
    Ponto de entrada principal do sistema.
    Orquestra o carregamento, processamento e medição da nuvem de pontos.
    """
    setup_logging()
    logging.info("--- Iniciando Sistema de Medição Corporal ---")

    # Garante que os diretórios de dados e saída existam
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # 1. Encontrar o arquivo de entrada
    input_file = find_input_file()
    if not input_file:
        logging.error("Nenhum arquivo .ply encontrado no diretório 'data'.")
        logging.error("Por favor, adicione um arquivo de nuvem de pontos para processar.")
        return

    logging.info(f"Arquivo de entrada: {input_file}")

    # 2. Processar a nuvem de pontos
    processed_pcd = process_point_cloud(input_file)
    if processed_pcd is None:
        logging.error("O processamento da nuvem de pontos falhou. Abortando.")
        return

    # 3. Extrair as circunferências
    measurements = extract_circumferences(processed_pcd)
    if not measurements:
        logging.warning("Nenhuma medida foi extraída.")
    
    # 4. Salvar o relatório de medições
    output_path = os.path.join("output", "measurements.csv")
    try:
        with open(output_path, "w") as f:
            f.write("Ponto_Medido,Circunferencia_mm\n")
            for point, circumference in measurements.items():
                f.write(f"{point},{circumference:.2f}\n")
        logging.info(f"Relatório de medidas salvo com sucesso em: {output_path}")
    except IOError as e:
        logging.error(f"Falha ao salvar o arquivo de relatório: {e}")

    logging.info("--- Sistema Finalizado ---")

if __name__ == "__main__":
    main()
