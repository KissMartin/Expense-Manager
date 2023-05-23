import datetime as dt
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import CENTER, END, NO, ttk


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Operator")
        self.geometry(f"{1400}x{800}")
        self.resizable(False, False)

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
        self.expenses_frame.grid_columnconfigure(0, weight=0)

        # Charts Frame
        self.charts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.charts_frame.grid_columnconfigure(1, weight=1)

        # Pie chart
        self.pie_charts_canvas = customtkinter.CTkCanvas(self.charts_frame, width=500, height=150, bg="#1a1a1a", highlightbackground='#1a1a1a')
        self.pie_charts_canvas.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.figure = plt.figure(figsize=(5, 4), dpi=100, facecolor="#1a1a1a")
        self.pie_chart = self.figure.add_subplot(111)  # type: ignore
        self.pie_labels = ['Categ1', 'Categ2', 'Categ3', 'Categ4']
        self.explode = (0, 0.0, 0.1, 0)
        self.pie_sizes = [15, 30, 45, 10]
        self.pie_chart.pie(self.pie_sizes, labels=self.pie_labels, autopct='%1.1f%%', shadow=True, startangle=90, explode=self.explode)
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
        self.figure2 = plt.figure(figsize=(5, 4), dpi=100, facecolor="#1a1a1a")
        self.bar_chart = self.figure2.add_subplot(111)  # type: ignore
        self.bar_chart.bar([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.bar_chart_canvas = FigureCanvasTkAgg(self.figure2, self.pie_charts_canvas)
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

        # Expenses frame elements
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#1f6aa5", foreground="white", rowheight=35, fieldbackground="#212121")

        self.tab_view_new = customtkinter.CTkTabview(self.expenses_frame, width=300, height=780)
        self.tab_view_new.grid(row=0, column=0, padx=(10, 5), pady=0, sticky="nesw")
        self.history_table = customtkinter.CTkTabview(self.expenses_frame, width=710, height=780)
        self.history_table.grid(row=0, column=1, padx=(10, 5), pady=0, sticky="nesw")
        self.tab_view_history = ttk.Treeview(self.expenses_frame)
        self.tab_view_history.grid(row=0, column=1, padx=30, pady=(50, 10), sticky="nesw")

        self.tab_view_new.add("New")
        self.history_table.add("History")
        self.tab_view_history['columns'] = ('name', 'type', 'date', 'price')
        self.tab_view_history.column("#0", width=0,  stretch=NO)
        self.tab_view_history.column("name", anchor=CENTER, width=80)
        self.tab_view_history.column("type", anchor=CENTER, width=80)
        self.tab_view_history.column("date", anchor=CENTER, width=80)
        self.tab_view_history.column("price", anchor=CENTER, width=80)

        self.tab_view_history.heading("#0", text="", anchor=CENTER)
        self.tab_view_history.heading("name", text="Name", anchor=CENTER)
        self.tab_view_history.heading("type", text="Type", anchor=CENTER)
        self.tab_view_history.heading("date", text="Date", anchor=CENTER)
        self.tab_view_history.heading("price", text="Price", anchor=CENTER)

        data = [
            ["Kristóf", "Food", "14 May 2023", "25"],
            ["Bence", "Transportation", "25 April 2023", "12"]
        ]

        global count
        count = 0
        for record in data:
            if record == data[0]:
                self.tab_view_history.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags="vilagos")
            else:
                self.tab_view_history.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags="sotet")
            count += 1
        self.tab_view_history.tag_configure("vilagos", background="#1f6aa5")
        self.tab_view_history.tag_configure("sotet", background="#212121")

        def input_record_expenses():
            global count
            self.tab_view_history.insert(parent='', index='end', iid=count, text='', values=(self.expenses_name_entry.get(), self.expenses_type_entry.get(), self.expenses_date_entry.get(), self.expenses_price_entry.get()))
            count += 1
            clear_form_expenses()

        def select_record():
            clear_form_expenses()
            selected = self.tab_view_history.focus()
            values = self.tab_view_history.item(selected, 'values')

            self.expenses_name_entry.insert(0, values[0])
            self.expenses_type_entry.set(values[1])
            self.expenses_date_entry.insert(0, values[2])
            self.expenses_price_entry.insert(0, values[3])

        def change_record():
            selected = self.tab_view_history.focus()
            if numbers_only_and_filled():
                self.tab_view_history.item(selected, text="", values=(self.expenses_name_entry.get(), self.expenses_type_entry.get(), self.expenses_date_entry.get(), self.expenses_price_entry.get()))
                clear_form_expenses()

        def delete():
            x = self.tab_view_history.selection()
            for record in x:
                self.tab_view_history.delete(record)

        def clear_form_expenses():
            self.expenses_name_entry.delete(0, END)
            self.expenses_type_entry.set("Food")
            self.expenses_date_entry.delete(0, END)
            self.expenses_price_entry.delete(0, END)

        def numbers_only_and_filled():
            if int(self.expenses_price_entry.get()):
                if self.expenses_name_entry.get() and self.expenses_date_entry.get() != "":
                    input_record_expenses()
            else:
                self.expenses_save.configure(command=0)

        self.expenses_main_title = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="New expense:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.expenses_main_title.grid(row=0, column=0, padx=110, pady=50, sticky="w")

        self.expenses_name = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="Name:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_name.grid(row=1, column=0, padx=50, pady=10, sticky="w")
        self.expenses_name_entry = customtkinter.CTkEntry(master=self.tab_view_new.tab("New"), width=200)
        self.expenses_name_entry.grid(row=1, column=0, padx=(140, 50), pady=10)

        self.expenses_type = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="Type:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_type.grid(row=2, column=0, padx=50, pady=10, sticky="w")
        self.expenses_type_entry = customtkinter.CTkOptionMenu(master=self.tab_view_new.tab("New"), width=200, values=["Housing", "Clothing", "Food", "Entertainment", "Transportation", "Other"])
        self.expenses_type_entry.grid(row=2, column=0, padx=(140, 50), pady=10)
        self.expenses_type_entry.set("Food")

        self.expenses_date = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="Date:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_date.grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.expenses_date_entry = customtkinter.CTkEntry(master=self.tab_view_new.tab("New"), width=200)
        self.expenses_date_entry.grid(row=3, column=0, padx=(140, 50), pady=10)

        self.expenses_price = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="Price:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_price.grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.expenses_price_entry = customtkinter.CTkEntry(master=self.tab_view_new.tab("New"), width=200)
        self.expenses_price_entry.grid(row=4, column=0, padx=(140, 50), pady=10)

        self.expenses_current_date = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Current Date", command=self.set_current_date_expenses)
        self.expenses_current_date.grid(row=5, column=0, sticky="w", pady=10, padx=50)
        self.expenses_save = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Save", command=numbers_only_and_filled)  # save with sqlite3
        self.expenses_save.grid(row=5, column=0, sticky="w", pady=10, padx=(215, 50))

        self.expenses_clear_form = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Clear", command=clear_form_expenses)
        self.expenses_clear_form.grid(row=6, column=0, sticky="w", pady=(10, 210), padx=(130, 50))

        self.expenses_select_record = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Select Rec", command=select_record)
        self.expenses_select_record.grid(row=7, column=0, sticky="w", pady=10, padx=(130, 50))

        self.expenses_change_record = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Change Rec", command=change_record)
        self.expenses_change_record.grid(row=8, column=0, sticky="w", pady=10, padx=50)
        self.expenses_delete_record = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Delete Rec", command=delete)
        self.expenses_delete_record.grid(row=8, column=0, sticky="w", pady=10, padx=(215, 50))

        # Subs & Sum frame and elements
        self.sub_n_sum_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.sub_n_sum_frame.grid(row=0, column=0)
        self.sub_n_sum_frame.grid_rowconfigure(6, weight=1)
        self.sub_n_sum_frame.grid_rowconfigure(7, weight=0)

        # self.sub_n_sum_income = customtkinter.CTkLabel(self.sub_n_sum_frame, text="Income:", font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.sub_n_sum_income.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # self.sub_n_sum_income_entry = customtkinter.CTkEntry(self.sub_n_sum_frame, width=200)
        # self.sub_n_sum_income_entry.grid(row=1, column=0, padx=20, pady=(0, 10))
        # self.sub_n_sum_warning_income = customtkinter.CTkLabel(self.sub_n_sum_frame, text="")
        # self.sub_n_sum_warning_income.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        # self.sub_n_sum_change = customtkinter.CTkButton(self.sub_n_sum_frame, text="Change Settings", command=self.change)
        # self.sub_n_sum_change.grid(row=6, column=0, sticky="ws", pady=10, padx=20)
        # self.sub_n_sum_apply_changes = customtkinter.CTkButton(self.sub_n_sum_frame, text="Apply Changes", command=self.validate)
        # self.sub_n_sum_apply_changes.grid(row=7, column=0, sticky="ws", pady=(10, 30), padx=20)
        # self.sub_n_sum_apply_changes_complete = customtkinter.CTkLabel(self.sub_n_sum_frame, text="")
        # self.sub_n_sum_apply_changes_complete.grid(row=7, column=1, sticky="ws", pady=(10, 30), padx=10)

        # Tab view for sub_n_sum
        self.tab_view_monthly = customtkinter.CTkTabview(self.sub_n_sum_frame, width=575, height=780)
        self.tab_view_monthly.grid(row=0, column=0, padx=(10, 5), pady=0, sticky="nesw")
        self.tab_view_yearly = customtkinter.CTkTabview(self.sub_n_sum_frame, width=575, height=780)
        self.tab_view_yearly.grid(row=0, column=1, padx=(10, 5), pady=0, sticky="nesw")

        self.tab_view_monthly.add("Monthly")
        self.tab_view_yearly.add("Yearly")

        self.sns_monthly_lab1 = customtkinter.CTkLabel(master=self.tab_view_monthly.tab("Monthly"), text="Name:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_monthly_lab1.grid(row=0, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_monthly_ent1 = customtkinter.CTkEntry(master=self.tab_view_monthly.tab("Monthly"), width=200)
        self.sns_monthly_ent1.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        self.sns_monthly_lab2 = customtkinter.CTkLabel(master=self.tab_view_monthly.tab("Monthly"), text="Price:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_monthly_lab2.grid(row=1, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sms_monthly_ent2 = customtkinter.CTkEntry(master=self.tab_view_monthly.tab("Monthly"), width=200)
        self.sms_monthly_ent2.grid(row=1, column=1, padx=20, pady=10, sticky="e")

        self.sms_monthly_lab3 = customtkinter.CTkLabel(master=self.tab_view_monthly.tab("Monthly"), text="Date:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sms_monthly_lab3.grid(row=2, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_monthly_ent3 = customtkinter.CTkEntry(master=self.tab_view_monthly.tab("Monthly"), width=200)
        self.sns_monthly_ent3.grid(row=2, column=1, padx=20, pady=10, sticky="e")

        self.sns_monthly_datenow = customtkinter.CTkButton(master=self.tab_view_monthly.tab("Monthly"), text="Current Date", command=self.set_current_date_monthly)
        self.sns_monthly_datenow.grid(row=3, column=0, sticky="w", padx=(90, 20), pady=20, ipadx=10)
        self.sns_monthly_add = customtkinter.CTkButton(master=self.tab_view_monthly.tab("Monthly"), text="Add", command=0)
        self.sns_monthly_add.grid(row=3, column=1, sticky="e", padx=20, pady=20, ipadx=10)

        self.sns_yearly_lab1 = customtkinter.CTkLabel(master=self.tab_view_yearly.tab("Yearly"), text="Name:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_yearly_lab1.grid(row=0, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_yearly_ent1 = customtkinter.CTkEntry(master=self.tab_view_yearly.tab("Yearly"), width=200)
        self.sns_yearly_ent1.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        self.sns_yearly_lab2 = customtkinter.CTkLabel(master=self.tab_view_yearly.tab("Yearly"), text="Price:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_yearly_lab2.grid(row=1, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sms_yearly_ent2 = customtkinter.CTkEntry(master=self.tab_view_yearly.tab("Yearly"), width=200)
        self.sms_yearly_ent2.grid(row=1, column=1, padx=20, pady=10, sticky="e")

        self.sms_yearly_lab3 = customtkinter.CTkLabel(master=self.tab_view_yearly.tab("Yearly"), text="Date:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sms_yearly_lab3.grid(row=2, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_yearly_ent3 = customtkinter.CTkEntry(master=self.tab_view_yearly.tab("Yearly"), width=200)
        self.sns_yearly_ent3.grid(row=2, column=1, padx=20, pady=10, sticky="e")

        self.sns_yearly_datenow = customtkinter.CTkButton(master=self.tab_view_yearly.tab("Yearly"), text="Current Date", command=self.set_current_date_yearly)
        self.sns_yearly_datenow.grid(row=3, column=0, sticky="w", padx=(90, 20), pady=20, ipadx=10)
        self.sns_yearly_add = customtkinter.CTkButton(master=self.tab_view_yearly.tab("Yearly"), text="Add", command=0)
        self.sns_yearly_add.grid(row=3, column=1, sticky="e", padx=20, pady=20, ipadx=10)

        self.tab_view_monthly_tree = ttk.Treeview(self.sub_n_sum_frame)
        self.tab_view_monthly_tree.grid(row=0, column=0, padx=20, pady=(260, 10), sticky="nesw")

        self.tab_view_monthly_tree['columns'] = ('name', 'date', 'price')
        self.tab_view_monthly_tree.column("#0", width=0,  stretch=NO)
        self.tab_view_monthly_tree.column("name", anchor=CENTER, width=60)
        self.tab_view_monthly_tree.column("date", anchor=CENTER, width=60)
        self.tab_view_monthly_tree.column("price", anchor=CENTER, width=60)

        self.tab_view_monthly_tree.heading("#0", text="", anchor=CENTER)
        self.tab_view_monthly_tree.heading("name", text="Name", anchor=CENTER)
        self.tab_view_monthly_tree.heading("date", text="Date", anchor=CENTER)
        self.tab_view_monthly_tree.heading("price", text="Price", anchor=CENTER)

        self.tab_view_yearly_tree = ttk.Treeview(self.sub_n_sum_frame)
        self.tab_view_yearly_tree.grid(row=0, column=1, padx=20, pady=(260, 10), sticky="nesw")

        self.tab_view_yearly_tree['columns'] = ('name', 'date', 'price')
        self.tab_view_yearly_tree.column("#0", width=0,  stretch=NO)
        self.tab_view_yearly_tree.column("name", anchor=CENTER, width=60)
        self.tab_view_yearly_tree.column("date", anchor=CENTER, width=60)
        self.tab_view_yearly_tree.column("price", anchor=CENTER, width=60)

        self.tab_view_yearly_tree.heading("#0", text="", anchor=CENTER)
        self.tab_view_yearly_tree.heading("name", text="Name", anchor=CENTER)
        self.tab_view_yearly_tree.heading("date", text="Date", anchor=CENTER)
        self.tab_view_yearly_tree.heading("price", text="Price", anchor=CENTER)

        def input_record_monthly():
            global count
            self.tab_view_monthly_tree.insert(parent='', index='end', iid=count, text='', values=(self.sns_monthly_ent1.get(), self.sns_monthly_ent3.get(), self.sms_monthly_ent2.get()))
            count += 1
            clear_form_montly()

        def numbers_only_and_filled_monthly():
            if int(self.sms_monthly_ent2.get()):
                if self.sns_monthly_ent1.get() and self.sns_monthly_ent3.get() != "":
                    input_record_monthly()
            else:
                self.sns_monthly_add.configure(command=0)

        def clear_form_montly():
            self.sns_monthly_ent1.delete(0, END)
            self.sns_monthly_ent3.delete(0, END)
            self.sms_monthly_ent2.delete(0, END)

        def input_record_yearly():
            global count
            self.tab_view_yearly_tree.insert(parent='', index='end', iid=count, text='', values=(self.sns_yearly_ent1.get(), self.sns_yearly_ent3.get(), self.sms_yearly_ent2.get()))
            count += 1
            clear_form_yearly()

        def numbers_only_and_filled_yearly():
            if int(self.sms_yearly_ent2.get()):
                if self.sns_yearly_ent1.get() and self.sns_yearly_ent3.get() != "":
                    input_record_yearly()
            else:
                self.sns_yearly_add.configure(command=0)

        def clear_form_yearly():
            self.sns_yearly_ent1.delete(0, END)
            self.sns_yearly_ent3.delete(0, END)
            self.sms_yearly_ent2.delete(0, END)

        # Default Frame (Loading Frame)
        self.select_frame_by_name("Subs & Sum")

    # Change Frame function
    def select_frame_by_name(self, name: str):

        self.expenses_button.configure(fg_color=("gray75", "gray25") if name == "Expenses" else "#1f6aa5")
        self.charts_button.configure(fg_color=("gray75", "gray25") if name == "Charts" else "#1f6aa5")
        self.sub_n_sum_button.configure(fg_color=("gray75", "gray25") if name == "Subs & Sum" else "#1f6aa5")  # ff8000 esetleges szín

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
        self.generate_update_chart()

    def generate_update_chart(self):
        pass

    def sub_n_sum_button_event(self):
        self.select_frame_by_name("Subs & Sum")

    def set_current_date_expenses(self):
        date = dt.datetime.now()
        self.expenses_date_entry.delete(0, 'end')
        self.expenses_date_entry.insert(0, f'{date:%d %B %Y}')

    def set_current_date_monthly(self):
        date = dt.datetime.now()
        self.sns_monthly_ent3.delete(0, 'end')
        self.sns_monthly_ent3.insert(0, f'{date:%d %B %Y}')

    def set_current_date_yearly(self):
        date = dt.datetime.now()
        self.sns_yearly_ent3.delete(0, 'end')
        self.sns_yearly_ent3.insert(0, f'{date:%d %B %Y}')

    # Validate fucntion for Subs & Sum menu
    # def validate(self):
    #     entry = self.sub_n_sum_income_entry
    #     warning = self.sub_n_sum_warning_income
    #     numbers_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    #     if len(entry.get()) <= 10:
    #         for i in entry.get().lower():
    #             if i not in numbers_list:
    #                 entry.configure(fg_color="#990000")
    #                 warning.configure(text="This value is incorrect!")
    #                 break
    #             entry.configure(state="disabled", fg_color="#006600")
    #             warning.configure(text="")
    #     else:
    #         entry.configure(fg_color="#990000")
    #         warning.configure(text="This value is incorrect!")

    # # Change function for sub_n_sum_frame
    # def change(self):
    #     entry = self.sub_n_sum_income_entry
    #     if entry.cget("state") == "disabled":
    #         entry.configure(state="normal")
    #         entry.configure(fg_color="#343638")

    # def reset_expenses(self):
    #     entrys = [self.expenses_name_entry, self.expenses_type_entry, self.expenses_date_entry]
    #     for entry in entrys:
    #         if entry == self.expenses_name_entry:
    #             self.expenses_name_entry.delete(0, 'end')
    #         elif entry == self.expenses_type_entry:
    #             self.expenses_type_entry.set("Food")
    #         elif entry == self.expenses_date_entry:
    #             self.expenses_date_entry.delete(0, 'end')


if __name__ == "__main__":
    app = App()
    app.mainloop()

# pyright: reportUnknownMemberType=false
# pyright: reportMissingTypeStubs=false
