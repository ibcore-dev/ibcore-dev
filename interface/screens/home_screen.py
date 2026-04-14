import customtkinter as ctk


class HomeScreen(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="IB CORE SYSTEMS",
            font=("Arial", 36, "bold")
        )
        title.pack(pady=30)

        subtitle = ctk.CTkLabel(
            self,
            text="BEM-VINDO À IB CORE SYSTEMS",
            font=("Arial", 20)
        )
        subtitle.pack(pady=10)

        orion = ctk.CTkLabel(
            self,
            text="ÓRION",
            font=("Arial", 48, "bold")
        )
        orion.pack(pady=20)

        enter_button = ctk.CTkButton(
            self,
            text="ACESSAR ÓRION",
            width=250,
            height=50,
            command=self.enter_orion
        )
        enter_button.pack(pady=40)

    def enter_orion(self):

        from screens.login_screen import LoginScreen

        self.pack_forget()

        login = LoginScreen(self.master)
        login.pack(fill="both", expand=True)