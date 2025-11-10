"""Testes para o módulo server."""

from pathlib import Path
from unittest.mock import patch

import pytest

from src.geodata_br_mcp import server


class TestServerHelpers:
    """Testes para funções auxiliares do servidor."""

    def test_get_state_file(self):
        """Testa obtenção do caminho do arquivo de estado."""
        file_path = server._get_state_file("SP")
        assert "geojs-35-mun.json" in str(file_path)
        assert "geojson" in str(file_path)

    def test_get_state_file_with_code(self):
        """Testa obtenção do caminho com código IBGE."""
        file_path = server._get_state_file("35")
        assert "geojs-35-mun.json" in str(file_path)

    def test_assert_data_root_exists(self):
        """Testa verificação de DATA_ROOT quando existe."""
        # DATA_ROOT deve existir (é o diretório do projeto)
        server._assert_data_root()  # Não deve lançar exceção

    def test_assert_data_root_not_exists(self):
        """Testa verificação de DATA_ROOT quando não existe."""
        with patch.object(server, "DATA_ROOT", Path("/caminho/inexistente")):
            with pytest.raises(RuntimeError, match="GEODATA_BR_PATH inválido"):
                server._assert_data_root()

    def test_load_state_geojson(self):
        """Testa carregamento de GeoJSON de um estado."""
        # Usa RR (Roraima - código 14) que tem arquivo menor
        geojson = server._load_state_geojson("14")
        assert "type" in geojson
        assert geojson["type"] == "FeatureCollection"
        assert "features" in geojson


class TestListStates:
    """Testes para a ferramenta list_states."""

    def test_list_states(self):
        """Testa listagem de estados."""
        states = server.list_states()

        # Deve retornar uma lista
        assert isinstance(states, list)
        assert len(states) > 0

        # Cada estado deve ter as chaves corretas
        state = states[0]
        assert "ibge_code" in state
        assert "uf" in state
        assert "name" in state
        assert "region" in state

    def test_list_states_geojson_not_found(self):
        """Testa listagem quando diretório geojson não existe."""
        fake_root = Path("/tmp/fake_geodata_test_nonexistent")
        with patch.object(server, "DATA_ROOT", fake_root):
            # DATA_ROOT "existe" mas não tem o diretório geojson
            fake_root.mkdir(parents=True, exist_ok=True)
            try:
                states = server.list_states()
                assert states == []
            finally:
                # Limpa o diretório temporário
                import shutil

                shutil.rmtree(fake_root, ignore_errors=True)


class TestGetStateInfo:
    """Testes para a ferramenta get_state_info."""

    def test_get_state_info_with_uf(self):
        """Testa obtenção de informações com UF."""
        info = server.get_state_info("RR")

        assert info["uf"] == "RR"
        assert info["name"] == "Roraima"
        assert info["region"] == "Norte"
        assert "total_municipalities" in info
        assert info["total_municipalities"] > 0

    def test_get_state_info_with_code(self):
        """Testa obtenção de informações com código IBGE."""
        info = server.get_state_info("14")

        assert info["uf"] == "RR"
        assert "total_municipalities" in info

    def test_get_state_info_invalid_uf(self):
        """Testa com UF inválida."""
        with pytest.raises(ValueError):
            server.get_state_info("XX")


class TestListMunicipalities:
    """Testes para a ferramenta list_municipalities."""

    def test_list_municipalities(self):
        """Testa listagem de municípios."""
        municipalities = server.list_municipalities("RR")

        assert isinstance(municipalities, list)
        assert len(municipalities) > 0

        # Verifica estrutura do primeiro município
        mun = municipalities[0]
        assert "id" in mun
        assert "name" in mun
        assert "description" in mun

    def test_list_municipalities_with_code(self):
        """Testa listagem com código IBGE."""
        municipalities = server.list_municipalities("14")
        assert len(municipalities) > 0

    def test_list_municipalities_invalid_uf(self):
        """Testa com UF inválida."""
        with pytest.raises(ValueError):
            server.list_municipalities("XX")


