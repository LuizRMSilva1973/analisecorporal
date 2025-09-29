import open3d as o3d
import logging
from config import PROCESSING_PARAMS

def process_point_cloud(file_path):
    """
    Carrega e pré-processa a nuvem de pontos.
    Inclui carregamento, remoção de outliers e alinhamento.
    """
    logging.info(f"Processando o arquivo: {file_path}")
    try:
        pcd = o3d.io.read_point_cloud(file_path)
        if not pcd.has_points():
            logging.error("A nuvem de pontos está vazia ou não pôde ser lida.")
            return None
    except Exception as e:
        logging.error(f"Falha ao ler o arquivo de nuvem de pontos: {e}")
        return None

    # 1. Remoção de outliers para limpar ruídos
    logging.info("Removendo outliers...")
    pcd = pcd.remove_statistical_outlier(
        nb_neighbors=PROCESSING_PARAMS["outlier_neighbors"],
        std_ratio=PROCESSING_PARAMS["outlier_std_ratio"]
    )[0]

    # 2. Alinhamento e centralização
    # Em um cenário real, isso poderia envolver algoritmos de registro ou PCA para alinhar o eixo do corpo com o eixo Y.
    # Por enquanto, apenas centralizamos o modelo na origem.
    logging.info("Centralizando a nuvem de pontos.")
    pcd.center()

    # 3. Estimativa de normais (necessário para algumas análises e visualizações)
    if not pcd.has_normals():
        logging.info("Estimando normais da nuvem de pontos.")
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=PROCESSING_PARAMS["normal_estimation_radius"],
                max_nn=PROCESSING_PARAMS["normal_estimation_max_nn"]
            )
        )

    logging.info("Pré-processamento da nuvem de pontos concluído.")
    return pcd
