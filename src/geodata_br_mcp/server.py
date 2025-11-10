import os
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("geodata-br-mcp")

# Importa configurações do módulo config
from .config import (
    IBGE_TO_STATE,
    STATE_TO_IBGE,
    GEOJSON_DIRECTORY,
    GEOJSON_FILENAME_PATTERN,
    ENV_DATA_PATH,
    MCP_SERVER_NAME,
    get_state_code,
)

# Importa funções utilitárias
from .utils import (
    load_geojson_with_cache,
    search_features_by_name,
    search_features_by_ibge,
    get_geojson_summary,
)

# Caminho do repositório local geodata-br (configure via env)
# Por padrão, usa o diretório onde o script está localizado
DEFAULT_PATH = Path(__file__).parent.parent.parent
DATA_ROOT = Path(os.environ.get(ENV_DATA_PATH, str(DEFAULT_PATH))).expanduser().resolve()

app = FastMCP(MCP_SERVER_NAME, dependencies=["mcp"])


def _assert_data_root():
    """Verifica se o diretório de dados existe."""
    if not DATA_ROOT.exists():
        logger.error(f"DATA_ROOT não encontrado: {DATA_ROOT}")
        raise RuntimeError(
            f"GEODATA_BR_PATH inválido ou não encontrado: {DATA_ROOT}\n"
            f"Configure a variável de ambiente GEODATA_BR_PATH com o caminho do repositório."
        )
    logger.info(f"DATA_ROOT configurado: {DATA_ROOT}")


def _get_state_file(uf_or_code: str) -> Path:
    """Retorna o caminho do arquivo GeoJSON para uma UF ou código IBGE.
    
    Args:
        uf_or_code: Sigla da UF (ex: "SP") ou código IBGE (ex: "35")
    
    Returns:
        Path do arquivo geojs-XX-mun.json
    """
    code = get_state_code(uf_or_code)
    filename = GEOJSON_FILENAME_PATTERN.format(code=code)
    return DATA_ROOT / GEOJSON_DIRECTORY / filename


def _load_state_geojson(uf_or_code: str) -> Dict[str, Any]:
    """Carrega o GeoJSON completo de um estado (com cache)."""
    file_path = _get_state_file(uf_or_code)
    return load_geojson_with_cache(file_path)


@app.tool()
def list_states() -> List[Dict[str, str]]:
    """Lista todos os estados disponíveis no repositório geodata-br.
    
    Returns:
        Lista de dicionários com informações dos estados (código IBGE, UF, nome, região)
    """
    logger.info("Tool list_states() chamada")
    _assert_data_root()
    
    states = []
    geojson_dir = DATA_ROOT / "geojson"
    
    if not geojson_dir.exists():
        logger.warning(f"Diretório geojson não encontrado: {geojson_dir}")
        return []
    
    # Lista os arquivos geojs-XX-mun.json
    for file in sorted(geojson_dir.glob("geojs-*-mun.json")):
        # Extrai o código IBGE do nome do arquivo
        code = file.stem.split("-")[1]
        
        if code in IBGE_TO_STATE:
            state_info = IBGE_TO_STATE[code].copy()
            state_info["ibge_code"] = code
            states.append(state_info)
    
    logger.info(f"Retornando {len(states)} estados")
    return states


@app.tool()
def get_state_info(uf: str = Field(description="Sigla da UF (ex: SP, RJ) ou código IBGE")) -> Dict[str, Any]:
    """Obtém informações detalhadas sobre um estado.
    
    Args:
        uf: Sigla da UF (ex: "SP") ou código IBGE (ex: "35")
    
    Returns:
        Dicionário com informações do estado incluindo quantidade de municípios
    """
    logger.info(f"Tool get_state_info() chamada com uf={uf}")
    _assert_data_root()
    
    # Carrega o GeoJSON
    geojson_data = _load_state_geojson(uf)
    
    # Obtém informações do estado usando config
    from .config import get_state_info as config_get_state_info
    state_info = config_get_state_info(uf)
    
    # Conta municípios
    if "features" in geojson_data:
        state_info["total_municipalities"] = len(geojson_data["features"])
        logger.info(f"Estado {uf}: {state_info['total_municipalities']} municípios")
    
    return state_info


