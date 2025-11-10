"""
Configuração de fixtures e setup para pytest.
"""

from pathlib import Path

import pytest


@pytest.fixture
def project_root():
    """Retorna o caminho raiz do projeto."""
    return Path(__file__).parent.parent


@pytest.fixture
def geojson_dir(project_root):
    """Retorna o caminho do diretório geojson."""
    return project_root / "geojson"


@pytest.fixture
def sample_geojson():
    """Retorna um GeoJSON de exemplo para testes."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"id": "3550308", "name": "São Paulo", "description": "São Paulo"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-46.826, -24.008],
                            [-46.365, -23.548],
                            [-46.365, -23.979],
                            [-46.826, -24.008],
                        ]
                    ],
                },
            },
            {
                "type": "Feature",
                "properties": {"id": "3509502", "name": "Campinas", "description": "Campinas"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-47.247, -22.731],
                            [-46.873, -22.690],
                            [-46.873, -23.120],
                            [-47.247, -22.731],
                        ]
                    ],
                },
            },
        ],
    }
