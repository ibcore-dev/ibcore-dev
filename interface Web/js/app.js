function irLogin() {
    window.location.href = "login.html";
}

function login() {
    let email = document.getElementById("email").value;
    let senha = document.getElementById("senha").value;

    if(email && senha){
        // Aqui depois vamos conectar com FastAPI
        window.location.href = "chat.html";
    } else {
        alert("Preencha os dados");
    }
}

function enviar() {
    let input = document.getElementById("input");
    let mensagens = document.getElementById("messages");

    let texto = input.value;

    mensagens.innerHTML += `<div class="msg user">Você: ${texto}</div>`;
    mensagens.innerHTML += `<div class="msg bot">Órion: Processando comando...</div>`;

    input.value = "";
}