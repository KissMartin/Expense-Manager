import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Operator")
        self.geometry(f"{1400}x{800}")

        self.sidebar_frame = SidebarFrame(master=self)
        self.sidebar_frame.grid(row=0, column=0)


class SidebarFrame(customtkinter.CTkFrame):  # pylint: disable=abstract-method
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.logo_label = customtkinter.CTkLabel(self, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self, text='asd')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=(10, 1000))


if __name__ == "__main__":
    app = App()
    app.mainloop()
