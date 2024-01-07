import sqlite3, sys, os
import tkinter as tk
from tkinter import ttk
import winsound
import customtkinter as ctk
from PIL import Image
import pandas as pd
from tkinter.messagebox import showerror, showinfo

STUDENT = ["ID студента","ФИО","Пол","Дата рождения","Адрес проживания","Телефон","Курс","ID группы","ID Специальности","ID Отделения","Год поступления","Год окончания","Номер студенческого билета","Курс","ID Вида финансирования","ID Сведений о родителях"]
GROUP = ["ID Группы", "Название группы"]
SPECIALNOSTI = ["ID Специальности","Название специальности"]
OTDEL = ["ID Отделения","Название отделения"]
FINANS = ["ID Вид финансирования", "Название"]
RODITELI = ["№","ФИО Матери", "ФИО Отца", "Телефон матери", "Телефон отца"]

ctk.set_default_color_theme("blue")

class WindowMain(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Студенческий отдел кадров')
        self.last_headers = None

        # Создание фрейма для отображения таблицы
        self.table_frame = ctk.CTkFrame(self, width=700, height=400)
        self.table_frame.grid(row=0, column=0, padx=5, pady=5)

        # Загрузка фона
        bg = ctk.CTkImage(Image.open("res\\images\\bg.png"), size=(700, 400))
        lbl = ctk.CTkLabel(self.table_frame, image=bg,)
        lbl.place(relwidth=1, relheight=1)

        # Создание меню
        self.menu_bar = tk.Menu(self, background='#555', foreground='white')

        # Меню "Файл"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)


 # Меню "Справочники"
        references_menu = tk.Menu(self.menu_bar, tearoff=0)
        references_menu.add_command(label="Группа", command=lambda: self.show_table("SELECT * FROM groups", GROUP))
        references_menu.add_command(label="Специальности", command=lambda: self.show_table("SELECT * FROM specialnosti", SPECIALNOSTI))
        references_menu.add_command(label="Отделение", command=lambda: self.show_table("SELECT * FROM otdelenije", OTDEL))
        references_menu.add_command(label="Вид финансирования", command=lambda: self.show_table("SELECT * FROM vid_finansirovanija", FINANS))
        self.menu_bar.add_cascade(label="Справочники", menu=references_menu)

        # Меню "Таблицы"
        tables_menu = tk.Menu(self.menu_bar, tearoff=0)
        tables_menu.add_command(label="Студент", command=lambda: self.show_table("SELECT * FROM student", STUDENT))
        tables_menu.add_command(label="Сведение о родителях", command=lambda: self.show_table("SELECT * FROM svedenija_o_roditel", RODITELI))
        self.menu_bar.add_cascade(label="Сведения", menu=tables_menu)

# Меню "Отчёты"
        reports_menu = tk.Menu(self.menu_bar, tearoff=0)
        reports_menu.add_command(label="Создать Отчёт", command=self.to_xlsx)
        self.menu_bar.add_cascade(label="Отчёты", menu=reports_menu)

        # Меню "Сервис"
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Руководство пользователя", command=lambda: self.open_help())
        help_menu.add_command(label="O программе", command=lambda: self.info_n())
        self.menu_bar.add_cascade(label="Сервис", menu=help_menu)

        
 # Настройка цветов меню
        file_menu.configure(bg='#555', fg='white')
        references_menu.configure(bg='#555', fg='white')
        tables_menu.configure(bg='#555', fg='white')
        reports_menu.configure(bg='#555', fg='white')
        help_menu.configure(bg='#555', fg='white')

        # Установка меню в главное окно
        self.config(menu=self.menu_bar)

        btn_width = 150
        pad = 5

        # Создание кнопок и виджетов для поиска и редактирования данных
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image\\image icon")
        self.deletes = ctk.CTkImage(Image.open(os.path.join(image_path, "delete.png")),size=(30, 30))
        self.change_add = ctk.CTkImage(Image.open(os.path.join(image_path, "2.png")), size=(20, 20))
        self.searchs = ctk.CTkImage(Image.open(os.path.join(image_path, "3.png")), size=(20, 20))
        self.cancellation = ctk.CTkImage(Image.open(os.path.join(image_path, "4.png")), size=(20, 20))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "5.png")) ,size=(26, 26))
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=15)
        self.navigation_frame.grid(row=0, column=1, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # редактирование
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="Редактирование", image=self.logo_image, compound="right", font=ctk.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # создание тем
        self.appearance_mode_label = ctk.CTkLabel(self.navigation_frame, text="Тема", anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        #тема по умолчанию
        self.appearance_mode_optionemenu.set("System")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=0, column=1)
        ctk.CTkButton(btn_frame, text="Добавить", font=ctk.CTkFont(size=15), image=self.change_add, compound="right", width=btn_width, command=self.add).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="Удалить", font=ctk.CTkFont(size=15), image=self.deletes, compound="right", width=btn_width, command=self.delete).pack(pady=pad)
        ctk.CTkButton(btn_frame, text="Изменить", font=ctk.CTkFont(size=15), image=self.change_add, compound="right", width=btn_width, command=self.change).pack(pady=pad)

        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=1, column=0, pady=pad)
        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Поиск строк")
        self.search_entry.grid(row=0, column=0, padx=pad)
        ctk.CTkButton(search_frame, text="Поиск", image=self.searchs, compound="right", width=50, font=ctk.CTkFont(size=13), command=self.search).grid(row=0, column=1, padx=pad)
        ctk.CTkButton(search_frame, text="Искать далее", width=50, font=ctk.CTkFont(size=13), command=self.search_next).grid(row=0, column=2, padx=pad)
        ctk.CTkButton(search_frame, text="Сброс", image=self.cancellation, compound="right", width=50, font=ctk.CTkFont(size=13), command=self.reset_search).grid(row=0, column=3, padx=pad)

    def open_help(self):
        os.system(r"C:\Users\DitWayT\Desktop\проектТРПО\html\main.html")

    def info_n(self):
        info()
        self.withdraw()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def search_in_table(self, table, search_terms, start_item=None):
        table.selection_remove(table.selection())  # Сброс предыдущего выделения

        items = table.get_children('')
        start_index = items.index(start_item) + 1 if start_item else 0

        for item in items[start_index:]:
            values = table.item(item, 'values')
            for term in search_terms:
                if any(term.lower() in str(value).lower() for value in values):
                    table.selection_add(item)
                    table.focus(item)
                    table.see(item)
                    return item  # Возвращаем найденный элемент



    def reset_search(self):
        if self.last_headers:
            self.table.selection_remove(self.table.selection())
        self.search_entry.delete(0, 'end')

    def search(self):
        if self.last_headers:
            self.current_item = self.search_in_table(self.table, self.search_entry.get().split(','))

    def search_next(self):
        if self.last_headers:
            if self.current_item:
                self.current_item = self.search_in_table(self.table, self.search_entry.get().split(','), start_item=self.current_item)
    
    
    def to_xlsx(self):
        if self.last_headers == GROUP:
            sql_query = "SELECT * FROM groups"
            table_name = "groups"
        elif self.last_headers == SPECIALNOSTI:
            sql_query = "SELECT * FROM specialnosti"
            table_name = "specialnosti"
        elif self.last_headers == OTDEL:
            sql_query = "SELECT * FROM otdelenije"
            table_name = "otdelenije"
        elif self.last_headers == FINANS:
            sql_query = "SELECT * FROM vid_finansirovanija"
            table_name = "vid_finansirovanija"
        elif self.last_headers == RODITELI:
            sql_query = "SELECT * FROM svedenija_o_roditel"
            table_name = "svedenija_o_roditel"
        elif self.last_headers == STUDENT:
            sql_query = "SELECT * FROM student"
            table_name = "student"
        else: return

        dir = sys.path[0] + "\\export"
        os.makedirs(dir, exist_ok=True)
        path = dir + f"\\{table_name}.xlsx"

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\labb18_bd.db")
        cursor = conn.cursor()
        # Получите данные из базы данных
        cursor.execute(sql_query)
        data = cursor.fetchall()
        # Создайте DataFrame из данных
        df = pd.DataFrame(data, columns=self.last_headers)
        # Создайте объект writer для записи данных в Excel
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        # Запишите DataFrame в файл Excel
        df.to_excel(writer, 'Лист 1', index=False)
        # Сохраните результат
        writer.close()

        showinfo(title="Успешно", message=f"Данные экспортированы в {path}")

    def show_table(self, sql_query, headers = None):# Очистка фрейма перед отображением новых данных
        for widget in self.table_frame.winfo_children(): widget.destroy()

        # Подключение к базе данных SQLite
        conn = sqlite3.connect("res\\labb18_bd.db")
        cursor = conn.cursor()

        # Выполнение SQL-запроса
        cursor.execute(sql_query)
        self.last_sql_query = sql_query

        # Получение заголовков таблицы и данных
        if headers == None: # если заголовки не были переданы используем те что в БД
            table_headers = [description[0] for description in cursor.description]
        else: # иначе используем те что передали
            table_headers = headers
            self.last_headers = headers
        table_data = cursor.fetchall()

        # Закрытие соединения с базой данных
        conn.close()
            
        canvas = ctk.CTkCanvas(self.table_frame, width=865, height=480)
        canvas.pack(fill="both", expand=True)

        x_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=canvas.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(xscrollcommand=x_scrollbar.set)

        self.table = ttk.Treeview(self.table_frame, columns=table_headers, show="headings", height=23)
        for header in table_headers: 
            self.table.heading(header, text=header)
            self.table.column(header, width=len(header) * 10 + 100) # установка ширины столбца исходя длины его заголовка
            if header == "№":
                self.table.column(header, width=0)
        for row in table_data: self.table.insert("", "end", values=row)

        canvas.create_window((0, 0), window=self.table, anchor="nw")

        self.table.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    def update_table(self):
        self.show_table(self.last_sql_query, self.last_headers)

    def add(self):
        if self.last_headers == GROUP:
            WindowGroup("add")
        elif self.last_headers == SPECIALNOSTI:
            WindowSpecialnosti("add")
        elif self.last_headers == OTDEL:
            WindowOtdel("add")
        elif self.last_headers == FINANS:
            WindowFinans("add")
        elif self.last_headers == RODITELI:
            WindowRoditeli("add")
        elif self.last_headers == STUDENT:
            WindowStudent("add")
        else: return

    def delete(self):
        if self.last_headers:
            select_item = self.table.selection()
            if select_item:
                item_data = self.table.item(select_item[0])["values"]
            else:
                showerror(title="Ошибка", message="He выбранна запись")
                return
        else:
            return

        if self.last_headers == GROUP:
            WindowGroup("delete", item_data)
        elif self.last_headers == SPECIALNOSTI:
            WindowSpecialnosti("delete", item_data)
        elif self.last_headers == OTDEL:
            WindowOtdel("delete", item_data)
        elif self.last_headers == FINANS:
            WindowFinans("delete", item_data)
        elif self.last_headers == RODITELI:
            WindowRoditeli("delete", item_data)
        elif self.last_headers == STUDENT:
            WindowStudent("delete", item_data)
        else: return
        
    def change(self):
        if self.last_headers:
            select_item = self.table.selection()
            if select_item:
                item_data = self.table.item(select_item[0])["values"]
            else:
                showerror(title="Ошибка", message="He выбранна запись")
                return
        else:
            return

        if self.last_headers == GROUP:
            WindowGroup("change", item_data)
        elif self.last_headers == SPECIALNOSTI:
            WindowSpecialnosti("change", item_data)
        elif self.last_headers == OTDEL:
            WindowOtdel("change", item_data)
        elif self.last_headers == FINANS:
            WindowFinans("change", item_data)
        elif self.last_headers == RODITELI:
            WindowRoditeli  ("change", item_data)
        elif self.last_headers == STUDENT:
            WindowStudent("change", item_data)

        else: return
