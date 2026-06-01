class InternalFunctions {
    static async encode(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    };
}

window.getLogin = async function() {
    try {
        const {value: username} = document.getElementById("InputName");
        const {value: password} = document.getElementById("InputPassword");
        if (password.length < 6) {
            console.log('a senha tem menos de 6 caracteres');
        } else {
            const encodedPassword = await InternalFunctions.encode(password);
            console.log(encodedPassword);
        }
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