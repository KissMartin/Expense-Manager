import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class MyTabView(customtkinter.CTkTabview):  # pylint: disable=abstract-method
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("tab 1")
        self.add("tab 2")

        self.label = customtkinter.CTkLabel(master=self.tab("tab 1"))
        self.label.grid(row=0, column=0, padx=20, pady=10)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Operator")
        self.geometry(f"{1400}x{800}")

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()
