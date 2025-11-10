"""
Testes para o módulo config.py
"""

import pytest
from src.geodata_br_mcp.config import (
    IBGE_TO_STATE,
    STATE_TO_IBGE,
    STATES_BY_REGION,
    validate_uf,
    validate_ibge_code,
    get_state_code,
    get_state_info,
    get_states_by_region,
    get_filename_for_state,
    get_all_states,
    get_total_states,
)


class TestConstants:
    """Testa as constantes de configuração."""

    def test_ibge_to_state_has_all_states(self):
        """Verifica se todos os 27 estados + DF + Brasil estão mapeados."""
        assert len(IBGE_TO_STATE) == 28  # 27 estados + DF + Brasil (100)
        assert "100" in IBGE_TO_STATE  # Brasil
        assert "35" in IBGE_TO_STATE  # São Paulo
        assert "33" in IBGE_TO_STATE  # Rio de Janeiro

    def test_state_to_ibge_reverse_mapping(self):
        """Verifica se o mapeamento reverso está correto."""
        assert STATE_TO_IBGE["SP"] == "35"
        assert STATE_TO_IBGE["RJ"] == "33"
        assert STATE_TO_IBGE["MG"] == "31"
        assert STATE_TO_IBGE["BR"] == "100"

    def test_states_by_region(self):
        """Verifica se os estados estão agrupados corretamente por região."""
        assert "Sul" in STATES_BY_REGION
        assert "Norte" in STATES_BY_REGION
        assert "Nordeste" in STATES_BY_REGION
        assert "Sudeste" in STATES_BY_REGION
        assert "Centro-Oeste" in STATES_BY_REGION

        # Verifica alguns estados
        assert "SP" in STATES_BY_REGION["Sudeste"]
        assert "RS" in STATES_BY_REGION["Sul"]
        assert "AM" in STATES_BY_REGION["Norte"]


class TestValidations:
    """Testa as funções de validação."""

    def test_validate_uf_valid(self):
        """Testa validação de UF válida."""
        assert validate_uf("SP") is True
        assert validate_uf("sp") is True  # Case insensitive
        assert validate_uf("RJ") is True

    def test_validate_uf_invalid(self):
        """Testa validação de UF inválida."""
        assert validate_uf("XX") is False
        assert validate_uf("ABC") is False
        assert validate_uf("") is False

    def test_validate_ibge_code_valid(self):
        """Testa validação de código IBGE válido."""
        assert validate_ibge_code("35") is True
        assert validate_ibge_code("33") is True
        assert validate_ibge_code("100") is True

    def test_validate_ibge_code_invalid(self):
        """Testa validação de código IBGE inválido."""
        assert validate_ibge_code("99") is False
        assert validate_ibge_code("00") is False
        assert validate_ibge_code("") is False


class TestStateFunctions:
    """Testa funções relacionadas a estados."""

    def test_get_state_code_with_uf(self):
        """Testa obter código IBGE a partir de UF."""
        assert get_state_code("SP") == "35"
        assert get_state_code("sp") == "35"  # Case insensitive
        assert get_state_code("RJ") == "33"

    def test_get_state_code_with_ibge(self):
        """Testa obter código IBGE a partir de código IBGE (retorna o mesmo)."""
        assert get_state_code("35") == "35"
        assert get_state_code("33") == "33"

    def test_get_state_code_invalid(self):
        """Testa obter código IBGE com entrada inválida."""
        with pytest.raises(ValueError):
            get_state_code("XX")

        with pytest.raises(ValueError):
            get_state_code("99")

    def test_get_state_info_with_uf(self):
        """Testa obter informações de estado por UF."""
        info = get_state_info("SP")
        assert info["uf"] == "SP"
        assert info["name"] == "São Paulo"
        assert info["region"] == "Sudeste"
        assert info["ibge_code"] == "35"

    def test_get_state_info_with_ibge(self):
        """Testa obter informações de estado por código IBGE."""
        info = get_state_info("35")
        assert info["uf"] == "SP"
        assert info["name"] == "São Paulo"

    def test_get_states_by_region_sul(self):
        """Testa obter estados da região Sul."""
        states = get_states_by_region("Sul")
        assert len(states) == 3
        ufs = [s["uf"] for s in states]
        assert "PR" in ufs
        assert "SC" in ufs
        assert "RS" in ufs

    def test_get_states_by_region_invalid(self):
        """Testa obter estados de região inválida."""
        with pytest.raises(ValueError):
            get_states_by_region("Inexistente")

    def test_get_filename_for_state(self):
        """Testa gerar nome de arquivo para estado."""
        assert get_filename_for_state("SP") == "geojs-35-mun.json"
        assert get_filename_for_state("35") == "geojs-35-mun.json"
        assert get_filename_for_state("RJ") == "geojs-33-mun.json"

    def test_get_all_states(self):
        """Testa obter todos os estados."""
        states = get_all_states()
        assert len(states) == 28  # 27 + DF + Brasil
        assert any(s["uf"] == "SP" for s in states)

    def test_get_total_states(self):
        """Testa contar total de estados (excluindo Brasil)."""
        assert get_total_states() == 27  # Exclui o código 100 (Brasil)

