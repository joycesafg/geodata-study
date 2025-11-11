# ✅ Checklist Antes de Commitar

## 🚀 Passo a Passo

### 1. Ative o Ambiente Virtual
```bash
source .venv/bin/activate
```

### 2. Execute os Testes
```bash
make check
```

Ou individualmente:
```bash
make lint-fix  # Corrige problemas de lint
make format    # Formata código
make test      # Executa testes
```

### 3. Verifique a Cobertura
```bash
# A cobertura deve estar >= 80%
pytest --cov=src/geodata_br_mcp --cov-report=term-missing
```

### 4. Commit
```bash
git add .
git commit -m "sua mensagem"
```

---

## 🛡️ O Que o Pre-commit Vai Verificar

Quando você fizer `git commit`, serão executados **localmente**:

1. ✅ **Validações Básicas**
   - Remove espaços em branco
   - Corrige line endings
   - Valida YAML/TOML

2. ✅ **Ruff** - Linter + Formatador
   - Analisa e corrige código

3. ✅ **Black** - Formatador
   - Garante estilo consistente

4. ✅ **MyPy** - Verificador de Tipos
   - Verifica tipos estáticos (apenas src/)

**Nota:** Os testes (Pytest) rodam automaticamente no **GitHub Actions CI/CD**, não no pre-commit local. Por isso é importante executar `make test` antes de fazer push!

---

## ⚠️ Execute Testes ANTES do Push

Os testes **não rodam no pre-commit local**, mas rodam no CI do GitHub Actions.

**Execute antes de fazer push:**
```bash
make test
# Se passar, faça push
git push
```

**Se precisar pular os hooks locais (não recomendado):**
```bash
git commit --no-verify -m "sua mensagem"
```

---

## 📊 Resultado Esperado do Pre-commit

Quando tudo estiver OK no commit local, você verá:

```
Trim Trailing Whitespace.............................Passed
Fix End of Files.....................................Passed
Check Yaml...........................................Passed
Check Toml...........................................Passed
Debug Statements (Python)............................Passed
Mixed line ending....................................Passed
Ruff Linter..........................................Passed
Ruff Formatter.......................................Passed
Black Code Formatter.................................Passed
MyPy Type Checker....................................Passed

[main abc1234] sua mensagem
 X files changed, Y insertions(+), Z deletions(-)
```

**Depois do Push:** O GitHub Actions vai executar os testes automaticamente!

---

## 🔥 Comandos Rápidos

```bash
# Verificar tudo de uma vez
make check

# Corrigir problemas automaticamente
make lint-fix && make format

# Ver cobertura de testes
make test-cov

# Ver todos os comandos disponíveis
make help
```

---

## 📁 Arquivos Ignorados

Os seguintes arquivos/diretórios são automaticamente ignorados:

- `geojson/` - Arquivos GeoJSON (muito grandes)
- `__pycache__/` - Cache do Python
- `.venv/` - Ambiente virtual
- `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/` - Caches

---

## 💡 Dicas

1. **Execute `make check` ANTES de commitar** para evitar surpresas
2. **Se um hook corrigir arquivos**, adicione-os novamente com `git add .` e tente o commit de novo
3. **Mantenha a cobertura >= 80%** - Adicione testes para código novo
4. **Use commits pequenos e frequentes** - Mais fácil de debugar

---

## 🆘 Ajuda

- **Problemas?** Veja [PRECOMMIT.md](PRECOMMIT.md)
- **Erros do CI?** Veja [CI_FIXES.md](CI_FIXES.md)
- **Comandos?** Execute `make help`

