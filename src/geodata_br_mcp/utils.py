"""
Funções utilitárias para o servidor MCP Geodata-BR.

Este módulo contém funções auxiliares para processamento de GeoJSON,
cache, busca e validação de dados.
"""

import json
import re
from pathlib import Path
from typing import Any

# Cache simples em memória para arquivos GeoJSON
_geojson_cache: dict[str, dict[str, Any]] = {}


def load_geojson_with_cache(file_path: Path) -> dict[str, Any]:
    """Carrega um arquivo GeoJSON com cache em memória.

    Args:
        file_path: Caminho do arquivo GeoJSON

    Returns:
        Dados GeoJSON parseados

    Raises:
        FileNotFoundError: Se o arquivo não existir
        json.JSONDecodeError: Se o arquivo não for JSON válido
    """
    file_str = str(file_path)

    # Verifica se está no cache
    if file_str in _geojson_cache:
        return _geojson_cache[file_str]

    # Carrega do disco
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Armazena no cache
    _geojson_cache[file_str] = data

    return data


def clear_cache():
    """Limpa o cache de arquivos GeoJSON."""
    global _geojson_cache
    _geojson_cache.clear()


def get_cache_size() -> int:
    """Retorna o número de arquivos no cache.

    Returns:
        Número de arquivos em cache
    """
    return len(_geojson_cache)


def normalize_text(text: str) -> str:
    """Normaliza texto para busca (remove acentos, converte para minúsculas).

    Args:
        text: Texto a ser normalizado

    Returns:
        Texto normalizado
    """
    # Remove acentos comuns
    replacements = {
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "ä": "a",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "í": "i",
        "ì": "i",
        "î": "i",
        "ï": "i",
        "ó": "o",
        "ò": "o",
        "õ": "o",
        "ô": "o",
        "ö": "o",
        "ú": "u",
        "ù": "u",
        "û": "u",
        "ü": "u",
        "ç": "c",
        "ñ": "n",
        "Á": "A",
        "À": "A",
        "Ã": "A",
        "Â": "A",
        "Ä": "A",
        "É": "E",
        "È": "E",
        "Ê": "E",
        "Ë": "E",
        "Í": "I",
        "Ì": "I",
        "Î": "I",
        "Ï": "I",
        "Ó": "O",
        "Ò": "O",
        "Õ": "O",
        "Ô": "O",
        "Ö": "O",
        "Ú": "U",
        "Ù": "U",
        "Û": "U",
        "Ü": "U",
        "Ç": "C",
        "Ñ": "N",
    }

    normalized = text
    for char, replacement in replacements.items():
        normalized = normalized.replace(char, replacement)

    return normalized.lower().strip()


def search_features_by_name(
    features: list[dict[str, Any]], search_term: str, exact: bool = False
) -> list[dict[str, Any]]:
    """Busca features por nome (com ou sem normalização).

    Args:
        features: Lista de features GeoJSON
        search_term: Termo de busca
        exact: Se True, busca exata; se False, busca parcial normalizada

    Returns:
        Lista de features que correspondem à busca
    """
    results = []

    if exact:
        # Busca exata (case-sensitive)
        for feature in features:
            props = feature.get("properties", {})
            name = props.get("name", "")
            if name == search_term:
                results.append(feature)
    else:
        # Busca normalizada e parcial
        normalized_search = normalize_text(search_term)
        for feature in features:
            props = feature.get("properties", {})
            name = props.get("name", "")
            normalized_name = normalize_text(name)

            if normalized_search in normalized_name or normalized_name in normalized_search:
                results.append(feature)

    return results


def search_features_by_ibge(
    features: list[dict[str, Any]], ibge_code: str
) -> dict[str, Any] | None:
    """Busca uma feature por código IBGE.

    Args:
        features: Lista de features GeoJSON
        ibge_code: Código IBGE do município

    Returns:
        Feature encontrada ou None
    """
    for feature in features:
        props = feature.get("properties", {})
        if props.get("id") == ibge_code:
            return feature
    return None


def filter_features_by_pattern(
    features: list[dict[str, Any]], pattern: str, field: str = "name"
) -> list[dict[str, Any]]:
    """Filtra features usando regex em um campo específico.

    Args:
        features: Lista de features GeoJSON
        pattern: Padrão regex
        field: Campo a ser buscado (padrão: "name")

    Returns:
        Lista de features que correspondem ao padrão
    """
    results = []
    regex = re.compile(pattern, re.IGNORECASE)

    for feature in features:
        props = feature.get("properties", {})
        value = props.get(field, "")

        if regex.search(value):
            results.append(feature)

    return results


