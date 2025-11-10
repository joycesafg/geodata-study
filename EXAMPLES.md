# 📚 Exemplos de Uso - Geodata-BR MCP Server

Este documento contém exemplos práticos de como usar o servidor MCP Geodata-BR com Claude, Cursor e outras ferramentas compatíveis.

## 🎯 Exemplos Básicos

### 1. Listar Estados Disponíveis

**Pergunta:**
```
"Quais estados você tem dados geográficos disponíveis?"
```

**O que acontece:**
- Claude usa a tool `list_states()`
- Retorna lista com 27 estados + DF + Brasil

**Resposta esperada:**
```
Tenho dados geográficos de todos os 27 estados brasileiros mais o Distrito Federal:

Região Norte: Rondônia, Acre, Amazonas, Roraima, Pará, Amapá, Tocantins
Região Nordeste: Maranhão, Piauí, Ceará, Rio Grande do Norte, Paraíba...
(etc.)
```

---

### 2. Informações sobre um Estado

**Pergunta:**
```
"Quantos municípios tem São Paulo?"
```

**O que acontece:**
- Claude usa `get_state_info("SP")`
- Retorna informações incluindo total de municípios

**Resposta esperada:**
```
São Paulo tem 645 municípios. É o estado com maior número de municípios do Brasil,
localizado na região Sudeste (código IBGE: 35).
```

---

### 3. Listar Municípios de um Estado

**Pergunta:**
```
"Liste os 10 primeiros municípios do Rio de Janeiro"
```

**O que acontece:**
- Claude usa `list_municipalities("RJ")`
- Retorna lista completa, Claude filtra os 10 primeiros

**Resposta esperada:**
```
Os 10 primeiros municípios do Rio de Janeiro são:
1. Angra dos Reis (3300100)
2. Aperibé (3300159)
3. Araruama (3300209)
...
```

---

### 4. Obter GeoJSON de um Município

**Pergunta:**
```
"Me dê o GeoJSON de Campinas"
```

**O que acontece:**
- Claude pergunta: "De qual estado?"
- Você responde: "São Paulo"
- Claude usa `get_municipality_geojson("SP", "Campinas")`

**Resposta esperada:**
```json
{
  "type": "Feature",
  "properties": {
    "id": "3509502",
    "name": "Campinas",
    "description": "Campinas"
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[
      [-47.123, -22.789],
      ...
    ]]]
  }
}
```

---

### 5. Busca por Código IBGE

**Pergunta:**
```
"Qual município tem o código IBGE 3550308?"
```

**O que acontece:**
- Claude usa `search_municipality_by_ibge("3550308")`
- Identifica automaticamente que é de SP (código 35)

**Resposta esperada:**
```
O código IBGE 3550308 corresponde a São Paulo, capital do estado de São Paulo.
```

---

## 🎨 Exemplos Avançados

### 6. Análise Comparativa

**Pergunta:**
```
"Compare o número de municípios das regiões Sul e Nordeste"
```

**O que acontece:**
- Claude usa `get_state_info()` para cada estado
- Soma municípios por região
- Faz a comparação

**Resposta esperada:**
```
Região Sul:
- Paraná: 399 municípios
- Santa Catarina: 295 municípios
- Rio Grande do Sul: 497 municípios
Total: 1.191 municípios

Região Nordeste:
- Maranhão: 217 municípios
- Piauí: 224 municípios
- Ceará: 184 municípios
- (continua...)
Total: 1.794 municípios

A região Nordeste tem aproximadamente 50% mais municípios que a região Sul.
```

---

### 7. Busca com Normalização

**Pergunta:**
```
"Encontre o município 'Brasilia' (sem acento)"
```

**O que acontece:**
- Claude usa `get_municipality_geojson("DF", "Brasilia")`
- A busca normaliza e encontra "Brasília"

**Resposta esperada:**
```
Encontrei Brasília (código IBGE: 5300108), capital do Brasil, 
localizada no Distrito Federal.

[GeoJSON retornado]
```

