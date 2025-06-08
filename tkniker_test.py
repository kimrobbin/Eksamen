import tkinter as tk
from tkinter import ttk, messagebox
from db import *
import hashlib
import random

def db_create():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS KR_BANK")
    mycursor.execute("USE KR_BANK")

    # Create users table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Create accounts table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        account_name VARCHAR(255) NOT NULL,
        saldo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
        konto_nummer VARCHAR(20) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    dbconn.commit()

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Kim Robbin's Bank")
        self.geometry("500x400")
        self.current_user = None
        
        # Initialize frames
        self.login_frame = None
        self.register_frame = None
        self.main_frame = None
        
        self.show_login()
        
    def show_login(self):
        self.clear_frames()
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(padx=20, pady=20)
        
        tk.Label(self.login_frame, text="Kim Robbin's Bank", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        tk.Label(self.login_frame, text="Brukernavn:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.login_frame, text="Passord:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.login_frame, text="Logg inn", command=self.login).pack(pady=10)
        tk.Button(self.login_frame, text="Opprett ny bruker", command=self.show_register).pack()
        
    def show_register(self):
        self.clear_frames()
        self.register_frame = tk.Frame(self)
        self.register_frame.pack(padx=20, pady=20)
        
        tk.Label(self.register_frame, text="Opprett ny bruker", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        tk.Label(self.register_frame, text="Brukernavn:").pack()
        self.new_username = tk.Entry(self.register_frame)
        self.new_username.pack(pady=5)
        
        tk.Label(self.register_frame, text="Passord:").pack()
        self.new_password = tk.Entry(self.register_frame, show="*")
        self.new_password.pack(pady=5)
        
        tk.Button(self.register_frame, text="Opprett bruker", command=self.create_user).pack(pady=10)
        tk.Button(self.register_frame, text="Tilbake", command=self.show_login).pack()
        
    def show_main_menu(self):
        self.clear_frames()
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(padx=20, pady=20)
        
        tk.Label(self.main_frame, text=f"Velkommen {self.current_user}", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        tk.Button(self.main_frame, text="Sjekk Saldo", command=self.show_balance).pack(pady=5)
        tk.Button(self.main_frame, text="Overfør penger", command=self.show_transfer).pack(pady=5)
        tk.Button(self.main_frame, text="Opprett konto", command=self.show_create_account).pack(pady=5)
        tk.Button(self.main_frame, text="Logg ut", command=self.logout).pack(pady=20)
        
    def show_balance(self):
        self.clear_frames()
        balance_frame = tk.Frame(self)
        balance_frame.pack(padx=20, pady=20)
        
        tk.Label(balance_frame, text="Dine kontoer", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Fetch accounts
        sql_statement = "SELECT * FROM accounts WHERE user_id = (SELECT id FROM users WHERE username = %s)"
        mycursor.execute(sql_statement, (self.current_user,))
        accounts = mycursor.fetchall()
        
        if accounts:
            for account in accounts:
                account_info = f"Konto: {account[2]}\nSaldo: {account[3]} kr\nKontonummer: {account[4]}"
                tk.Label(balance_frame, text=account_info).pack(pady=5)
        else:
            tk.Label(balance_frame, text="Ingen kontoer funnet").pack(pady=5)
            
        tk.Button(balance_frame, text="Tilbake", command=self.show_main_menu).pack(pady=10)
        
    def show_create_account(self):
        self.clear_frames()
        account_frame = tk.Frame(self)
        account_frame.pack(padx=20, pady=20)
        
        tk.Label(account_frame, text="Opprett ny konto", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        tk.Label(account_frame, text="Kontonavn:").pack()
        self.account_name = tk.Entry(account_frame)
        self.account_name.pack(pady=5)
        
        tk.Button(account_frame, text="Opprett konto", command=self.create_account).pack(pady=10)
        tk.Button(account_frame, text="Tilbake", command=self.show_main_menu).pack()
        
    def clear_frames(self):
        for widget in self.winfo_children():
            widget.destroy()
            
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        sql_statement = "SELECT * FROM users WHERE username = %s AND password = %s"
        mycursor.execute(sql_statement, (username, hashed_password))
        mycursor.fetchall()
        
        if mycursor.rowcount > 0:
            self.current_user = username
            self.show_main_menu()
        else:
            messagebox.showerror("Feil", "Feil brukernavn eller passord")
            
    def create_user(self):
        username = self.new_username.get()
        password = self.new_password.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            sql_statement = "INSERT INTO users (username, password) VALUES (%s, %s)"
            mycursor.execute(sql_statement, (username, hashed_password))
            dbconn.commit()
            messagebox.showinfo("Suksess", "Bruker opprettet!")
            self.show_login()
        except:
            messagebox.showerror("Feil", "Kunne ikke opprette bruker")
            
    def create_account(self):
        account_name = self.account_name.get()
        konto_nummer = f"{random.randint(1000,9999)}.{random.randint(10,99)}.{random.randint(10000,99999)}"
        
        try:
            sql_statement = "INSERT INTO accounts (user_id, account_name, konto_nummer) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s)"
            mycursor.execute(sql_statement, (self.current_user, account_name, konto_nummer))
            dbconn.commit()
            messagebox.showinfo("Suksess", "Konto opprettet!")
            self.show_main_menu()
        except:
            messagebox.showerror("Feil", "Kunne ikke opprette konto")
            
    def logout(self):
        self.current_user = None
        self.show_login()
        
    def show_transfer(self):
        # TODO: Implement money transfer functionality
        messagebox.showinfo("Info", "Overføring kommer snart!")
        self.show_main_menu()

if __name__ == "__main__":
    db_create()  # Create database if not exists
    app = BankApp()
    app.mainloop()