def extract_municipality_names(features: list[dict[str, Any]]) -> list[str]:
    """Extrai apenas os nomes dos municípios de uma lista de features.

    Args:
        features: Lista de features GeoJSON

    Returns:
        Lista de nomes de municípios
    """
    return [feature.get("properties", {}).get("name", "") for feature in features]


def extract_municipality_ids(features: list[dict[str, Any]]) -> list[str]:
    """Extrai apenas os códigos IBGE dos municípios.

    Args:
        features: Lista de features GeoJSON

    Returns:
        Lista de códigos IBGE
    """
    return [feature.get("properties", {}).get("id", "") for feature in features]


def get_feature_bounds(feature: dict[str, Any]) -> tuple[float, float, float, float] | None:
    """Calcula o bounding box (bounds) de uma feature.

    Args:
        feature: Feature GeoJSON

    Returns:
        Tupla (min_lon, min_lat, max_lon, max_lat) ou None se inválido
    """
    geometry = feature.get("geometry", {})
    coordinates = geometry.get("coordinates", [])

    if not coordinates:
        return None

    # Flatten coordinates (pode ter múltiplos níveis)
    def flatten_coords(coords, depth=0):
        """Recursivamente flatten coordenadas."""
        if not coords:
            return []

        # Se é uma coordenada [lon, lat]
        if isinstance(coords[0], (int, float)):
            return [coords]

        # Se é lista de coordenadas
        result = []
        for item in coords:
            result.extend(flatten_coords(item, depth + 1))
        return result

    all_coords = flatten_coords(coordinates)

    if not all_coords:
        return None

    lons = [c[0] for c in all_coords if len(c) >= 2]
    lats = [c[1] for c in all_coords if len(c) >= 2]

    if not lons or not lats:
        return None

    return (min(lons), min(lats), max(lons), max(lats))


def validate_geojson_structure(data: dict[str, Any]) -> tuple[bool, str | None]:
    """Valida a estrutura básica de um GeoJSON.

    Args:
        data: Dados a serem validados

    Returns:
        Tupla (is_valid, error_message)
    """
    # Verifica se tem type
    if "type" not in data:
        return False, "Missing 'type' field"

    geojson_type = data["type"]

    # FeatureCollection
    if geojson_type == "FeatureCollection":
        if "features" not in data:
            return False, "FeatureCollection missing 'features' field"

        if not isinstance(data["features"], list):
            return False, "'features' must be a list"

        return True, None

    # Feature
    elif geojson_type == "Feature":
        if "geometry" not in data:
            return False, "Feature missing 'geometry' field"

        if "properties" not in data:
            return False, "Feature missing 'properties' field"

        return True, None

    # Geometry types
    elif geojson_type in [
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
    ]:
        if "coordinates" not in data:
            return False, f"{geojson_type} missing 'coordinates' field"

        return True, None

    return False, f"Unknown GeoJSON type: {geojson_type}"


def count_features(geojson_data: dict[str, Any]) -> int:
    """Conta o número de features em um GeoJSON.

    Args:
        geojson_data: Dados GeoJSON

    Returns:
        Número de features
    """
    if geojson_data.get("type") == "FeatureCollection":
        return len(geojson_data.get("features", []))
    elif geojson_data.get("type") == "Feature":
        return 1
    return 0


def get_geojson_summary(geojson_data: dict[str, Any]) -> dict[str, Any]:
    """Retorna um resumo das informações de um GeoJSON.

    Args:
        geojson_data: Dados GeoJSON

    Returns:
        Dicionário com resumo (type, feature_count, etc.)
    """
    geojson_type = geojson_data.get("type", "Unknown")
    feature_count = count_features(geojson_data)

    summary = {
        "type": geojson_type,
        "feature_count": feature_count,
    }

    if geojson_type == "FeatureCollection":
        features = geojson_data.get("features", [])
        if features:
            # Propriedades disponíveis
            first_props = features[0].get("properties", {})
            summary["available_properties"] = list(first_props.keys())

            # Tipos de geometria
            geometry_types = set()
            for feature in features:
                geom_type = feature.get("geometry", {}).get("type")
                if geom_type:
                    geometry_types.add(geom_type)
            summary["geometry_types"] = list(geometry_types)

    return summary


# Exporta as principais funções
__all__ = [
    "load_geojson_with_cache",
    "clear_cache",
    "get_cache_size",
    "normalize_text",
    "search_features_by_name",
    "search_features_by_ibge",
    "filter_features_by_pattern",
    "extract_municipality_names",
    "extract_municipality_ids",
    "get_feature_bounds",
    "validate_geojson_structure",
    "count_features",
    "get_geojson_summary",
]
