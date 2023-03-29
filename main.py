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

        self.nav_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(4, weight=1)

        # Main Frame, Sidebar elements
        self.label = customtkinter.CTkLabel(self.nav_frame, text="Expense Operator", fg_color="transparent", font=customtkinter.CTkFont(size=20, weight="bold"), compound="left")
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ewn")
        self.expenses_button = customtkinter.CTkButton(self.nav_frame, text='Expenses', command=self.expenses_button_event)
        self.expenses_button.grid(row=1, column=0, padx=20, pady=10, sticky="ewn")
        self.charts_button = customtkinter.CTkButton(self.nav_frame, text='Charts', command=self.charts_button_event)
        self.charts_button.grid(row=2, column=0, padx=20, pady=10, sticky="enw")
        self.settings_button = customtkinter.CTkButton(self.nav_frame, text='Settings', command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, padx=20, pady=10, sticky="ewn")
        self.logged_in_as = customtkinter.CTkLabel(self.nav_frame, text='Logged in as: ')
        self.logged_in_as.grid(row=4, column=0, padx=20, pady=10, sticky="sw")

        # Different Frames
        self.expenses_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.expenses_frame.grid_columnconfigure(0, weight=1)

        self.charts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Settings Frame elements
        self.settings_income = customtkinter.CTkLabel(self.settings_frame, text="Income:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.settings_income.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.settings_income_entry = customtkinter.CTkEntry(self.settings_frame, width=200)
        self.settings_income_entry.grid(row=1, column=0, padx=20, pady=10)
        self.settings_warning = customtkinter.CTkLabel(self.settings_frame, text="")
        self.settings_warning.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.settings_income_entry.insert(10, "012345678900")
        self.validate(self.settings_income_entry, self.settings_warning)
        # if len(self.settings_income_entry.get()) > 10:
        #     self.settings_income_entry.delete(10, "end")

        self.settings_monthly_exp = customtkinter.CTkLabel(self.settings_frame, text="Monthly Expenses:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.settings_monthly_exp.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.settings_monthly_exp_entry = customtkinter.CTkEntry(self.settings_frame, width=200,)
        self.settings_monthly_exp_entry.grid(row=3, column=0, padx=20, pady=10)
        self.settings_warning = customtkinter.CTkLabel(self.settings_frame, text="")
        self.settings_warning.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        self.settings_yearly_exp = customtkinter.CTkLabel(self.settings_frame, text="Yearly Expenses:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.settings_yearly_exp.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.settings_yearly_exp_entry = customtkinter.CTkEntry(self.settings_frame, width=200)
        self.settings_yearly_exp_entry.grid(row=5, column=0, padx=20, pady=10)
        self.settings_warning = customtkinter.CTkLabel(self.settings_frame, text="")
        self.settings_warning.grid(row=5, column=1, padx=20, pady=10, sticky="w")

        # self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.settings_frame, values=["Light", "Dark", "System"],
        #                                                         command=self.change_appearance_mode_event)
        # self.appearance_mode_menu.grid(row=1, column=1, padx=20, pady=20, sticky="s")

        # Default Frame (Loadin Frame)
        self.select_frame_by_name("Settings")

    # Change Frame function
    def select_frame_by_name(self, name: str):

        self.expenses_button.configure(fg_color=("gray75", "gray25") if name == "Expenses" else "#1f6aa5")
        self.charts_button.configure(fg_color=("gray75", "gray25") if name == "Charts" else "#1f6aa5")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "Settings" else "#1f6aa5")

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

    # Swap Frame functions
    def expenses_button_event(self):
        self.select_frame_by_name("Expenses")

    def charts_button_event(self):
        self.select_frame_by_name("Charts")

    def settings_button_event(self):
        self.select_frame_by_name("Settings")

    def validate(self, entry: customtkinter.CTkEntry, entry_label: customtkinter.CTkLabel):
        if len(entry.get()) > 10:
            entry.configure()
            entry_label.configure(text="Warning: The value is too long", text_color="red")
            return True
        else:
            return False
    # Appearance Mode function
    # def change_appearance_mode_event(self, new_appearance_mode: str):
    #     customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()

# pyright: reportUnknownMemberType=false
# pyright: reportMissingTypeStubs=false
