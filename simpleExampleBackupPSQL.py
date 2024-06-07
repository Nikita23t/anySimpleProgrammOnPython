import tkinter as tk
import psycopg2
from psycopg2.extras import DictCursor


connection = psycopg2.connect(host="127.0.0.1", database="pierrdoon", user="pierrdoon", password="0451", port="5432")
cursor = connection.cursor(cursor_factory=DictCursor)



def show_record():
    cursor = connection.cursor(cursor_factory=DictCursor)
    cursor.execute('SELECT  *  FROM orders')
    data = cursor.fetchall()
    cursor.close()
    text.delete('1.0', 'end')
    text1.delete('1.0', 'end')
    for i in range(len(data)):
        text.insert('end', ' order id: ' + str(data[i][0]) + ', customer id:  ' + str(data[i][1]) + ', amount: ' + str(data[i][2]) + ', created:  ' + str(data[i][3]) + ', updated:  ' + str(data[i][4]) + ' ' +'\n\n')


def show_record_backup():
    data = text1.get("1.0", "end")
    cursor = connection.cursor(cursor_factory=DictCursor)
    cursor.execute('SELECT  *  FROM orders1 WHERE customer_id = %s', [data])
    data = cursor.fetchall()
    cursor.close()
    text1.delete('1.0', 'end')
    text2.delete('1.0', 'end')
    for i in range(len(data)):
        text2.insert('end', ' order id: ' + str(data[i][0]) + ', customer id:  ' + str(data[i][1]) + ', amount: ' + str(data[i][2]) + ', created:  ' + str(data[i][3]) + ', updated:  ' + str(data[i][4]) + ' ' + '\n\n')


def insert_record():
    data = text1.get("1.0", "end").split()
    x = data[0]
    b = data[1]
    cursor = connection.cursor(cursor_factory=DictCursor)
    cursor.execute('INSERT INTO orders (customer_id, amount) VALUES (%s, %s) ON CONFLICT (order_id) DO UPDATE SET amount = EXCLUDED.amount', [x, b])
    cursor.execute("INSERT INTO orders1 SELECT  *  FROM orders WHERE orders.customer_id = %s", [x])
    connection.commit()
    cursor.close()
    text1.delete('1.0', 'end')


def delete_record():
    data = text1.get("1.0", "end")
    cursor = connection.cursor(cursor_factory=DictCursor)
    cursor.execute('DELETE FROM orders WHERE customer_id = %s', [data])
    connection.commit()
    cursor.close()
    text1.delete('1.0', 'end')


def change_record():
    data = text1.get("1.0", "end").split()
    x = data[0]
    b = data[1]
    cursor = connection.cursor(cursor_factory=DictCursor)
    cursor.execute('UPDATE orders SET amount = %s, updated_at = NOW() WHERE customer_id = %s', [b, x])
    cursor.execute("INSERT INTO orders1 SELECT  *  FROM orders WHERE orders.customer_id = %s", [x])
    connection.commit()
    cursor.close()
    text1.delete('1.0', 'end')


def backup_record():
    data = text1.get("1.0", "end").split()
    x = data[0]
    b = str(data[1] + ' ' + data[2])
    cursor = connection.cursor(cursor_factory=DictCursor)
    cursor.execute("DELETE FROM orders WHERE customer_id = %s", [x])
    cursor.execute("INSERT INTO orders SELECT  *  FROM orders1 WHERE orders1.customer_id = %s AND orders1.updated_at = %s", [x, b])
    cursor.execute('UPDATE orders SET updated_at = NOW() WHERE customer_id = %s', [x])
    cursor.execute("INSERT INTO orders1 SELECT  *  FROM orders WHERE orders.customer_id = %s", [x])
    connection.commit()
    cursor.close()
    text1.delete('1.0', 'end')


win = tk.Tk()
win.geometry('1100x800')

text = tk.Text(win)
text.config(width=160, height=20)
text.pack()

label = tk.Label(win, text='ввод')
label.pack()

text1 = tk.Text(win)
text1.config(width=100, height=3)
text1.pack()

label = tk.Label(win, text='бекапчик')
label.pack()

text2 = tk.Text(win)
text2.config(width=160, height=15)
text2.pack()

butFor = tk.Button(win, text='Показать данные', command=show_record)
butFor.pack()

increment = tk.Button(win, text='Добавить данные (указать новые id и стоимость)', command=insert_record)
increment.pack()

decrement = tk.Button(win, text='Удалить данные (указать customer_id)', command=delete_record)
decrement.pack()

butFor = tk.Button(win, text='Изменить данные (указать через пробел id пользователя и новую стоимость)', command=change_record)
butFor.pack()

rollback_button = tk.Button(win, text="Вернуть данные (указываем через пробел customer_id и нужные все данные из updated)", command=backup_record)
rollback_button.pack()

butFor4 = tk.Button(win, text='Показать бекап (указать customer_id)', command=show_record_backup)
butFor4.pack()

win.mainloop()