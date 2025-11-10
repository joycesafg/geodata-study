# 🚀 Instalação do Geodata-BR MCP Server

Este guia explica como instalar e configurar o servidor MCP do Geodata-BR para uso com Claude Desktop e Cursor.

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Claude Desktop ou Cursor (opcional, para integração)
- Git (para clonar o repositório)

## 🔧 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/tthiagosantos/geodata-br.git
cd geodata-br
```

### 2. Instale as Dependências

**Opção A: Usando pip**
```bash
pip install -r requirements.txt
```

**Opção B: Usando uv (recomendado para desenvolvimento)**
```bash
uv pip install -e .
```

**Opção C: Para desenvolvimento com ferramentas**
```bash
pip install -r requirements-dev.txt
```

### 3. Configure o Ambiente (Opcional)

Se o servidor estiver em um diretório diferente dos dados GeoJSON:

```bash
cp .env.example .env
# Edite o arquivo .env e configure GEODATA_BR_PATH
```

## 🔌 Integração com Claude Desktop

### macOS / Linux

1. **Encontre o arquivo de configuração do Claude:**
```bash
# macOS
~/.config/Claude/claude_desktop_config.json

# Linux
~/.config/Claude/claude_desktop_config.json
```

2. **Adicione a configuração do servidor:**

Abra o arquivo e adicione a seguinte configuração (ajuste o caminho):

```json
{
  "mcpServers": {
    "geodata-br": {
      "command": "python",
      "args": [
        "-m",
        "src.geodata_br_mcp.server"
      ],
      "cwd": "/caminho/completo/para/geodata-br",
      "env": {
        "GEODATA_BR_PATH": "/caminho/completo/para/geodata-br"
      }
    }
  }
}
```

**Exemplo prático:**
```json
{
  "mcpServers": {
    "geodata-br": {
      "command": "python",
      "args": [
        "-m",
        "src.geodata_br_mcp.server"
      ],
      "cwd": "/Users/seu_usuario/Documents/geodata-br",
      "env": {
        "GEODATA_BR_PATH": "/Users/seu_usuario/Documents/geodata-br"
      }
    }
  }
}
```

3. **Reinicie o Claude Desktop**

### Windows

1. **Encontre o arquivo de configuração:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

2. **Adicione a configuração** (ajuste os caminhos com barras invertidas):

```json
{
  "mcpServers": {
    "geodata-br": {
      "command": "python",
      "args": [
        "-m",
        "src.geodata_br_mcp.server"
      ],
      "cwd": "C:\\Users\\SeuUsuario\\Documents\\geodata-br",
      "env": {
        "GEODATA_BR_PATH": "C:\\Users\\SeuUsuario\\Documents\\geodata-br"
      }
    }
  }
}
```

3. **Reinicie o Claude Desktop**

## 🎯 Integração com Cursor

### Configuração no Cursor

1. **Abra as configurações do Cursor** (Cmd/Ctrl + ,)

2. **Vá para "MCP Servers"** ou edite diretamente o arquivo de configuração

3. **Adicione o servidor geodata-br:**

```json
{
  "mcp.servers": {
    "geodata-br": {
      "command": "python",
      "args": ["-m", "src.geodata_br_mcp.server"],
      "cwd": "/caminho/completo/para/geodata-br",
      "env": {
        "GEODATA_BR_PATH": "/caminho/completo/para/geodata-br"
      }
    }
  }
}
```

4. **Reinicie o Cursor**

## 🧪 Testando a Instalação

### Teste Local

Execute o servidor manualmente para verificar se está funcionando:

```bash
cd geodata-br
python -m src.geodata_br_mcp.server
```

Se tudo estiver correto, o servidor ficará aguardando comandos via stdio.

### Teste com MCP Inspector

Use a ferramenta oficial de debug do MCP:

```bash
npx @modelcontextprotocol/inspector python -m src.geodata_br_mcp.server
```

Isso abrirá uma interface web onde você pode testar as tools do servidor.

## ✅ Verificando se Funciona

### No Claude Desktop

Após configurar e reiniciar, você pode perguntar ao Claude:

```
"Quais estados você tem dados geográficos disponíveis?"
```

O Claude deve listar os estados brasileiros usando a tool `list_states`.

### No Cursor

Após configurar, você pode usar comandos como:

```
"Liste os municípios de São Paulo"
"Me mostre o GeoJSON de Campinas"
```

## 🐛 Troubleshooting

### Erro: "Arquivo não encontrado"

**Problema:** O servidor não encontra os arquivos GeoJSON.

**Solução:** Verifique se o `GEODATA_BR_PATH` está configurado corretamente e aponta para o diretório que contém a pasta `geojson/`.

### Erro: "Módulo não encontrado"

**Problema:** Python não encontra o módulo `mcp` ou `pydantic`.

**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Command not found: python"

**Problema:** O comando `python` não está disponível no PATH.

**Solução:** Use `python3` ao invés de `python` na configuração, ou crie um alias/symlink.

### Claude/Cursor não reconhece o servidor

**Solução 1:** Verifique se o arquivo de configuração JSON está válido (use um validador JSON).

**Solução 2:** Certifique-se de que os caminhos são absolutos (não use `~` ou caminhos relativos).

**Solução 3:** Reinicie completamente a aplicação (feche e abra novamente).

### Teste de permissões

Verifique se o Python tem permissão para executar:

```bash
chmod +x src/geodata_br_mcp/server.py
```

## 📚 Próximos Passos

- Leia [EXAMPLES.md](EXAMPLES.md) para ver exemplos de uso
- Leia [README_MCP.md](README_MCP.md) para entender as tools disponíveis
- Contribua com o projeto no GitHub!

## 🆘 Suporte

Se tiver problemas:

1. Verifique os logs do Claude Desktop/Cursor
2. Teste o servidor manualmente conforme descrito acima
3. Abra uma issue no GitHub com detalhes do erro

---

**Desenvolvido com ❤️ para a comunidade brasileira de dados geográficos**

