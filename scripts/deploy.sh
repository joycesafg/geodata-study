#!/bin/bash
# Script de Deploy para Produção

set -e

echo "🚀 Iniciando deploy do Geodata-BR MCP..."

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variáveis
APP_DIR="/opt/geodata-br"
DATA_DIR="/opt/geodata-br-data"
BACKUP_DIR="/opt/backups"
USER="geodata-mcp"

# Verificar se está rodando como root ou sudo
if [ "$EUID" -ne 0 ]; then
   echo -e "${RED}❌ Execute com sudo${NC}"
   exit 1
fi

# Criar backup
echo -e "${YELLOW}📦 Criando backup...${NC}"
BACKUP_FILE="${BACKUP_DIR}/geodata-br-$(date +%Y%m%d-%H%M%S).tar.gz"
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_FILE" -C "$(dirname $APP_DIR)" "$(basename $APP_DIR)"
echo -e "${GREEN}✅ Backup criado: $BACKUP_FILE${NC}"

# Parar serviço
echo -e "${YELLOW}⏸️  Parando serviço...${NC}"
systemctl stop geodata-mcp || true
echo -e "${GREEN}✅ Serviço parado${NC}"

# Atualizar código
echo -e "${YELLOW}📥 Atualizando código...${NC}"
cd "$APP_DIR"
sudo -u "$USER" git pull origin main
echo -e "${GREEN}✅ Código atualizado${NC}"

# Atualizar dependências
echo -e "${YELLOW}📦 Atualizando dependências...${NC}"
sudo -u "$USER" bash -c "source .venv/bin/activate && pip install -r requirements.txt"
echo -e "${GREEN}✅ Dependências atualizadas${NC}"

# Verificar configuração
if [ ! -f "$APP_DIR/.env.production" ]; then
    echo -e "${RED}❌ Arquivo .env.production não encontrado!${NC}"
    echo -e "${YELLOW}Criando do exemplo...${NC}"
    cp "$APP_DIR/.env.production.example" "$APP_DIR/.env.production"
    echo -e "${YELLOW}⚠️  EDITE $APP_DIR/.env.production antes de reiniciar!${NC}"
    exit 1
fi

# Reiniciar serviço
echo -e "${YELLOW}▶️  Iniciando serviço...${NC}"
systemctl start geodata-mcp
sleep 2
echo -e "${GREEN}✅ Serviço iniciado${NC}"

# Verificar status
echo -e "${YELLOW}🔍 Verificando status...${NC}"
if systemctl is-active --quiet geodata-mcp; then
    echo -e "${GREEN}✅ Serviço está ATIVO${NC}"
    systemctl status geodata-mcp --no-pager
else
    echo -e "${RED}❌ Serviço FALHOU ao iniciar!${NC}"
    journalctl -u geodata-mcp -n 50 --no-pager
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Deploy concluído com sucesso!${NC}"
echo ""
echo "📊 Comandos úteis:"
echo "  Ver logs:     sudo journalctl -u geodata-mcp -f"
echo "  Status:       sudo systemctl status geodata-mcp"
echo "  Parar:        sudo systemctl stop geodata-mcp"
echo "  Reiniciar:    sudo systemctl restart geodata-mcp"
echo "  Restaurar:    tar -xzf $BACKUP_FILE -C /"
