"""
Testes básicos de importação dos módulos.
"""


def test_import_config():
    """Testa se o módulo config pode ser importado."""
    from src.geodata_br_mcp import config

    assert config is not None


def test_import_utils():
    """Testa se o módulo utils pode ser importado."""
    from src.geodata_br_mcp import utils

    assert utils is not None


def test_import_server():
    """Testa se o módulo server pode ser importado."""
    from src.geodata_br_mcp import server

    assert server is not None


def test_config_exports():
    """Testa se config exporta as constantes esperadas."""
    from src.geodata_br_mcp.config import (
        IBGE_TO_STATE,
        STATE_TO_IBGE,
        STATES_BY_REGION,
    )

    assert IBGE_TO_STATE is not None
    assert STATE_TO_IBGE is not None
    assert STATES_BY_REGION is not None


def test_utils_exports():
    """Testa se utils exporta as funções esperadas."""
    from src.geodata_br_mcp.utils import (
        normalize_text,
        search_features_by_name,
        validate_geojson_structure,
    )

    assert callable(normalize_text)
    assert callable(search_features_by_name)
    assert callable(validate_geojson_structure)


def test_server_has_app():
    """Testa se server tem o objeto app (FastMCP)."""
    from src.geodata_br_mcp.server import app

    assert app is not None
    # Verifica se é uma instância de FastMCP
    assert hasattr(app, "run")
