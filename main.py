"""
Comandos de implementação de API
em Python com o framework
FastAPI

1) Instalação das dependências no Terminal: 
- pip install fastapi
- pip install uvicorn
- pip install mysql-connector-python

2) Execução do servidor no Terminal:
- uvicorn main:app --reload
- endereço do servidor:
    localhost:8000

3) Acesso à documentação da API
- digitar na barra de endereços:
    localhost:8000/docs

"""


from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import mysql.connector

app = FastAPI()

@app.get("/")
def saudacao():
    return {"mensagem":"API funcionando"}

#Conectar ao banco de dados 'novaloja'
def conectarBD():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'novaloja'
    )

# Rota de busca de produtos
@app.get("/produtos")
def buscaProdutos():
    conexao = conectarBD()
    cursor = conexao.cursor()
    comando = "SELECT * FROM produtos"
    cursor.execute(comando)
    resultado = cursor.fetchall()
    produtos = []
    for row in resultado:
        produto = {"id": row[0], "nome": row[1], "valor": row[2]}
        produtos.append(produto)
    return {"produtos" : produtos}
"""
[produtos][id]
[produtos][nome]
[produtos][valor]
"""

# Rota de busca do produto pelo id
@app.get("/produtos/{id}")
def buscaProdutoID(id: int):
    conexao = conectarBD()
    cursor = conexao.cursor()
    comando = "SELECT * FROM produtos WHERE id = %s"
    values = (id,)
    cursor.execute(comando, values)
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code = 404, detail="Produto não encontrado")
    
    produto = {"id": resultado[0], "nome": resultado[1], "valor": resultado[2]}
    return {"produto" : produto}

# Rota de busca do produto pelo nome
@app.get("/produtos/nome/{nome}")
def buscaProdutoNome(nome: str):
    conexao = conectarBD()
    cursor = conexao.cursor()
    comando = "SELECT * FROM produtos WHERE nome = %s"
    values = (nome,)
    cursor.execute(comando, values)
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code = 404, detail="Produto não encontrado com esse nome")
    
    produto = {"id": resultado[0], "nome": resultado[1], "valor": resultado[2]}
    return {"produto" : produto}

# Rota de cadastro de produto
""" @app.post("/produtos")
def criaProduto(nome: str, valor: int):
    conexao = conectarBD()
    cursor = conexao.cursor()
    comando = "INSERT INTO produtos(nome, valor) VALUES(%s, %s)"
    values = (nome, valor)
    cursor.execute(comando, values)
    return {"mensagem": "Produto cadastrado com sucesso"}
 """
# Rota de cadastro de produto com requisição no corpo em JSON
@app.post("/produtos", response_model = dict)
def criaProduto(produto: dict):
    conexao = conectarBD()
    cursor = conexao.cursor()
    comando = "INSERT INTO produtos(nome, valor) VALUES(%s, %s)"
    values = (produto["nome"], produto["valor"])
    cursor.execute(comando, values)
    produto = cursor.lastrowid
    return {"mensagem": "Produto cadastrado com sucesso"}

# Rota para atualizar um produto
@app.put("/produtos/{id}", response_model = dict)
def alteraProduto(produto: dict, id: int, nome: str = None, valor: int = None):
    conexao = conectarBD()
    cursor = conexao.cursor()
    comando = "SELECT * FROM produtos WHERE id = %s"
    values = (id,)
    cursor.execute(comando, values)
    resultado = cursor.fetchone()
    print("Produto encontrado")
    if resultado is None:
        raise HTTPException(status_code = 404, detail="Produto não encontrado")
    if nome is not None and valor is not None:
        comando = "UPDATE produtos SET nome = %s, valor = %s WHERE id = %s"
        values = (produto["nome"], produto["valor"])
        cursor.execute(comando, values)
        conexao.commit()
        #cursor.close()
        #conexao.end()
    return {"mensagem" : "Produto atualizado com sucesso"}

# Rota de excluir um produto
@app.delete("/produtos/{id}")
def excluiProduto(id: int):
    conexao = conectarBD()
    cursor = conexao.cursor()
    comando = "SELECT * FROM produtos WHERE id = %s"
    values = (id,)
    cursor.execute(comando, values)
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code = 404, detail="Produto não encontrado")
    else:
        comando = "DELETE FROM produtos WHERE id = %s"
        values = (id,)
        cursor.execute(comando, values)
    return {"mensagem" : "Produto excluído com sucesso"}
