import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

import sqlite3 as sql

def frame_Sings(f):
    Sings_label = Label(f, text="Название признака:", background='#BDECB6')
    Sings_label.pack(pady=5, padx=50, anchor='w')

    Sings_entry = Entry(f, width=50)
    Sings_entry.pack(pady=5, padx=50, anchor='w')

    save_button = tk.Button(f, text="Добавить", command=lambda: save_Sings_info(Sings_entry))
    save_button.pack(pady=10, padx=300, anchor='w')

    Sings_label = Label(f, text="Признаки:", background='#BDECB6')
    Sings_label.pack(pady=5, padx=50, anchor='w')

    button_scroll_frame = Frame(f)
    button_scroll_frame.pack(pady=(2, 50), padx=(50, 50), anchor="e", fill="both")


    # Создаем поле для вывода текста
    global output_text_2
    output_text_2 = Listbox(button_scroll_frame, height=10, width=50)
    output_text_2.pack(pady=0, padx=0, side="left", fill="both", expand=True)

    # Заполняем поле текущими значениями
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    data_dis = cursor.execute("SELECT * FROM Sings").fetchall()
    for d in data_dis:
        output_text_2.insert('end', d[1])

    connection.commit()
    connection.close()

    # Создаем вертикальную полосу прокрутки для текстового поля
    scrollbar = Scrollbar(button_scroll_frame, command=output_text_2.yview)
    scrollbar.pack(side='right', fill='y', padx=(0, 0), pady=0)

    # Привязываем вертикальную полосу прокрутки к текстовому полю
    output_text_2.config(yscrollcommand=scrollbar.set)

    # Добавляем кнопку для удаления выделенного элемента из списка
    delete_button = Button(f, text="Удалить", command=delete_selected_item_2)
    delete_button.pack(pady=(5, 5), padx=5, side="top")

def save_Sings_info(Sings_entry):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    name_Sings = Sings_entry.get()
    output_text_2.insert('end', name_Sings + '\n')
    print("Saved Sings info:", name_Sings)

    id_list = cursor.execute('''SELECT MAX(id) FROM Sings; ''').fetchall()
    if id_list and id_list[0][0] is not None:
        id_Disease = id_list[0][0] + 1
    else:
        id_Disease = 1
    data_dis = [(id_Disease, name_Sings)]
    cursor.executemany('''INSERT INTO Sings (id, name_sings) VALUES (?, ?);''', data_dis)
    print(cursor.execute("SELECT * FROM Sings").fetchall())

    connection.commit()
    connection.close()

def delete_selected_item_2():
    # Удаляем выделенный элемент из списка
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_index = output_text_2.curselection()
    select_name = output_text_2.get(selected_index)
    if selected_index:
        output_text_2.delete(selected_index)

        delete_Disease = f"DELETE FROM Sings WHERE name_sings = ?"
        cursor.execute(delete_Disease, (select_name,))
        print(cursor.execute("SELECT * FROM Sings").fetchall())

    connection.commit()
    connection.close()
