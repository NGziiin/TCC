class InternalFunctions {
    static async encode(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    };

    static async UploadDados(username, password){
        const dados = {
            nome: username,
            senha: password
        };

        try {
            const resposta = await fetch('http://127.0.0.1:8080/DadosLogin', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(dados)
            });
            if (!resposta.ok) {
                new Error(`Erro na requisição: ${resposta.status} - ${resposta.statusText}`)
            }

            const resultado = await resposta.json();
            console.log('resposta da API:', resultado);
        } catch (erro) {
            console.error('falha ao enviar dados: ', erro.message)
        }
    }
}

window.getLogin = async function() {
    try {
        const {value: username} = document.getElementById("InputName");
        const {value: password} = document.getElementById("InputPassword");

        const encodedPassword = await InternalFunctions.encode(password);
        await InternalFunctions.UploadDados(username, encodedPassword)


    } catch (error) {
        console.error(error);
    }
}

window.togglePasswordVisibility = async function() {
    const input = document.getElementById("InputPassword");
    const icon = document.getElementById('iconEye');

    if (input.type === 'password'){
        input.type = 'text';
        icon.src= "../../image/Visible.png";
        icon.alt = "";
    }else {
        input.type = 'password';
        icon.src= "../../image/Invisible.png";
        icon.alt = "";
    }
}