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

// =========================
// 📈 GRÁFICO
// =========================
function atualizarGrafico(dados) {

    new Chart(document.getElementById("grafico"), {
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

// =========================
// 🚀 INICIAR
// =========================
carregarDashboard();
carregarUsuarios();

// 🔄 Atualiza a cada 5 segundos
setInterval(() => {
    carregarDashboard();
    carregarUsuarios();
}, 5000);