class TestGetMunicipalityGeoJSON:
    """Testes para a ferramenta get_municipality_geojson."""

    def test_get_municipality_by_name(self):
        """Testa busca de município por nome."""
        # Boa Vista é a capital de Roraima
        municipality = server.get_municipality_geojson("RR", "Boa Vista")

        assert municipality is not None
        assert "type" in municipality
        assert municipality["type"] == "Feature"
        assert "properties" in municipality
        assert "name" in municipality["properties"]

    def test_get_municipality_normalized_search(self):
        """Testa busca normalizada (sem acentos)."""
        # Testa busca sem acento
        municipality = server.get_municipality_geojson("RR", "boa vista")
        assert municipality is not None

    def test_get_municipality_not_found(self):
        """Testa busca de município inexistente."""
        with pytest.raises(ValueError, match="não encontrado"):
            server.get_municipality_geojson("RR", "Município Inexistente XYZ")

    def test_get_municipality_invalid_uf(self):
        """Testa com UF inválida."""
        with pytest.raises(ValueError):
            server.get_municipality_geojson("XX", "Cidade")


class TestSearchMunicipalityByIBGE:
    """Testes para a ferramenta search_municipality_by_ibge."""

    def test_search_municipality_by_ibge_valid(self):
        """Testa busca por código IBGE válido."""
        # 1400100 = Boa Vista/RR
        municipality = server.search_municipality_by_ibge("1400100")

        assert municipality is not None
        assert "type" in municipality
        assert municipality["type"] == "Feature"
        assert "properties" in municipality
        assert municipality["properties"]["id"] == "1400100"

    def test_search_municipality_by_ibge_not_found(self):
        """Testa busca de código IBGE com código de estado válido mas município inexistente."""
        with pytest.raises(ValueError, match="não encontrado"):
            # Usa código de estado válido (14=RR) mas município inexistente
            server.search_municipality_by_ibge("1499999")

    def test_search_municipality_by_ibge_invalid_state_code(self):
        """Testa com código de estado inválido."""
        with pytest.raises(ValueError, match="Código de estado inválido"):
            server.search_municipality_by_ibge("9999999")


class TestLoadStateGeoJSON:
    """Testes para a função _load_state_geojson (privada mas testável)."""

    def test_load_state_geojson(self):
        """Testa carregamento de GeoJSON completo do estado."""
        geojson = server._load_state_geojson("RR")

        assert geojson["type"] == "FeatureCollection"
        assert "features" in geojson
        assert len(geojson["features"]) > 0

    def test_load_state_geojson_with_code(self):
        """Testa com código IBGE."""
        geojson = server._load_state_geojson("14")
        assert geojson["type"] == "FeatureCollection"

    def test_load_state_geojson_invalid_uf(self):
        """Testa com UF inválida."""
        with pytest.raises(ValueError):
            server._load_state_geojson("XX")


class TestGetBrazilGeoJSON:
    """Testes para a ferramenta get_brazil_geojson."""

    def test_get_brazil_geojson(self):
        """Testa obtenção de GeoJSON completo do Brasil."""
        geojson = server.get_brazil_geojson()

        assert geojson["type"] == "FeatureCollection"
        assert "features" in geojson
        # Brasil tem mais de 5000 municípios
        assert len(geojson["features"]) > 5000

    def test_get_brazil_geojson_structure(self):
        """Testa estrutura do GeoJSON do Brasil."""
        geojson = server.get_brazil_geojson()

        # Verifica que tem features de diferentes estados
        state_codes = set()
        for feature in geojson["features"][:100]:  # Verifica os primeiros 100
            if "properties" in feature and "id" in feature["properties"]:
                # Os 2 primeiros dígitos são o código do estado
                state_code = feature["properties"]["id"][:2]
                state_codes.add(state_code)

        # Deve ter municípios de vários estados
        assert len(state_codes) > 1


class TestAppInstance:
    """Testes para a instância do aplicativo MCP."""

    def test_app_exists(self):
        """Testa se a instância do app foi criada."""
        assert server.app is not None
        assert hasattr(server.app, "tool")

    def test_app_name(self):
        """Testa se o app tem o nome correto."""
        assert server.MCP_SERVER_NAME in str(server.app.name)
