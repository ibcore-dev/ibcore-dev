from controller.auth_controller import AuthController
from screens.chat_screen import ChatScreen
import customtkinter as ctk


class LoginScreen(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.auth = AuthController()

        title = ctk.CTkLabel(self, text="ÓRION NEXUS", font=("Arial",36,"bold"))
        title.pack(pady=40)

        self.email = ctk.CTkEntry(self, placeholder_text="Usuário", width=300)
        self.email.pack(pady=10)

        self.password = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=300)
        self.password.pack(pady=10)

        login_button = ctk.CTkButton(self, text="Entrar", width=300, command=self.login)
        login_button.pack(pady=20)

    def login(self):

        username = self.email.get()
        password = self.password.get()

        token = self.auth.login(username, password)

        if token:

            self.pack_forget()

            chat = ChatScreen(self.master, token)
            chat.pack(fill="both", expand=True)