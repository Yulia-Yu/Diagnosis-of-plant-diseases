import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

import sqlite3 as sql


def frame_Disease(f):
    disease_label = Label(f, text="Название заболевания:", background='#BDECB6')
    disease_label.pack(pady=5, padx=50, anchor='w')

    disease_entry = Entry(f, width=50)
    disease_entry.pack(pady=5, padx=50, anchor='w')

    save_button = tk.Button(f, text="Добавить", command=lambda: save_disease_info(disease_entry))
    save_button.pack(pady=10, padx=300, anchor='w')

    disease_label = Label(f, text="Заболевания:", background='#BDECB6')
    disease_label.pack(pady=5, padx=50, anchor='w')

    button_scroll_frame = Frame(f)
    button_scroll_frame.pack(pady=(2, 50), padx=(50, 50), anchor="e", fill="both")

    # Создаем поле для вывода текста
    global output_text
    output_text = Listbox(button_scroll_frame, height=10, width=50)
    output_text.pack(pady=0, padx=0, side="left", fill="both", expand=True)

    #Заполняем поле текущими значениями
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    data_dis = cursor.execute("SELECT * FROM Disease").fetchall()
    for d in data_dis:
        output_text.insert('end', d[1])

    connection.commit()
    connection.close()

    # Создаем вертикальную полосу прокрутки для текстового поля
    scrollbar = Scrollbar(button_scroll_frame, command=output_text.yview)
    scrollbar.pack(side='right', fill='y', padx=(0, 0), pady=0)

    # Привязываем вертикальную полосу прокрутки к текстовому полю
    output_text.config(yscrollcommand=scrollbar.set)

    # Добавляем кнопку для удаления выделенного элемента из списка
    delete_button = Button(f, text="Удалить", command=delete_selected_item)
    delete_button.pack(pady=(5, 5), padx=5, side="top")

def save_disease_info(disease_entry):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    name_disease = disease_entry.get()
    output_text.insert('end', name_disease )

    id_list = cursor.execute('''SELECT MAX(id) FROM Disease; ''').fetchall()
    id_Disease = id_list[0][0] + 1
    data_dis = [(id_Disease, name_disease)]
    cursor.executemany('''INSERT INTO Disease (id, name_dis) VALUES (?, ?);''', data_dis)
    print(cursor.execute("SELECT * FROM Disease").fetchall())

    connection.commit()
    connection.close()

def delete_selected_item():
    # Удаляем выделенный элемент из списка
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_index = output_text.curselection()
    select_name = output_text.get(selected_index)
    print(select_name)
    if selected_index:
        output_text.delete(selected_index)

        delete_Disease = f"DELETE FROM Disease WHERE name_dis = ?"
        cursor.execute(delete_Disease, (select_name,))
        print(cursor.execute("SELECT * FROM Disease").fetchall())

    connection.commit()
    connection.close()


