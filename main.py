from db import *
import os
import hashlib
import random
import getpass

# Funksjon for å opprette databasen og tabellen


def db_create():
    mycursor.execute("CREATE DATABASE IF NOT EXISTS KR_BANK")
    mycursor.execute("USE KR_BANK")

    # Opprett users tabell
    mycursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Opprett accounts tabell
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


db_create()

# Krypterer passordet


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def linje():
    print("--------------------------------------------------")

def enter():
    input("Trykk Enter for å fortsette...")  

# Hovedmeny


def ui():
    os.system("cls")  # Tømmer skjermen
    linje()
    print("Velkommen til Kim Robbin's bank")
    linje()
    print("1. Logg inn")
    print("2. Opprett en ny bruker")
    print("3. Avslutt")
    user_input = input("Velg et alternativ: ")
    return user_input

# brukerinnlogging


def login():
    os.system("cls")
    linje()
    print("Logg inn")
    linje()
    username = input("Skriv inn brukernavn: ")
    password = getpass.getpass("Skriv inn passord: ") # getpass gjør at passordet ikke vises i terminalen
    hased_password = hash_password(password)

    # Sjekker om brukernavn og passord matcher i databasen
    sql_statement = ( """SELECT * FROM users
                         WHERE username = %s AND password = %s""")
    mycursor.execute(sql_statement, (username, hased_password))
    mycursor.fetchall()

    if mycursor.rowcount > 0:
        linje()
        print("Innlogging vellykket!")
        linje
        enter()# Venter på brukerens inndata før å gå videre
        return username
    else:
        print("Feil brukernavn eller passord.")

# Opptetelse av nye bruker


def create_user():
    os.system("cls")
    linje()
    print("Opprett en ny bruker")
    linje()
    username = input("Skriv inn ønsket brukernavn: ")
    password = getpass.getpass("Skriv inn ønsket passord: ")
    hased_password = hash_password(password)

    # Legger til ny bruker i databasen
    sql_statement = ("INSERT INTO users (username, password) VALUES (%s, %s)")
    mycursor.execute(sql_statement, (username, hased_password))
    dbconn.commit()


        
# UI etter inlogging


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

# Oppretter en ny konto
def opprett_konto():
    os.system("cls")
    linje()
    print("Opprett konto")
    linje()
    konto_navn = input("Skriv inn kontonavn: ")
    
    #  tilfeldig kontonummer 
    konto_nummer1 = random.randint(1000,9999)
    konto_nummer2 = random.randint(10,99)
    konto_nummer3 = random.randint(10000,99999)
    
    # Kombiner kontonummerne
    konto_nummer = f"{konto_nummer1}.{konto_nummer2}.{konto_nummer3}"
    sql_statement = ("INSERT INTO accounts (user_id, account_name, konto_nummer) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s)")
    mycursor.execute(sql_statement, (logged_in_user, konto_navn, konto_nummer))
    dbconn.commit()
    
    print("Konto opprettet!")
    enter()
    
# sjekke saldo 
def saldo():
    os.system("cls")
    linje()
    print("Sjekk saldo")
    linje()
    # Henter brukerens kontoer
    sql_statement = ("""SELECT * FROM accounts WHERE
                     user_id = (SELECT id FROM users WHERE username = %s)""")
    mycursor.execute(sql_statement, (logged_in_user,))
    accounts = mycursor.fetchall()
    
    if accounts:
        print("Dine kontoer:")
        for account in accounts:
            print(f"Kontonavn: {account[2]}, Saldo: {account[3]}, Kontonummer: {account[4]}")
        linje()
        enter()


def overforing():
    os.system("cls")
    print("OVERFØRING AV PENGER")
    linje()
    send_money = input("Hvor mye vil du overføre: ")
    linje()
    
    if send_money.isnumeric(): # Sjekker om det er et tall
        # print("DEt er et tall!")
        send_money = int(send_money)
        print("Hvor skal du sende pengene: ")
        
        sql_statement = ("""SELECT * FROM accounts WHERE
                         user_id = (SELECT id FROM users WHERE username = %s)""")
        mycursor.execute(sql_statement, (logged_in_user,))
        accounts = mycursor.fetchall()
        
        if accounts:
            for  account in accounts:
                print(f". Kontonavn: {account[2]}, Kontonummer: {account[4]}")
        
        konto_valg = input("Skriv in kontonummer: ")
        
        
        
      
        update = """
        UPDATE accounts SET saldo = saldo + %s
        WHERE konto_nummer = %s           
        
        """
        mycursor.execute(update, (send_money, konto_valg, ))
        
        print(f"Overført {send_money} kr til konto {konto_valg}")
        dbconn.commit()
            
        enter()
    else:
        print("Du må skrive inn et gyldig tall")  
        enter()
    

# Hovedprogramløkke
login_loop = True
while login_loop:
    user_input = ui()

    # Håndterer innlogging
    if user_input == "1":
        logged_in_user = login()

        # Etter inloging logikk
        if logged_in_user:
            login_loop = False

            logged_in = True
            while logged_in:
                home_input = home(logged_in_user)

                if home_input == "1":
                   
                    saldo()

                elif home_input == "2":
                    overforing()

                elif home_input == "3":
                    print("Oppretter konto")
                    opprett_konto()

                elif home_input == "4":
                    print("Logger ut...")
                    

                    login_loop = True
                    logged_in = False

    # Håndterer opprettelse av ny bruker
    elif user_input == "2":
        create_user()

    # Avslutter programmet
    elif user_input == "3":
        exit()
