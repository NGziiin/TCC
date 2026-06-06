const { contextBridge } = require('electron');
const path = require('path');
const fs = require('fs');

function LoadingFille(nomeAlvo, caminhoInicial, subpasta = null) {
  let atual = caminhoInicial;

  while (true) {
    const nomePasta = path.basename(atual);

    if (nomePasta === nomeAlvo) {
      if (subpasta) {
        return path.join(atual, subpasta, 'ConfigsSystem.json');
      }
    }

    const anterior = path.dirname(atual);

    if (anterior === atual) {
      return null;
    }

    atual = anterior;
  }
}

function ReadJson() {
  const inicio = __dirname;

  const JSONPath = LoadingFille(
      'TCC',
      inicio,
      'configs'
  );

  const data = fs.readFileSync(JSONPath, 'utf8');

  return JSON.parse(data);
}

contextBridge.exposeInMainWorld('API', {

  GetServerIP: () => {
    const config = ReadJson();
    return config.ip;
  },

  Login: async (usuario, senha) => {

    const config = ReadJson();

    const resposta = await fetch(
        `${config.ip}/DadosLogin`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            nome: usuario,
            senha: senha
          })
        }
    );

    return await resposta.json();
  }
});