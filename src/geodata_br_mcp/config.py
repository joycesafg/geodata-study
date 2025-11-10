"""
Configurações e mapeamentos para o servidor MCP Geodata-BR.

Este módulo contém todos os mapeamentos de códigos IBGE para estados brasileiros,
organizados por região e com informações completas.
"""

# Mapeamento completo de códigos IBGE para estados brasileiros
# Formato: código IBGE -> {uf, nome completo, região}
IBGE_TO_STATE: dict[str, dict[str, str]] = {
    # Região Norte
    "11": {"uf": "RO", "name": "Rondônia", "region": "Norte"},
    "12": {"uf": "AC", "name": "Acre", "region": "Norte"},
    "13": {"uf": "AM", "name": "Amazonas", "region": "Norte"},
    "14": {"uf": "RR", "name": "Roraima", "region": "Norte"},
    "15": {"uf": "PA", "name": "Pará", "region": "Norte"},
    "16": {"uf": "AP", "name": "Amapá", "region": "Norte"},
    "17": {"uf": "TO", "name": "Tocantins", "region": "Norte"},
    # Região Nordeste
    "21": {"uf": "MA", "name": "Maranhão", "region": "Nordeste"},
    "22": {"uf": "PI", "name": "Piauí", "region": "Nordeste"},
    "23": {"uf": "CE", "name": "Ceará", "region": "Nordeste"},
    "24": {"uf": "RN", "name": "Rio Grande do Norte", "region": "Nordeste"},
    "25": {"uf": "PB", "name": "Paraíba", "region": "Nordeste"},
    "26": {"uf": "PE", "name": "Pernambuco", "region": "Nordeste"},
    "27": {"uf": "AL", "name": "Alagoas", "region": "Nordeste"},
    "28": {"uf": "SE", "name": "Sergipe", "region": "Nordeste"},
    "29": {"uf": "BA", "name": "Bahia", "region": "Nordeste"},
    # Região Sudeste
    "31": {"uf": "MG", "name": "Minas Gerais", "region": "Sudeste"},
    "32": {"uf": "ES", "name": "Espírito Santo", "region": "Sudeste"},
    "33": {"uf": "RJ", "name": "Rio de Janeiro", "region": "Sudeste"},
    "35": {"uf": "SP", "name": "São Paulo", "region": "Sudeste"},
    # Região Sul
    "41": {"uf": "PR", "name": "Paraná", "region": "Sul"},
    "42": {"uf": "SC", "name": "Santa Catarina", "region": "Sul"},
    "43": {"uf": "RS", "name": "Rio Grande do Sul", "region": "Sul"},
    # Região Centro-Oeste
    "50": {"uf": "MS", "name": "Mato Grosso do Sul", "region": "Centro-Oeste"},
    "51": {"uf": "MT", "name": "Mato Grosso", "region": "Centro-Oeste"},
    "52": {"uf": "GO", "name": "Goiás", "region": "Centro-Oeste"},
    "53": {"uf": "DF", "name": "Distrito Federal", "region": "Centro-Oeste"},
    # Brasil completo
    "100": {"uf": "BR", "name": "Brasil", "region": "Brasil"},
}

# Mapeamento reverso: UF -> código IBGE
# Exemplo: "SP" -> "35", "RJ" -> "33"
STATE_TO_IBGE: dict[str, str] = {v["uf"]: k for k, v in IBGE_TO_STATE.items()}

# Agrupamento de estados por região
STATES_BY_REGION: dict[str, list[str]] = {
    "Norte": ["RO", "AC", "AM", "RR", "PA", "AP", "TO"],
    "Nordeste": ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"],
    "Sudeste": ["MG", "ES", "RJ", "SP"],
    "Sul": ["PR", "SC", "RS"],
    "Centro-Oeste": ["MS", "MT", "GO", "DF"],
}

# Mapeamento de região -> código IBGE
REGION_TO_IBGE_CODES: dict[str, list[str]] = {
    region: [STATE_TO_IBGE[uf] for uf in ufs] for region, ufs in STATES_BY_REGION.items()
}

# Nome dos arquivos GeoJSON por padrão
GEOJSON_FILENAME_PATTERN = "geojs-{code}-mun.json"
GEOJSON_DIRECTORY = "geojson"

