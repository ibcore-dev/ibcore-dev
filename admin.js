const API = "https://orion-api-d5gp.onrender.com";

// 🔐 TOKEN
let token = localStorage.getItem("token");

if (!token) {
    alert("Você precisa estar logado");
    window.location.href = "index.html";
}

// =========================
// 📊 DASHBOARD
// =========================
async function carregarDashboard() {

    try {
        const res = await fetch(API + "/admin/dashboard", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        if (!res.ok) {
            console.error(data);
            return;
        }

        document.getElementById("usuarios").innerText = data.usuarios;
        document.getElementById("mensagens").innerText = data.mensagens;
        document.getElementById("ia").innerText = data.ia;
        document.getElementById("erros").innerText = data.erros;

        atualizarGrafico(data.historico);

    } catch (e) {
        console.error("Erro dashboard:", e);
    }
}

// =========================
// 👥 USUÁRIOS
// =========================
async function carregarUsuarios() {

    try {
        const res = await fetch(API + "/admin/usuarios", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        if (!res.ok) {
            console.error(data);
            return;
        }

        const lista = document.getElementById("lista-usuarios");
        lista.innerHTML = "";

        data.usuarios.forEach(user => {
            const div = document.createElement("div");
            div.className = "usuario-item";
            div.innerText = user;
            lista.appendChild(div);
        });

    } catch (e) {
        console.error("Erro usuários:", e);
    }
}

async function carregarMensagens() {

    try {
        const res = await fetch(API + "/admin/mensagens", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        if (!res.ok) {
            console.error(data);
            return;
        }

        const lista = document.getElementById("lista-mensagens");
        lista.innerHTML = "";

        data.mensagens.forEach(msg => {
            const div = document.createElement("div");
            div.className = "mensagem-item";

            div.innerHTML = `
                <strong>Usuário:</strong> ${msg.pergunta}<br>
                <strong>Órion:</strong> ${msg.resposta}<br>
                <small>${msg.data}</small>
            `;

            lista.appendChild(div);
        });

    } catch (e) {
        console.error("Erro mensagens:", e);
    }
}
// =========================
// 📈 GRÁFICO
// =========================
let grafico;

function atualizarGrafico(dados) {

    if (grafico) {
        grafico.destroy();
    }

    grafico = new Chart(document.getElementById("grafico"), {
        type: 'line',
        data: {
            labels: ["Seg", "Ter", "Qua", "Qui", "Sex"],
            datasets: [{
                label: "Uso",
                data: dados,
                tension: 0.4
            }]
        }
    });
}

async function carregarErros() {

    try {
        const res = await fetch(API + "/admin/erros", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        if (!res.ok) {
            console.error(data);
            return;
        }

        const lista = document.getElementById("lista-erros");
        lista.innerHTML = "";

        data.erros.forEach(erro => {
            const div = document.createElement("div");
            div.className = "erro-item";

            div.innerHTML = `
                <strong>${erro.mensagem}</strong><br>
                <small>${erro.data} | ${erro.rota}</small>
            `;

            lista.appendChild(div);
        });

    } catch (e) {
        console.error("Erro ao carregar erros:", e);
    }
}
// =========================
// 🚀 INICIAR
// =========================
carregarDashboard();
carregarUsuarios();
carregarMensagens();  // 🔥 faltava
carregarErros();      // 🔥 faltava

// 🔄 Atualiza a cada 5 segundos
setInterval(() => {
    carregarDashboard();
    carregarUsuarios();
    carregarMensagens();
    carregarErros(); // 
}, 5000);