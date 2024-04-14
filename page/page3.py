import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

import sqlite3 as sql

def update_listbox(event, combo_box, listbox):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]
    print(ind_s)
    options = cursor.execute("SELECT name_Possible_values FROM Possible_values WHERE id_sings = ?", (ind_s, )).fetchall()
    options = [item[0] for item in options]
    print(options)
    listbox.delete(0, tk.END)  # Очищаем содержимое листбокса
    for d in options:
        output_text_3.insert('end', d)

    connection.commit()
    connection.close()

def frame_Possible_values(f):
    Possible_values_label = Label(f, text="Название признака:", background='#BDECB6')
    Possible_values_label.pack(pady=5, padx=50, anchor='w')

    #Получение списка признаков
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    options = cursor.execute("SELECT name_sings FROM Sings").fetchall()
    options = [item[0] for item in options]

    connection.commit()
    connection.close()

    print(options)
    combo_box = Combobox(f, values=options)
    combo_box.pack(pady=5, padx=50, anchor='w')

    Possible_values_label = Label(f, text="Возможное значение признака:", background='#BDECB6')
    Possible_values_label.pack(pady=5, padx=50, anchor='w')

    Possible_values_entry = Entry(f, width=50)
    Possible_values_entry.pack(pady=5, padx=50, anchor='w')

    save_button = tk.Button(f, text="Добавить", command=lambda: save_Possible_values_info(Possible_values_entry, combo_box))
    save_button.pack(pady=10, padx=300, anchor='w')

    Possible_values_label = Label(f, text="Список значений признаков:", background='#BDECB6')
    Possible_values_label.pack(pady=5, padx=50, anchor='w')

    button_scroll_frame = Frame(f)
    button_scroll_frame.pack(pady=(2, 50), padx=(50, 50), anchor="e", fill="both")

    # Создаем поле для вывода текста
    global output_text_3
    output_text_3 = Listbox(button_scroll_frame, height=10, width=50)
    output_text_3.pack(pady=0, padx=0, side="left", fill="both", expand=True)

    combo_box.bind("<<ComboboxSelected>>",  lambda event: update_listbox(event, combo_box, output_text_3))

    # Создаем вертикальную полосу прокрутки для текстового поля
    scrollbar = Scrollbar(button_scroll_frame, command=output_text_3.yview)
    scrollbar.pack(side='right', fill='y', padx=(0, 0), pady=0)

    # Привязываем вертикальную полосу прокрутки к текстовому полю
    output_text_3.config(yscrollcommand=scrollbar.set)

    # Добавляем кнопку для удаления выделенного элемента из списка
    delete_button = Button(f, text="Удалить", command=lambda: delete_selected_item_3(combo_box))
    delete_button.pack(pady=(5, 5), padx=5, side="top")

def save_Possible_values_info(Possible_values_entry, combo_box):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box.get()  # Получаем выбранный элемент из выпадающего списка
    print(selected_item)
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]
    print(ind_s)

    name_Possible_values = Possible_values_entry.get()
    output_text_3.insert('end', name_Possible_values + '\n')
    print("Saved disease info:", name_Possible_values)

    id_list = cursor.execute('''SELECT MAX(id) FROM Possible_values; ''').fetchall()
    if id_list and id_list[0][0] is not None:
        id_Disease = id_list[0][0] + 1
    else:
        id_Disease = 1
    data_dis = [(id_Disease, ind_s, name_Possible_values)]
    cursor.executemany('''INSERT INTO Possible_values (id, id_sings, name_Possible_values) VALUES (?, ?, ?);''', data_dis)
    print(cursor.execute("SELECT * FROM Possible_values").fetchall())

    connection.commit()
    connection.close()

def delete_selected_item_3(combo_box):
    # Удаляем выделенный элемент из списка
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    selected_item = combo_box.get()  # Получаем выбранный элемент из выпадающего списка
    ind_s = cursor.execute("SELECT id FROM Sings WHERE name_sings = ?", (selected_item,)).fetchone()[0]
    print(ind_s)

    selected_index = output_text_3.curselection()
    select_name = output_text_3.get(selected_index)

    if selected_index:
        output_text_3.delete(selected_index)

        delete_Disease = f"DELETE FROM Possible_values WHERE name_Possible_values = ? and id_sings = ?"
        cursor.execute(delete_Disease, (select_name, ind_s))
        print(cursor.execute("SELECT * FROM Possible_values").fetchall())

    connection.commit()
    connection.close()