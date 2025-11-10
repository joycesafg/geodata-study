#!/bin/bash
# Script de instalação do Pre-commit

set -e

echo "🔧 Instalando Pre-commit..."
echo ""

# Verifica se está em um ambiente virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  AVISO: Você não está em um ambiente virtual!"
    echo "   Recomendamos criar um ambiente virtual primeiro:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Instalação cancelada."
        exit 1
    fi
fi

# Instala as dependências de desenvolvimento
echo "📦 Instalando dependências de desenvolvimento..."
pip install -r requirements-dev.txt

# Instala os hooks do pre-commit
echo ""
echo "🪝 Configurando hooks do pre-commit..."
pre-commit install

# Executa os hooks em todos os arquivos (primeira vez)
echo ""
echo "🧪 Executando pre-commit em todos os arquivos pela primeira vez..."
echo "   (Isso pode demorar um pouco na primeira execução)"
echo ""
pre-commit run --all-files || true

echo ""
echo "✅ Pre-commit instalado com sucesso!"
echo ""
echo "📝 Comandos úteis:"
echo "   - pre-commit run --all-files  : Executa em todos os arquivos"
echo "   - pre-commit run <hook-id>    : Executa um hook específico"
echo "   - pre-commit autoupdate       : Atualiza as versões dos hooks"
echo "   - pre-commit uninstall        : Remove os hooks do git"
echo ""
echo "🎉 Agora os hooks serão executados automaticamente antes de cada commit!"
