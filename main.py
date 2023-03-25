import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Operator")
        self.geometry(f"{1400}x{800}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.nav_frame = NavFrame(self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(4, weight=1)

        self.settings_menu = Settings(master=self)
        self.settings_button = customtkinter.CTkButton(self, text="Settings", command=None)


class Settings(customtkinter.CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="CTkEntry")


class NavFrame(customtkinter.CTkFrame):  # pylint: disable=abstract-method
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.logo_label = customtkinter.CTkLabel(self, text="Expense Operator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.expenses = customtkinter.CTkButton(self, text='Expenses')
        self.expenses.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.charts = customtkinter.CTkButton(self, text='Charts')
        self.charts.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_button = customtkinter.CTkButton(self, text='Settings')
        self.settings_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.logged_in_as = customtkinter.CTkLabel(self, text='Logged in as: ')
        self.logged_in_as.grid(row=4, column=0, padx=20, pady=10, sticky="sw")


if __name__ == "__main__":
    app = App()
    app.mainloop()
