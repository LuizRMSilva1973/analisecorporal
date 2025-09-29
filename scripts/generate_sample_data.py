import open3d as o3d
import numpy as np
import os

def generate_sample_body(output_dir="data"):
    """
    Gera uma nuvem de pontos em forma de cilindro para simular um corpo humano simplificado.
    Salva o resultado como um arquivo .ply.
    """
    print("Gerando corpo de prova 3D...")
    
    # Parâmetros do cilindro (corpo)
    height = 1.8  # 1.8 metros de altura
    radius = 0.3  # 0.3 metros de raio
    num_points = 20000

    # Gerar pontos em coordenadas cilíndricas
    theta = np.random.rand(num_points) * 2.0 * np.pi  # Ângulo
    z = (np.random.rand(num_points) - 0.5) * height # Altura (centralizado em 0)
    r = radius * np.sqrt(np.random.rand(num_points)) # Raio com distribuição uniforme de área

    # Converter para coordenadas cartesianas
    x = r * np.cos(theta)
    y = z # Usando Y como eixo vertical
    z_cartesian = r * np.sin(theta)

    points = np.vstack((x, y, z_cartesian)).T

    # Adicionar um pouco de ruído para realismo
    noise = np.random.normal(scale=0.01, size=points.shape)
    points += noise

    # Criar objeto PointCloud do Open3D
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    # Garantir que o diretório de saída exista
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "corpo_de_prova.ply")

    # Salvar o arquivo .ply
    o3d.io.write_point_cloud(output_path, pcd)
    print(f"Corpo de prova salvo em: {output_path}")

if __name__ == "__main__":
    # Este script deve ser executado do diretório raiz do projeto
    generate_sample_body()
