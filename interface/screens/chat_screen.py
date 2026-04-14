import customtkinter as ctk
from controller.chat_controller import ChatController


class ChatScreen(ctk.CTkFrame):

    def __init__(self, master, token):
        super().__init__(master)

        self.controller = ChatController(token)

        # =========================
        # CONFIGURAÇÃO VISUAL
        # =========================

        self.configure(fg_color="#1b1b1b")

        title = ctk.CTkLabel(
            self,
            text="ÓRION NEXUS - SISTEMA ATIVO",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        # =========================
        # CHAT BOX
        # =========================

        self.chat_box = ctk.CTkTextbox(
            self,
            width=850,
            height=450,
            corner_radius=12,
            font=("Consolas", 14)
        )

        self.chat_box.pack(pady=20)
        self.chat_box.insert("end", "🤖 Órion: Sistema iniciado. Como posso ajudar?\n\n")

        # =========================
        # BARRA INFERIOR
        # =========================

        bottom = ctk.CTkFrame(self)
        bottom.pack(pady=10)

        self.entry = ctk.CTkEntry(
            bottom,
            placeholder_text="Digite sua mensagem...",
            width=650,
            height=35,
            font=("Arial", 14)
        )

        self.entry.pack(side="left", padx=10)

        # ENTER envia mensagem
        self.entry.bind("<Return>", self.send_message_event)

        send = ctk.CTkButton(
            bottom,
            text="Enviar",
            width=120,
            height=35,
            command=self.send_message
        )

        send.pack(side="left")

        # foco automático
        self.entry.focus()

    # =========================
    # EVENTO ENTER
    # =========================

    def send_message_event(self, event):
        self.send_message()

    # =========================
    # ENVIO DE MENSAGEM
    # =========================

    def send_message(self):

        text = self.entry.get().strip()

        if not text:
            return

        # mensagem do usuário
        self.chat_box.insert("end", f"👤 Você: {text}\n")
        self.chat_box.see("end")

        # resposta do Orion
        response = self.controller.send_message(text)

        self.chat_box.insert("end", f"🤖 Órion: {response}\n\n")
        self.chat_box.see("end")

        # limpa campo
        self.entry.delete(0, "end")