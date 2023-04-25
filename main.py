import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Operator")
        self.geometry(f"{1400}x{800}")
        self.minsize(800, 600)
        self.resizable(True, False)

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
        self.charts_button = customtkinter.CTkButton(self.nav_frame, text='Charts', command=self.charts_button_event)  # + update charts
        self.charts_button.grid(row=2, column=0, padx=20, pady=10, sticky="enw")
        self.sub_n_sum_button = customtkinter.CTkButton(self.nav_frame, text='Subs & Sum', command=self.sub_n_sum_button_event)
        self.sub_n_sum_button.grid(row=3, column=0, padx=20, pady=10, sticky="ewn")
        self.logged_in_as = customtkinter.CTkLabel(self.nav_frame, text='Logged in as: ')
        self.logged_in_as.grid(row=4, column=0, padx=20, pady=10, sticky="sw")

        # Expenses Frames
        self.expenses_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.expenses_frame.grid_columnconfigure(0, weight=1)

        # Charts Frame
        self.charts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.charts_frame.grid_columnconfigure(0, weight=1)

        # Pie chart
        self.pie_charts_canvas = customtkinter.CTkCanvas(self.charts_frame, width=500, height=150, bg="#1a1a1a", highlightbackground='#1a1a1a')
        self.pie_charts_canvas.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.figure = plt.figure(figsize=(5, 4), dpi=100, facecolor="#1a1a1a")
        self.pie_chart = self.figure.add_subplot(111)  # type: ignore
        self.pie_chart.pie([1, 2, 3, 4], labels=['Frogs', 'Hogs', 'Dogs', 'Logs'], autopct='%1.1f%%', shadow=True, startangle=90)
        self.pie_chart_canvas = FigureCanvasTkAgg(self.figure, self.pie_charts_canvas)
        for text in self.pie_chart.texts:  # type: ignore
            text.set_color('white')
        self.pie_chart.set_facecolor("#1a1a1a")
        self.pie_chart.tick_params(axis='x', colors='white')
        self.pie_chart.tick_params(axis='y', colors='white')
        self.pie_chart.xaxis.label.set_color('white')
        self.pie_chart.yaxis.label.set_color('white')
        self.pie_chart_canvas.draw()
        self.pie_chart_canvas.get_tk_widget().grid(row=1, column=0, padx=20, sticky="nsew")

        # Bar chart
        self.bar_chart_canvas = customtkinter.CTkCanvas(self.charts_frame, width=500, height=150, bg="#1a1a1a", highlightbackground='#1a1a1a')
        self.bar_chart_canvas.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.figure2 = plt.figure(figsize=(5, 4), dpi=100, facecolor="#1a1a1a")
        self.bar_chart = self.figure2.add_subplot(111)  # type: ignore
        self.bar_chart.bar([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.bar_chart_canvas = FigureCanvasTkAgg(self.figure2, self.bar_chart_canvas)
        self.bar_chart.set_facecolor("#1a1a1a")
        self.bar_chart.set_ylabel('Amount earned')
        self.bar_chart.set_xlabel('Month')
        self.bar_chart.tick_params(axis='x', colors='white')
        self.bar_chart.tick_params(axis='y', colors='white')
        self.bar_chart.xaxis.label.set_color('white')
        self.bar_chart.yaxis.label.set_color('white')
        self.bar_chart.spines['bottom'].set_color('white')
        self.bar_chart.spines['right'].set_color('white')
        self.bar_chart.spines['left'].set_color('white')
        self.bar_chart.spines['top'].set_color('white')
        self.bar_chart_canvas.draw()
        self.bar_chart_canvas.get_tk_widget().grid(row=1, column=1, padx=20, sticky="nsew")

        # Subs & Sum frame and elements
        self.sub_n_sum_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.sub_n_sum_frame.grid(row=0, column=0, sticky="nsew")
        self.sub_n_sum_frame.grid_rowconfigure(6, weight=1)
        self.sub_n_sum_frame.grid_rowconfigure(7, weight=0)

        self.sub_n_sum_income = customtkinter.CTkLabel(self.sub_n_sum_frame, text="Income:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sub_n_sum_income.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.sub_n_sum_income_entry = customtkinter.CTkEntry(self.sub_n_sum_frame, width=200)
        self.sub_n_sum_income_entry.grid(row=1, column=0, padx=20, pady=10)
        self.sub_n_sum_warning_income = customtkinter.CTkLabel(self.sub_n_sum_frame, text="")
        self.sub_n_sum_warning_income.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.sub_n_sum_monthly_exp = customtkinter.CTkLabel(self.sub_n_sum_frame, text="Monthly Subscriptions:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sub_n_sum_monthly_exp.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.sub_n_sum_monthly_exp_entry = customtkinter.CTkEntry(self.sub_n_sum_frame, width=200)
        self.sub_n_sum_monthly_exp_entry.grid(row=3, column=0, padx=20, pady=10)
        self.sub_n_sum_warning_monthly = customtkinter.CTkLabel(self.sub_n_sum_frame, text="")
        self.sub_n_sum_warning_monthly.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        self.sub_n_sum_yearly_exp = customtkinter.CTkLabel(self.sub_n_sum_frame, text="Yearly Subscriptions:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sub_n_sum_yearly_exp.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.sub_n_sum_yearly_exp_entry = customtkinter.CTkEntry(self.sub_n_sum_frame, width=200)
        self.sub_n_sum_yearly_exp_entry.grid(row=5, column=0, padx=20, pady=10)
        self.sub_n_sum_warning_yearly = customtkinter.CTkLabel(self.sub_n_sum_frame, text="")
        self.sub_n_sum_warning_yearly.grid(row=5, column=1, padx=20, pady=10, sticky="w")

        self.sub_n_sum_change = customtkinter.CTkButton(self.sub_n_sum_frame, text="Change Settings", command=self.change)
        self.sub_n_sum_change.grid(row=6, column=0, sticky="ws", pady=10, padx=20)
        self.sub_n_sum_apply_changes = customtkinter.CTkButton(self.sub_n_sum_frame, text="Apply Changes", command=self.validate)
        self.sub_n_sum_apply_changes.grid(row=7, column=0, sticky="ws", pady=(10, 30), padx=20)
        self.sub_n_sum_apply_changes_complete = customtkinter.CTkLabel(self.sub_n_sum_frame, text="")
        self.sub_n_sum_apply_changes_complete.grid(row=7, column=1, sticky="ws", pady=(10, 30), padx=10)

        # Default Frame (Loading Frame)
        self.select_frame_by_name("Charts")

    # Change Frame function
    def select_frame_by_name(self, name: str):

        self.expenses_button.configure(fg_color=("gray75", "gray25") if name == "Expenses" else "#1f6aa5")
        self.charts_button.configure(fg_color=("gray75", "gray25") if name == "Charts" else "#1f6aa5")
        self.sub_n_sum_button.configure(fg_color=("gray75", "gray25") if name == "Subs & Sum" else "#1f6aa5")  # 1f6aa5

        if name == "Expenses":
            self.expenses_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.expenses_frame.grid_forget()
        if name == "Charts":
            self.charts_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.charts_frame.grid_forget()
        if name == "Subs & Sum":
            self.sub_n_sum_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sub_n_sum_frame.grid_forget()

    # Swap Frame functions
    def expenses_button_event(self):
        self.select_frame_by_name("Expenses")

    def charts_button_event(self):
        self.select_frame_by_name("Charts")
        # todo: function which updates the chart with the new data

    def sub_n_sum_button_event(self):
        self.select_frame_by_name("Subs & Sum")

    # Validate fucntion for Subs & Sum menu
    def validate(self):
        entrys_warnings = {
            self.sub_n_sum_income_entry: self.sub_n_sum_warning_income,
            self.sub_n_sum_monthly_exp_entry: self.sub_n_sum_warning_monthly,
            self.sub_n_sum_yearly_exp_entry: self.sub_n_sum_warning_yearly
        }
        numbers_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for entry, warning in entrys_warnings.items():
            if len(entry.get()) <= 10:
                for i in entry.get().lower():
                    if i not in numbers_list:
                        entry.configure(fg_color="#990000")
                        warning.configure(text="This value is incorrect!")
                        break
                    entry.configure(state="disabled", fg_color="#006600")
                    warning.configure(text="")
            else:
                entry.configure(fg_color="#990000")
                warning.configure(text="This value is incorrect!")

    # Change function for sub_n_sum_frame
    def change(self):
        entrys = [self.sub_n_sum_income_entry, self.sub_n_sum_monthly_exp_entry, self.sub_n_sum_yearly_exp_entry]
        for entry in entrys:
            if entry.cget("state") == "disabled":
                entry.configure(state="normal")
                entry.configure(fg_color="#343638")


if __name__ == "__main__":
    app = App()
    app.mainloop()

# pyright: reportUnknownMemberType=false
# pyright: reportMissingTypeStubs=false
