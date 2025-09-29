# Arquivo de Configuração para o Sistema de Medição

# Parâmetros de processamento da nuvem de pontos
PROCESSING_PARAMS = {
    "outlier_neighbors": 20,
    "outlier_std_ratio": 2.0,
    "normal_estimation_radius": 0.1,
    "normal_estimation_max_nn": 30
}

# Pontos de medição (nome: porcentagem da altura total, de baixo para cima)
# 0.0 é a base (pés), 1.0 é o topo (cabeça).
MEASUREMENT_POINTS = {
    "perna_panturrilha": 0.25,
    "perna_coxa": 0.45,
    "torso_abdomen": 0.60,
    "torso_cintura": 0.65,
    "torso_peito": 0.70,
}

# Parâmetros para o corte e medição
MEASUREMENT_PARAMS = {
    "slice_thickness_m": 0.01  # Espessura da fatia para análise (1 cm)
}

# Configurações de Logging
LOGGING_CONFIG = {
    "level": "INFO", # Nível do log (DEBUG, INFO, WARNING, ERROR)
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "file": "output/processing.log"
}
