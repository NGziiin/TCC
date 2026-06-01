const path = require("node:path");
const fs = require("node:fs")
const http = require('node:http')

// função para ir até a pasta especifica
function LoadingFille(nomeAlvo, caminhoInicial, subpasta = null) {
    let atual = caminhoInicial;

    while (true) {
        const nomePasta = path.basename(atual);

        if (nomePasta === nomeAlvo) {
            if (subpasta) {
                return path.join(atual, subpasta, 'ConfigsSystem.json'); //encontrou
            }
        }

        const anterior = path.dirname(atual);

        if (anterior === atual) {
            // chegamos na raiz e não encontramos
            return null;
        }

        atual = anterior;
    }
}

// função para ler as informações do JSON
function ReadJson(JSONPath) {
    try {
        const data = fs.readFileSync(JSONPath, 'utf-8');
        return JSON.parse(data);
    } catch (error) {
        console.log(error);
        return null;
    }
}

// função para conectar no servidor local
function ConnectLocalServer(JSONinfo){
    let { Network, ip } = JSONinfo;

    fetch(ip)
    .then(response => response.text())
    .then(dados => console.log('dados do servidor:', dados))
    .catch(error => console.log(error));
}
async function main() {
    //declaração das variáveis
    const inicio = path.dirname(__filename);
    const ReturnFile = 'TCC';

    const JSONPath = LoadingFille(ReturnFile, inicio, 'configs');
    const JSONinfo = ReadJson(JSONPath);
    console.log("variável JSONinfo: ", JSONinfo);
    ConnectLocalServer(JSONinfo)
}

main()