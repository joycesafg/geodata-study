# 🗺️ Geodata-BR MCP Server

Servidor MCP (Model Context Protocol) para acesso a dados geográficos do Brasil. Fornece acesso programático aos dados GeoJSON de todos os municípios brasileiros, organizados por estado.

## 📖 Sobre o Projeto

Este é um servidor MCP que expõe os dados geográficos do [Geodata-BR](https://github.com/tthiagosantos/geodata-br) através de ferramentas (tools) que podem ser usadas por Claude, Cursor e outras aplicações compatíveis com MCP.

### O que é MCP?

[Model Context Protocol](https://modelcontextprotocol.io/) é um protocolo aberto que permite que modelos de IA interajam com fontes de dados e ferramentas externas de forma padronizada e segura.

## ✨ Funcionalidades

- 🗺️ Acesso a dados GeoJSON de **todos os 5.570 municípios brasileiros**
- 📊 Dados organizados por **27 estados + Distrito Federal**
- 🔍 Busca por **nome** (com normalização de acentos) ou **código IBGE**
- 💾 **Cache inteligente** para melhor performance
- 🎯 **6 tools** disponíveis para uso
- 📍 Dados completos do **Brasil inteiro** (geojs-100-mun.json)

## 🛠️ Tools Disponíveis

### 1. `list_states()`

Lista todos os estados disponíveis no repositório.

**Retorno:**
```json
[
  {
    "ibge_code": "35",
    "uf": "SP",
    "name": "São Paulo",
    "region": "Sudeste"
  },
  ...
]
```

**Uso:**
```
"Liste todos os estados disponíveis"
"Quais UFs você tem dados?"
```

---

### 2. `get_state_info(uf)`

Obtém informações detalhadas sobre um estado específico, incluindo quantidade de municípios.

**Parâmetros:**
- `uf` (string): Sigla da UF (ex: "SP") ou código IBGE (ex: "35")

**Retorno:**
```json
{
  "ibge_code": "35",
  "uf": "SP",
  "name": "São Paulo",
  "region": "Sudeste",
  "total_municipalities": 645
}
```

**Uso:**
```
"Quantos municípios tem São Paulo?"
"Me dê informações sobre o estado de MG"
"Qual a região do Ceará?"
```

---

### 3. `list_municipalities(uf)`

Lista todos os municípios de um estado.

**Parâmetros:**
- `uf` (string): Sigla da UF ou código IBGE

**Retorno:**
```json
[
  {
    "id": "3550308",
    "name": "São Paulo",
    "description": "São Paulo"
  },
  {
    "id": "3509502",
    "name": "Campinas",
    "description": "Campinas"
  },
  ...
]
```

**Uso:**
```
"Liste os municípios de São Paulo"
"Quais são as cidades do Rio de Janeiro?"
"Mostre todos os municípios da Bahia"
```

---

### 4. `get_municipality_geojson(uf, municipality_name)`

Obtém o GeoJSON completo de um município específico.

**Parâmetros:**
- `uf` (string): Sigla da UF ou código IBGE
- `municipality_name` (string): Nome do município

**Retorno:**
```json
{
  "type": "Feature",
  "properties": {
    "id": "3550308",
    "name": "São Paulo",
    "description": "São Paulo"
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[...]]]
  }
}
```

**Uso:**
```
"Me dê o GeoJSON de Campinas"
"Mostre o polígono de Belo Horizonte"
"Preciso das coordenadas geográficas de Curitiba"
```

**Nota:** A busca é **case-insensitive** e **normaliza acentos**. Funciona com "Sao Paulo", "São Paulo", "são paulo", etc.

---

### 5. `search_municipality_by_ibge(ibge_code)`

Busca um município pelo código IBGE (7 dígitos).

**Parâmetros:**
- `ibge_code` (string): Código IBGE de 7 dígitos

**Retorno:**
```json
{
  "type": "Feature",
  "properties": {
    "id": "3550308",
    "name": "São Paulo",
    "description": "São Paulo"
  },
  "geometry": { ... }
}
```

**Uso:**
```
"Busque o município com código IBGE 3550308"
"Qual município tem o código 3304557?"
"Me mostre o GeoJSON do IBGE 2927408"
```

**Nota:** Os 2 primeiros dígitos identificam o estado automaticamente.

---

### 6. `get_brazil_geojson()`

Retorna o GeoJSON completo do Brasil com todos os municípios.

**Retorno:**
```json
{
  "type": "FeatureCollection",
  "features": [
    { "type": "Feature", "properties": {...}, "geometry": {...} },
    ...
  ]
}
```

**Uso:**
```
"Me dê o GeoJSON completo do Brasil"
"Preciso de todos os municípios brasileiros"
"Mostre o mapa do Brasil inteiro"
```

**⚠️ Atenção:** Este arquivo é grande (~60MB). Use com moderação.

---

## 📁 Estrutura dos Dados

Os dados seguem o formato GeoJSON padrão:

```javascript
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": "3550308",         // Código IBGE (7 dígitos)
        "name": "São Paulo",     // Nome do município
        "description": "São Paulo"
      },
      "geometry": {
        "type": "Polygon",       // Ou MultiPolygon
        "coordinates": [[[
          [-46.365, -23.548],    // [longitude, latitude]
          ...
        ]]]
      }
    }
  ]
}
```

### Códigos IBGE

- **2 primeiros dígitos:** Código do estado
  - `35` = São Paulo
  - `33` = Rio de Janeiro
  - `31` = Minas Gerais
  - etc.

- **7 dígitos completos:** Código único do município

## 🚀 Performance e Cache

O servidor implementa **cache inteligente em memória**:

- Arquivos GeoJSON são carregados apenas uma vez
- Carregamentos subsequentes usam cache
- Cache persiste durante a execução do servidor
- Reduz tempo de resposta de segundos para milissegundos

### Estatísticas

- **Estados:** 27 + DF + Brasil = 29 arquivos
- **Municípios:** 5.570 no total
- **Tamanho médio:** 2-5 MB por arquivo de estado
- **Brasil completo:** ~60 MB

## 🔍 Busca Inteligente

### Normalização de Texto

A busca por nome de município normaliza automaticamente:

- **Remove acentos:** "São Paulo" = "Sao Paulo"
- **Case-insensitive:** "são paulo" = "SÃO PAULO"
- **Busca parcial:** "Paulo" encontra "São Paulo"

Exemplos que funcionam:
- "Brasília" / "Brasilia"
- "Florianópolis" / "Florianopolis"
- "Belém" / "Belem"

## 📊 Casos de Uso

### Análise de Dados Geográficos

```
"Quantos municípios tem a região Sudeste?"
"Liste as cidades do Nordeste que começam com 'São'"
```

### Mapas e Visualizações

```
"Me dê o GeoJSON de todos os municípios de São Paulo para criar um mapa"
"Preciso das coordenadas de Manaus"
```

### Validação de Códigos

```
"Verifique se o código IBGE 3550308 é válido"
"Qual município tem o código 5300108?"
```

### Pesquisa

```
"Encontre o município 'Feira de Santana' na Bahia"
"Busque informações sobre Joinville"
```

## 🏗️ Arquitetura do Servidor

```
geodata-br/
├── src/
│   └── geodata_br_mcp/
│       ├── server.py      # Servidor MCP principal (6 tools)
│       ├── config.py      # Mapeamentos IBGE ↔ UF
│       └── utils.py       # Funções auxiliares (cache, busca)
├── geojson/              # Dados GeoJSON
│   ├── geojs-35-mun.json # São Paulo
│   ├── geojs-33-mun.json # Rio de Janeiro
│   └── ...
├── pyproject.toml        # Configuração do projeto
└── requirements.txt      # Dependências
```

### Módulos

**server.py**
- Define as 6 tools MCP
- Gerencia comunicação via stdio
- Orquestra config e utils

**config.py**
- Mapeamento de códigos IBGE
- Validações
- Constantes

**utils.py**
- Cache de arquivos
- Busca normalizada
- Processamento de GeoJSON
- Validações

## 🔧 Desenvolvimento

### Executar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python -m src.geodata_br_mcp.server
```

### Testar com MCP Inspector

```bash
npx @modelcontextprotocol/inspector python -m src.geodata_br_mcp.server
```

### Executar Testes

```bash
pytest tests/
```

### Code Quality

```bash
# Formatar código
black src/

# Lint
ruff src/

# Type checking
mypy src/
```

## 📚 Recursos

- [Instalação](INSTALL.md) - Guia completo de instalação
- [Exemplos](EXAMPLES.md) - Exemplos práticos de uso
- [Repositório Original](https://github.com/tthiagosantos/geodata-br) - Dados GeoJSON
- [MCP Protocol](https://modelcontextprotocol.io/) - Especificação do protocolo

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

- 🐛 Reportar bugs
- 💡 Sugerir novas features
- 📝 Melhorar a documentação
- 🔧 Enviar pull requests

## 📄 Licença

Este projeto usa a mesma licença do projeto original:

**CC0 1.0 Universal** - Dedicação ao Domínio Público

Você pode copiar, modificar, distribuir e usar o trabalho, mesmo para fins comerciais, sem pedir permissão.

## 🙏 Créditos

- **Dados GeoJSON:** [IBGE](http://ibge.gov.br/)
- **Repositório Original:** [geodata-br](https://github.com/tthiagosantos/geodata-br)
- **MCP Protocol:** [Anthropic](https://www.anthropic.com/)

---

**Desenvolvido com ❤️ para a comunidade brasileira de dados geográficos**