---

### 8. Criar Mapa de Estado Inteiro

**Pergunta:**
```
"Me dê os dados para criar um mapa de todos os municípios de Santa Catarina"
```

**O que acontece:**
- Claude usa `list_municipalities("SC")`
- Para cada município, usa `get_municipality_geojson()`
- Compila em uma FeatureCollection

**Nota:** Este é um caso de uso intensivo. Para estados grandes, considere usar apenas `list_municipalities()` e carregar GeoJSONs sob demanda.

---

### 9. Encontrar Municípios com Padrão

**Pergunta:**
```
"Liste todos os municípios de São Paulo que começam com 'São'"
```

**O que acontece:**
- Claude usa `list_municipalities("SP")`
- Filtra os nomes que começam com "São"

**Resposta esperada:**
```
Encontrei 51 municípios em São Paulo que começam com "São":

1. São Paulo (3550308)
2. São Bernardo do Campo (3548708)
3. São Caetano do Sul (3548807)
4. São Carlos (3548906)
5. São José dos Campos (3549904)
...
```

---

### 10. Validação de Dados

**Pergunta:**
```
"Verifique se o código IBGE 9999999 é válido"
```

**O que acontece:**
- Claude tenta `search_municipality_by_ibge("9999999")`
- Retorna erro (código de estado 99 não existe)

**Resposta esperada:**
```
O código IBGE 9999999 não é válido. Os dois primeiros dígitos (99) 
não correspondem a nenhum estado brasileiro.
```

---

## 🗺️ Casos de Uso Reais

### Caso 1: Visualização de Dados

**Cenário:** Você está criando um dashboard e precisa de dados geográficos.

**Conversa:**
```
Você: "Preciso criar um mapa coroplético de São Paulo mostrando população por município. 
      Me ajude a obter os dados geográficos."

Claude: "Vou buscar os dados dos municípios de São Paulo para você."
[Usa list_municipalities("SP")]

Claude: "São Paulo tem 645 municípios. Para o mapa coroplético, você precisará:
        1. Os GeoJSONs dos municípios (que posso fornecer)
        2. Dados de população (de outra fonte)
        
        Quer que eu busque os GeoJSONs de alguns municípios específicos ou prefere 
        trabalhar com a lista completa?"

Você: "Me dê os GeoJSONs das 10 maiores cidades"

Claude: [Busca os GeoJSONs de São Paulo, Guarulhos, Campinas, etc.]
```

---

### Caso 2: Análise de Proximidade

**Cenário:** Você quer saber quais municípios fazem fronteira com outro.

**Conversa:**
```
Você: "Quais municípios fazem fronteira com Campinas?"

Claude: "Para determinar isso, vou precisar dos dados geográficos de Campinas 
        e dos municípios ao redor."
[Usa get_municipality_geojson("SP", "Campinas")]

Claude: "Campinas tem estas coordenadas como limites:
        [analisa o polígono]
        
        Para identificar os vizinhos com precisão, seria necessário analisar 
        todos os 645 municípios de SP e verificar quais compartilham fronteiras.
        Quer que eu liste os municípios próximos a Campinas para você verificar?"
```

**Nota:** Análise de fronteiras requer algoritmos geoespaciais adicionais que não estão implementados nas tools.

---

### Caso 3: Geocodificação Reversa

**Cenário:** Você tem coordenadas e quer saber qual município.

**Conversa:**
```
Você: "Em qual município está o ponto [-46.633, -23.550]?"

Claude: "Essas coordenadas estão próximas à região de São Paulo. Vou verificar os 
        limites dos municípios dessa área."
[Usa get_municipality_geojson para municípios candidatos]

Claude: "O ponto [-46.633, -23.550] está dentro dos limites do município de 
        São Paulo (capital)."
```

**Nota:** Para geocodificação precisa, é recomendado usar bibliotecas especializadas como `shapely`.

---

### Caso 4: Exportação de Dados

