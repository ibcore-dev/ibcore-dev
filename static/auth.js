const API = "https://orion-api-d5gp.onrender.com";

// =========================
// 🔐 LOGIN
// =========================
async function login() {

    let username = document.getElementById("loginUser").value;
    let password = document.getElementById("loginPass").value;

    if (!username || !password) {
        alert("Preencha usuário e senha");
        return;
    }

    try {
        let r = await fetch(API + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        let data = await r.json();

        if (!r.ok) {
            alert(data.detail || "Login inválido");
            return;
        }

        // 🔥 SALVA TOKEN
        localStorage.setItem("token", data.access_token);

        // 🔥 SALVA USUÁRIO
        localStorage.setItem("username", username);

        console.log("TOKEN SALVO:", data.access_token);

        alert("Login realizado com sucesso!");

        // 🚀 REDIRECIONA
        window.location.href = "orion_chat.html";

    } catch (e) {
        alert("Erro de conexão com servidor");
        console.error(e);
    }
}