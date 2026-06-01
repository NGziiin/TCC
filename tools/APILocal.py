from fastapi import FastAPI

# Criando a aplicação FastAPI
app = FastAPI()

# Rota inicial
@app.get("/")
def read_root():
    return {"mensagem": "olá"}

# Rota para receber as informações do login
@app.post("/DadosLogin")
async def login(username: str, password: str):
    body = {"username": username, "password": password}
    return {'status': "ok", 'dados': body}

