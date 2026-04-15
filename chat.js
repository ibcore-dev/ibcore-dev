const API = "https://orion-api-d5gp.onrender.com/command";

async function send() {

    let input = document.getElementById("input");
    let message = input.value;

    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    let token = localStorage.getItem("token");

    if (!token) {
        alert("Sessão expirada");
        return;
    }

    try {
        let r = await fetch(API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                input: message
            })
        });

        let data = await r.json();

        // 🔥 TRATAMENTO DE ERRO
        if (!r.ok) {
            addMessage(data.detail || "Erro no servidor", "orion");
            return;
        }

        addMessage(data.response || "Sem resposta", "orion");

    } catch (e) {
        addMessage("Erro ao conectar com o Órion", "orion");
        console.error(e);
    }
}