from tkinter import *
import mysql.connector
from tkinter import messagebox

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mataji"
)

mycursor = mydb.cursor()
mycursor.execute("USE drugs")

def srch(name):
    sql = "select * from drug where name = %s"
    val = (name, )
    mycursor.execute(sql, val)
    rec=mycursor.fetchall()
    if len(rec) == 0: return 0
    else:
        return rec[0][1]

def create_window():
    window = Toplevel(root)
    window.minsize(width=200, height=50)
    Label(window, text="Drug Name").grid(row=0)
    x = Entry(window)
    x.grid(row=0, column=1)
    Label(window, text="Price").grid(row=1)
    y = Entry(window)
    y.grid(row=1, column=1)

    def add():
        sql = "INSERT INTO drug (name, price) VALUES (%s, %s);"
        val = (str(x.get()), float(y.get()))
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.execute("SELECT * FROM drug;")
        window.destroy()
    Button(window, text='Submit', fg='black', command=add).grid(row=2, column=3)

def create_window2(z):
    window = Toplevel(root)
    window.minsize(width=200, height=50)
    Label(window, text="Drug Name : " + z).grid(row=0)
    Label(window, text="Price").grid(row=1)
    y = Entry(window)
    y.grid(row=1, column=1)
    tmp = 0
    def add():
        p = float(y.get())
        sql = "INSERT INTO drug (name, price) VALUES (%s, %s);"
        val = (z,p)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.execute("SELECT * FROM drug;")
        tmp = p
        window.destroy()
    Button(window, text='Submit', fg='black', command=add).grid(row=2, column=3)
    return tmp
def create_window1():
    window = Toplevel(root)
    window.minsize(width=200, height=140)
    Label(window, text="Medicine Name").grid(row=0)
    med=Entry(window)
    med.grid(row=0, column=1)
    Label(window, text="No. of Drugs").grid(row=1)
    n=Entry(window)
    n.grid(row=1, column=1)
    def clk():
        x = Toplevel(window)
        name,qty=[],[]
        Label(x, text="Drug Name ").grid(row=0, column=0)
        Label(x, text="Drug qty. in mg ").grid(row=0, column=1)
        rng=int(n.get())
        for i in range(rng):
            y = Entry(x)
            y.grid(row=i+1, column=0)
            name.append(y)
            z = Entry(x)
            z.grid(row=i+1, column=1)
            qty.append(z)
        def add():
            prc=0
            for i in range(rng):
                nm=str(name[i].get())
                p=srch(nm)
                if p: prc+=p*int(qty[i].get())
                else:
                    messagebox.showerror("Error", "Drug data NOT found. Insert Details for "+nm)
                    prc+=create_window2(nm)*int(qty[i].get())
            sql = "INSERT INTO medic (name, price) VALUES (%s, %s);"
            val = (str(med.get()), float(prc))
            mycursor.execute(sql, val)
            mydb.commit()
            window.destroy()
        Button(x, text='Submit', fg='black', command=add).grid(row=i+2, column=1)
    Button(window, text='Submit', fg='black', command=clk).grid(row=4, column=3)

root = Tk()
root.minsize(width=555, height=444)
frame = Frame(root)
frame.pack()
frame.pack(side=TOP)
root.resizable(width=False, height=False)
bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)
redbutton = Button(frame, text='Inset Drug', fg='red', bd='50', command=create_window)
redbutton.pack(side=LEFT)
greenbutton = Button(frame, text='Insert Medicine', fg='brown', bd='50', command=create_window1)
greenbutton.pack(side=LEFT)
bluebutton = Button(bottomframe, text='Save', fg='blue', bd='50')
bluebutton.pack(side=LEFT)
blackbutton = Button(bottomframe, text='Display', fg='black', bd='50')
blackbutton.pack(side=LEFT)
root.mainloop()