# Configurações do servidor MCP
MCP_SERVER_NAME = "geodata-br"
MCP_SERVER_VERSION = "0.1.0"
MCP_SERVER_DESCRIPTION = (
    "Servidor MCP para acesso a dados geográficos do Brasil (GeoJSON de municípios por estado)"
)

# Variáveis de ambiente
ENV_DATA_PATH = "GEODATA_BR_PATH"


# Validação básica
def validate_uf(uf: str) -> bool:
    """Valida se uma sigla de UF é válida.

    Args:
        uf: Sigla da UF (ex: "SP", "RJ")

    Returns:
        True se for válida, False caso contrário
    """
    return uf.upper() in STATE_TO_IBGE


def validate_ibge_code(code: str) -> bool:
    """Valida se um código IBGE de estado é válido.

    Args:
        code: Código IBGE (ex: "35", "33")

    Returns:
        True se for válido, False caso contrário
    """
    return code in IBGE_TO_STATE


def get_state_code(uf_or_code: str) -> str:
    """Retorna o código IBGE a partir de uma UF ou código.

    Args:
        uf_or_code: Sigla da UF (ex: "SP") ou código IBGE (ex: "35")

    Returns:
        Código IBGE do estado

    Raises:
        ValueError: Se a UF ou código for inválido
    """
    # Se já é um código IBGE válido
    if uf_or_code in IBGE_TO_STATE:
        return uf_or_code

    # Se é uma sigla de UF
    uf_upper = uf_or_code.upper()
    if uf_upper in STATE_TO_IBGE:
        return STATE_TO_IBGE[uf_upper]

    raise ValueError(f"UF ou código IBGE inválido: {uf_or_code}")


def get_state_info(uf_or_code: str) -> dict[str, str]:
    """Retorna informações completas de um estado.

    Args:
        uf_or_code: Sigla da UF (ex: "SP") ou código IBGE (ex: "35")

    Returns:
        Dicionário com uf, nome, região e código IBGE

    Raises:
        ValueError: Se a UF ou código for inválido
    """
    code = get_state_code(uf_or_code)
    info = IBGE_TO_STATE[code].copy()
    info["ibge_code"] = code
    return info


def get_states_by_region(region: str) -> list[dict[str, str]]:
    """Retorna todos os estados de uma região.

    Args:
        region: Nome da região (Norte, Nordeste, Sudeste, Sul, Centro-Oeste)

    Returns:
        Lista de dicionários com informações dos estados da região

    Raises:
        ValueError: Se a região for inválida
    """
    if region not in STATES_BY_REGION:
        valid_regions = ", ".join(STATES_BY_REGION.keys())
        raise ValueError(f"Região inválida: {region}. Regiões válidas: {valid_regions}")

    return [get_state_info(uf) for uf in STATES_BY_REGION[region]]


def get_filename_for_state(uf_or_code: str) -> str:
    """Retorna o nome do arquivo GeoJSON para um estado.

    Args:
        uf_or_code: Sigla da UF (ex: "SP") ou código IBGE (ex: "35")

    Returns:
        Nome do arquivo (ex: "geojs-35-mun.json")
    """
    code = get_state_code(uf_or_code)
    return GEOJSON_FILENAME_PATTERN.format(code=code)


# Informações úteis para debug
def get_all_states() -> list[dict[str, str]]:
    """Retorna informações de todos os estados.

    Returns:
        Lista com todos os estados e suas informações
    """
    return [get_state_info(code) for code in sorted(IBGE_TO_STATE.keys())]


def get_total_states() -> int:
    """Retorna o número total de estados (excluindo Brasil).

    Returns:
        Número de estados (27)
    """
    return len(IBGE_TO_STATE) - 1  # -1 para excluir "100" (Brasil)


# Exporta as principais constantes e funções
__all__ = [
    "IBGE_TO_STATE",
    "STATE_TO_IBGE",
    "STATES_BY_REGION",
    "REGION_TO_IBGE_CODES",
    "GEOJSON_FILENAME_PATTERN",
    "GEOJSON_DIRECTORY",
    "MCP_SERVER_NAME",
    "MCP_SERVER_VERSION",
    "MCP_SERVER_DESCRIPTION",
    "ENV_DATA_PATH",
    "validate_uf",
    "validate_ibge_code",
    "get_state_code",
    "get_state_info",
    "get_states_by_region",
    "get_filename_for_state",
    "get_all_states",
    "get_total_states",
]
