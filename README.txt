# Criar ambiente corretamente para rodar projeto

Caso esteja utilizando um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

```

Instalar dependências 
```bash
pip install psycopg2 sqlalchemy sqlacodegen
```

Gerar modelo `VIEW` com sqlacodegen:
```bash
sqlacodegen postgresql://usuario:senha@localhost/northwind --outfile=model.py

```
 
