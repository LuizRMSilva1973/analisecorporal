# Análise Corporal 3D — Medição Automática de Circunferências

[![CI](https://github.com/LuizRMSilva1973/analisecorporal/actions/workflows/ci.yml/badge.svg)](https://github.com/LuizRMSilva1973/analisecorporal/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Open3D](https://img.shields.io/badge/Open3D-ready-success)](http://www.open3d.org/)
[![License](https://img.shields.io/github/license/LuizRMSilva1973/analisecorporal)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/LuizRMSilva1973/analisecorporal)](https://github.com/LuizRMSilva1973/analisecorporal/commits/main)
[![Repo size](https://img.shields.io/github/repo-size/LuizRMSilva1973/analisecorporal)](https://github.com/LuizRMSilva1973/analisecorporal)

Sistema em Python para medir circunferências corporais automaticamente a partir de nuvens de pontos 3D (formato `.ply`). O pipeline realiza pré‑processamento geométrico e extrai perímetros em alturas padronizadas do corpo, gerando um relatório em CSV. Projetado para funcionar com dados de scanners 3D e arquivos sintéticos de teste.

— Consulte também: `proposta_tecnica_comercial_scaner_corporal.md`

## Visão Geral

- Entrada: nuvem de pontos 3D do corpo (`data/*.ply`).
- Processamento: remoção de outliers, centralização, estimativa de normais e fatiamento horizontal (eixo Y como vertical).
- Medição: projeção da fatia no plano XZ, cálculo do casco convexo (Convex Hull) e soma das arestas para obter a circunferência (mm).
- Saída: `output/measurements.csv` com as circunferências por ponto anatômico e `output/processing.log` com o log do processamento.

## Principais Recursos

- Medições em alturas padronizadas (percentuais da altura total): panturrilha, coxa, abdômen, cintura e peito.
- Pipeline robusto com remoção estatística de outliers e estimativa de normais (Open3D).
- Arquitetura simples, modular e testável (`src/processing.py`, `src/measurement.py`, `src/config.py`).
- Script utilitário para gerar nuvem de pontos sintética de um “corpo de prova”.

## Arquitetura e Fluxo

1. Carregamento (`Open3D`): leitura do `.ply` para `PointCloud`.
2. Limpeza: remoção de outliers estatísticos conforme `PROCESSING_PARAMS`.
3. Centralização: recentra o modelo na origem e estima normais se necessário.
4. Fatiamento: para cada ponto de interesse em `MEASUREMENT_POINTS`, define‑se uma altura `slice_y` e selecionam‑se pontos dentro de `slice_thickness`.
5. Projeção 2D: projeta a fatia no plano XZ e calcula o casco convexo (`scipy.spatial.ConvexHull`).
6. Perímetro: soma do comprimento das arestas do casco convexo, convertido para milímetros.
7. Relatório: salva `output/measurements.csv` e um log completo em `output/processing.log`.

Arquivos‑chave:
- `src/main.py`: orquestra o fluxo de ponta a ponta e salva o relatório.
- `src/processing.py`: pré‑processamento da nuvem (outliers, centralização, normais).
- `src/measurement.py`: cálculo das circunferências por fatia.
- `src/config.py`: parâmetros do pipeline (processamento, pontos de medida e logging).

### Visual

Diagrama do pipeline de medição:

```mermaid
graph LR
    A["PLY em data"] --> B["Carregar nuvem Open3D"];
    B --> C["Remover outliers"];
    C --> D["Centralizar e normais"];
    D --> E["Fatiar por Y em pontos"];
    E --> F["Projeção XZ"];
    F --> G["Casco convexo (ConvexHull)"];
    G --> H["Somar arestas → perímetro"];
    H --> I["Salvar CSV e log"];
```

Opcionalmente, substitua por um print/gif do seu fluxo real:

![Pipeline preview](docs/assets/pipeline.png)

## Requisitos

- Python 3.10+
- Dependências (instaladas via `pip`): `numpy`, `open3d`, `scipy`, `scikit-learn`, `flask`, `pytest`.
  - Observação: `open3d` pode exigir bibliotecas de sistema (ex.: `libgl1` em Linux).

## Instalação

Opcional, mas recomendado, use um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

## Uso

1. Adicione um arquivo `.ply` em `data/` (ex.: `data/corpo_de_prova.ply`).
2. Execute:
   ```bash
   python src/main.py
   ```
3. Resultados:
   - `output/measurements.csv`: `Ponto_Medido,Circunferencia_mm`.
   - `output/processing.log`: log detalhado do pipeline.

### Exemplo de Saída

`output/measurements.csv` (exemplo):

```csv
Ponto_Medido,Circunferencia_mm
perna_panturrilha,310.42
perna_coxa,495.87
torso_abdomen,890.13
torso_cintura,780.66
torso_peito,960.55
```

## Gerar Dados de Exemplo (Opcional)

Para testar sem um scanner, gere uma nuvem sintética cilíndrica:

```bash
python scripts/generate_sample_data.py
python src/main.py
```

## Configuração

Edite `src/config.py` para ajustar:
- `PROCESSING_PARAMS`: vizinhança e desvio para remoção de outliers; raio e `max_nn` para normais.
- `MEASUREMENT_POINTS`: mapeia nomes dos pontos a percentuais da altura (0.0 = pés, 1.0 = cabeça).
- `MEASUREMENT_PARAMS.slice_thickness_m`: espessura da fatia (m) usada no fatiamento.
- `LOGGING_CONFIG`: nível, formato e arquivo de log.

## Suposições e Limitações

- Eixo vertical: assume‑se Y como vertical. Caso o scanner use outro eixo, alinhe os dados antes.
- Unidades: assume‑se que o `.ply` está em metros; a saída é convertida para milímetros.
- Casco convexo: aproxima o contorno como convexo; concavidades locais podem subestimar a circunferência real.
- Qualidade da nuvem: ruídos, buracos e baixa densidade afetam a precisão; ajuste `slice_thickness_m` e filtros.

## Testes

O pacote inclui um teste que valida a medição em um cilindro ideal:

```bash
pytest -q
```

## Roadmap (Ideias Futuras)

- Alinhamento automático por PCA/ICP para padronizar a orientação do corpo.
- Identificação de marcos anatômicos por segmentação (ex.: junções de membros).
- Contorno não convexo (ex.: alfa‑shape) para capturar concavidades.
- Exportação adicional: JSON com metadados e gráficos das fatias.
- Interface web minimal (Flask) para upload e visualização.

## Licença

Este projeto é distribuído sob termos definidos pelo(s) autor(es).
