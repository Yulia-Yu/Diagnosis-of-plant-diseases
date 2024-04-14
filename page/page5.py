import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

import sqlite3 as sql

def update_combox_1(event, combo_box, combo_box_2):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_s = cursor.execute("SELECT id FROM Disease WHERE name_dis = ?", (selected_item,)).fetchone()[0]
    print(ind_s)
    options = cursor.execute("SELECT name_sings FROM Picture JOIN Sings on Sings.id = id_sings WHERE id_dis = ?", (ind_s,)).fetchall()
    options = [item[0] for item in options]
    print(options)
    output_text_5.delete(0, tk.END)  # Очищаем содержимое листбокса
    for d in options:
        output_text_5.insert('end', d)

    connection.commit()
    connection.close()

def frame_Picture(f):
    Picture_label = Label(f, text="Название заболевания:", background='#BDECB6')
    Picture_label.pack(pady=5, padx=50, anchor='w')

    # Получение списка признаков
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    options = cursor.execute("SELECT name_dis FROM Disease").fetchall()
    options = [item[0] for item in options]

    connection.commit()
    connection.close()

    combo_box_1 = Combobox(f, values=options)
    combo_box_1.pack(pady=5, padx=50, anchor='w')

    Picture_label = Label(f, text="Признаки:", background='#BDECB6')
    Picture_label.pack(pady=5, padx=50, anchor='w')

    # Получение списка признаков
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    options = cursor.execute("SELECT name_sings FROM Sings").fetchall()
    options = [item[0] for item in options]

    connection.commit()
    connection.close()

    combo_box_2 = Combobox(f, values=options)
    combo_box_2.pack(pady=5, padx=50, anchor='w')

    save_button = tk.Button(f, text="Выбрать", command=lambda: save_Picture_info(combo_box_2, combo_box_1))
    save_button.pack(pady=10, padx=300, anchor='w')

    Normal_values_label = Label(f, text="Выбранные признаки:", background='#BDECB6')
    Normal_values_label.pack(pady=5, padx=50, anchor='w')

    button_scroll_frame = Frame(f)
    button_scroll_frame.pack(pady=(2, 50), padx=(50, 50), anchor="e", fill="both")

    # Создаем поле для вывода текста
    global output_text_5
    output_text_5 = Listbox(button_scroll_frame, height=10, width=50)
    output_text_5.pack(pady=0, padx=0, side="left", fill="both", expand=True)

    combo_box_1.bind("<<ComboboxSelected>>", lambda event: update_combox_1(event, combo_box_1, combo_box_2))

    # Создаем вертикальную полосу прокрутки для текстового поля
    scrollbar = Scrollbar(button_scroll_frame, command=output_text_5.yview)
    scrollbar.pack(side='right', fill='y', padx=(0, 0), pady=0)

    # Привязываем вертикальную полосу прокрутки к текстовому полю
    output_text_5.config(yscrollcommand=scrollbar.set)

    # Добавляем кнопку для удаления выделенного элемента из списка
    delete_button = Button(f, text="Удалить", command=lambda: delete_selected_item_5(combo_box_1))
    delete_button.pack(pady=(5, 5), padx=5, side="top")

def save_Picture_info(Picture_entry, combo_box_2):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box_2.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_d = cursor.execute("SELECT id FROM Disease WHERE name_dis = ?", (selected_item,)).fetchone()[0]
    print(ind_d)

    name_Picture = Picture_entry.get()
    output_text_5.insert('end', name_Picture + '\n')
    print("Saved disease info:", name_Picture)

    id_list = cursor.execute('''SELECT MAX(id) FROM Picture; ''').fetchall()
    if id_list and id_list[0][0] is not None:
        id_Disease = id_list[0][0] + 1
    else:
        id_Disease = 1

    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (name_Picture,)).fetchone()[0]
    print(ind_s)
    data_dis = [(id_Disease, ind_d, ind_s)]
    cursor.executemany('''INSERT INTO Picture (id, id_dis, id_sings) VALUES (?, ?, ?);''',
                       data_dis)
    print(cursor.execute("SELECT * FROM Picture").fetchall())

    connection.commit()
    connection.close()

def delete_selected_item_5(combo_box):
    # Удаляем выделенный элемент из списка
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box.get()  # Получаем выбранный элемент из выпадающего списка
    ind_d = cursor.execute("SELECT id FROM Disease WHERE name_dis = ?", (selected_item,)).fetchone()[0]
    print(ind_d)

    selected_index = output_text_5.curselection()
    select_name = output_text_5.get(selected_index)
    print(select_name)
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (select_name,)).fetchone()[0]
    print(ind_s)
    if selected_index:
        output_text_5.delete(selected_index)

        delete_Disease = f"DELETE FROM Picture WHERE id_dis = ? and id_sings = ?"
        cursor.execute(delete_Disease, (ind_d, ind_s))
        print(cursor.execute("SELECT * FROM Picture").fetchall())

    connection.commit()
    connection.close()