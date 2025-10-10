import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import hashlib
import datetime

# ==========================
# Login / Registration App
# ==========================
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Booking Login")
        self.root.geometry("420x350")
        self.root.configure(bg="#0f2027")

        # Gradient Background
        self.canvas = tk.Canvas(self.root, width=420, height=350, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.gradient(self.canvas, "#2193b0", "#6dd5ed")

        # Login Frame
        frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=280)

        tk.Label(frame, text="🎟️ Welcome 🎟️",
                 font=("Poppins", 18, "bold"), bg="white", fg="#1e3c72").pack(pady=15)

        # Username
        tk.Label(frame, text="Username", bg="white", fg="#555", font=("Arial", 11, "bold")).pack()
        self.username = tk.Entry(frame, font=("Arial", 12), bd=2, relief="flat", bg="#f2f2f2")
        self.username.pack(ipady=5, padx=20, pady=5, fill="x")

        # Password
        tk.Label(frame, text="Password", bg="white", fg="#555", font=("Arial", 11, "bold")).pack()
        self.password = tk.Entry(frame, show="*", font=("Arial", 12), bd=2, relief="flat", bg="#f2f2f2")
        self.password.pack(ipady=5, padx=20, pady=5, fill="x")

        # Buttons
        login_btn = tk.Button(frame, text="Login", command=self.login,
                              bg="#1e3c72", fg="white", font=("Arial", 12, "bold"),
                              bd=0, relief="flat", width=12, cursor="hand2")
        login_btn.pack(pady=10)
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#2a5298"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#1e3c72"))

        register_btn = tk.Button(frame, text="Register", command=self.register,
                                 bg="#6dd5ed", fg="black", font=("Arial", 12, "bold"),
                                 bd=0, relief="flat", width=12, cursor="hand2")
        register_btn.pack()
        register_btn.bind("<Enter>", lambda e: register_btn.config(bg="#90e0ef"))
        register_btn.bind("<Leave>", lambda e: register_btn.config(bg="#6dd5ed"))

    def gradient(self, canvas, color1, color2):
        """Draw vertical gradient"""
        for i in range(350):
            r1, g1, b1 = self.root.winfo_rgb(color1)
            r2, g2, b2 = self.root.winfo_rgb(color2)
            r = int(r1 + (r2 - r1) * i / 350) >> 8
            g = int(g1 + (g2 - g1) * i / 350) >> 8
            b = int(b1 + (b2 - b1) * i / 350) >> 8
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, 420, i, fill=color)

    # DB connection
    def dbFun(self):
        self.con = pymysql.connect(
            host="localhost",
            user="root",
            passwd="Harsh6054",
            database="rec"
        )
        self.cur = self.con.cursor()

    def hash_pwd(self, pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()

    def login(self):
        self.dbFun()
        u, p = self.username.get(), self.hash_pwd(self.password.get())
        self.cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
        result = self.cur.fetchone()
        self.con.close()

        if result:
            self.root.destroy()
            main_root = tk.Tk()
            MovieApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        self.dbFun()
        u, p = self.username.get(), self.hash_pwd(self.password.get())
        try:
            self.cur.execute("INSERT INTO users (username,password) VALUES (%s,%s)", (u, p))
            self.con.commit()
            messagebox.showinfo("Success", "User registered successfully")
        except:
            messagebox.showerror("Error", "Username already exists")
        self.con.close()


# ==========================
# Movie Ticket Reservation
# ==========================
class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Ticket Reservation System")
        self.root.geometry("1100x700")
        self.root.configure(bg="#e0f7fa")

        # Header
        header = tk.Label(self.root, text="🎥 Movie Ticket Reservation 🎥",
                          bg="#0077b6", fg="white",
                          font=("Poppins", 30, "bold"), pady=20)
        header.pack(fill="x")

        # Main Frame
        shadow = tk.Frame(self.root, bg="#023e8a")
        shadow.place(x=65, y=115, width=970, height=530)

        self.frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.frame.place(x=50, y=100, width=970, height=530)

        # Form Section
        tk.Label(self.frame, text="Select Show:", bg="white",
                 fg="#03045e", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=20, pady=25, sticky="w")
        self.opt = ttk.Combobox(self.frame, font=("Arial", 13, "bold"), width=17)
        self.opt.grid(row=0, column=1, padx=10, pady=25)
        self.load_shows()

        tk.Label(self.frame, text="Your Name:", bg="white",
                 fg="#03045e", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=20, pady=25, sticky="w")
        self.name = tk.Entry(self.frame, bd=2, width=18, font=("Arial", 13), bg="#caf0f8", relief="flat")
        self.name.grid(row=0, column=3, padx=10, pady=25)

        choose_btn = tk.Button(self.frame, text="🎟️ Choose Seat", command=self.chooseSeat,
                               font=("Arial", 13, "bold"), width=15,
                               bg="#0096c7", fg="white", relief="flat", cursor="hand2")
        choose_btn.grid(row=0, column=4, padx=30, pady=25)
        choose_btn.bind("<Enter>", lambda e: choose_btn.config(bg="#0077b6"))
        choose_btn.bind("<Leave>", lambda e: choose_btn.config(bg="#0096c7"))

        # Table Section
        self.tabFun()

    # ================== Functionalities ==================
    def dbFun(self):
        self.con = pymysql.connect(
            host="localhost",
            user="root",
            passwd="Harsh6054",
            database="rec"
        )
        self.cur = self.con.cursor()

    def load_shows(self):
        try:
            self.dbFun()
            self.cur.execute("SELECT show_no FROM movie")
            shows = [str(r[0]) for r in self.cur.fetchall()]
            self.opt['values'] = shows
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def tabFun(self):
        tabFrame = tk.Frame(self.frame, bd=2, relief="ridge", bg="#edf6f9")
        tabFrame.place(width=920, height=400, x=25, y=100)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#0077b6", foreground="white")
        style.configure("Treeview", font=("Arial", 11), rowheight=28)

        self.table = ttk.Treeview(tabFrame, columns=("showNo","time","movie","price","seats"), show="headings")
        for col, txt in zip(("showNo","time","movie","price","seats"),
                            ("Show No","Time","Movie Name","Price","Available Seats")):
            self.table.heading(col, text=txt)
            self.table.column(col, width=180, anchor="center")

        self.table.pack(fill="both", expand=1)
        self.showFun()

    def showFun(self):
        try:
            self.dbFun()
            self.cur.execute("SELECT * FROM movie")
            data = self.table.get_children()
            self.table.delete(*data)
            for i in self.cur.fetchall():
                self.table.insert('', tk.END, values=i)
            self.con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # ===== Seat Selection =====
    def chooseSeat(self):
        opt = self.opt.get()
        name = self.name.get()
        if not opt or not name:
            messagebox.showerror("Error", "Please select a show and enter your name!")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Choose Seat - Show {opt}")
        win.geometry("500x400")
        win.configure(bg="#caf0f8")

        try:
            self.dbFun()
            self.cur.execute("SELECT seat_id, seat_no, status FROM seats WHERE show_no=%s", (opt,))
            seats = self.cur.fetchall()
            self.con.close()

            row, col = 0, 0
            for seat in seats:
                seat_id, seat_no, status = seat
                color = "green" if status == "available" else "red"
                state = "normal" if status == "available" else "disabled"

                btn = tk.Button(win, text=seat_no, width=8, height=2, bg=color,
                                state=state,
                                command=lambda sid=seat_id, sno=seat_no: self.reserveSeat(sid, sno, opt, name, win))
                btn.grid(row=row, column=col, padx=10, pady=10)

                col += 1
                if col == 5:
                    col = 0
                    row += 1
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # ===== Reserve Seat =====
    def reserveSeat(self, seat_id, seat_no, show_no, name, win):
        try:
            self.dbFun()
            self.cur.execute("UPDATE seats SET status='booked' WHERE seat_id=%s", (seat_id,))
            self.cur.execute("UPDATE movie SET total_seats = total_seats - 1 WHERE show_no=%s", (show_no,))
            self.cur.execute("SELECT price FROM movie WHERE show_no=%s", (show_no,))
            price = self.cur.fetchone()[0]
            self.cur.execute("INSERT INTO bookings (name, show_no, seat_no, price) VALUES (%s,%s,%s,%s)",
                             (name, show_no, seat_no, price))
            self.con.commit()
            self.con.close()

            win.destroy()
            self.showFun()
            self.showTicket(name, show_no, seat_no, price)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # ===== Ticket Display =====
    def showTicket(self, name, show_no, seat_no, price):
        ticket_win = tk.Toplevel(self.root)
        ticket_win.title("Movie Ticket Receipt")
        ticket_win.geometry("420x350")
        ticket_win.configure(bg="#edf6f9")

        tk.Label(ticket_win, text="🎟️ Movie Ticket 🎟️", font=("Arial", 18, "bold"),
                 fg="#03045e", bg="#edf6f9").pack(pady=15)

        try:
            self.dbFun()
            self.cur.execute("SELECT movie_name, show_time FROM movie WHERE show_no=%s", (show_no,))
            movie = self.cur.fetchone()
            self.con.close()
        except:
            movie = ("Unknown", "N/A")

        details_frame = tk.Frame(ticket_win, bg="white", bd=2, relief="solid")
        details_frame.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(details_frame, text=f"Name: {name}", font=("Arial", 14), bg="white", anchor="w").pack(pady=5, padx=10, fill="x")
        tk.Label(details_frame, text=f"Movie: {movie[0]}", font=("Arial", 14), bg="white", anchor="w").pack(pady=5, padx=10, fill="x")
        tk.Label(details_frame, text=f"Show Time: {movie[1]}", font=("Arial", 14), bg="white", anchor="w").pack(pady=5, padx=10, fill="x")
        tk.Label(details_frame, text=f"Show No: {show_no}", font=("Arial", 14), bg="white", anchor="w").pack(pady=5, padx=10, fill="x")
        tk.Label(details_frame, text=f"Seat No: {seat_no}", font=("Arial", 14), bg="white", anchor="w").pack(pady=5, padx=10, fill="x")
        tk.Label(details_frame, text=f"Price: ₹{price}", font=("Arial", 14), fg="green", bg="white", anchor="w").pack(pady=5, padx=10, fill="x")
        tk.Label(details_frame, text=f"Booking Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                 font=("Arial", 12), bg="white", anchor="w").pack(pady=10, padx=10, fill="x")

        tk.Button(ticket_win, text="✅ Done", command=ticket_win.destroy,
                  font=("Arial", 12), bg="red", fg="white").pack(pady=15)


# ==========================
# Main Function
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()
