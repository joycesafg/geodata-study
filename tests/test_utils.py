"""
Testes para o módulo utils.py
"""

from typing import Any

import pytest

from src.geodata_br_mcp.utils import (
    clear_cache,
    count_features,
    extract_municipality_ids,
    extract_municipality_names,
    filter_features_by_pattern,
    get_cache_size,
    get_geojson_summary,
    normalize_text,
    search_features_by_ibge,
    search_features_by_name,
    validate_geojson_structure,
)


class TestNormalization:
    """Testa normalização de texto."""

    def test_normalize_text_removes_accents(self):
        """Testa remoção de acentos."""
        assert normalize_text("São Paulo") == "sao paulo"
        assert normalize_text("Brasília") == "brasilia"
        assert normalize_text("José") == "jose"

    def test_normalize_text_lowercase(self):
        """Testa conversão para minúsculas."""
        assert normalize_text("SÃO PAULO") == "sao paulo"
        assert normalize_text("São Paulo") == "sao paulo"

    def test_normalize_text_strips_whitespace(self):
        """Testa remoção de espaços extras."""
        assert normalize_text("  São Paulo  ") == "sao paulo"

    def test_normalize_text_cedilla(self):
        """Testa remoção de cedilha."""
        assert normalize_text("Conceição") == "conceicao"


class TestFeatureSearch:
    """Testa funções de busca em features."""

    @pytest.fixture
    def sample_features(self):
        """Fixture com features de exemplo."""
        return [
            {
                "type": "Feature",
                "properties": {"id": "3550308", "name": "São Paulo", "description": "São Paulo"},
                "geometry": {"type": "Point", "coordinates": [-46.633, -23.550]},
            },
            {
                "type": "Feature",
                "properties": {"id": "3509502", "name": "Campinas", "description": "Campinas"},
                "geometry": {"type": "Point", "coordinates": [-47.060, -22.905]},
            },
            {
                "type": "Feature",
                "properties": {
                    "id": "3548708",
                    "name": "São Bernardo do Campo",
                    "description": "São Bernardo do Campo",
                },
                "geometry": {"type": "Point", "coordinates": [-46.565, -23.691]},
            },
        ]

    def test_search_features_by_name_exact(self, sample_features):
        """Testa busca por nome (não-normalizada)."""
        results = search_features_by_name(sample_features, "Campinas")
        assert len(results) == 1
        assert results[0]["properties"]["name"] == "Campinas"

    def test_search_features_by_name_normalized(self, sample_features):
        """Testa busca por nome normalizada."""
        results = search_features_by_name(sample_features, "sao paulo")
        assert len(results) >= 1
        # Deve encontrar "São Paulo" e "São Bernardo do Campo"

    def test_search_features_by_name_partial(self, sample_features):
        """Testa busca parcial por nome."""
        results = search_features_by_name(sample_features, "São")
        assert len(results) == 2  # São Paulo e São Bernardo

    def test_search_features_by_ibge(self, sample_features):
        """Testa busca por código IBGE."""
        result = search_features_by_ibge(sample_features, "3550308")
        assert result is not None
        assert result["properties"]["name"] == "São Paulo"

    def test_search_features_by_ibge_not_found(self, sample_features):
        """Testa busca por código IBGE não existente."""
        result = search_features_by_ibge(sample_features, "9999999")
        assert result is None

    def test_filter_features_by_pattern(self, sample_features):
        """Testa filtro com regex."""
        results = filter_features_by_pattern(sample_features, r"^São")
        assert len(results) == 2  # São Paulo e São Bernardo


class TestFeatureExtraction:
    """Testa funções de extração de dados."""

    @pytest.fixture
    def sample_features(self):
        """Fixture com features de exemplo."""
        return [
            {
                "type": "Feature",
                "properties": {"id": "3550308", "name": "São Paulo"},
                "geometry": {},
            },
            {
                "type": "Feature",
                "properties": {"id": "3509502", "name": "Campinas"},
                "geometry": {},
            },
        ]

    def test_extract_municipality_names(self, sample_features):
        """Testa extração de nomes."""
        names = extract_municipality_names(sample_features)
        assert len(names) == 2
        assert "São Paulo" in names
        assert "Campinas" in names

    def test_extract_municipality_ids(self, sample_features):
        """Testa extração de códigos IBGE."""
        ids = extract_municipality_ids(sample_features)
        assert len(ids) == 2
        assert "3550308" in ids
        assert "3509502" in ids


class TestGeoJSONValidation:
    """Testa validação de estrutura GeoJSON."""

    def test_validate_feature_collection(self):
        """Testa validação de FeatureCollection."""
        data = {"type": "FeatureCollection", "features": []}
        is_valid, error = validate_geojson_structure(data)
        assert is_valid is True
        assert error is None

    def test_validate_feature(self):
        """Testa validação de Feature."""
        data = {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        }
        is_valid, error = validate_geojson_structure(data)
        assert is_valid is True
        assert error is None

    def test_validate_geometry(self):
        """Testa validação de Geometry."""
        data = {"type": "Point", "coordinates": [0, 0]}
        is_valid, error = validate_geojson_structure(data)
        assert is_valid is True
        assert error is None

    def test_validate_invalid_missing_type(self):
        """Testa validação com type faltando."""
        data: dict[str, Any] = {"features": []}
        is_valid, error = validate_geojson_structure(data)
        assert is_valid is False
        assert error is not None
        assert "type" in error

    def test_validate_invalid_feature_collection(self):
        """Testa validação de FeatureCollection inválida."""
        data: dict[str, Any] = {"type": "FeatureCollection"}
        is_valid, error = validate_geojson_structure(data)
        assert is_valid is False
        assert error is not None
        assert "features" in error


class TestGeoJSONAnalysis:
    """Testa funções de análise de GeoJSON."""

    def test_count_features_in_collection(self):
        """Testa contagem de features em FeatureCollection."""
        data = {"type": "FeatureCollection", "features": [{}, {}, {}]}
        assert count_features(data) == 3

    def test_count_features_single(self):
        """Testa contagem de feature única."""
        data = {"type": "Feature", "properties": {}, "geometry": {}}
        assert count_features(data) == 1

    def test_count_features_invalid(self):
        """Testa contagem em estrutura inválida."""
        data = {"type": "Point", "coordinates": [0, 0]}
        assert count_features(data) == 0

    def test_get_geojson_summary(self):
        """Testa geração de resumo de GeoJSON."""
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"id": "123", "name": "Test"},
                    "geometry": {"type": "Polygon", "coordinates": []},
                }
            ],
        }
        summary = get_geojson_summary(data)

        assert summary["type"] == "FeatureCollection"
        assert summary["feature_count"] == 1
        assert "available_properties" in summary
        assert "id" in summary["available_properties"]
        assert "name" in summary["available_properties"]
        assert "Polygon" in summary["geometry_types"]


class TestCache:
    """Testa funcionalidades de cache."""

    def test_clear_cache(self):
        """Testa limpeza de cache."""
        clear_cache()
        assert get_cache_size() == 0

    def test_get_cache_size(self):
        """Testa obtenção do tamanho do cache."""
        clear_cache()
        size = get_cache_size()
        assert isinstance(size, int)
        assert size >= 0
