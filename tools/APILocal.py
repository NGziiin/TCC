from fastapi import FastAPI
from pydantic import BaseModel

# Criando a aplicação FastAPI
app = FastAPI()

#Usado para pegar as informações do login
class LoginJSON(BaseModel):
    nome: str
    senha: str

# Rota inicial
@app.get("/")
def read_root():
    return {"mensagem": "olá"}

# Rota para receber as informações do login
@app.post("/DadosLogin")
async def login(dados: LoginJSON):

    # importando o arquivo
    from core.validationLogin import ITFunctionLogin

    # função para verificar a senha
    instancePy = ITFunctionLogin()
    VerPython = instancePy.login(dados.nome, dados.senha)#verifica no banco de dados o login

    return {'status' : VerPython}