**Cenário:** Você quer exportar dados para uso em GIS.

**Conversa:**
```
Você: "Preciso exportar os dados de todos os municípios do Paraná em formato GeoJSON"

Claude: "Vou buscar todos os municípios do Paraná para você."
[Usa list_municipalities("PR")]

Claude: "O Paraná tem 399 municípios. Como você prefere receber os dados?
        
        Opção 1: Um arquivo único com todos os municípios (FeatureCollection)
        Opção 2: Arquivos individuais por município
        Opção 3: Lista de códigos IBGE para você processar externamente"

Você: "Opção 1"

Claude: [Compila todos os GeoJSONs em uma FeatureCollection]
"Aqui está o GeoJSON completo do Paraná com todos os 399 municípios:
[GeoJSON completo]"
```

---

### Caso 5: Pesquisa Textual

**Cenário:** Encontrar municípios com nome específico.

**Conversa:**
```
Você: "Existem municípios chamados 'Santa Maria' no Brasil?"

Claude: [Busca em vários estados]

Claude: "Encontrei 5 municípios chamados 'Santa Maria':
        
        1. Santa Maria (RS) - 4316907
        2. Santa Maria (RN) - 2411205
        3. Santa Maria da Boa Vista (PE) - 2612554
        4. Santa Maria da Vitória (BA) - 2928109
        5. Santa Maria das Barreiras (PA) - 1506500
        
        Qual deles você gostaria de obter mais informações?"
```

---

## 💡 Dicas de Uso

### ✅ Boas Práticas

1. **Seja específico com nomes:**
   - ✅ "Município de São José dos Campos em SP"
   - ❌ "São José" (pode haver vários)

2. **Use códigos IBGE quando possível:**
   - ✅ "Busque o código 3550308"
   - Mais preciso que busca por nome

3. **Divida tarefas grandes:**
   - ✅ "Liste os municípios do Acre" (221 municípios)
   - ❌ "Me dê o GeoJSON de todos os municípios do Brasil" (muito grande)

4. **Aproveite a normalização:**
   - ✅ "Florianopolis" funciona
   - ✅ "florianopolis" funciona
   - ✅ "FLORIANOPOLIS" funciona

### ⚠️ Limitações

1. **Análises geoespaciais avançadas** (interseção, união, buffer) não estão disponíveis
2. **Dados populacionais** não estão incluídos (apenas geometrias)
3. **Arquivos grandes** (como Brasil completo) podem ser lentos na primeira vez

### 🚀 Performance

- **1ª chamada:** Pode demorar alguns segundos (carrega do disco)
- **Chamadas subsequentes:** Milissegundos (usa cache)
- **Melhor performance:** Usar `list_municipalities()` antes de buscar GeoJSONs individuais

---

## 🤔 FAQ

**P: Posso usar para criar mapas web?**
R: Sim! Os GeoJSONs são compatíveis com Leaflet, Mapbox, Google Maps, etc.

**P: Os dados são atualizados?**
R: Os dados vêm do IBGE através do repositório geodata-br. Verifique a data no repositório original.

**P: Posso modificar os limites dos municípios?**
R: Sim, mas as modificações não serão salvas no servidor. Use os dados como base para seu projeto.

**P: Funciona offline?**
R: Sim, uma vez que os arquivos GeoJSON estejam no seu disco.

**P: Qual a precisão dos polígonos?**
R: Os dados vêm do IBGE e têm precisão adequada para a maioria dos usos. Para aplicações que requerem alta precisão, consulte diretamente o IBGE.

---

## 📚 Recursos Adicionais

- [README_MCP.md](README_MCP.md) - Documentação técnica completa
- [INSTALL.md](INSTALL.md) - Guia de instalação
- [GeoJSON.org](https://geojson.org/) - Especificação do formato
- [IBGE](https://www.ibge.gov.br/) - Fonte dos dados

---

**Tem mais exemplos ou casos de uso? Contribua com o projeto!** 🚀

