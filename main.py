import datetime as dt
import sqlite3
from tkinter import CENTER, END, MULTIPLE, NO, ttk
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

        # Main Frame, Sidebar elements
        self.label = customtkinter.CTkLabel(self.nav_frame, text="Expense Operator", fg_color="transparent", font=customtkinter.CTkFont(size=20, weight="bold"), compound="left")
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ewn")
        self.expenses_button = customtkinter.CTkButton(self.nav_frame, text='Expenses', command=self.expenses_button_event)
        self.expenses_button.grid(row=1, column=0, padx=20, pady=10, sticky="ewn")
        self.stats_button = customtkinter.CTkButton(self.nav_frame, text='Statistics', command=self.stats_button_event)  # + update charts
        self.stats_button.grid(row=2, column=0, padx=20, pady=10, sticky="enw")
        self.subs_button = customtkinter.CTkButton(self.nav_frame, text='Subscriptions', command=self.sub_button_event)
        self.subs_button.grid(row=3, column=0, padx=20, pady=10, sticky="ewn")

        # Stats Frame
        self.stats_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.stats_frame.grid_columnconfigure(1, weight=1)

        self.stats_numbers = customtkinter.CTkTabview(self.stats_frame, width=1165, height=335)
        self.stats_numbers.grid(row=0, column=0, padx=(10, 5), pady=0, sticky="nesw")
        self.stats_charts = customtkinter.CTkTabview(self.stats_frame, width=1165, height=390)
        self.stats_charts.grid(row=1, column=0, padx=(10, 5), pady=0, sticky="nesw")

        self.stats_numbers.add("Stats")
        self.stats_charts.add("Charts")

        self.currency = customtkinter.CTkLabel(self.stats_numbers.tab("Stats"), text="Main Currency type:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.currency.grid(row=1, column=0, padx=20, pady=10, sticky="sw")
        self.currency_entry = customtkinter.CTkOptionMenu(self.stats_numbers.tab("Stats"), values=["Euro [EUR]", "Dollar [USD]", "Forint [HUF]", "Pound [GBP]"])
        self.currency_entry.grid(row=1, column=1, padx=20, pady=10, sticky="sw")

        # Pie chart
        self.pie_charts_canvas = customtkinter.CTkCanvas(self.stats_charts.tab("Charts"), width=500, height=150, bg="#1a1a1a", highlightbackground='#1a1a1a')
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

        # Expenses Frame
        self.expenses_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.expenses_frame.grid_columnconfigure(0, weight=0)

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
        self.tab_view_history.column("#0", width=0, stretch=NO)
        self.tab_view_history.column("name", anchor=CENTER, width=80)
        self.tab_view_history.column("type", anchor=CENTER, width=80)
        self.tab_view_history.column("date", anchor=CENTER, width=80)
        self.tab_view_history.column("price", anchor=CENTER, width=80)

        self.tab_view_history.heading("#0", text="", anchor=CENTER)
        self.tab_view_history.heading("name", text="Name", anchor=CENTER)
        self.tab_view_history.heading("type", text="Type", anchor=CENTER)
        self.tab_view_history.heading("date", text="Date", anchor=CENTER)
        self.tab_view_history.heading("price", text="Price", anchor=CENTER)

        self.expenses_table()
        # def select_record():
        #     clear_form_expenses()
        #     selected = self.tab_view_history.focus()
        #     values = self.tab_view_history.item(selected, 'values')

        #     self.expenses_name_entry.insert(0, values[0])
        #     self.expenses_type_entry.set(values[1])
        #     self.expenses_date_entry.insert(0, values[2])
        #     self.expenses_price_entry.insert(0, values[3].split(' ')[0])

        # def change_record():
        #     selected = self.tab_view_history.focus()
        #     print(selected)
        #     if numbers_only_and_filled():
        #         self.tab_view_history.item(selected, text="", values=(self.expenses_name_entry.get(), self.expenses_type_entry.get(), self.expenses_date_entry.get(), self.expenses_price_entry.get()))
        #         clear_form_expenses()

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

        self.expenses_curr = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="Currency:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_curr.grid(row=3, column=0, padx=50, pady=10, sticky="w")
        self.expenses_curr_ent = customtkinter.CTkOptionMenu(master=self.tab_view_new.tab("New"), width=200, values=["Euro [EUR]", "Dollar [USD]", "Forint [HUF]", "Pound [GBP]"])
        self.expenses_curr_ent.grid(row=3, column=0, padx=(140, 50), pady=10)

        self.expenses_date = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="Date:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_date.grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.expenses_date_entry = customtkinter.CTkEntry(master=self.tab_view_new.tab("New"), width=200)
        self.expenses_date_entry.grid(row=4, column=0, padx=(140, 50), pady=10)

        self.expenses_price = customtkinter.CTkLabel(master=self.tab_view_new.tab("New"), text="Price:", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.expenses_price.grid(row=5, column=0, padx=50, pady=10, sticky="w")
        self.expenses_price_entry = customtkinter.CTkEntry(master=self.tab_view_new.tab("New"), width=200)
        self.expenses_price_entry.grid(row=5, column=0, padx=(140, 50), pady=10)

        self.expenses_current_date = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Current Date", command=self.set_current_date_expenses)
        self.expenses_current_date.grid(row=6, column=0, sticky="w", pady=10, padx=50)
        self.expenses_save = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Save", command=self.numbers_only_and_filled)
        self.expenses_save.grid(row=6, column=0, sticky="w", pady=10, padx=(215, 50))

        # self.expenses_clear_form = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Clear", command=clear_form_expenses)
        # self.expenses_clear_form.grid(row=7, column=0, sticky="w", pady=(10, 190), padx=(130, 50))

        # self.expenses_select_record = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Select Rec", command=select_record)
        # self.expenses_select_record.grid(row=8, column=0, sticky="w", pady=10, padx=(130, 50))

        # self.expenses_change_record = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Change Rec", command=change_record)
        # self.expenses_change_record.grid(row=9, column=0, sticky="w", pady=10, padx=50)

        self.expenses_delete_record = customtkinter.CTkButton(master=self.tab_view_new.tab("New"), text="Delete Rec", command=self.delete_record)
        self.expenses_delete_record.grid(row=7, column=0, sticky="w", pady=10, padx=(130, 50))

        # Subscriptions frame and elements
        self.subs_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.subs_frame.grid(row=0, column=0)
        self.subs_frame.grid_rowconfigure(6, weight=1)
        self.subs_frame.grid_rowconfigure(7, weight=0)

        # Tab view for subscriptions

        self.tab_view_monthly = customtkinter.CTkTabview(self.subs_frame, width=575, height=780)
        self.tab_view_monthly.grid(row=0, column=0, padx=(10, 5), pady=0, sticky="nesw")
        self.tab_view_yearly = customtkinter.CTkTabview(self.subs_frame, width=575, height=780)
        self.tab_view_yearly.grid(row=0, column=1, padx=(10, 5), pady=0, sticky="nesw")

        self.tab_view_monthly.add("Monthly")
        self.tab_view_yearly.add("Yearly")

        self.sns_monthly_name_lab = customtkinter.CTkLabel(master=self.tab_view_monthly.tab("Monthly"), text="Name:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_monthly_name_lab.grid(row=0, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_monthly_name_ent = customtkinter.CTkEntry(master=self.tab_view_monthly.tab("Monthly"), width=200)
        self.sns_monthly_name_ent.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        self.sns_monthly_price_lab = customtkinter.CTkLabel(master=self.tab_view_monthly.tab("Monthly"), text="Price:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_monthly_price_lab.grid(row=1, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_monthly_price_ent = customtkinter.CTkEntry(master=self.tab_view_monthly.tab("Monthly"), width=200)
        self.sns_monthly_price_ent.grid(row=1, column=1, padx=20, pady=10, sticky="e")

        self.sns_monthly_date_lab = customtkinter.CTkLabel(master=self.tab_view_monthly.tab("Monthly"), text="Date:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_monthly_date_lab.grid(row=2, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_monthly_date_ent = customtkinter.CTkEntry(master=self.tab_view_monthly.tab("Monthly"), width=200)
        self.sns_monthly_date_ent.grid(row=2, column=1, padx=20, pady=10, sticky="e")

        self.sns_monthly_curr_lab = customtkinter.CTkLabel(master=self.tab_view_monthly.tab("Monthly"), text="Currency:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_monthly_curr_lab.grid(row=3, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_monthy_curr_ent = customtkinter.CTkOptionMenu(master=self.tab_view_monthly.tab("Monthly"), width=200, values=["Euro [EUR]", "Dollar [USD]", "Forint [HUF]", "Pound [GBP]"])
        self.sns_monthy_curr_ent.grid(row=3, column=1, padx=20, pady=10)

        self.sns_monthly_datenow = customtkinter.CTkButton(master=self.tab_view_monthly.tab("Monthly"), text="Current Date", command=self.set_current_date_monthly)
        self.sns_monthly_datenow.grid(row=4, column=0, sticky="w", padx=(90, 20), pady=20, ipadx=10)

        self.sns_yearly_name_lab = customtkinter.CTkLabel(master=self.tab_view_yearly.tab("Yearly"), text="Name:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_yearly_name_lab.grid(row=0, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_yearly_name_ent = customtkinter.CTkEntry(master=self.tab_view_yearly.tab("Yearly"), width=200)
        self.sns_yearly_name_ent.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        self.sms_yearly_date_lab = customtkinter.CTkLabel(master=self.tab_view_yearly.tab("Yearly"), text="Date:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sms_yearly_date_lab.grid(row=1, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_yearly_date_ent = customtkinter.CTkEntry(master=self.tab_view_yearly.tab("Yearly"), width=200)
        self.sns_yearly_date_ent.grid(row=1, column=1, padx=20, pady=10, sticky="e")

        self.sns_yearly_price_lab = customtkinter.CTkLabel(master=self.tab_view_yearly.tab("Yearly"), text="Price:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_yearly_price_lab.grid(row=2, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_yearly_price_ent = customtkinter.CTkEntry(master=self.tab_view_yearly.tab("Yearly"), width=200)
        self.sns_yearly_price_ent.grid(row=2, column=1, padx=20, pady=10, sticky="e")

        self.sns_yearly_curr_lab = customtkinter.CTkLabel(master=self.tab_view_yearly.tab("Yearly"), text="Currency:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sns_yearly_curr_lab.grid(row=3, column=0, padx=(90, 20), pady=10, sticky="w")
        self.sns_yearly_curr_ent = customtkinter.CTkOptionMenu(master=self.tab_view_yearly.tab("Yearly"), width=200, values=["Euro [EUR]", "Dollar [USD]", "Forint [HUF]", "Pound [GBP]"])
        self.sns_yearly_curr_ent.grid(row=3, column=1, padx=20, pady=10)

        self.sns_yearly_datenow = customtkinter.CTkButton(master=self.tab_view_yearly.tab("Yearly"), text="Current Date", command=self.set_current_date_yearly)
        self.sns_yearly_datenow.grid(row=4, column=0, sticky="w", padx=(90, 20), pady=20, ipadx=10)

        self.tab_view_monthly_tree = ttk.Treeview(self.subs_frame)
        self.tab_view_monthly_tree.grid(row=0, column=0, padx=20, pady=(300, 10), sticky="nesw")

        self.tab_view_monthly_tree['columns'] = ('name', 'date', 'price')
        self.tab_view_monthly_tree.column("#0", width=0, stretch=NO)
        self.tab_view_monthly_tree.column("name", anchor=CENTER, width=60)
        self.tab_view_monthly_tree.column("date", anchor=CENTER, width=60)
        self.tab_view_monthly_tree.column("price", anchor=CENTER, width=60)

        self.tab_view_monthly_tree.heading("#0", text="", anchor=CENTER)
        self.tab_view_monthly_tree.heading("name", text="Name", anchor=CENTER)
        self.tab_view_monthly_tree.heading("date", text="Date", anchor=CENTER)
        self.tab_view_monthly_tree.heading("price", text="Price", anchor=CENTER)

        self.tab_view_yearly_tree = ttk.Treeview(self.subs_frame)
        self.tab_view_yearly_tree.grid(row=0, column=1, padx=20, pady=(300, 10), sticky="nesw")

        self.tab_view_yearly_tree['columns'] = ('name', 'date', 'price')
        self.tab_view_yearly_tree.column("#0", width=0, stretch=NO)
        self.tab_view_yearly_tree.column("name", anchor=CENTER, width=60)
        self.tab_view_yearly_tree.column("date", anchor=CENTER, width=60)
        self.tab_view_yearly_tree.column("price", anchor=CENTER, width=60)

        self.tab_view_yearly_tree.heading("#0", text="", anchor=CENTER)
        self.tab_view_yearly_tree.heading("name", text="Name", anchor=CENTER)
        self.tab_view_yearly_tree.heading("date", text="Date", anchor=CENTER)
        self.tab_view_yearly_tree.heading("price", text="Price", anchor=CENTER)

        self.subs_table('monthly')
        self.subs_table('yearly')

        self.sns_monthly_add = customtkinter.CTkButton(master=self.tab_view_monthly.tab("Monthly"), text="Add", command=self.numbers_only_and_filled_monthly)
        self.sns_monthly_add.grid(row=4, column=1, sticky="e", padx=20, pady=20, ipadx=10)
        self.sns_yearly_add = customtkinter.CTkButton(master=self.tab_view_yearly.tab("Yearly"), text="Add", command=self.numbers_only_and_filled_yearly)
        self.sns_yearly_add.grid(row=4, column=1, sticky="e", padx=20, pady=20, ipadx=10)

        # Default Frame (Loading Frame)
        self.select_frame_by_name("Expenses")

    # Change Frame function
    def select_frame_by_name(self, name: str):

        self.expenses_button.configure(fg_color=("gray75", "gray25") if name == "Expenses" else "#1f6aa5")
        self.stats_button.configure(fg_color=("gray75", "gray25") if name == "Statistics" else "#1f6aa5")
        self.subs_button.configure(fg_color=("gray75", "gray25") if name == "Subscriptions" else "#1f6aa5")  # ff8000 esetleges szín

        if name == "Expenses":
            self.expenses_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.expenses_frame.grid_forget()
        if name == "Statistics":
            self.stats_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.stats_frame.grid_forget()
        if name == "Subscriptions":
            self.subs_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.subs_frame.grid_forget()

    def subs_table(self, table):
        if table == 'monthly':
            table_name = 'monthly_subs'
            tree = self.tab_view_monthly_tree
        elif table == 'yearly':
            table_name = 'yearly_subs'
            tree = self.tab_view_yearly_tree
        res = self.db_cur.execute(f"SELECT * FROM {table_name}")
        datas = res.fetchall()
        for record in datas:
            symbol = self.curr_type_to_symbol(record[4])
            price = f"{record[2]} {symbol}"
            if record[0] % 2 == 0:
                tree.insert(parent='', index='end', values=(record[1], record[3], price), tags="light")
            else:
                tree.insert(parent='', index='end', values=(record[1], record[3], price), tags="dark")
        tree.tag_configure("light", background="#1f6aa5")
        tree.tag_configure("dark", background="#212121")

    def numbers_only_and_filled_monthly(self):
        if float(self.sns_monthly_price_ent.get()):
            if self.sns_monthly_name_ent.get() and self.sns_monthly_date_ent.get() != "":
                self.input_record('monthly')
        else:
            self.sns_monthly_add.configure(command=0)

    def clear_form_fields(self, frame):
        if frame == 'expenses':
            self.expenses_name_entry.delete(0, END)
            self.expenses_type_entry.set("Food")
            # self.expenses_curr_ent.set() set it to default
            self.expenses_date_entry.delete(0, END)
            self.expenses_price_entry.delete(0, END)
        elif frame == 'monthly':
            self.sns_monthly_name_ent.delete(0, END)
            self.sns_monthly_date_ent.delete(0, END)
            self.sns_monthly_price_ent.delete(0, END)
        elif frame == 'yearly':
            self.sns_yearly_name_ent.delete(0, END)
            self.sns_yearly_date_ent.delete(0, END)
            self.sns_yearly_price_ent.delete(0, END)

    def numbers_only_and_filled_yearly(self):
        if float(self.sns_yearly_price_ent.get()):
            if self.sns_yearly_name_ent.get() and self.sns_yearly_date_ent.get() != "":
                self.input_record('yearly')
        else:
            self.sns_yearly_add.configure(command=0)

    def delete_record(self):
        x = self.tab_view_history.selection()
        for record in x:
            value = self.tab_view_history.item(record)["values"]
            price = value[3].split(' ')[0]
            query = f"DELETE FROM expenses WHERE name='{value[0]}' AND type='{value[1]}' AND date='{value[2]}' AND price='{price}'"
            self.db_con.execute(query)
            self.db_con.commit()
            self.tab_view_history.delete(record)

    def numbers_only_and_filled(self):
        if float(self.expenses_price_entry.get()):
            if self.expenses_name_entry.get() and self.expenses_date_entry.get() != "":
                self.input_record_expenses()
        else:
            self.expenses_save.configure(command=0)

    def curr_type_to_symbol(self, curr_type):
        match curr_type:
            case "Euro [EUR]":
                return '€'
            case "Dollar [USD]":
                return '$'
            case "Forint [HUF]":
                return 'Ft'
            case  "Pound [GBP]":
                return '£'

    def expenses_table(self):
        res = self.db_cur.execute("SELECT * FROM expenses")
        datas = res.fetchall()
        for record in datas:
            symbol = self.curr_type_to_symbol(record[5])
            price = f"{record[4]} {symbol}"
            if record[0] % 2 == 0:
                self.tab_view_history.insert(parent='', index='end', values=(record[1], record[2], record[3], price), tags="light")
            else:
                self.tab_view_history.insert(parent='', index='end', values=(record[1], record[2], record[3], price), tags="dark")
        self.tab_view_history.tag_configure("light", background="#1f6aa5")
        self.tab_view_history.tag_configure("dark", background="#212121")

    def refresh_expenses_table(self):
        res = self.db_cur.execute("SELECT id, name, type, date, price, curr_type FROM expenses ORDER BY id DESC LIMIT 1")
        datas = res.fetchone()
        symbol = self.curr_type_to_symbol(datas[5])
        price = f"{datas[4]} {symbol}"
        if datas[0] % 2 == 0:
            self.tab_view_history.insert(parent='', index='end', values=(datas[1], datas[2], datas[3], price), tags="light")
        else:
            self.tab_view_history.insert(parent='', index='end', values=(datas[1], datas[2], datas[3], price), tags="dark")
        self.tab_view_history.tag_configure("light", background="#1f6aa5")
        self.tab_view_history.tag_configure("dark", background="#212121")

    def input_record_expenses(self):
        query = f"INSERT INTO expenses (name, type, date, price, curr_type) VALUES ('{self.expenses_name_entry.get()}', '{self.expenses_type_entry.get()}', '{self.expenses_date_entry.get()}', '{self.expenses_price_entry.get()}', '{self.expenses_curr_ent.get()}')"
        self.db_cur.execute(query)
        self.db_con.commit()
        self.refresh_expenses_table()
        self.clear_form_fields('expenses')

    def input_record(self, table):
        if table == 'yearly':
            db_table = 'yearly_subs'
            curr_table = self.tab_view_yearly_tree
            entries = [self.sns_yearly_name_ent.get(), self.sns_yearly_date_ent.get(), self.sns_yearly_price_ent.get(), self.sns_yearly_curr_ent.get()]
        elif table == 'monthly':
            db_table = 'monthly_subs'
            curr_table = self.tab_view_monthly_tree
            entries = [self.sns_monthly_name_ent.get(), self.sns_monthly_date_ent.get(), self.sns_monthly_price_ent.get(), self.sns_monthy_curr_ent.get()]
        query = f"INSERT INTO {db_table} (name, date, price, curr_type) VALUES ('{entries[0]}', '{entries[1]}', '{entries[2]}', '{entries[3]}')"
        self.db_cur.execute(query)
        self.db_con.commit()
        self.refresh_sub_table(curr_table, db_table)
        self.clear_form_fields(table)

    def refresh_sub_table(self, table, db_table):
        curr_table: ttk.Treeview = table
        res = self.db_cur.execute(f"SELECT id, name, price, date, curr_type FROM {db_table} ORDER BY id DESC LIMIT 1")
        datas = res.fetchone()
        symbol = self.curr_type_to_symbol(datas[4])
        price = f"{datas[3]} {symbol}"
        if datas[0] % 2 == 0:
            curr_table.insert(parent='', index='end', values=(datas[1], price, datas[4], price), tags="light")
        else:
            curr_table.insert(parent='', index='end', values=(datas[1], price, datas[4], price), tags="dark")
        curr_table.tag_configure("light", background="#1f6aa5")
        curr_table.tag_configure("dark", background="#212121")

    # Swap Frame functions
    def expenses_button_event(self):
        self.select_frame_by_name("Expenses")

    def stats_button_event(self):
        self.select_frame_by_name("Statistics")
        self.generate_update_chart()

    def generate_update_chart(self):
        pass

    def sub_button_event(self):
        self.select_frame_by_name("Subscriptions")

    def set_current_date_expenses(self):
        date = dt.datetime.now()
        self.expenses_date_entry.delete(0, 'end')
        self.expenses_date_entry.insert(0, f'{date:%d %B %Y}')

    def set_current_date_monthly(self):
        date = dt.datetime.now()
        self.sns_monthly_date_ent.delete(0, 'end')
        self.sns_monthly_date_ent.insert(0, f'{date:%d %B %Y}')

    def set_current_date_yearly(self):
        date = dt.datetime.now()
        self.sns_yearly_date_ent.delete(0, 'end')
        self.sns_yearly_date_ent.insert(0, f'{date:%d %B %Y}')

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
