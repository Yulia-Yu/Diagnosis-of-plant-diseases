import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

import sqlite3 as sql

def update_combox_1(event, combo_box, combo_box_2, combo_box_0):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]
    print(ind_s)
    options = cursor.execute("SELECT name_Possible_values FROM Possible_values WHERE id_sings = ?", (ind_s,)).fetchall()
    options = [item[0] for item in options]
    print(options)

    combo_box_2.set("")
    combo_box_2['values'] = ()
    combo_box_2['values'] = options

    output_text_6.delete(0, tk.END)  # Очищаем содержимое листбокса
    selected_item = combo_box_0.get()
    ind_d = cursor.execute("SELECT id FROM Disease WHERE name_dis = ?", (selected_item,)).fetchone()[0]

    options = cursor.execute("SELECT name_Possible_values FROM signs_of_disease JOIN Possible_values on Possible_values.id = id_Possible_values WHERE signs_of_disease.id_sings = ? and signs_of_disease.id_dis = ? ", (ind_s, ind_d)).fetchall()
    options = [item[0] for item in options]
    print(options)
    for d in options:
        output_text_6.insert('end', d)
    connection.commit()
    connection.close()

def update_combox_2(event, combo_box, combo_box_2):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_d = cursor.execute("SELECT id FROM Disease WHERE name_dis = ?", (selected_item,)).fetchone()[0]
    print(ind_d)
    options = cursor.execute("SELECT name_sings FROM Picture JOIN Sings on Sings.id = id_sings WHERE id_dis = ?", (ind_d,)).fetchall()
    options = [item[0] for item in options]
    print(options)

    combo_box_2.set("")
    combo_box_2['values'] = ()
    combo_box_2['values'] = options

    output_text_6.delete(0, tk.END)  # Очищаем содержимое листбокса

    connection.commit()
    connection.close()

def frame_signs_of_disease(f):
    signs_of_disease_label = Label(f, text="Название заболевания:", background='#BDECB6')
    signs_of_disease_label.pack(pady=5, padx=50, anchor='w')

    # Получение списка признаков
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    options = cursor.execute("SELECT name_dis FROM Disease").fetchall()
    options = [item[0] for item in options]

    connection.commit()
    connection.close()

    combo_box_1 = Combobox(f, values=options)
    combo_box_1.pack(pady=5, padx=50, anchor='w')

    signs_of_disease_label = Label(f, text="Название признака:", background='#BDECB6')
    signs_of_disease_label.pack(pady=5, padx=50, anchor='w')


    combo_box_2 = Combobox(f, values=options)
    combo_box_2.pack(pady=5, padx=50, anchor='w')
    combo_box_1.bind("<<ComboboxSelected>>",
                     lambda event, cb1=combo_box_1, cb0=combo_box_2: update_combox_2(event, cb1, cb0))

    signs_of_disease_label = Label(f, text="Выбрать значение:", background='#BDECB6')
    signs_of_disease_label.pack(pady=5, padx=50, anchor='w')

    combo_box_3 = Combobox(f, values=options)
    combo_box_3.pack(pady=5, padx=50, anchor='w')
    combo_box_2.bind("<<ComboboxSelected>>",
                     lambda event, cb1=combo_box_2, cb2=combo_box_3, cb0=combo_box_1: update_combox_1(event, cb1, cb2, cb0))

    save_button = tk.Button(f, text="Выбрать", command=lambda: save_signs_of_disease_info(combo_box_3, combo_box_1, combo_box_2))
    save_button.pack(pady=10, padx=300, anchor='w')

    signs_of_disease_label = Label(f, text="Значения признака:", background='#BDECB6')
    signs_of_disease_label.pack(pady=5, padx=50, anchor='w')

    button_scroll_frame = Frame(f)
    button_scroll_frame.pack(pady=(2, 50), padx=(50, 50), anchor="e", fill="both")

    # Создаем поле для вывода текста
    global output_text_6
    output_text_6 = Listbox(button_scroll_frame, height=10, width=50)
    output_text_6.pack(pady=0, padx=0, side="left", fill="both", expand=True)


    # Создаем вертикальную полосу прокрутки для текстового поля
    scrollbar = Scrollbar(button_scroll_frame, command=output_text_6.yview)
    scrollbar.pack(side='right', fill='y', padx=(0, 0), pady=0)

    # Привязываем вертикальную полосу прокрутки к текстовому полю
    output_text_6.config(yscrollcommand=scrollbar.set)

    # Добавляем кнопку для удаления выделенного элемента из списка
    delete_button = Button(f, text="Удалить",  command=lambda: delete_selected_item_6(combo_box_1, combo_box_2))
    delete_button.pack(pady=(5, 5), padx=5, side="top")

def save_signs_of_disease_info(signs_of_disease_entry, combo_box_1, combo_box_2):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box_1.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_d = cursor.execute("SELECT id FROM Disease WHERE name_dis = ?", (selected_item,)).fetchone()[0]
    print(ind_d)

    selected_item = combo_box_2.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]
    print(ind_s)

    name = signs_of_disease_entry.get()
    output_text_6.insert('end', name + '\n')
    print("Saved disease info:", name)

    ind_p = cursor.execute("SELECT id FROM Possible_values WHERE name_Possible_values = ?", (name,)).fetchone()[0]

    id_list = cursor.execute('''SELECT MAX(id) FROM signs_of_disease; ''').fetchall()
    if id_list and id_list[0][0] is not None:
        id_Disease = id_list[0][0] + 1
    else:
        id_Disease = 1
    data_dis = [(id_Disease, ind_d, ind_s, ind_p)]
    cursor.executemany('''INSERT INTO signs_of_disease (id, id_dis, id_sings, id_Possible_values) VALUES (?, ?, ?, ?);''',
                       data_dis)
    print(cursor.execute("SELECT * FROM signs_of_disease").fetchall())

    connection.commit()
    connection.close()

def delete_selected_item_6(combo_box_1, combo_box_2):
    # Удаляем выделенный элемент из списка
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box_1.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_d = cursor.execute("SELECT id FROM Disease WHERE name_dis = ?", (selected_item,)).fetchone()[0]
    print(ind_d)

    selected_item = combo_box_2.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]
    print(ind_s)

    selected_index = output_text_6.curselection()
    select_name = output_text_6.get(selected_index)
    ind_p = cursor.execute("SELECT id FROM Possible_values WHERE name_Possible_values = ?", (select_name,)).fetchone()[0]
    if selected_index:
        output_text_6.delete(selected_index)

        delete_Disease = f"DELETE FROM signs_of_disease WHERE id_dis = ? and id_sings = ? and id_Possible_values = ?"
        cursor.execute(delete_Disease, (ind_d, ind_s, ind_p))
        print(cursor.execute("SELECT * FROM signs_of_disease").fetchall())

    connection.commit()
    connection.close()