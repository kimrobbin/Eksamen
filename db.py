import mysql.connector


dbconn = mysql.connector.connect(
    host="10.100.10.139",
    user="bank",
    password="kimrobbin", 
    connect_timeout=10
)

mycursor = dbconn.cursor()

if (dbconn):
    print("Connected to database")
else:
    print("Failed to connect to database")
    
