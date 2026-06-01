from fastapi import FastAPI
from pydantic import BaseModel

# Criando a aplicação FastAPI
app = FastAPI()

#Usado para pegar as informações do login
class Login(BaseModel):
    nome: str
    senha: str

# Rota inicial
@app.get("/")
def read_root():
    return {"mensagem": "olá"}

# Rota para receber as informações do login
@app.post("/DadosLogin")
async def login(dados: Login):
    body = dados
    print(f'informações do login: {body}')
    return {'status': "ok", 'dados': body}