class WindowGroup(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Номер группы").grid(row=1, column=0)
            self.n_group = tk.Entry(self, width=20)
            self.n_group.grid(row=1, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=2, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Группы'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Номер группы").grid(row=1, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=1, column=1)
            self.n_group = tk.Entry(self, width=20)
            self.n_group.grid(row=1, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=2, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        n_group = self.n_group.get()
        if n_group:
            try:
                conn = sqlite3.connect("res\\labb18_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO groups (N_grupp) VALUES (?)",
                            (n_group,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM groups WHERE id_group = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) 

    def change(self):
        n_group = self.n_group.get() or self.select_row[1]
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                           UPDATE groups SET (N_grupp) = (?) 
                           WHERE id_group = {self.select_row[0]}''', (n_group,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowSpecialnosti(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Название специальности").grid(row=1, column=0)
            self.name_spec = tk.Entry(self, width=20)
            self.name_spec.grid(row=1, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=2, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Специальности'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Название специальности").grid(row=1, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=1, column=1)
            self.name_spec = tk.Entry(self, width=20)
            self.name_spec.grid(row=1, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=2, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        name_spec = self.name_spec.get()
        if name_spec:
            try:
                conn = sqlite3.connect("res\\labb18_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO specialnosti (Nazvanije_specialnosti) VALUES (?)",
                            (name_spec,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM specialnosti WHERE id_specialnosti = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        name_spec = self.name_spec.get() or self.select_row[1]
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                           UPDATE specialnosti SET Nazvanije_specialnosti = ?
                           WHERE id_specialnosti = {self.select_row[0]}''', (name_spec,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowOtdel(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Название Отделения").grid(row=1, column=0)
            self.n_otd = tk.Entry(self, width=20)
            self.n_otd.grid(row=1, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=2, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Отделение'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[0]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Название отделения").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.n_otd = tk.Entry(self, width=20)
            self.n_otd.grid(row=2, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=3, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=3, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        n_otd = self.n_otd.get()
        if n_otd:
            try:
                conn = sqlite3.connect("res\\labb18_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO otdelenije (Nazvanije_otdelenije) VALUES (?)",
                            (n_otd,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM otdelenije WHERE id_otdelenije = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        n_otd = self.n_otd.get() or self.select_row[1]

        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                        UPDATE otdelenije SET Nazvanije_otdelenije = ? 
                        WHERE id_otdelenije = {self.select_row[0]}''', (n_otd,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowFinans(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="Название вида финансирования").grid(row=1, column=0)
            self.n_fin = tk.Entry(self, width=20)
            self.n_fin.grid(row=1, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=2, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Вид финансирования'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[0]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="Название вида финансирования").grid(row=1, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=2, column=1)
            self.n_fin = tk.Entry(self, width=20)
            self.n_fin.grid(row=1, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=2, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=2, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        n_fin = self.n_fin.get()
        if n_fin:
            try:
                conn = sqlite3.connect("res\\labb18_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO vid_finansirovanija (Nazvanije_vid_finansirovanija) VALUES (?)",
                            (n_fin,))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM vid_finansirovanija WHERE id_vid_finansirovanija = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        n_fin = self.n_fin.get() or self.select_row[1]

        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                        UPDATE vid_finansirovanija SET Nazvanije_vid_finansirovanija = ? 
                        WHERE id_vid_finansirovanija = {self.select_row[0]}''', (n_fin,))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowRoditeli(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="ФИО Матери").grid(row=1, column=0)
            self.fio_mat = tk.Entry(self, width=20)
            self.fio_mat.grid(row=1, column=1)

            tk.Label(self, text="ФИО Отца").grid(row=2, column=0)
            self.fio_otc = tk.Entry(self, width=20)
            self.fio_otc.grid(row=2, column=1)

            tk.Label(self, text="Телефон матери").grid(row=3, column=0)
            self.tel_mat = tk.Entry(self, width=20)
            self.tel_mat.grid(row=3, column=1)

            tk.Label(self, text="Телефон отца").grid(row=4, column=0)
            self.tel_otc = tk.Entry(self, width=20)
            self.tel_otc.grid(row=4, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=5, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=5, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Сведения о родителях'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[0]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="ФИО Матери").grid(row=1, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=1, column=1)
            self.fio_mat = tk.Entry(self, width=20)
            self.fio_mat.grid(row=1, column=2)

            tk.Label(self, text="ФИО Отца").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=2, column=1)
            self.fio_otc = tk.Entry(self, width=20)
            self.fio_otc.grid(row=2, column=2)

            tk.Label(self, text="Телефон матери").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[3]).grid(row=3, column=1)
            self.tel_mat = tk.Entry(self, width=20)
            self.tel_mat.grid(row=3, column=2)

            tk.Label(self, text="Телефон отца").grid(row=4, column=0)
            tk.Label(self, text=self.select_row[4]).grid(row=4, column=1)
            self.tel_otc = tk.Entry(self, width=20)
            self.tel_otc.grid(row=4, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=5, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=5, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        fio_mat = self.fio_mat.get()
        fio_otc = self.fio_otc.get()
        tel_mat = self.tel_mat.get()
        tel_otc = self.tel_otc.get()
        if fio_mat and fio_otc and tel_mat and tel_otc:
            try:
                conn = sqlite3.connect("res\\labb18_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO svedenija_o_roditel (FIO_materi, FIO_otsa, telephon_materi, telephon_otsa) VALUES (?, ?, ?, ?)",
                            (fio_mat, fio_otc, tel_mat, tel_otc))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM svedenija_o_roditel WHERE id_svedenija_o_roditel = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        fio_mat = self.fio_mat.get() or self.select_row[1]
        fio_otc = self.fio_otc.get() or self.select_row[2]
        tel_mat = self.tel_mat.get() or self.select_row[3]
        tel_otc = self.tel_otc.get() or self.select_row[4]

        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                            UPDATE svedenija_o_roditel 
                            SET FIO_materi = ?, FIO_otsa = ?, telephon_materi = ?, telephon_otsa = ?
                            WHERE id_svedenija_o_roditel = ?''', (fio_mat, fio_otc, tel_mat, tel_otc, self.select_row[0]))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))

class WindowStudent(tk.Toplevel):
    def __init__(self, operation, select_row = None):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        if select_row: self.select_row = select_row

        if operation == "add":
            tk.Label(self, text="ФИО").grid(row=1, column=0)
            self.fio_stl = tk.Entry(self, width=20)
            self.fio_stl.grid(row=1, column=1)

            tk.Label(self, text="Пол").grid(row=2, column=0)
            self.pol = tk.Entry(self, width=20)
            self.pol.grid(row=2, column=1)

            tk.Label(self, text="Дата рождения").grid(row=3, column=0)
            self.happy_br = tk.Entry(self, width=20)
            self.happy_br.grid(row=3, column=1)

            tk.Label(self, text="Адрес").grid(row=4, column=0)
            self.adres = tk.Entry(self, width=20)
            self.adres.grid(row=4, column=1)

            tk.Label(self, text="Телефон").grid(row=5, column=0)
            self.tel = tk.Entry(self, width=20)
            self.tel.grid(row=5, column=1)

            tk.Label(self, text="Курс").grid(row=6, column=0)
            self.kurs = tk.Entry(self, width=20)
            self.kurs.grid(row=6, column=1)

            tk.Label(self, text="Год поступления").grid(row=7, column=0)
            self.year_rec = tk.Entry(self, width=20)
            self.year_rec.grid(row=7, column=1)

            tk.Label(self, text="Год окончания").grid(row=8, column=0)
            self.year_endings = tk.Entry(self, width=20)
            self.year_endings.grid(row=8, column=1)

            tk.Label(self, text="Номер студенческого билета").grid(row=9, column=0)
            self.num_stud_ticket = tk.Entry(self, width=20)
            self.num_stud_ticket.grid(row=9, column=1)

            tk.Label(self, text="ID Группы").grid(row=10, column=0)
            self.id_group = tk.Entry(self, width=20)
            self.id_group.grid(row=10, column=1)

            tk.Label(self, text="ID Специальности").grid(row=11, column=0)
            self.id_spec = tk.Entry(self, width=20)
            self.id_spec.grid(row=11, column=1)

            tk.Label(self, text="ID Отделения").grid(row=12, column=0)
            self.id_otdel = tk.Entry(self, width=20)
            self.id_otdel.grid(row=12, column=1)

            tk.Label(self, text="ID Вида финансирования").grid(row=13, column=0)
            self.id_fin = tk.Entry(self, width=20)
            self.id_fin.grid(row=13, column=1)

            tk.Label(self, text="ID Сведение о родителях").grid(row=14, column=0)
            self.id_rod = tk.Entry(self, width=20)
            self.id_rod.grid(row=14, column=1)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=15, column=0)
            tk.Button(self, text="Сохранить", command=self.add).grid(row=15, column=1, sticky="e")

        elif operation == "delete":
            tk.Label(self, text=f"Вы действиельно хотите удалить запись\nИз таблицы 'Студент'?").grid(row=0, column=0, columnspan=2)
            tk.Label(self, text=f"Значение: {self.select_row[1]}").grid(row=1, column=0, columnspan=2)
            tk.Button(self, text="Да", command=self.delete, width=12).grid(row=2, column=0)
            tk.Button(self, text="Нет", command=self.quit_win, width=12).grid(row=2, column=1)
        
        elif operation == "change":
            tk.Label(self, text="Наименование поля").grid(row=0, column=0)
            tk.Label(self, text="Текушее значение ").grid(row=0, column=1)
            tk.Label(self, text="Новое значение   ").grid(row=0, column=2)

            tk.Label(self, text="ФИО").grid(row=1, column=0)
            tk.Label(self, text=self.select_row[1]).grid(row=1, column=1)
            self.fio_stl = tk.Entry(self, width=20)
            self.fio_stl.grid(row=1, column=2)

            tk.Label(self, text="Пол").grid(row=2, column=0)
            tk.Label(self, text=self.select_row[2]).grid(row=2, column=1)
            self.pol = tk.Entry(self, width=20)
            self.pol.grid(row=2, column=2)

            tk.Label(self, text="Дата рождения").grid(row=3, column=0)
            tk.Label(self, text=self.select_row[3]).grid(row=3, column=1)
            self.happy_br = tk.Entry(self, width=20)
            self.happy_br.grid(row=3, column=2)

            tk.Label(self, text="Адрес").grid(row=4, column=0)
            tk.Label(self, text=self.select_row[4]).grid(row=4, column=1)
            self.adres = tk.Entry(self, width=20)
            self.adres.grid(row=4, column=2)

            tk.Label(self, text="Телефон").grid(row=5, column=0)
            tk.Label(self, text=self.select_row[5]).grid(row=5, column=1)
            self.tel = tk.Entry(self, width=20)
            self.tel.grid(row=5, column=2)

            tk.Label(self, text="Курс").grid(row=6, column=0)
            tk.Label(self, text=self.select_row[6]).grid(row=6, column=1)
            self.kurs = tk.Entry(self, width=20)
            self.kurs.grid(row=6, column=2)

            tk.Label(self, text="Год поступления").grid(row=7, column=0)
            tk.Label(self, text=self.select_row[7]).grid(row=7, column=1)
            self.year_rec = tk.Entry(self, width=20)
            self.year_rec.grid(row=7, column=2)

            tk.Label(self, text="Год окончания").grid(row=8, column=0)
            tk.Label(self, text=self.select_row[8]).grid(row=8, column=1)
            self.year_endings = tk.Entry(self, width=20)
            self.year_endings.grid(row=8, column=2)

            tk.Label(self, text="Номер студенческого билета").grid(row=9, column=0)
            tk.Label(self, text=self.select_row[9]).grid(row=9, column=1)
            self.num_stud_ticket = tk.Entry(self, width=20)
            self.num_stud_ticket.grid(row=9, column=2)

            tk.Label(self, text="ID Группы").grid(row=10, column=0)
            tk.Label(self, text=self.select_row[10]).grid(row=10, column=1)
            self.id_group = tk.Entry(self, width=20)
            self.id_group.grid(row=10, column=2)

            tk.Label(self, text="ID Специальности").grid(row=11, column=0)
            tk.Label(self, text=self.select_row[11]).grid(row=11, column=1)
            self.id_spec = tk.Entry(self, width=20)
            self.id_spec.grid(row=11, column=2)

            tk.Label(self, text="ID Отделения").grid(row=12, column=0)
            tk.Label(self, text=self.select_row[12]).grid(row=12, column=1)
            self.id_otdel = tk.Entry(self, width=20)
            self.id_otdel.grid(row=12, column=2)

            tk.Label(self, text="ID Вид финансирования").grid(row=13, column=0)
            tk.Label(self, text=self.select_row[13]).grid(row=13, column=1)
            self.id_fin = tk.Entry(self, width=20)
            self.id_fin.grid(row=13, column=2)

            tk.Label(self, text="ID Сведение о родителях").grid(row=14, column=0)
            tk.Label(self, text=self.select_row[14]).grid(row=14, column=1)
            self.id_rod = tk.Entry(self, width=20)
            self.id_rod.grid(row=14, column=2)

            tk.Button(self, text="Отмена", command=self.quit_win).grid(row=15, column=0)
            tk.Button(self, text="Сохранить", command=self.change).grid(row=15, column=2, sticky="e")
    
    def quit_win(self):
        win.deiconify()
        win.update_table()
        self.destroy()
    
    def add(self):
        fio_stl = self.fio_stl.get()
        pol = self.pol.get()
        happy_br = self.happy_br.get()
        adres = self.adres.get()
        tel = self.tel.get()
        kurs = self.kurs.get()
        year_rec = self.year_rec.get()
        year_endings = self.year_endings.get()
        num_stud_ticket = self.num_stud_ticket.get()
        id_group = self.id_group.get()
        id_spec = self.id_spec.get()
        id_otdel = self.id_otdel.get()
        id_fin = self.id_fin.get()
        id_rod = self.id_rod.get()
        if fio_stl and pol and happy_br and adres and tel and kurs and year_rec and year_endings and num_stud_ticket and id_group and id_spec and id_otdel and id_fin and id_rod:
            try:
                conn = sqlite3.connect("res\\labb18_bd.db")
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO student (FIO, pol, data_rozdenija, adres, telefon, kurs, god_postuplenija, god_okonchanija, nomer_stud_bileta, id_group, id_specialnosti, id_otdelenije, id_vid_finansirovanija, id_svedenija_o_roditel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (fio_stl, pol, happy_br, adres, tel, kurs, year_rec, year_endings, num_stud_ticket, id_group, id_spec, id_otdel, id_fin, id_rod))
                conn.commit()
                conn.close()
                self.quit_win()
            except sqlite3.Error as e:
                showerror(title="Ошибка", message=str(e))
        else:
            showerror(title="Ошибка", message="Заполните все поля")

    def delete(self):
        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM student WHERE id_student = ?", (self.select_row[0],))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e)) #or self.select_row[1]

    def change(self):
        fio_stl = self.fio_stl.get() or self.select_row[1]
        pol = self.pol.get() or self.select_row[2]
        happy_br = self.happy_br.get() or self.select_row[3]
        adres = self.adres.get() or self.select_row[4]
        tel = self.tel.get() or self.select_row[5]
        kurs = self.kurs.get() or self.select_row[6]
        year_rec = self.year_rec.get() or self.select_row[7]
        year_endings = self.year_endings.get() or self.select_row[8]
        num_stud_ticket = self.num_stud_ticket.get() or self.select_row[9]
        id_group = self.id_group.get() or self.select_row[10]
        id_spec = self.id_spec.get() or self.select_row[11]
        id_otdel = self.id_otdel.get() or self.select_row[12]
        id_fin = self.id_fin.get() or self.select_row[13]
        id_rod = self.id_rod.get() or self.select_row[14]

        try:
            conn = sqlite3.connect("res\\labb18_bd.db")
            cursor = conn.cursor()
            cursor.execute(f'''
                        UPDATE student 
                        SET FIO = ?, pol = ?, data_rozdenija = ?, adres = ?, telefon = ?, kurs = ?, god_postuplenija = ?, god_okonchanija = ?, nomer_stud_bileta = ?, id_group = ?, id_specialnosti = ?, id_otdelenije = ?, id_vid_finansirovanija = ?, id_svedenija_o_roditel = ? 
                        WHERE id_student = ?''', (fio_stl, pol, happy_br, adres, tel, kurs, year_rec, year_endings, num_stud_ticket, id_group, id_spec, id_otdel, id_fin, id_rod, self.select_row[0]))
            conn.commit()
            conn.close()
            self.quit_win()
        except sqlite3.Error as e:
            showerror(title="Ошибка", message=str(e))
            
# о программе
class info (ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit_win())
        self.title('О программе')

        self.image_frame = ctk.CTkFrame(self, width=250, height=500)
        self.image_frame.grid(row=0, column=0, padx=5, pady=5)

        self.textbox = ctk.CTkFrame(self, width=600)
        self.textbox.grid(row=0, column=1, padx=(20), pady=(5), sticky="nsew")
        self.navigation_frame_label = ctk.CTkLabel(self.textbox, text="О программе", compound="right", font=ctk.CTkFont(size=18, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.info_frame = ctk.CTkLabel(self.textbox, text='Программное средтсво "Студенческий отдел кадров"\n'
                                                          ' \nВерсия: 0.1 \n'
                                                          ' \nРазработала: Чаевская Евгения Васильевна\n'
                                                          ' \nГод выпуска: 2023\n'
                                                          ' \nПрограммное средство "Студенческий отдел кадров" разработанно с целью\n'
                                                          '  организации и управление студенческим трудоустройством, а также решения\n различных вопросов, связанных с учебным процессом.', font=ctk.CTkFont(size=14, weight="bold"))
        self.info_frame.grid(row=1, column=0, padx=20, pady=20)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=3, column=1, sticky="e", pady=5, padx=20)

        ctk.CTkButton(btn_frame, text="ОК", width=100, command=self.quit_win, compound="right",
                      font=ctk.CTkFont(size=15)).grid(row=3, column=0, sticky="w")
        # Загрузка фона
        bg = ctk.CTkImage(Image.open("image\\image\\info.jpg"), size=(250, 500))
        lbl = ctk.CTkLabel(self.image_frame, image=bg, text=' ', font=("Calibri", 40))
        lbl.place(relwidth=1, relheight=1)


    def quit_win(self):
        win.deiconify()
        self.destroy()


        
if __name__ == "__main__":
    win = WindowMain()
    win.mainloop()
