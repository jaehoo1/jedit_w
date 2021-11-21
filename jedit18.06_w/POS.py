#!/usr/bin/python3
#!/home/jacker/anaconda3/bin/python3
import tkinter as tk
from tkinter import messagebox
import datetime

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def add(item):
    global sum
    if item not in price:
        print("no item")
    item_price = price.get(item)
    sum += int(item_price)
    order.append(item)
    textarea.insert(tk.INSERT, item + " ")
    label1['text'] = "금액 : " + str(sum) + "원"

def remove():
    global sum
    item_price = price.get(order[-1])
    sum -= int(item_price)
    order.remove(order[-1])
    string = ""
    for i in order:
        string = string + i + ' '
    textarea.delete("1.0", "end")
    textarea.insert(tk.INSERT, string)
    label1['text'] = "금액 : " + str(sum) + "원"

def btn_order():
    msgbox = tk.messagebox.askquestion('확인', '주문을 마치시겠습니까?')
    if msgbox == 'yes':
        global sum
        global order
        fp = open("./ITEMLOG", 'a')
        fp.write(textarea.get("1.0", "end")[0:-1] + "\n")
        fp.close()
        fp = open("./MONEYLOG", 'a')
        fp.write(str(sum) + "\n")
        fp.close()
        fp = open("./TIMELOG", 'a')
        now = str(datetime.datetime.now())
        hour = int(now[11:13])
        string = ''
        if hour < 12:
            string += '오전 '
        else:
            string += '오후 '
        if hour > 12:
            hour -= 12
        string += str(hour) + ':' + now[14:16] + ' '
        string += now[:10]
        fp.write(string + "\n")
        fp.close()
        textarea.delete("1.0", "end")
        sum = 0
        label1['text'] = "금액 : " + str(sum) + "원"
        order = []

fp = open('./ITEM', 'r', encoding='UTF-8')
data = fp.read()
fp.close()
keys = []
values = []
data_list = data.split("\n")
idx = 0
loop = len(data_list)
if data_list[-1] == "":
    loop -= 1
for data in data_list:
    if idx==loop:
        break
    pair = data.split("=")
    keys.append(pair[0])
    values.append(pair[1])
    idx += 1

# price = {'상추' : 2000, '대파' : 3000, '깻잎' : 1000, '고추' : 2000, '감자' : 4000}
price = {}
j = 0
for i in keys:
    price[i] = values[j]
    j += 1
order = []
sum = 0

window = tk.Tk()
window.title("POS")
window.geometry("300x500")
center(window)

frame1 = tk.Frame(window)
frame1.pack()

idx = 0
for i in price:
    name = i
    if idx==0:
        A=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(A), width=10, height=2).grid(row=idx, column=0)
    elif idx==1:
        B=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(B), width=10, height=2).grid(row=idx, column=0)
    elif idx==2:
        C=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(C), width=10, height=2).grid(row=idx, column=0)
    elif idx==3:
        D=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(D), width=10, height=2).grid(row=idx, column=0)
    elif idx==4:
        E=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(E), width=10, height=2).grid(row=idx, column=0)
    elif idx==5:
        F=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(F), width=10, height=2).grid(row=idx, column=0)
    elif idx==6:
        G=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(G), width=10, height=2).grid(row=idx, column=0)
    elif idx==7:
        H=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(H), width=10, height=2).grid(row=idx, column=0)
    elif idx==8:
        I=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(I), width=10, height=2).grid(row=idx, column=0)
    elif idx==9:
        J=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(J), width=10, height=2).grid(row=idx, column=0)
    elif idx==10:
        K=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(K), width=10, height=2).grid(row=idx, column=0)
    elif idx==11:
        L=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(L), width=10, height=2).grid(row=idx, column=0)
    elif idx==12:
        M=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(M), width=10, height=2).grid(row=idx, column=0)
    elif idx==13:
        N=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(N), width=10, height=2).grid(row=idx, column=0)
    elif idx==14:
        O=i
        tk.Button(frame1, text=name, command=lambda x=idx: add(O), width=10, height=2).grid(row=idx, column=0)
    idx += 1
tk.Button(frame1, text="remove", command=remove, width=10, height=2).grid(row=idx, column=0)
idx += 1
tk.Button(frame1, text="주문", command=btn_order, width=10, height=2).grid(row=idx, column=0)

label1 = tk.Label(window, text="금액 : 0원", width=100, height=2, fg="blue")
label1.pack()

textarea = tk.Text(window)
textarea.pack()

window.mainloop()