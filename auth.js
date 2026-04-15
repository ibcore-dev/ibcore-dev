const API = "https://orion-api-d5gp.onrender.com";

async function login() {

    let username = document.getElementById("loginUser").value.trim();
    let password = document.getElementById("loginPass").value.trim();

    console.log("ENVIANDO:", username, password); // DEBUG

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

        console.log("RESPOSTA:", data); // DEBUG

        if (!r.ok) {
            alert(JSON.stringify(data)); // 🔥 MOSTRA ERRO REAL
            return;
        }

        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", username);

        alert("Login OK");

        window.location.href = "orion_chat.html";

    } catch (e) {
        console.error("ERRO:", e);
        alert("Erro de conexão");
    }
}