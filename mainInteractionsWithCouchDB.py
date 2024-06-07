import tkinter as tk
from tkinter import messagebox
import couchdb


couch = couchdb.Server('http://login:password@127.0.0.1:5984/')
db_name = 'testdb'
db = couch[db_name]


def check_connection():
    try:
        info = couch.version()
        messagebox.showinfo("Подключение к CouchDB", f"Успешно подключено к CouchDB\nВерсия: {info}")
        return couch
    except Exception as e:
        messagebox.showerror("Подключение к CouchDB", f"Ошибка подключения к CouchDB: {e}")
        return None


def add_record():
    doc_id = text1.get("1.0", "end")
    data1 = text2.get("1.0", "end").split(' ')
    text1.delete('1.0', 'end')
    text2.delete('1.0', 'end')
    z = data1[0]
    x = data1[1]
    c = data1[2]
    data = {
        "user_id": str(z),
        "user_name": str(x),
        "user_status": str(c)
    }
    add_document(doc_id, data)

def change_record():
    doc_id = text1.get("1.0", "end")
    data1 = text2.get("1.0", "end").split(' ')
    text1.delete('1.0', 'end')
    text2.delete('1.0', 'end')
    z = data1[0]
    x = data1[1]
    c = data1[2]
    data = {
        "user_id": str(z),
        "user_name": str(x),
        "user_status": str(c)
    }
    update_document(doc_id, data)


def add_document(doc_id, data):
    if doc_id in db:
        messagebox.showerror("Документ с таким ID уже существует")
    else:
        db[doc_id] = data
        messagebox.showinfo(" ", "Документ успешно отправлен")


def get_document():
    doc_id = text1.get("1.0", "end")
    text1.delete('1.0', 'end')
    try:
        doc = db[doc_id]
        text.delete('1.0', 'end')
        text.insert('end', '\n'.join([f"{key}: {value}" for key, value in doc.items()]))
    except couchdb.http.ResourceNotFound:
        messagebox.showerror("Документ не найден")


def update_document(doc_id, data):
    try:
        doc = db[doc_id]
        for key in data:
            doc[key] = data[key]
        db[doc_id] = doc
        messagebox.showinfo(" ", "Документ успешно обновлен")
    except couchdb.http.ResourceNotFound:
        messagebox.showerror("Документ для обновления не найден")


def delete_document():
    doc_id = text1.get("1.0", "end")
    text1.delete('1.0', 'end')
    try:
        del db[doc_id]
        messagebox.showinfo(" ", "Документ успешно удален")
    except couchdb.http.ResourceNotFound:
        messagebox.showerror("Документ для удаления не найден")

def all_document():
    text.delete('1.0', 'end')
    for doc_id in db:
        doc = db[doc_id]
        text.insert('end', '\n'.join([f"{key}: {value}" for key, value in doc.items()]))
        text.insert(tk.END, '\n\n' + '-' * 50 + '\n\n')


win = tk.Tk()
win.geometry('500x800')

text = tk.Text(win)
text.config(width=100, height=30)
text.pack()

label = tk.Label(win, text='Ввод id документа')
label.pack()

text1 = tk.Text(win)
text1.config(width=50, height=2)
text1.pack()

label = tk.Label(win, text='Ввод через пробел user_id, user_name, user_status')
label.pack()

text2 = tk.Text(win)
text2.config(width=50, height=3)
text2.pack()

butFor = tk.Button(win, text='Проверить подключение к БД', command=check_connection)
butFor.pack()

butFor2 = tk.Button(win, text='Вывести все документы', command=all_document)
butFor2.pack()

increment = tk.Button(win, text='Добавить', command=add_record)
increment.pack()

decrement = tk.Button(win, text='Вывести по ID', command=get_document)
decrement.pack()

butFor1 = tk.Button(win, text='Поменять данные', command=change_record)
butFor1.pack()

butFor = tk.Button(win, text='Удалить по ID', command=delete_document)
butFor.pack()

win.mainloop()