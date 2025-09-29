import numpy as np
import logging
from scipy.spatial import ConvexHull
from config import MEASUREMENT_POINTS, MEASUREMENT_PARAMS

def extract_circumferences(pcd):
    """
    Extrai as circunferências do corpo em pontos padronizados.

    Args:
        pcd (open3d.geometry.PointCloud): A nuvem de pontos pré-processada.

    Returns:
        dict: Um dicionário com os nomes dos pontos e suas circunferências em mm.
    """
    logging.info("Iniciando a extração de circunferências.")
    measurements = {}

    # Obter os limites verticais do modelo (assumindo Y como eixo vertical)
    min_bound = pcd.get_min_bound()
    max_bound = pcd.get_max_bound()
    height = max_bound[1] - min_bound[1]

    if height <= 0:
        logging.error("Altura do modelo 3D é zero ou negativa. Impossível medir.")
        return {}

    points = np.asarray(pcd.points)

    for name, percentage in MEASUREMENT_POINTS.items():
        # Calcular a altura exata do corte (slice)
        slice_y = min_bound[1] + height * percentage
        logging.debug(f"Medindo o ponto '{name}' na altura {slice_y:.2f}m.")

        # Selecionar os pontos que compõem a fatia horizontal
        slice_thickness = MEASUREMENT_PARAMS["slice_thickness_m"]
        slice_indices = np.where(np.abs(points[:, 1] - slice_y) < (slice_thickness / 2.0))[0]

        if len(slice_indices) < 20: # Aumentado o limite mínimo de pontos
            logging.warning(f"Pontos insuficientes ({len(slice_indices)}) para medir '{name}'.")
            measurements[name] = 0
            continue

        # Projetar os pontos da fatia no plano 2D (X, Z)
        slice_points_2d = points[slice_indices][:, [0, 2]]

        try:
            # Calcular o casco convexo (Convex Hull) para definir o contorno
            hull = ConvexHull(slice_points_2d)
            
            # Calcular o perímetro somando o comprimento de cada aresta do casco
            circumference_m = 0
            for simplex in hull.simplices:
                p1 = slice_points_2d[simplex[0]]
                p2 = slice_points_2d[simplex[1]]
                circumference_m += np.linalg.norm(p1 - p2)

            measurements[name] = circumference_m * 1000  # Converter para milímetros
            logging.info(f"Medida para '{name}': {measurements[name]:.2f} mm")

        except Exception as e:
            logging.error(f"Falha ao calcular o casco convexo para '{name}': {e}. A medição foi ignorada.")
            measurements[name] = 0

    logging.info("Extração de circunferências concluída.")
    return measurements
