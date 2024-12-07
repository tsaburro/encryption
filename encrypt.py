# Allows user to create username and password, then encrypts, and stores the information for later access.
import bcrypt
import subprocess
import psycopg2
from psycopg2 import sql
import base64

DB_CONFIG = {
    "dbname": "storage",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"ERROR: Unable to connect to the database: {e}")
        exit()

def check_login(user, pswd):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # check query table for username and password
        query = sql.SQL("SELECT password_hash FROM userdata;")
        cur.execute(query, (user,))
        result = cur.fetchone()

        # if exist
        if (result):
            db_pass = result[0]
            if bcrypt.checkpw(pswd.encode("utf-8"), db_pass.encode("utf-8")):
                print("-- LOGIN SUCCESSFUL! --")
                return
        # if not exist
        print("-- ERROR: USERNAME OR PASSWORD INCORRECT --")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cur.close()
        conn.close()

def check_register(user):
    try:
        # connect to database
        conn = connect_to_db()
        cur =conn.cursor()

        # checks is username already exist
        query = sql.SQL("SELECT username FROM userdata WHERE username = %s")
        cur.execute(query, (user,))
        if cur.fetchone():
            return False
        else:
            return True
    finally:
        # close out of database
        cur.close()
        conn.close()

def register():
    print("-- CREATE AN ACCOUNT --")
    username = input("Username: ")
    password = input("Password: ")
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    check_register(username)
    if (check_register):
        # adding new username/password to db
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            query = sql.SQL("INSERT INTO userdata (username, password_hash) VALUES (%s, %s);")
            cur.execute(query, (username, hash))
        finally:
            conn.commit()
            cur.close()
            conn.close()
        print("-- ACCOUNT REGISTERED --")
        login()
    else:
        print("-- ERROR: ACCOUNT MAY ALREADY EXIST --")

def login():
    print("A) Login")
    print("B) Register")
    print("Q) Exit")
    choice = input(">> ")

    if (choice == "A" or choice == "a" or choice == "Login"):
        print("-- ENTER USERNAME AND PASSWORD --")
        username = input("Username: ")
        password = input("Password: ")
        check_login(username, password)
    elif(choice == "B" or choice == "b" or choice == "Register"):
        register()
    elif(choice == "Q" or choice =="q" or choice == "Exit"):
        exit()
    else:
        print("ERROR")
        login()

login()