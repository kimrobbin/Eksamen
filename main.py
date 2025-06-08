from db import * 
import os 
import hashlib


def db_create():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS KR_BANK")
    mycursor.execute("USE KR_BANK")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
        )""")

db_create()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def linje():
    print("--------------------------------------------------")

def ui():
    os.system("cls")
    linje()
    print("Velkommen til Kim Robbin's bank")
    linje()
    print("1. Log in")
    print("2. Opprett en ny bruker")
    print("3. Avslutt")
    user_input = input("Velg et alternativ: ")
    return user_input

def login():
    os.system("cls")
    linje()
    print("Logg inn")
    linje()
    username = input("Skriv inn brukernavn: ")
    password = input("Skriv inn passord: ")
    hased_password = hash_password(password)
    sql_statement = ("SELECT * FROM users WHERE username = %s AND password = %s")
    mycursor.execute(sql_statement, (username, hased_password))
    mycursor.fetchall()
    if mycursor.rowcount > 0:
        print("Innlogging vellykket!")
        return username 
     
        
        
    else:
        print("Feil brukernavn eller passord.")

def create_user():
    os.system("cls")
    linje()
    print("Opprett en ny bruker")
    linje()
    username = input("Skriv inn ønsket brukernavn: ")
    password = input("Skriv inn ønsket passord: ")
    hased_password = hash_password(password)
    sql_statement = ("INSERT INTO users (username, password) VALUES (%s, %s)") 
    mycursor.execute(sql_statement, (username, hased_password))
    dbconn.commit()      
    
def home(username):
    
    os.system("cls")
    linje()
    print(f"Velkommen {username}")
    linje()
    print("1. Sjekk Saldo")
    print("2. Overfør penger")
    print("3. Opprett konto")
    print("4. Logg ut")
    
    home_input = input("Velg et alternativ: ")
    return home_input

login_loop = True
while login_loop:
 
    user_input = ui()
    
    if user_input == "1":    
        logged_in_user = login()
        if logged_in_user:
            login_loop = False
            
            logged_in = True
            while logged_in:
                home_input = home(logged_in_user)
                
                if home_input == "1":
                    print("Sjekke saldo")
                elif home_input == "2":
                    print("Overføre penger")
                elif home_input == "3":
                    print("Opprette konto")
                elif home_input == "4":
                    print("Logger ut...")
                    login_loop = True
                    logged_in = False
                    
                
    elif user_input == "2":
        create_user()
        
        
    elif user_input == "3":
        exit()

            
            
        
