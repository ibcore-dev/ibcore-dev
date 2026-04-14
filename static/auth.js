const API = "http://127.0.0.1:8000";

// =========================
// 🔐 LOGIN
// =========================
async function login() {
    let username = document.getElementById("loginUser").value;
    let password = document.getElementById("loginPass").value;

    try {
        let r = await fetch(API + "/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });

        if (!r.ok) {
            alert("Login inválido");
            return;
        }

        let data = await r.json();

        // 🔥 SALVA TOKEN
        localStorage.setItem("token", data.access_token);

        // 🔥 SALVA USERNAME (IMPORTANTE)
        localStorage.setItem("username", username);

        // 🔥 REDIRECIONA PRO ÓRION
        window.location.href = "orion_chat.html";

    } catch (e) {
        alert("Erro de conexão com servidor");
    }
}