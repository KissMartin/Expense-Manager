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
        self.expenses_button = customtkinter.CTkButton(self, text='Expenses')
        self.expenses_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.charts_button = customtkinter.CTkButton(self, text='Charts')
        self.charts_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_button = customtkinter.CTkButton(self, text='Settings')
        self.settings_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.logged_in_as = customtkinter.CTkLabel(self, text='Logged in as: ')
        self.logged_in_as.grid(row=4, column=0, padx=20, pady=10, sticky="sw")

        self.expenses_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.expenses_frame.grid_columnconfigure(0, weight=1)

        self.charts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.home_frame_button_1 = customtkinter.CTkButton(self.expenses_frame, text="")
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.expenses_frame, text="CTkButton", compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.expenses_frame, text="CTkButton", compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.expenses_frame, text="CTkButton", compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.select_frame_by_name("Expenses")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.expenses_button.configure(fg_color=("gray75", "gray25") if name == "Expenses" else "transparent")
        self.charts_button.configure(fg_color=("gray75", "gray25") if name == "Charts" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "Settings" else "transparent")

        # show selected frame
        if name == "Expenses":
            self.expenses_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.expenses_frame.grid_forget()
        if name == "Charts":
            self.charts_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.charts_frame.grid_forget()
        if name == "Settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    @property
    def expenses_button_event(self):
        self.select_frame_by_name("home")

    @property
    def charts_button_event(self):
        self.select_frame_by_name("frame_2")

    @property
    def settings_button_event(self):
        self.select_frame_by_name("frame_3")


if __name__ == "__main__":
    app = App()
    app.mainloop()
