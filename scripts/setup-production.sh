#!/bin/bash
# Script de Setup Inicial para Produção

set -e

echo "🔧 Setup Inicial do Geodata-BR MCP para Produção"

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variáveis
APP_DIR="/opt/geodata-br"
DATA_DIR="/opt/geodata-br-data"
LOG_DIR="/var/log/geodata-br"
USER="geodata-mcp"

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
   echo -e "${RED}❌ Execute com sudo${NC}"
   exit 1
fi

# 1. Criar usuário
echo -e "${YELLOW}👤 Criando usuário $USER...${NC}"
if id "$USER" &>/dev/null; then
    echo -e "${GREEN}✅ Usuário $USER já existe${NC}"
else
    useradd -r -m -s /bin/bash "$USER"
    echo -e "${GREEN}✅ Usuário $USER criado${NC}"
fi

# 2. Criar diretórios
echo -e "${YELLOW}📁 Criando diretórios...${NC}"
mkdir -p "$APP_DIR"
mkdir -p "$DATA_DIR/geojson"
mkdir -p "$LOG_DIR"
mkdir -p /opt/backups
echo -e "${GREEN}✅ Diretórios criados${NC}"

# 3. Clonar repositório
echo -e "${YELLOW}📥 Clonando repositório...${NC}"
if [ -d "$APP_DIR/.git" ]; then
    echo -e "${YELLOW}⚠️  Repositório já existe, pulando clone${NC}"
else
    read -p "URL do repositório Git: " REPO_URL
    git clone "$REPO_URL" "$APP_DIR"
    echo -e "${GREEN}✅ Repositório clonado${NC}"
fi

# 4. Criar ambiente virtual
echo -e "${YELLOW}🐍 Criando ambiente virtual...${NC}"
sudo -u "$USER" python3 -m venv "$APP_DIR/.venv"
echo -e "${GREEN}✅ Ambiente virtual criado${NC}"

# 5. Instalar dependências
echo -e "${YELLOW}📦 Instalando dependências...${NC}"
sudo -u "$USER" bash -c "source $APP_DIR/.venv/bin/activate && pip install --upgrade pip && pip install -r $APP_DIR/requirements.txt"
echo -e "${GREEN}✅ Dependências instaladas${NC}"

# 6. Criar arquivo de configuração
echo -e "${YELLOW}⚙️  Criando configuração...${NC}"
if [ ! -f "$APP_DIR/.env.production" ]; then
    cp "$APP_DIR/.env.production.example" "$APP_DIR/.env.production"
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edite $APP_DIR/.env.production${NC}"
else
    echo -e "${GREEN}✅ Configuração já existe${NC}"
fi

# 7. Ajustar permissões
echo -e "${YELLOW}🔐 Ajustando permissões...${NC}"
chown -R "$USER:$USER" "$APP_DIR"
chown -R "$USER:$USER" "$DATA_DIR"
chown -R "$USER:$USER" "$LOG_DIR"
chmod 600 "$APP_DIR/.env.production"
chmod +x "$APP_DIR/scripts/"*.sh
echo -e "${GREEN}✅ Permissões ajustadas${NC}"

# 8. Criar serviço systemd
echo -e "${YELLOW}🔄 Criando serviço systemd...${NC}"
cat > /etc/systemd/system/geodata-mcp.service << SYSTEMD
[Unit]
Description=Geodata BR MCP Server
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/.venv/bin"
EnvironmentFile=$APP_DIR/.env.production
ExecStart=$APP_DIR/.venv/bin/python $APP_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=append:$LOG_DIR/stdout.log
StandardError=append:$LOG_DIR/stderr.log

# Segurança
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$LOG_DIR

[Install]
WantedBy=multi-user.target
SYSTEMD

systemctl daemon-reload
systemctl enable geodata-mcp
echo -e "${GREEN}✅ Serviço systemd criado e habilitado${NC}"

# 9. Configurar logrotate
echo -e "${YELLOW}📝 Configurando logrotate...${NC}"
cat > /etc/logrotate.d/geodata-mcp << LOGROTATE
$LOG_DIR/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 $USER $USER
    sharedscripts
    postrotate
        systemctl reload geodata-mcp > /dev/null 2>&1 || true
    endscript
}
LOGROTATE
echo -e "${GREEN}✅ Logrotate configurado${NC}"

# 10. Instruções finais
echo ""
echo -e "${GREEN}🎉 Setup concluído!${NC}"
echo ""
echo -e "${YELLOW}📋 PRÓXIMOS PASSOS:${NC}"
echo ""
echo "1. Copie os arquivos GeoJSON para $DATA_DIR/geojson/"
echo "   Exemplo: scp -r geojson/* $USER@servidor:$DATA_DIR/geojson/"
echo ""
echo "2. Edite a configuração:"
echo "   nano $APP_DIR/.env.production"
echo ""
echo "3. Inicie o serviço:"
echo "   sudo systemctl start geodata-mcp"
echo ""
echo "4. Verifique o status:"
echo "   sudo systemctl status geodata-mcp"
echo ""
echo "5. Veja os logs:"
echo "   sudo journalctl -u geodata-mcp -f"
echo ""
