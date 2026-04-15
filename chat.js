const API = "http://127.0.0.1:8000/command";

function addMessage(text, sender) {

    let wrapper = document.createElement("div");
    wrapper.className = sender;

    let bubble = document.createElement("div");
    bubble.innerText = text;

    wrapper.appendChild(bubble);

    document.getElementById("messages").appendChild(wrapper);

    document.getElementById("messages").scrollTop = 9999;
}

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
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                token: token,
                input: message
            })
        });

        let data = await r.json();

        addMessage(data.response, "orion");

    } catch (e) {
        addMessage("Erro ao conectar com o Órion", "orion");
    }
}