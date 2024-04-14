import tkinter as tk
from tkinter import *
from tkinter.ttk import Notebook, Style, Combobox

from page.page1 import frame_Disease
from page.page2 import frame_Sings
from page.page3 import frame_Possible_values
from page.page4 import frame_Normal_values
from page.page5 import frame_Picture
from page.page6 import frame_signs_of_disease

root = tk.Tk()

# Создание стиля для вкладок
style = Style(root)
style.configure('lefttab.TNotebook', tabposition='wn')
style.configure('lefttab.TNotebook.Tab', padding=[10, 5], font=('Helvetica', 10, 'bold'))

# Создание вкладок
notebook = Notebook(root, style='lefttab.TNotebook')
f1 = tk.Frame(notebook, bg='#BDECB6', width=500, height=600)
f2 = tk.Frame(notebook, bg='#BDECB6', width=700, height=600)
f3 = tk.Frame(notebook, bg='#BDECB6', width=700, height=600)
f4 = tk.Frame(notebook, bg='#BDECB6', width=700, height=600)
f5 = tk.Frame(notebook, bg='#BDECB6', width=700, height=600)
f6 = tk.Frame(notebook, bg='#BDECB6', width=700, height=600)
f7 = tk.Frame(notebook, bg='black', width=700, height=600)
notebook.add(f1, text='Заболевания')
notebook.add(f2, text='Признаки')
notebook.add(f3, text='Возможные значения признаков')
notebook.add(f4, text='Нормальные значения признаков')
notebook.add(f5, text='Картина заболевания')
notebook.add(f6, text='Значения признаков для заболевания')
notebook.add(f7, text='Проверка полноты знаний')
notebook.pack()

frame_Disease(f1)
frame_Sings(f2)
frame_Possible_values(f3)
frame_Normal_values(f4)
frame_Picture(f5)
frame_signs_of_disease(f6) 

root.mainloop()
