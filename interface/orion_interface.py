import customtkinter as ctk
from screens.home_screen import HomeScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class OrionInterface(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ÓRION - IB Core Systems")
        self.geometry("1200x800")

        self.token = None

        self.show_home()

    def show_home(self):

        for widget in self.winfo_children():
            widget.destroy()

        home = HomeScreen(self)
        home.pack(fill="both", expand=True)


if __name__ == "__main__":

    app = OrionInterface()
    app.mainloop()