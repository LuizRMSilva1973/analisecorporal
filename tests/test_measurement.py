import pytest
import numpy as np
import open3d as o3d
import sys
import os

# Adiciona o diretório src ao path para poder importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from measurement import extract_circumferences

@pytest.fixture
def sample_cylinder_pcd():
    """Cria uma nuvem de pontos de um cilindro para usar como base nos testes."""
    height = 2.0
    radius = 0.5
    points = []
    # Cria um cilindro simples
    for y in np.linspace(-height / 2, height / 2, 100):
        for angle in np.linspace(0, 2 * np.pi, 100):
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)
            points.append([x, y, z])
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.array(points))
    return pcd

def test_extract_circumferences(sample_cylinder_pcd):
    """
    Testa a função de extração de circunferência em um cilindro perfeito.
    A circunferência em qualquer altura deve ser 2 * pi * r.
    """
    measurements = extract_circumferences(sample_cylinder_pcd)
    
    # Circunferência esperada (2 * pi * r) em mm
    expected_circumference = 2 * np.pi * 0.5 * 1000
    
    assert len(measurements) > 0, "Nenhuma medida foi extraída"
    
    for point, circumference in measurements.items():
        # Verifica se a medida calculada está próxima da esperada (margem de 2%)
        assert np.isclose(circumference, expected_circumference, rtol=0.02), \
            f"Medida incorreta para '{point}'. Esperado: {expected_circumference:.2f}, Obtido: {circumference:.2f}"