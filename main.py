import datetime as dt
import sqlite3
from tkinter import CENTER, END, NO, ttk
import tkcalendar
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
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.nav_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")

        self.db_con = sqlite3.connect("database.db")
        self.db_cur = self.db_con.cursor()
        self.main_currency = self.main_curr_type()

        # Main Frame, Sidebar elements
        self.label = customtkinter.CTkLabel(self.nav_frame, text="Expense Operator", fg_color="transparent", font=customtkinter.CTkFont(size=20, weight="bold"), compound="left")
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ewn")
        self.expenses_button = customtkinter.CTkButton(self.nav_frame, text='Expenses', command=lambda: self.frame_button_events('expenses'))
        self.expenses_button.grid(row=1, column=0, padx=20, pady=10, sticky="ewn")
        self.income_button = customtkinter.CTkButton(self.nav_frame, text='Income', command=lambda: self.frame_button_events("income"))
        self.income_button.grid(row=2, column=0, padx=20, pady=10, sticky="ewn")
        self.stats_button = customtkinter.CTkButton(self.nav_frame, text='Statistics', command=lambda: self.frame_button_events("statistics"))
        self.stats_button.grid(row=3, column=0, padx=20, pady=10, sticky="enw")
        # self.subs_button = customtkinter.CTkButton(self.nav_frame, text='Subscriptions', command=lambda: self.frame_button_events("subscriptions"))
        # self.subs_button.grid(row=4, column=0, padx=20, pady=10, sticky="ewn")

        # Stats Frame
        self.stats_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.stats_frame.grid_columnconfigure(1, weight=1)

        self.stats_numbers = customtkinter.CTkTabview(self.stats_frame, width=1165, height=335)
        self.stats_numbers.grid(row=0, column=0, padx=(10, 5), pady=0, sticky="ne")
        self.stats_charts = customtkinter.CTkTabview(self.stats_frame, width=1165, height=390)
        self.stats_charts.grid(row=1, column=0, padx=(10, 5), pady=0, sticky="nesw")

        self.stats_numbers.add("Stats")
        self.stats_charts.add("Charts")

        self.currency = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="Main Currency type:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.currency.grid(row=2, column=0, padx=20, pady=10, sticky="sw")
        self.currency_entry = customtkinter.CTkOptionMenu(self.stats_numbers.tab("Stats"), values=["Euro [EUR]", "Dollar [USD]", "Forint [HUF]", "Pound [GBP]"])
        self.currency_entry.grid(row=2, column=0, padx=(180, 20), pady=10, sticky="sw")
        self.currency_entry.set(self.main_currency)
        self.currency_set = customtkinter.CTkButton(self.stats_numbers.tab("Stats"), text="Set currency type", command=self.main_curr_refresh)
        self.currency_set.grid(row=2, column=0, padx=(350, 0), pady=10)
        self.stats_label = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="Statistics:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.stats_label.grid(row=0, column=0, padx=20, pady=10, sticky="sw")
        self.stats_date_from = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="From:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.stats_date_from.grid(row=0, column=0, padx=(120, 20), pady=10, sticky="sw")
        self.stats_date_from = customtkinter.CTkButton(
            self.stats_numbers.tab("Stats"),
            text=self.set_start_date('stats'),
            command=lambda: self.date_select(
                "stats",
                "from"),
            fg_color="#343638",
            border_color="#565b5e",
            hover_color="#565b5e",
            font=customtkinter.CTkFont(
                size=14),
            border_width=2)
        self.stats_date_from.grid(row=0, column=0, padx=(180, 10), pady=10, sticky="sw")
        # self.date_button_from.configure(text=dt.datetime.now().strftime("%Y-%m-%d"))
        self.stats_date_to = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="To:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.stats_date_to.grid(row=0, column=0, padx=(330, 20), pady=10, sticky="sw")
        self.stats_date_to = customtkinter.CTkButton(self.stats_numbers.tab("Stats"), text=dt.datetime.now().strftime("%Y-%m-%d"), command=lambda: self.date_select("stats", "to"), fg_color="#343638",
                                                     border_color="#565b5e", hover_color="#565b5e", font=customtkinter.CTkFont(size=14), border_width=2)
        self.stats_date_to.grid(row=0, column=0, padx=(370, 20), pady=10, sticky="sw")
        # self.date_button_to.configure(text=dt.datetime.now().strftime("%Y-%m-%d"))
        self.toplevel_window = None

        self.stats_curr_balance = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="Current Balance:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.stats_curr_balance.grid(row=3, column=0, padx=20, pady=10, sticky="sw")
        self.stats_curr_balance_label = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), width=150, text='')
        self.stats_curr_balance_label.grid(row=3, column=0, padx=(180, 20), pady=10, sticky="sw")

        self.stats_income = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="Income:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.stats_income.grid(row=4, column=0, padx=20, pady=10, sticky="sw")
        self.stats_income_label = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), width=150, text="")
        self.stats_income_label.grid(row=4, column=0, padx=(180, 20), pady=10, sticky="sw")
        self.stats_expenses = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="Expenses:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.stats_expenses.grid(row=5, column=0, padx=20, pady=10, sticky="sw")
        self.stats_expenses_label = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), width=150, text="")
        self.stats_expenses_label.grid(row=5, column=0, padx=(180, 20), pady=10, sticky="sw")
        self.stats_subs_cost = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="Subscriptions cost:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.stats_subs_cost.grid(row=6, column=0, padx=20, pady=10, sticky="sw")
        self.stats_subs_cost_label = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), width=150, text="")
        self.stats_subs_cost_label.grid(row=6, column=0, padx=(180, 20), pady=10, sticky="sw")

        # Income frame
        self.income_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.income_frame.grid_columnconfigure(0, weight=0)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#1f6aa5", foreground="white", rowheight=35, fieldbackground="#212121")

        self.tab_new_income = customtkinter.CTkTabview(self.income_frame, width=300, height=780)
        self.tab_new_income.grid(row=0, column=0, padx=(10, 5), pady=0, sticky="nesw")
        self.tab_income_hist = customtkinter.CTkTabview(self.income_frame, width=710, height=780)
        self.tab_income_hist.grid(row=0, column=1, padx=(10, 5), pady=0, sticky="nesw")
        self.income_history = ttk.Treeview(self.income_frame)
        self.income_history.grid(row=0, column=1, padx=30, pady=(100, 10), sticky="nesw")

        self.tab_new_income.add("New Income")
        self.tab_income_hist.add("Income History")
        self.income_history['columns'] = ('name', 'type', 'date', 'price', 'frequency')
        self.income_history.column("#0", width=0, stretch=NO)
        self.income_history.column("name", anchor=CENTER, width=80)
        self.income_history.column("type", anchor=CENTER, width=80)
        self.income_history.column("date", anchor=CENTER, width=80)
        self.income_history.column("price", anchor=CENTER, width=80)
        self.income_history.column("frequency", anchor=CENTER, width=80)

        self.income_history.heading("#0", text="", anchor=CENTER)
        self.income_history.heading("name", text="Name", anchor=CENTER)
        self.income_history.heading("type", text="Type", anchor=CENTER, command=lambda: self.sort_by("type", "income"))
        self.income_history.heading("date", text="Date", anchor=CENTER)
        self.income_history.heading("price", text="Price", anchor=CENTER, command=lambda: self.sort_by("price", "income"))
        self.income_history.heading("frequency", text="Frequency", anchor=CENTER)

        self.income_date_from = customtkinter.CTkLabel(self.tab_income_hist.tab("Income History"), text="From:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.income_date_from.grid(row=0, column=0, padx=(120, 20), pady=10, sticky="sw")
        self.income_date_from_btn = customtkinter.CTkButton(
            self.tab_income_hist.tab("Income History"),
            text=self.set_start_date("income"),
            command=lambda: self.date_select(
                "income",
                "from"),
            fg_color="#343638",
            border_color="#565b5e",
            hover_color="#565b5e",
            font=customtkinter.CTkFont(
                size=14),
            border_width=2)
        self.income_date_from_btn.grid(row=0, column=0, padx=(180, 10), pady=10, sticky="sw")
        self.income_date_to_btn = customtkinter.CTkButton(self.tab_income_hist.tab("Income History"), text=dt.datetime.now().strftime("%Y-%m-%d"), command=lambda: self.date_select('income', 'to'), fg_color="#343638",
                                                          border_color="#565b5e", hover_color="#565b5e", font=customtkinter.CTkFont(size=14), border_width=2)
        self.income_date_to_btn.grid(row=0, column=0, padx=(370, 20), pady=10, sticky="sw")
        self.income_date_to = customtkinter.CTkLabel(self.tab_income_hist.tab("Income History"), text="To:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.income_date_to.grid(row=0, column=0, padx=(330, 20), pady=10, sticky="sw")

        self.refresh_range_histories('income')

        self.income_main_title = customtkinter.CTkLabel(master=self.tab_new_income.tab("New Income"), text="New expense:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.income_main_title.grid(row=0, column=0, padx=110, pady=50, sticky="w")

        self.income_name = customtkinter.CTkLabel(master=self.tab_new_income.tab("New Income"), text="Name:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.income_name.grid(row=1, column=0, padx=50, pady=10, sticky="w")
        self.income_name_entry = customtkinter.CTkEntry(master=self.tab_new_income.tab("New Income"), width=200)
        self.income_name_entry.grid(row=1, column=0, padx=(140, 50), pady=10)

        self.income_type = customtkinter.CTkLabel(master=self.tab_new_income.tab("New Income"), text="Type:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.income_type.grid(row=2, column=0, padx=50, pady=10, sticky="w")
        self.income_type_entry = customtkinter.CTkOptionMenu(master=self.tab_new_income.tab("New Income"), width=200, values=["Salary, Wage", "Interest", "Commission", "Gift", "Other"])
        self.income_type_entry.grid(row=2, column=0, padx=(140, 50), pady=10)

        self.income_curr = customtkinter.CTkLabel(master=self.tab_new_income.tab("New Income"), text="Currency:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.income_curr.grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.income_curr_ent = customtkinter.CTkOptionMenu(master=self.tab_new_income.tab("New Income"), width=200, values=["Euro [EUR]", "Dollar [USD]", "Forint [HUF]", "Pound [GBP]"])
        self.income_curr_ent.grid(row=3, column=0, padx=(140, 50), pady=10)

        self.income_date = customtkinter.CTkLabel(master=self.tab_new_income.tab("New Income"), text="Date:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.income_date.grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.income_date_entry = customtkinter.CTkEntry(master=self.tab_new_income.tab("New Income"), width=200)
        self.income_date_entry.grid(row=4, column=0, padx=(140, 50), pady=10)

        self.income_amount = customtkinter.CTkLabel(master=self.tab_new_income.tab("New Income"), text="Amount:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.income_amount.grid(row=5, column=0, padx=50, pady=10, sticky="w")
        self.income_amount_ent = customtkinter.CTkEntry(master=self.tab_new_income.tab("New Income"), width=200)
        self.income_amount_ent.grid(row=5, column=0, padx=(140, 50), pady=10)

        self.income_frequency = customtkinter.CTkLabel(master=self.tab_new_income.tab("New Income"), text="Frequency:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.income_frequency.grid(row=6, column=0, padx=50, pady=10, sticky="w")
        self.income_frequency_ent = customtkinter.CTkOptionMenu(master=self.tab_new_income.tab("New Income"), width=200, values=["One time", "Monthly", "Yearly"])
        self.income_frequency_ent.grid(row=6, column=0, padx=(140, 50), pady=10)

        self.income_current_date = customtkinter.CTkButton(master=self.tab_new_income.tab("New Income"), text="Current Date", command=lambda: self.set_current_date("income"))
        self.income_current_date.grid(row=7, column=0, sticky="w", pady=10, padx=50)
        self.income_save = customtkinter.CTkButton(master=self.tab_new_income.tab("New Income"), text="Save", command=lambda: self.validate_inputs('income'))
        self.income_save.grid(row=7, column=0, sticky="w", pady=10, padx=(215, 50))

        self.income_delete_record = customtkinter.CTkButton(master=self.tab_new_income.tab("New Income"), text="Delete Rec", command=lambda: self.delete_record_histories('income'))
        self.income_delete_record.grid(row=8, column=0, sticky="w", pady=10, padx=(130, 50))

        # Expenses Frame
        self.expenses_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.expenses_frame.grid_columnconfigure(0, weight=0)

        # Expenses frame elements
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#1f6aa5", foreground="white", rowheight=35, fieldbackground="#212121")

        self.tab_new_expense = customtkinter.CTkTabview(self.expenses_frame, width=300, height=780)
        self.tab_new_expense.grid(row=0, column=0, padx=(10, 5), pady=0, sticky="nesw")
        self.tab_expense_hist = customtkinter.CTkTabview(self.expenses_frame, width=710, height=780)
        self.tab_expense_hist.grid(row=0, column=1, padx=(10, 5), pady=0, sticky="nesw")
        self.expenses_history = ttk.Treeview(self.expenses_frame)
        self.expenses_history.grid(row=0, column=1, padx=30, pady=(100, 10), sticky="nesw")

        self.tab_new_expense.add("New Expense")
        self.tab_expense_hist.add("Expense History")
        self.expenses_history['columns'] = ('name', 'type', 'date', 'price', 'frequency')
        self.expenses_history.column("#0", width=0, stretch=NO)
        self.expenses_history.column("name", anchor=CENTER, width=80)
        self.expenses_history.column("type", anchor=CENTER, width=80)
        self.expenses_history.column("date", anchor=CENTER, width=80)
        self.expenses_history.column("price", anchor=CENTER, width=80)
        self.expenses_history.column("frequency", anchor=CENTER, width=80)

        self.expenses_history.heading("#0", text="", anchor=CENTER)
        self.expenses_history.heading("name", text="Name", anchor=CENTER)
        self.expenses_history.heading("type", text="Type", anchor=CENTER, command=lambda: self.sort_by("type", "expenses"))
        self.expenses_history.heading("date", text="Date", anchor=CENTER)
        self.expenses_history.heading("price", text="Price", anchor=CENTER, command=lambda: self.sort_by("price", "expenses"))
        self.expenses_history.heading("frequency", text="Frequency", anchor=CENTER)

        self.expenses_date_from = customtkinter.CTkLabel(self.tab_expense_hist.tab("Expense History"), text="From:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.expenses_date_from.grid(row=0, column=0, padx=(120, 20), pady=10, sticky="sw")
        self.expenses_date_from_btn = customtkinter.CTkButton(
            self.tab_expense_hist.tab("Expense History"),
            text=self.set_start_date("expenses"),
            command=lambda: self.date_select(
                "expenses",
                "from"),
            fg_color="#343638",
            border_color="#565b5e",
            hover_color="#565b5e",
            font=customtkinter.CTkFont(
                size=14),
            border_width=2)
        self.expenses_date_from_btn.grid(row=0, column=0, padx=(180, 10), pady=10, sticky="sw")
        self.expenses_date_to_btn = customtkinter.CTkButton(self.tab_expense_hist.tab("Expense History"), text=dt.datetime.now().strftime("%Y-%m-%d"), command=lambda: self.date_select("expenses", "to"), fg_color="#343638",
                                                            border_color="#565b5e", hover_color="#565b5e", font=customtkinter.CTkFont(size=14), border_width=2)
        self.expenses_date_to_btn.grid(row=0, column=0, padx=(370, 20), pady=10, sticky="sw")

        self.expenses_date_to = customtkinter.CTkLabel(self.tab_expense_hist.tab("Expense History"), text="To:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.expenses_date_to.grid(row=0, column=0, padx=(330, 20), pady=10, sticky="sw")

        self.refresh_range_histories('expenses')

        self.expenses_main_title = customtkinter.CTkLabel(master=self.tab_new_expense.tab("New Expense"), text="New expense:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.expenses_main_title.grid(row=0, column=0, padx=110, pady=50, sticky="w")

        self.expenses_name = customtkinter.CTkLabel(master=self.tab_new_expense.tab("New Expense"), text="Name:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_name.grid(row=1, column=0, padx=50, pady=10, sticky="w")
        self.expenses_name_entry = customtkinter.CTkEntry(master=self.tab_new_expense.tab("New Expense"), width=200)
        self.expenses_name_entry.grid(row=1, column=0, padx=(140, 50), pady=10)

        self.expenses_type = customtkinter.CTkLabel(master=self.tab_new_expense.tab("New Expense"), text="Type:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_type.grid(row=2, column=0, padx=50, pady=10, sticky="w")
        self.expenses_type_entry = customtkinter.CTkOptionMenu(master=self.tab_new_expense.tab("New Expense"), width=200, values=["Housing", "Clothing", "Food", "Entertainment", "Transportation", "Subscription", "Other"])
        self.expenses_type_entry.grid(row=2, column=0, padx=(140, 50), pady=10)

        self.expenses_curr = customtkinter.CTkLabel(master=self.tab_new_expense.tab("New Expense"), text="Currency:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_curr.grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.expenses_curr_ent = customtkinter.CTkOptionMenu(master=self.tab_new_expense.tab("New Expense"), width=200, values=["Euro [EUR]", "Dollar [USD]", "Forint [HUF]", "Pound [GBP]"])
        self.expenses_curr_ent.grid(row=3, column=0, padx=(140, 50), pady=10)

        self.expenses_date = customtkinter.CTkLabel(master=self.tab_new_expense.tab("New Expense"), text="Date:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_date.grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.expenses_date_entry = customtkinter.CTkEntry(master=self.tab_new_expense.tab("New Expense"), width=200)
        self.expenses_date_entry.grid(row=4, column=0, padx=(140, 50), pady=10)

        self.expenses_price = customtkinter.CTkLabel(master=self.tab_new_expense.tab("New Expense"), text="Price:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_price.grid(row=5, column=0, padx=50, pady=10, sticky="w")
        self.expenses_price_entry = customtkinter.CTkEntry(master=self.tab_new_expense.tab("New Expense"), width=200)
        self.expenses_price_entry.grid(row=5, column=0, padx=(140, 50), pady=10)

        self.expenses_frequency = customtkinter.CTkLabel(master=self.tab_new_expense.tab("New Expense"), text="Frequency:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_frequency.grid(row=6, column=0, padx=50, pady=10, sticky="w")
        self.expenses_frequency_ent = customtkinter.CTkOptionMenu(master=self.tab_new_expense.tab("New Expense"), width=200, values=["One time", "Monthly", "Yearly"])
        self.expenses_frequency_ent.grid(row=6, column=0, padx=(140, 50), pady=10)

        self.expenses_current_date = customtkinter.CTkButton(master=self.tab_new_expense.tab("New Expense"), text="Current Date", command=lambda: self.set_current_date("expenses"))
        self.expenses_current_date.grid(row=7, column=0, sticky="w", pady=10, padx=50)
        self.expenses_save = customtkinter.CTkButton(master=self.tab_new_expense.tab("New Expense"), text="Save", command=lambda: self.validate_inputs('expenses'))
        self.expenses_save.grid(row=7, column=0, sticky="w", pady=10, padx=(215, 50))

        self.expenses_delete_record = customtkinter.CTkButton(master=self.tab_new_expense.tab("New Expense"), text="Delete Rec", command=lambda: self.delete_record_histories("expenses"))
        self.expenses_delete_record.grid(row=8, column=0, sticky="w", pady=10, padx=(130, 50))

        self.select_frame_by_name("Expenses")

    def set_start_date(self, table: str) -> str:
        if table == "stats":
            res_exp = self.db_cur.execute("SELECT MIN(date) FROM expenses")
            date_exp = res_exp.fetchone()[0]
            res_inc = self.db_cur.execute("SELECT MIN(date) FROM income")
            date_inc = res_inc.fetchone()[0]
            if date_exp is None or date_exp is None:
                date = dt.datetime.now().strftime("%Y-%m-%d")
            elif date_exp is None and date_inc is not None:
                date = date_inc
            elif date_exp is not None and date_inc is None:
                date = date_exp
            else:
                date = min(date_exp, date_inc)
            return str(date)
        res = self.db_cur.execute(f"SELECT MIN(date) FROM {table}")
        date = res.fetchone()[0]
        if date is None:
            date = dt.datetime.now().strftime("%Y-%m-%d")
        return str(date)

    def sort_treeview(self, sort_by: str, table: str, sort_category: customtkinter.CTkOptionMenu):
        sort_w = sort_category.get()
        self.toplevel_window.withdraw()
        self.toplevel_window = None
        if table == 'expenses':
            history = self.expenses_history
            date_from = self.expenses_date_from_btn.cget("text")
            date_to = self.expenses_date_to_btn.cget("text")
        elif table == 'income':
            history = self.income_history
            date_from = self.income_date_from_btn.cget("text")
            date_to = self.income_date_to_btn.cget("text")
        for i in history.get_children():
            history.delete(i)
        if sort_by == 'type':
            res = self.db_cur.execute(f"SELECT * FROM {table} DESC WHERE type='{sort_w}' AND date BETWEEN date('{date_from}') AND date('{date_to}')")
        elif sort_by == 'price':
            res = self.db_cur.execute(f"SELECT * FROM {table} ORDER BY price DESC WHERE date BETWEEN date('{date_from}') AND date('{date_to}')")
        datas = res.fetchall()
        self.history_table_format(datas, history)

    def sort_by(self, sort_by: str, table: str):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = customtkinter.CTkToplevel(self)
            self.toplevel_window.title(f"Sort by {sort_by}")
            self.toplevel_window.geometry("300x300")
            self.toplevel_window.resizable(False, False)
        else:
            self.toplevel_window.focus()
        if sort_by == "name":
            pass
        elif sort_by == "type":
            if table == 'expenses':
                values = ["Housing", "Clothing", "Food", "Entertainment", "Transportation", "Subscription", "Other"]
            elif table == 'income':
                values = ["Salary, Wage", "Interest", "Commission", "Gift", "Other"]
            sort_category = customtkinter.CTkOptionMenu(self.toplevel_window, width=200, values=values)
            sort_category.grid(row=0, column=0, padx=(35, 20), pady=20)
            sort_btn = customtkinter.CTkButton(self.toplevel_window, text="Sort", command=lambda: self.sort_treeview("type", table, sort_category))
            sort_btn.grid(row=1, column=0, padx=(35, 20), pady=20)
            sort_reset = customtkinter.CTkButton(self.toplevel_window, text="Reset", command=lambda: self.refresh_range_histories(table))
            sort_reset.grid(row=2, column=0, padx=(35, 20), pady=20)

    def gui_print(self, table: str):
        date_from = self.stats_date_from.cget("text")
        date_to = self.stats_date_to.cget("text")
        main_curr = self.curr_type_to_symbol(self.main_curr_type())
        if table == 'income':
            self.stat_income(main_curr, date_from, date_to)
        elif table == 'balance':
            self.stat_balance(main_curr, date_from, date_to)
        elif table == 'expenses':
            self.stat_expenses(main_curr, date_from, date_to)
        elif table == 'subs':
            self.stat_subs(main_curr, date_from, date_to)
        else:
            self.stat_income(main_curr, date_from, date_to)
            self.stat_balance(main_curr, date_from, date_to)
            self.stat_expenses(main_curr, date_from, date_to)
            self.stat_subs(main_curr, date_from, date_to)

    def currency_format(self, label: customtkinter.CTkLabel, main_curr: str, operator: str, numbers: int):
        if main_curr in ['Ft', '€']:
            label.configure(text=f"{operator}{abs(float(numbers)):,} {main_curr}".replace(',', ' '))
        else:
            label.configure(text=f"{operator}{main_curr} {abs(float(numbers)):,}".replace(',', ' '))

    def main_curr_type(self):
        res = self.db_cur.execute("SELECT curr_type FROM currencies WHERE main_curr=1")
        main = res.fetchone()[0]
        return main

    def main_curr_refresh(self):
        self.db_cur.execute("UPDATE currencies SET main_curr=0")
        self.db_cur.execute(f"UPDATE currencies SET main_curr=1 WHERE curr_type='{self.currency_entry.get()}'")
        self.db_con.commit()
        self.gui_print('all')

    def monthly_yearly_stat(self, table: str, date_from: str, date_to: str):
        if table == 'income':
            db_table = 'income'
        elif table == 'expenses':
            db_table = 'expenses'
        curr_time = dt.datetime.now().strftime("%Y-%m-%d")
        res = self.db_cur.execute(f"SELECT price, date FROM {db_table} WHERE date BETWEEN date('{date_from}') AND date('{date_to}') AND frequency='Monthly'")
        monthly_data = res.fetchall()
        monthly = 0
        if monthly_data is not None:
            for record in monthly_data:
                months = (dt.datetime.strptime(curr_time, "%Y-%m-%d").year - dt.datetime.strptime(record[1], "%Y-%m-%d").year) * 12 + (dt.datetime.strptime(curr_time, "%Y-%m-%d").month - dt.datetime.strptime(record[1], "%Y-%m-%d").month)
                if dt.datetime.strptime(curr_time, "%Y-%m-%d").day == dt.datetime.strptime(record[1], "%Y-%m-%d").day:
                    months += 1
                total = record[0] * months
                monthly += total
        else:
            monthly = 0
        res = self.db_cur.execute(f"SELECT price, date FROM {db_table} WHERE date BETWEEN date('{date_from}') AND date('{date_to}') AND frequency='Yearly'")
        yearly_data = res.fetchall()
        yearly = 0
        if yearly_data is not None:
            for record in yearly_data:
                years = dt.datetime.strptime(curr_time, "%Y-%m-%d").year - dt.datetime.strptime(record[1], "%Y-%m-%d").year + 1
                if dt.datetime.strptime(curr_time, "%Y-%m-%d").month == dt.datetime.strptime(record[1], "%Y-%m-%d").month and dt.datetime.strptime(curr_time, "%Y-%m-%d").day == dt.datetime.strptime(record[1], "%Y-%m-%d").day:
                    years += 1
                total = record[0] * years
                yearly += total
        else:
            yearly = 0
        return monthly, yearly

    def stat_income(self, main_curr: str, date_from: str, date_to: str):
        res = self.db_cur.execute(f"SELECT SUM(price) FROM income WHERE date BETWEEN date('{date_from}') AND date('{date_to}') AND frequency='One time'")
        income = res.fetchone()[0]
        label = self.stats_income_label
        monthly, yearly = self.monthly_yearly_stat('income', date_from, date_to)
        income += monthly + yearly
        operator = ''
        if income is None:
            income = 'N/A'
            label.configure(text=f"{income}")
        else:
            self.currency_format(label, main_curr, operator, income)
        return income

    def stat_expenses(self, main_curr: str, date_from: str, date_to: str):
        res = self.db_cur.execute(f"SELECT SUM(price) FROM expenses WHERE date BETWEEN date('{date_from}') AND date('{date_to}') AND frequency='One time'")
        expenses = res.fetchone()[0]
        label = self.stats_expenses_label
        monthly, yearly = self.monthly_yearly_stat('expenses', date_from, date_to)
        expenses += monthly + yearly
        operator = '-'
        if expenses is None:
            expenses = 'N/A'
            label.configure(text=f"{expenses}")
        else:
            self.currency_format(label, main_curr, operator, expenses)
        return expenses

    def stat_subs(self, main_curr: str, date_from: str, date_to: str):
        res = self.db_cur.execute(f"SELECT SUM(price) FROM expenses WHERE date BETWEEN date('{date_from}') AND date('{date_to}') AND frequency='Monthly' OR frequency='Yearly'")
        subs = res.fetchone()[0]
        label = self.stats_subs_cost_label
        operator = '-'
        if subs is None:
            subs = 'N/A'
            label.configure(text=f"{subs}")
        else:
            self.currency_format(label, main_curr, operator, subs)
        return subs

    def stat_balance(self, main_curr: str, date_from: str, date_to: str):
        income = self.stat_income(main_curr, date_from, date_to)
        expenses = self.stat_expenses(main_curr, date_from, date_to)
        subs = self.stat_subs(main_curr, date_from, date_to)
        stats = [income, expenses]
        for i in range(len(stats)):
            if stats[i] == "N/A":
                stats[i] = 0
        balance = float(stats[0]) - float(stats[1])
        label = self.stats_curr_balance_label
        if balance < 0:
            operator = '-'
        else:
            operator = ''
        self.currency_format(label, main_curr, operator, balance)

    def date_select(self, frame: str, which_date: str):
        if frame == "stats":
            if which_date == "from":
                date = self.stats_date_from
            elif which_date == "to":
                date = self.stats_date_to
        elif frame == "income":
            if which_date == "from":
                date = self.income_date_from_btn
            elif which_date == "to":
                date = self.income_date_to_btn
        elif frame == "expenses":
            if which_date == "from":
                date = self.expenses_date_from_btn
            elif which_date == "to":
                date = self.expenses_date_to_btn
        curr_year = dt.datetime.now().year
        curr_month = dt.datetime.now().month
        curr_day = dt.datetime.now().day
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = customtkinter.CTkToplevel(self)
            self.toplevel_window.title("Date Selector")
            self.toplevel_window.geometry("300x300")
            self.toplevel_window.resizable(False, False)
            calendar = tkcalendar.Calendar(self.toplevel_window, selectmode="day", year=curr_year, month=curr_month, day=curr_day, date_pattern="y-mm-dd")
            calendar.grid(row=0, column=0, padx=(35, 20), pady=20)
            save_date = customtkinter.CTkButton(self.toplevel_window, text="Set date", command=lambda: self.set_date(calendar, date, frame))
            save_date.grid(row=1, column=0, padx=(35, 20), pady=20)
        else:
            self.toplevel_window.focus()

    def set_date(self, calendar: tkcalendar.Calendar, which_date: str, frame: str):
        date = calendar.get_date()
        which_date.configure(text=f"{date}")
        self.toplevel_window.withdraw()
        self.toplevel_window = None
        if frame == 'stats':
            self.refresh_range_stats()
        elif frame == 'income':
            self.refresh_range_histories('income')
        elif frame == 'expenses':
            self.refresh_range_histories('expenses')

    def refresh_range_stats(self):
        main_curr = self.curr_type_to_symbol(self.main_curr_type())
        date_from = self.stats_date_from.cget("text")
        date_to = self.stats_date_to.cget("text")
        self.stat_income(main_curr, date_from, date_to)
        self.stat_expenses(main_curr, date_from, date_to)
        self.stat_subs(main_curr, date_from, date_to)
        self.stat_balance(main_curr, date_from, date_to)
        self.gen_expense_chart(date_from, date_to)
        self.gen_income_chart(date_from, date_to)

    def refresh_range_histories(self, table: str):
        if table == 'expenses':
            date_from = self.expenses_date_from_btn.cget("text")
            date_to = self.expenses_date_to_btn.cget("text")
            history = self.expenses_history
        elif table == 'income':
            date_from = self.income_date_from_btn.cget("text")
            date_to = self.income_date_to_btn.cget("text")
            history = self.income_history
        for i in history.get_children():
            history.delete(i)
        self.history_tables(table, date_from, date_to)

    def gen_expense_chart(self, date_from: str, date_to: str):
        res = self.db_cur.execute(f"SELECT COUNT(type), type FROM expenses WHERE date BETWEEN date('{date_from}') AND date('{date_to}') GROUP BY type")
        datas = res.fetchall()
        cat_sum = 0
        pie_exp_labels = []
        pie_exp_sizes = []
        for data in datas:
            pie_exp_labels.append(data[1])
            pie_exp_sizes.append(data[0])
            cat_sum += data[0]
        pie_charts_canvas = customtkinter.CTkCanvas(self.stats_charts.tab("Charts"), width=500, height=150, bg="#212121", highlightbackground='#1a1a1a')
        pie_charts_canvas.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew")
        figure = plt.figure(figsize=(5, 4), dpi=100, facecolor="#212121")
        pie_chart = figure.add_subplot(111)  # type: ignore
        explode = []
        for i in range(len(pie_exp_sizes)):
            if pie_exp_sizes[i] == max(pie_exp_sizes):
                explode.append(0.1)
            else:
                explode.append(0)
        pie_chart.pie(pie_exp_sizes, labels=pie_exp_labels, autopct='%1.1f%%', shadow=True, startangle=90, explode=explode)
        pie_chart_canvas = FigureCanvasTkAgg(figure, pie_charts_canvas)
        for text in pie_chart.texts:  # type: ignore
            text.set_color('white')
        pie_chart.set_title("Expenses by category", color="white")
        pie_chart.set_facecolor("#212121")
        pie_chart.tick_params(axis='x', colors='white')
        pie_chart.tick_params(axis='y', colors='white')
        pie_chart.xaxis.label.set_color('white')
        pie_chart.yaxis.label.set_color('white')
        pie_chart_canvas.draw()
        pie_chart_canvas.get_tk_widget().grid(row=1, column=0, padx=20, sticky="nsew")
        pie_charts_canvas.config(highlightthickness=0)

    def gen_income_chart(self, date_from: str, date_to: str):
        res = self.db_cur.execute(f"SELECT COUNT(type), type FROM income WHERE date BETWEEN date('{date_from}') AND date('{date_to}') GROUP BY type")
        datas = res.fetchall()
        cat_sum = 0
        pie_inc_labels = []
        pie_inc_sizes = []
        for data in datas:
            pie_inc_labels.append(data[1])
            pie_inc_sizes.append(data[0])
            cat_sum += data[0]
        pie_charts_canvas = customtkinter.CTkCanvas(self.stats_charts.tab("Charts"), width=500, height=150, bg="#212121", highlightbackground='#1a1a1a')
        pie_charts_canvas.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="nsew")
        figure = plt.figure(figsize=(5, 4), dpi=100, facecolor="#212121")
        pie_chart = figure.add_subplot(111)  # type: ignore
        explode = []
        for i in range(len(pie_inc_sizes)):
            if pie_inc_sizes[i] == max(pie_inc_sizes):
                explode.append(0.1)
            else:
                explode.append(0)
        pie_chart.pie(pie_inc_sizes, labels=pie_inc_labels, autopct='%1.1f%%', shadow=True, startangle=90, explode=explode)
        pie_chart_canvas = FigureCanvasTkAgg(figure, pie_charts_canvas)
        for text in pie_chart.texts:  # type: ignore
            text.set_color('white')
        pie_chart.set_title("Income by Category", color="white")
        pie_chart.set_facecolor("#212121")
        pie_chart.tick_params(axis='x', colors='white')
        pie_chart.tick_params(axis='y', colors='white')
        pie_chart.xaxis.label.set_color('white')
        pie_chart.yaxis.label.set_color('white')
        pie_chart_canvas.draw()
        pie_chart_canvas.get_tk_widget().grid(row=1, column=1, padx=20, sticky="nsew")
        pie_charts_canvas.config(highlightthickness=0)

    def select_frame_by_name(self, name: str):

        self.expenses_button.configure(fg_color=("gray75", "gray25") if name == "Expenses" else "#1f6aa5")
        self.income_button.configure(fg_color=("gray75", "gray25") if name == "Income" else "#1f6aa5")
        self.stats_button.configure(fg_color=("gray75", "gray25") if name == "Statistics" else "#1f6aa5")

        if name == "Expenses":
            self.expenses_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.expenses_frame.grid_forget()
        if name == "Income":
            self.income_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.income_frame.grid_forget()
        if name == "Statistics":
            self.stats_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.stats_frame.grid_forget()

    def clear_form_fields(self, tree: str):
        if tree == 'expenses':
            self.expenses_name_entry.delete(0, END)
            self.expenses_curr_ent.set(self.main_currency)
            self.expenses_date_entry.delete(0, END)
            self.expenses_price_entry.delete(0, END)
        elif tree == 'income':
            self.income_name_entry.delete(0, END)
            self.income_curr_ent.set(self.main_currency)
            self.income_date_entry.delete(0, END)
            self.income_amount_ent.delete(0, END)

    def delete_record_histories(self, table: str):
        if table == 'income':
            db_table = 'income'
            history = self.income_history
        elif table == 'expenses':
            db_table = 'expenses'
            history = self.expenses_history
        x = history.selection()
        for record in x:
            value = history.item(record)["values"]
            print(value)
            price = value[3].split(' ')[0]
            query = f"DELETE FROM {db_table} WHERE name='{value[0]}' AND type='{value[1]}' AND date='{value[2]}' AND price='{price}' AND frequency='{value[4]}'"
            self.db_con.execute(query)
            self.db_con.commit()
            history.delete(record)

    def validate_inputs(self, table: str):
        if table == 'expenses':
            if float(self.expenses_price_entry.get()):
                if self.expenses_name_entry.get() and self.expenses_date_entry.get() != "":
                    self.input_record_histories("expenses")
            else:
                self.expenses_save.configure(command=0)
        elif table == 'income':
            if float(self.income_amount_ent.get()):
                if self.income_name_entry.get() and self.income_date_entry.get() != "":
                    self.input_record_histories("income")
            else:
                self.income_save.configure(command=0)

    def curr_type_to_symbol(self, curr_type: str):
        match curr_type:
            case "Euro [EUR]":
                return '€'
            case "Dollar [USD]":
                return '$'
            case "Forint [HUF]":
                return 'Ft'
            case  "Pound [GBP]":
                return '£'

    def history_tables(self, table: str, date_from: str, date_to: str):
        if table == 'income':
            db_table = 'income'
            history = self.income_history
        elif table == 'expenses':
            db_table = 'expenses'
            history = self.expenses_history
        res = self.db_cur.execute(f"SELECT * FROM {db_table} WHERE date BETWEEN date('{date_from}') AND date('{date_to}') ORDER BY id")
        datas = res.fetchall()
        self.history_table_format(datas, history)

    def history_table_format(self, datas: list, history: ttk.Treeview):
        for record in datas:
            symbol = self.curr_type_to_symbol(record[5])
            price = f"{record[4]} {symbol}"
            if record[0] % 2 == 0:
                history.insert(parent='', index='end', values=(record[1], record[2], record[3], price, record[6]), tags="light")
            else:
                history.insert(parent='', index='end', values=(record[1], record[2], record[3], price, record[6]), tags="dark")
        history.tag_configure("light", background="#1f6aa5")
        history.tag_configure("dark", background="#212121")

    def refresh_history_tables(self, table: str, date_from: str, date_to: str):
        if table == 'income':
            history = self.income_history
        elif table == 'expenses':
            history = self.expenses_history
        res = self.db_cur.execute(f"SELECT * FROM {table} WHERE date BETWEEN date('{date_from}') AND date('{date_to}') ORDER BY id DESC LIMIT 1")
        datas = res.fetchall()
        self.history_table_format(datas, history)

    def input_record_histories(self, table: str):
        if table == 'income':
            date_from = self.expenses_date_from_btn.cget("text")
            date_to = self.expenses_date_to_btn.cget("text")
            entries = [self.income_name_entry.get(), self.income_type_entry.get(), self.income_date_entry.get(), self.income_amount_ent.get(), self.income_curr_ent.get(), self.income_frequency_ent.get()]
        elif table == 'expenses':
            date_from = self.income_date_from_btn.cget("text")
            date_to = self.income_date_to_btn.cget("text")
            entries = [self.expenses_name_entry.get(), self.expenses_type_entry.get(), self.expenses_date_entry.get(), self.expenses_price_entry.get(), self.expenses_curr_ent.get(), self.expenses_frequency_ent.get()]
        query = f"INSERT INTO {table} (name, type, date, price, curr_type, frequency) VALUES ('{entries[0]}', '{entries[1]}', '{entries[2]}', '{entries[3]}', '{entries[4]}', '{entries[5]}')"
        self.db_cur.execute(query)
        self.db_con.commit()
        self.refresh_history_tables(table, date_from, date_to)
        self.clear_form_fields(table)

    def refresh_sub_table(self, table: ttk.Treeview, db_table: str):
        curr_table: ttk.Treeview = table
        res = self.db_cur.execute(f"SELECT id, name, price, date, curr_type FROM {db_table} ORDER BY id DESC LIMIT 1")
        datas = res.fetchone()
        symbol = self.curr_type_to_symbol(datas[4])
        price = f"{datas[2]} {symbol}"
        if datas[0] % 2 == 0:
            curr_table.insert(parent='', index='end', values=(datas[1], datas[3], price), tags="light")
        else:
            curr_table.insert(parent='', index='end', values=(datas[1], datas[3], price), tags="dark")
        curr_table.tag_configure("light", background="#1f6aa5")
        curr_table.tag_configure("dark", background="#212121")

    # Swap Frame functions
    def frame_button_events(self, frame: str):
        if frame == 'expenses':
            self.select_frame_by_name("Expenses")
        elif frame == 'income':
            self.select_frame_by_name("Income")
        elif frame == 'statistics':
            self.select_frame_by_name("Statistics")
            self.refresh_range_stats()

    def set_current_date(self, frame: str):
        date = dt.datetime.now()
        if frame == 'expenses':
            self.expenses_date_entry.delete(0, 'end')
            self.expenses_date_entry.insert(0, f'{date:%Y-%m-%d}')
        elif frame == 'income':
            self.income_date_entry.delete(0, 'end')
            self.income_date_entry.insert(0, f'{date:%Y-%m-%d}')

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


if __name__ == "__main__":
    app = App()
    app.mainloop()


# pyright: reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false
# pyright: reportMatchNotExhaustive=false
# pyright: reportUnboundVariable=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownLambdaType=false
