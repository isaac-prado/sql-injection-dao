# 📦 Configuração do Ambiente para Rodar o Projeto

Este guia irá ajudá-lo a configurar corretamente o ambiente para o projeto com banco de dados `northwind`.

---

## ✅ Passo 1: Criar Ambiente Virtual

Recomenda-se utilizar um ambiente virtual para isolar as dependências do projeto.

### Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

---

## 📥 Passo 2: Instalar Dependências

Instale os pacotes necessários utilizando o `pip`:

```bash
pip install psycopg2 sqlalchemy
```

---

## 🔧 Passo 3: Configurar Credenciais do Banco

Substitua as credenciais de acesso ao banco PostgreSQL no arquivo:

```
db/orm/database.py
```

e também em:

```
db/noorm/database.py
```

> 🔒 Altere `usuário` e `senha` conforme o seu ambiente local.

---
