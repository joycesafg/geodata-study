
Geodata BR - Brasil
===================

Este projeto contém arquivos [Geojson](http://geojson.org/) com os perímetros
dos municípios brasileiros dividido por estado


### Região Norte
* AC / Acre - [geojson/geojs-12-mun.json](geojson/geojs-12-mun.json)
* AM / Amazonas - [geojson/geojs-13-mun.json](geojson/geojs-13-mun.json)
* AP / Amapá - [geojson/geojs-16-mun.json](geojson/geojs-16-mun.json)
* PA / Pará  - [geojson/geojs-15-mun.json](geojson/geojs-15-mun.json)
* RO / Rondônia - [geojson/geojs-11-mun.json](geojson/geojs-11-mun.json)
* RR / Roraima - [geojson/geojs-14-mun.json](geojson/geojs-14-mun.json)
* TO / Tocantins - [geojson/geojs-17-mun.json](geojson/geojs-17-mun.json)


### Região Nordeste
* AL / Alagoas - [geojson/geojs-27-mun.json](geojson/geojs-27-mun.json)
* BA / Bahia - [geojson/geojs-29-mun.json](geojson/geojs-29-mun.json)
* CE / Ceará - [geojson/geojs-23-mun.json](geojson/geojs-23-mun.json)
* MA / Maranhão - [geojson/geojs-21-mun.json](geojson/geojs-21-mun.json)
* PB / Paraíba - [geojson/geojs-25-mun.json](geojson/geojs-25-mun.json)
* PE / Pernambuco - [geojson/geojs-26-mun.json](geojson/geojs-26-mun.json)
* PI / Piauí - [geojson/geojs-22-mun.json](geojson/geojs-22-mun.json)
* RN / Rio Grande do Norte - [geojson/geojs-24-mun.json](geojson/geojs-24-mun.json)
* SE / Sergipe - [geojson/geojs-28-mun.json](geojson/geojs-28-mun.json)


### Região Sudeste
* ES / Espírito Santo - [geojson/geojs-32-mun.json](geojson/geojs-32-mun.json)
* MG / Minas Gerais - [geojson/geojs-31-mun.json](geojson/geojs-31-mun.json)
* RJ / Rio de Janeiro - [geojson/geojs-33-mun.json](geojson/geojs-33-mun.json)
* SP / São Paulo - [geojson/geojs-35-mun.json](geojson/geojs-35-mun.json)


### Região Sul
* PR / Paraná - [geojson/geojs-41-mun.json](geojson/geojs-41-mun.json)
* RS / Rio Grande do Sul - [geojson/geojs-43-mun.json](geojson/geojs-43-mun.json)
* SC / Santa Catarina - [geojson/geojs-42-mun.json](geojson/geojs-42-mun.json)


### Região Centro-Oeste
* DF / Distrito Federal - [geojson/geojs-53-mun.json](geojson/geojs-53-mun.json) 
* GO / Goiás - [geojson/geojs-52-mun.json](geojson/geojs-52-mun.json)
* MT / Mato Grosso - [geojson/geojs-51-mun.json](geojson/geojs-51-mun.json)
* MS / Mato Grosso do Sul - [geojson/geojs-50-mun.json](geojson/geojs-50-mun.json)


### Brasil
* BR / Brasil - [geojson/geojs-100-mun.json](geojson/geojs-100-mun.json)


Fonte dos dados
---------------
[IBGE](http://ibge.gov.br/)


Desenvolvimento
---------------

Este projeto usa ferramentas modernas de qualidade de código para garantir consistência e qualidade.

### 🚀 Configuração Rápida

```bash
# Clone o repositório
git clone <seu-repositorio>
cd geodata-study

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instale as dependências de desenvolvimento
pip install -r requirements-dev.txt

# Configure os hooks do pre-commit
pre-commit install

# Ou use o script automatizado
chmod +x .pre-commit-install.sh
./.pre-commit-install.sh
```

### 🛠️ Ferramentas Configuradas

- **Pre-commit**: Hooks automáticos antes de cada commit
- **Ruff**: Linter e formatador rápido (Python)
- **Black**: Formatador de código
- **MyPy**: Verificação de tipos estáticos
- **Pytest**: Framework de testes com cobertura de código

### 📝 Comandos Úteis

```bash
# Usando Make (recomendado)
make help              # Mostra todos os comandos disponíveis
make install-dev       # Instala dependências + pre-commit
make test              # Executa os testes
make test-cov          # Executa testes com cobertura
make lint              # Executa o linter
make format            # Formata o código
make check             # Executa todas as verificações

# Ou comandos diretos
pre-commit run --all-files  # Executa todos os hooks
pytest -v                   # Executa os testes
ruff check .                # Executa o linter
black .                     # Formata o código
```

### 📚 Documentação Adicional

- [PRECOMMIT.md](PRECOMMIT.md) - Guia completo do pre-commit
- [INSTALL.md](INSTALL.md) - Instruções de instalação
- [EXAMPLES.md](EXAMPLES.md) - Exemplos de uso
- [README_MCP.md](README_MCP.md) - Documentação do servidor MCP

### 🔄 CI/CD

O projeto inclui workflow do GitHub Actions (`.github/workflows/quality-checks.yml`) que executa automaticamente:
- Testes em múltiplas versões do Python (3.10, 3.11, 3.12)
- Verificações de qualidade de código
- Análise de cobertura de testes


Licença
-------
Creative Commons [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) - Dedicação ao Domínio Público. Ver arquivo [LICENSE.md](LICENSE.md)


Projetos relacionados
--------------------- 
* https://github.com/fititnt/gis-dataset-brasil
* https://github.com/carolinabigonha/br-atlas
* https://github.com/luizpedone/municipal-brazilian-geodata


Palavras-chave / Keywords
-------------------------
BR, Brasil, Brazil, mapa, map, mapas, maps, Geojson, geo, json, GIS
