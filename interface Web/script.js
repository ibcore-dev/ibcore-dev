const API = "http://127.0.0.1:8000";

// ===== NAVEGAÇÃO =====

function goLogin() {
    window.location.href = "login.html";
}

function goRegister() {
    window.location.href = "register.html";
}

// ===== LOGIN =====

async function login() {

    let username = document.getElementById("user").value;
    let password = document.getElementById("pass").value;

    let res = await fetch(API + "/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });

    let data = await res.json();

    if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "chat.html";
    } else {
        alert("Erro login");
    }
}

// ===== REGISTER =====

async function register() {

    let username = document.getElementById("newUser").value;
    let password = document.getElementById("newPass").value;

    let res = await fetch(API + "/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });

    let data = await res.json();

    alert(data.message);
}

// ===== CHAT =====

async function send() {

    let msg = document.getElementById("msg").value;
    let token = localStorage.getItem("token");

    let res = await fetch(API + "/command", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            token: token,
            input: msg
        })
    });

    let data = await res.json();

    let box = document.getElementById("messages");

    box.innerHTML += `<p>Você: ${msg}</p>`;
    box.innerHTML += `<p>Órion: ${data.response}</p>`;
}