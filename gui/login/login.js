// aqui são as funções que comunicam com o HTML
window.getLogin = async function() {
    try {
        const { value: username} = document.getElementById("InputName");
        const { value: password} = document.getElementById("InputPassword");

        if (!username) {
            document.getElementById('InputName')
                .setAttribute('placeholder', 'insira um nome');
            return;
        }
        if (!password) {
            document.getElementById('InputPassword')
                .setAttribute('placeholder', 'insira uma senha');
            return;
        }

        const resultado = await window.API.Login(username, password);

        if (resultado.Status === true){
            localStorage.setItem('Token', resultado.Token);
            window.location.href='../main/main.html';
        } else {
            document.getElementById('InputPassword').value = '';
            document.getElementById('InputName').value = '';
            const dialogo = document.getElementById('ErroLogin');
            const erroButton = document.getElementById('Errologinbutton');

            dialogo.showModal()

            erroButton.addEventListener('click', () => {
                dialogo.close();
            });
        }

    } catch (error) {
        console.error(error);
    }
}

// ICONE DE VISUALIZAR A SENHA
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