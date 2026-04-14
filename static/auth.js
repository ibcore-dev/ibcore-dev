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
            body: JSON.stringify({ username, password })
        });

        let data = await r.json();

        if (!r.ok) {
            alert(data.detail || "Login inválido");
            return;
        }

        // 🔐 salva token
        localStorage.setItem("token", data.access_token);

        // 👤 salva usuário
        localStorage.setItem("username", username);

        alert("Login realizado com sucesso!");

        // 🚀 redireciona pro chat
        window.location.href = "orion_chat.html";

    } catch (e) {
        alert("Erro de conexão com servidor");
        console.error(e);
    }
}