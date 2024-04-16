import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

import sqlite3 as sql

my_dict = dict()

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

    connection.commit()
    connection.close()

def frame_user(f):
    Normal_values_label = Label(f, text="Наблюдаемые признаки:", background='#BDECB6')
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

    Normal_values_label = Label(f, text="Значение наблюдаемого признака:", background='#BDECB6')
    Normal_values_label.pack(pady=5, padx=50, anchor='w')

    combo_box_2 = Combobox(f, values=options)
    combo_box_2.pack(pady=5, padx=50, anchor='w')
    combo_box_1.bind("<<ComboboxSelected>>",
                     lambda event, cb1=combo_box_1, cb2=combo_box_2: update_combox_1(event, cb1, cb2))

    save_button = tk.Button(f, text="Добавить", command=lambda: save_Normal_values_info(combo_box_2, combo_box_1))
    save_button.pack(pady=10, padx=300, anchor='w')

    Normal_values_label = Label(f, text="Список значений признаков:", background='#BDECB6')
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

    # Добавляем кнопку для диагноза выделенного элемента из списка
    delete_button = Button(f, text="Поставить диагноз", command=lambda: diagnoz(f))
    delete_button.pack(pady=(5, 5), padx=5, side="top")


def save_Normal_values_info(Normal_values_entry, combo_box_1):
    selected_item = combo_box_1.get()

    name_Normal_values = Normal_values_entry.get()

    my_dict[selected_item] = name_Normal_values
    print("Словарь после добавления:", my_dict)

    output_text_4.insert('end', selected_item + ': ' + name_Normal_values + '\n')
    print("Saved disease info:", name_Normal_values)


def delete_selected_item_4(combo_box_1, combo_box_2):
    # Удаляем выделенный элемент из списка
    selected_index = output_text_4.curselection()
    selected_item = combo_box_1.get()

    if selected_index:
        p = output_text_4.get(selected_index)
        output_text_4.delete(selected_index)
        if p.find(":") != -1:
            p = p[:p.find(":")]
            del my_dict[p]
            print("Словарь после удаления:", my_dict)


def diagnoz(f):
    connection = sql.connect('my_database.db')
    cursor = connection.cursor()

    count = cursor.execute("SELECT COUNT(name_dis) FROM Disease").fetchone()[0]
    print(count)

    flag = False

    cur = 0
    while cur < count:
        new_dict = dict()

        dis = cursor.execute("SELECT id, name_dis FROM Disease").fetchall()
        id = dis[cur][0]
        name = dis[cur][1]
        print(id , " " + name)

        sings = cursor.execute("SELECT id_sings FROM Picture WHERE id_dis = ?", (id,)).fetchall()
        count_sin = len(sings)
        print(sings)

        s = 0
        while s < count_sin:
            p_v = cursor.execute("SELECT id_Possible_values FROM signs_of_disease WHERE id_dis = ? and id_sings = ?", (id,sings[s][0])).fetchone()[0]
            n_p = cursor.execute("SELECT name_Possible_values FROM Possible_values WHERE id = ?", (p_v, )).fetchone()[0]
            s_n = cursor.execute("SELECT name_Sings FROM Sings WHERE id = ?", (sings[s][0],)).fetchone()[0]
            print("Название признака: ", s_n, " значение: ", n_p)

            new_dict[s_n] = n_p
            s += 1

        count_p = 0
        for d in new_dict:
            if d in my_dict:
                if new_dict.get(d) == my_dict.get(d):
                    count_p +=1
            else:
                print(-1)

        if count_p == count_sin:

            flag = True
            new_window = tk.Toplevel(f, background='#BDECB6')
            new_window.geometry("300x200")
            new_window.title("Диагноз")
            label = Label(new_window, text="Диагноз: " + name, background='#BDECB6')
            label.pack(pady=(50, 0), padx=75, anchor='w')
        cur += 1

    if flag == False:
        new_window = tk.Toplevel(f, background='#BDECB6')
        new_window.geometry("300x200")
        new_window.title("Диагноз")
        label = Label(new_window, text="Диагноз: Здоров", background='#BDECB6')
        label.pack(pady=(50, 0), padx=75, anchor='w')

    connection.close()

    output_text_4.delete(0, tk.END)  # Очищаем содержимое листбокса
    my_dict.clear()
    new_dict.clear()