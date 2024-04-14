import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

import sqlite3 as sql

def update_combox_1(event, combo_box, combo_box_2):
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

    output_text_4.delete(0, tk.END)  # Очищаем содержимое листбокса
    options = cursor.execute("SELECT name_Possible_values FROM Normal_values JOIN Possible_values on Possible_values.id = id_Possible_values WHERE Normal_values.id_sings = ?", (ind_s,)).fetchall()
    options = [item[0] for item in options]
    print(options)
    for d in options:
        output_text_4.insert('end', d)
    connection.commit()
    connection.close()

def frame_Normal_values(f):
    Normal_values_label = Label(f, text="Название признака:", background='#BDECB6')
    Normal_values_label.pack(pady=5, padx=50, anchor='w')

    # Получение списка признаков
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    options = cursor.execute("SELECT name_sings FROM Sings").fetchall()
    options = [item[0] for item in options]

    connection.commit()
    connection.close()

    print(options)
    combo_box_1 = Combobox(f, values=options)
    combo_box_1.pack(pady=5, padx=50, anchor='w')

    Normal_values_label = Label(f, text="Возможное значение признака:", background='#BDECB6')
    Normal_values_label.pack(pady=5, padx=50, anchor='w')


    combo_box_2 = Combobox(f, values=options)
    combo_box_2.pack(pady=5, padx=50, anchor='w')
    combo_box_1.bind("<<ComboboxSelected>>", lambda event, cb1=combo_box_1, cb2=combo_box_2: update_combox_1(event, cb1, cb2))

    save_button = tk.Button(f, text="Добавить", command=lambda: save_Normal_values_info(combo_box_2, combo_box_1))
    save_button.pack(pady=10, padx=300, anchor='w')

    Normal_values_label = Label(f, text="Список нормальных значений признака:", background='#BDECB6')
    Normal_values_label.pack(pady=5, padx=50, anchor='w')

    button_scroll_frame = Frame(f)
    button_scroll_frame.pack(pady=(2, 50), padx=(50, 50), anchor="e", fill="both")

    # Создаем поле для вывода текста
    global output_text_4
    output_text_4 = Listbox(button_scroll_frame, height=10, width=50)
    output_text_4.pack(pady=0, padx=0, side="left", fill="both", expand=True)

    # Создаем вертикальную полосу прокрутки для текстового поля
    scrollbar = Scrollbar(button_scroll_frame, command=output_text_4.yview)
    scrollbar.pack(side='right', fill='y', padx=(0, 0), pady=0)

    # Привязываем вертикальную полосу прокрутки к текстовому полю
    output_text_4.config(yscrollcommand=scrollbar.set)

    # Добавляем кнопку для удаления выделенного элемента из списка
    delete_button = Button(f, text="Удалить", command=lambda: delete_selected_item_4(combo_box_1, combo_box_2))
    delete_button.pack(pady=(5, 5), padx=5, side="top")

def save_Normal_values_info(Normal_values_entry, combo_box_1):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box_1.get()  # Получаем выбранный элемент из выпадающего списка
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]

    name_Normal_values = Normal_values_entry.get()
    output_text_4.insert('end', name_Normal_values + '\n')
    print("Saved disease info:", name_Normal_values)
    print(selected_item, " ", ind_s)
    ind_p = cursor.execute("SELECT id FROM Possible_values WHERE name_Possible_values = ? and id_sings = ?", (name_Normal_values, ind_s)).fetchone()[0]

    id_list = cursor.execute('''SELECT MAX(id) FROM Normal_values; ''').fetchall()
    if id_list and id_list[0][0] is not None:
        id_Disease = id_list[0][0] + 1
    else:
        id_Disease = 1


    data_dis = [(id_Disease, ind_s, ind_p)]
    cursor.executemany('''INSERT INTO Normal_values (id, id_sings, id_Possible_values) VALUES (?, ?, ?);''',
                       data_dis)
    print(cursor.execute("SELECT * FROM Normal_values").fetchall())

    connection.commit()
    connection.close()

def delete_selected_item_4(combo_box_1, combo_box_2):
    # Удаляем выделенный элемент из списка
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box_1.get()  # Получаем выбранный элемент из выпадающего списка
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]
    print(ind_s)

    selected_index = output_text_4.curselection()
    select_name = output_text_4.get(selected_index)
    print(select_name, " ", ind_s)
    ind_p = cursor.execute("SELECT id FROM Possible_values WHERE name_Possible_values = ? and id_sings = ?", (select_name, ind_s)).fetchone()[0]
    if selected_index:
        output_text_4.delete(selected_index)

        delete_Disease = f"DELETE FROM Normal_values WHERE id_Possible_values = ? and id_sings = ?"
        cursor.execute(delete_Disease, (ind_p, ind_s))
        print(cursor.execute("SELECT * FROM Normal_values").fetchall())

    connection.commit()
    connection.close()