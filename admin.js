const API = "https://orion-api-d5gp.onrender.com";

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
            console.error("Erro dashboard:", data);
            return;
        }

        // 🔥 atualiza cards
        document.getElementById("usuarios").innerText = data.usuarios || 0;
        document.getElementById("mensagens").innerText = data.mensagens || 0;
        document.getElementById("ia").innerText = data.ia || 0;
        document.getElementById("erros").innerText = data.erros || 0;

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
            console.error("Erro usuários:", data);
            return;
        }

        const lista = document.getElementById("lista-usuarios");

        if (!lista) return;

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
// ⚠️ ERROS
// =========================
async function carregarErros() {

    try {
        const res = await fetch(API + "/admin/errors", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        if (!res.ok) {
            console.error("Erro ao buscar erros:", data);
            return;
        }

        const lista = document.getElementById("lista-erros");

        if (!lista) return;

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
// 📈 GRÁFICO (CORRIGIDO)
// =========================
let chartInstance = null;

function atualizarGrafico(dados) {

    const canvas = document.getElementById("grafico");
    if (!canvas) return;

    const dadosSeguros = Array.isArray(dados) ? dados : [0, 0, 0, 0, 0];

    // 🔥 cria só uma vez
    if (!chartInstance) {
        chartInstance = {
            type: 'line',
            data: {
                labels: ["Seg", "Ter", "Qua", "Qui", "Sex"],
                datasets: [{
                    label: "Uso",
                    data: dadosSeguros,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
        return;
    }


}

// =========================
// 🚀 INICIAR
// =========================
function iniciarPainel() {
    console.log("🚀 Painel iniciado");

    carregarDashboard();
    carregarUsuarios();
    carregarErros();
}

// chama uma vez
iniciarPainel();

// 🔄 Atualização automática
setInterval(() => {
    console.log("🔄 Atualizando...");

    carregarDashboard();
    carregarUsuarios();
    carregarErros();

}, 5000);