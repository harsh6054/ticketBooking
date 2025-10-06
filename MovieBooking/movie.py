import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class movies():
    def __init__(self,root):
        self.root = root
        self.root.title("Movie Ticket Reservation")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.config(bg="#f0f0f0")

        # Title
        title = tk.Label(self.root, text="Movie Ticket Reservation", bd=4, relief="raised",fg="white", bg="#008080", font=("Arial",50,"bold"))
        title.pack(side="top", fill="x")

        # global variables
        self.row = 4
        self.seat = 5

        # Frame
        self.frame = tk.Frame(self.root, bd=3, relief="ridge", bg="white")
        self.frame.place(width=self.width-300, height=self.height-180, x=150, y=100)

        # --- Custom Styles ---
        style = ttk.Style()
        style.theme_use("clam")

        # Combobox style
        style.configure("TCombobox",fieldbackground="white",background="#e8e8e8",bordercolor="#008080",foreground="black",padding=5,relief="flat")
        style.map("TCombobox",fieldbackground=[('readonly', 'white')],background=[('active', '#d0f0ef')],bordercolor=[('focus', '#008080')])

        # Entry style
        style.configure("Custom.TEntry",fieldbackground="white",bordercolor="#008080",relief="flat",padding=6)
        style.configure("Highlight.TEntry",fieldbackground="#f8f8f8",bordercolor="#008080",relief="flat",padding=6)

        # Labels and inputs
        optLbl = tk.Label(self.frame, text="Select Show:", bg="white",fg="#333333", font=("Arial",18,"bold"))
        optLbl.grid(row=0, column=0, padx=20, pady=30)

        self.opt = ttk.Combobox(self.frame, font=("Arial",15),values=("First","Second","Third"), width=17, state="readonly")
        self.opt.set("Select One")
        self.opt.grid(row=0, column=1, padx=10, pady=30, ipady=3)

        nameLbl = tk.Label(self.frame, text="Your Name:", bg="white",fg="#333333", font=("Arial",18,"bold"))
        nameLbl.grid(row=0, column=2, padx=20, pady=30)

        self.name = ttk.Entry(self.frame, style="Custom.TEntry", font=("Arial",15), width=18)
        self.name.grid(row=0, column=3, padx=10, pady=30, ipady=3)

        # Focus effect for entry box
        self.name.bind("<FocusIn>", lambda e: self.name.configure(style="Highlight.TEntry"))
        self.name.bind("<FocusOut>", lambda e: self.name.configure(style="Custom.TEntry"))

        # Buttons
        okBtn = tk.Button(self.frame, command=self.reserveFun, text="Reserve", font=("Arial",15,"bold"), width=10, bg="#008080", fg="white", activebackground="#006666", activeforeground="white", relief="flat", cursor="hand2")
        okBtn.grid(row=0, column=4, padx=30, pady=30)

        showBtn = tk.Button(self.frame, command=self.showBookedTickets, text="Show Booked Tickets", font=("Arial",15,"bold"), width=20, bg="#006666", fg="white", activebackground="#004d4d", activeforeground="white", relief="flat", cursor="hand2")
        showBtn.grid(row=0, column=5, padx=30, pady=30)

        self.tabFun()

    def tabFun(self):
        # Table Frame
        tabFrame = tk.Frame(self.frame, bd=2, relief="groove", bg="white")
        tabFrame.place(width=self.width-400, height=self.height-300, x=50,y=90)

        x_scrol = tk.Scrollbar(tabFrame,orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        # Table style (neutral)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 13), rowheight=35,background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"),background="#008080", foreground="white")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,columns=("showNo","time","movie","price","seats"), style="Treeview")
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("showNo", text="Show_No")
        self.table.heading("time", text="Time_Table")
        self.table.heading("movie", text="Movie_Name")
        self.table.heading("price", text="Price")
        self.table.heading("seats", text="Total_Seats")
        self.table["show"]="headings"

        self.table.column("showNo", width=200)
        self.table.column("time", width=200)
        self.table.column("movie", width=300)
        self.table.column("price", width=120, anchor="center")
        self.table.column("seats", width=120, anchor="center")
        
        self.table.pack(fill="both", expand=1)
        self.showFun()

    def showFun(self):
        try:
            self.dbFun()
            self.cur.execute("select * from movie")
            data = self.cur.fetchall()

            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('',tk.END, values=i)

            self.con.close()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def reserveFun(self):
        opt = self.opt.get() 
        name = self.name.get()   
        if opt and name and opt != "Select One":
            try:
                self.dbFun()
                self.cur.execute("select show_time, movie_name, price, seats from movie where show_no=%s", (opt,))
                row = self.cur.fetchone()
                if row and row[3] > 0:
                    if self.row > 0:
                        if self.seat > 0:
                            self.seat -= 1
                            upd = row[3]-1
                            self.cur.execute("update movie set seats=%s where show_no=%s",(upd,opt))
                            # Insert into bookings table
                            self.cur.execute("insert into bookings (show_no, customer_name, row_no, seat_no) values (%s,%s,%s,%s)",
                                             (opt, name, 5-self.row, 5-self.seat))
                            self.con.commit()
                            tk.messagebox.showinfo("Success",
                                f"Seat No.{5-self.seat} in row.{5-self.row} is Reserved For Mr/Mrs.{name}\nNow Pay {row[2]}$")

                            self.cur.execute("select * from movie ")
                            data = self.cur.fetchall()

                            self.table.delete(*self.table.get_children())
                            for i in data:
                                self.table.insert('',tk.END, values=i)

                            self.con.close()
                        else:
                            self.row -= 1
                            self.seat = 5
                else:
                    tk.messagebox.showerror("Error","All Seats Reserved for this Show")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
        else:
            tk.messagebox.showerror("Error","Please Fill All Input Fields!")

    def showBookedTickets(self):
        try:
            self.dbFun()
            self.cur.execute("select * from bookings")
            data = self.cur.fetchall()
            self.con.close()
            
            if not data:
                tk.messagebox.showinfo("Booked Tickets", "No tickets booked yet.")
                return
            
            details = ""
            for d in data:
                details += f"Booking ID: {d[0]} | Show No: {d[1]} | Name: {d[2]} | Row: {d[3]} | Seat: {d[4]}\n"
            
            tk.messagebox.showinfo("Booked Tickets", details)
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="", database="movies")
        self.cur = self.con.cursor()
        
    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

root = tk.Tk()
obj = movies(root)
root.mainloop()