@app.tool()
def list_municipalities(uf: str = Field(description="Sigla da UF (ex: SP, RJ) ou código IBGE")) -> List[Dict[str, str]]:
    """Lista todos os municípios de um estado.
    
    Args:
        uf: Sigla da UF (ex: "SP") ou código IBGE (ex: "35")
    
    Returns:
        Lista de municípios com id (código IBGE), nome e descrição
    """
    logger.info(f"Tool list_municipalities() chamada com uf={uf}")
    _assert_data_root()
    
    geojson_data = _load_state_geojson(uf)
    
    municipalities = []
    for feature in geojson_data.get("features", []):
        props = feature.get("properties", {})
        municipalities.append({
            "id": props.get("id", ""),
            "name": props.get("name", ""),
            "description": props.get("description", "")
        })
    
    logger.info(f"Retornando {len(municipalities)} municípios de {uf}")
    return municipalities


@app.tool()
def get_municipality_geojson(
    uf: str = Field(description="Sigla da UF (ex: SP, RJ) ou código IBGE"),
    municipality_name: str = Field(description="Nome do município (ex: São Paulo, Campinas)")
) -> Dict[str, Any]:
    """Obtém o GeoJSON de um município específico.
    
    Args:
        uf: Sigla da UF (ex: "SP") ou código IBGE (ex: "35")
        municipality_name: Nome do município (busca case-insensitive e normalizada)
    
    Returns:
        Feature GeoJSON do município
    """
    logger.info(f"Tool get_municipality_geojson() chamada com uf={uf}, municipality_name={municipality_name}")
    _assert_data_root()
    
    geojson_data = _load_state_geojson(uf)
    features = geojson_data.get("features", [])
    
    # Usa a função de busca do utils (com normalização de texto)
    results = search_features_by_name(features, municipality_name)
    
    if results:
        result_name = results[0].get("properties", {}).get("name", "")
        logger.info(f"Município encontrado: {result_name}")
        return results[0]  # Retorna o primeiro resultado
    
    logger.warning(f"Município '{municipality_name}' não encontrado em {uf.upper()}")
    raise ValueError(f"Município '{municipality_name}' não encontrado em {uf.upper()}")


@app.tool()
def search_municipality_by_ibge(
    ibge_code: str = Field(description="Código IBGE do município (7 dígitos)")
) -> Dict[str, Any]:
    """Busca um município pelo código IBGE.
    
    Args:
        ibge_code: Código IBGE de 7 dígitos do município
    
    Returns:
        Feature GeoJSON do município
    """
    logger.info(f"Tool search_municipality_by_ibge() chamada com ibge_code={ibge_code}")
    _assert_data_root()
    
    # Os 2 primeiros dígitos são o código do estado
    if len(ibge_code) < 2:
        logger.error(f"Código IBGE inválido (muito curto): {ibge_code}")
        raise ValueError("Código IBGE deve ter pelo menos 2 dígitos")
    
    state_code = ibge_code[:2]
    
    if state_code not in IBGE_TO_STATE:
        logger.error(f"Código de estado inválido: {state_code}")
        raise ValueError(f"Código de estado inválido: {state_code}")
    
    geojson_data = _load_state_geojson(state_code)
    features = geojson_data.get("features", [])
    
    # Usa a função de busca do utils
    result = search_features_by_ibge(features, ibge_code)
    
    if result:
        result_name = result.get("properties", {}).get("name", "")
        logger.info(f"Município encontrado: {result_name} ({ibge_code})")
        return result
    
    logger.warning(f"Município com código IBGE {ibge_code} não encontrado")
    raise ValueError(f"Município com código IBGE {ibge_code} não encontrado")


@app.tool()
def get_brazil_geojson() -> Dict[str, Any]:
    """Obtém o GeoJSON completo do Brasil com todos os municípios.
    
    Returns:
        GeoJSON FeatureCollection com todos os municípios do Brasil
    """
    logger.info("Tool get_brazil_geojson() chamada")
    logger.warning("Carregando arquivo grande (~60MB)")
    _assert_data_root()
    
    result = _load_state_geojson("100")
    feature_count = len(result.get("features", []))
    logger.info(f"GeoJSON do Brasil carregado: {feature_count} municípios")
    
    return result


if __name__ == "__main__":
    # Inicia o servidor MCP via stdio
    logger.info("=== Geodata-BR MCP Server Iniciando ===")
    logger.info(f"Python Path: {os.sys.executable}")
    logger.info(f"DATA_ROOT: {DATA_ROOT}")
    logger.info(f"Versão: 0.1.0")
    
    try:
        app.run()
    except Exception as e:
        logger.error(f"Erro fatal ao executar servidor: {e}", exc_info=True)
        raise