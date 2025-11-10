# Pre-commit - Guia de Uso

## 🚀 Instalação

```bash
# Opção 1: Script automatizado
./.pre-commit-install.sh

# Opção 2: Com Make
make install-dev

# Opção 3: Manual
pip install -r requirements-dev.txt
pre-commit install
```

## 🛠️ O Que Faz

Toda vez que você faz `git commit`, executa automaticamente:

- ✅ **Ruff** - Linter + formatador
- ✅ **Black** - Formatação de código
- ✅ **MyPy** - Verificação de tipos (apenas src/)
- ✅ Validações básicas (espaços, YAML, JSON, etc)

**Nota:** Os testes (Pytest) rodam no GitHub Actions CI/CD, não no pre-commit local.

## 💻 Comandos Úteis

```bash
# Desenvolvimento
make test              # Executa testes
make lint-fix          # Corrige problemas
make format            # Formata código
make check             # Verifica tudo

# Pre-commit
pre-commit run --all-files              # Executa em todos os arquivos
pre-commit run ruff --all-files         # Apenas ruff
pre-commit autoupdate                   # Atualiza versões

# Commit
git commit -m "mensagem"                # Normal (hooks automáticos)
git commit --no-verify -m "mensagem"    # Pula hooks (emergência)

# Execute os testes ANTES de commitar (recomendado)
make test  # ou: pytest -v --cov=src/geodata_br_mcp
```

## 🐛 Problemas Comuns

**Hooks modificaram meus arquivos**
```bash
# Normal! Ruff/Black formatam automaticamente
git add .
git commit -m "mensagem"
```

**Testes falharam**
```bash
# Corrija o código e tente novamente
pytest -v  # Ver os erros
```

**MyPy reclamando de tipos**
```python
# Adicione type hints
def funcao(x: int) -> str:
    return str(x)

# Ou ignore casos específicos
result = foo()  # type: ignore
```

## ⚙️ Configuração

- **Pre-commit**: `.pre-commit-config.yaml`
- **Ruff/Black/MyPy/Pytest**: `pyproject.toml`

## 📚 Mais Info

- Documentação: https://pre-commit.com/
- Comandos Make: `make help`
- Ajuda: `pre-commit --help`
