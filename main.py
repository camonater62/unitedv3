import urllib.parse
from flask import Flask, request, Response
import os
import validators
import sqlite3
import urllib

sqliteConnection = sqlite3.connect('sql.db')
cursor = sqliteConnection.cursor()
print("DB Init")

query = 'select sqlite_version();'
cursor.execute(query)

result = cursor.fetchall()
print(f"SQLite Version is {result}")

cursor.execute('''CREATE TABLE IF NOT EXISTS videos
               (url TEXT, votes integer)''')

cursor.close()
sqliteConnection.commit()
sqliteConnection.close()


app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return "Pong!"

@app.route("/recommended", methods=['GET'])
def recommended():
    print(request)
    try:
        connection = sqlite3.connect("sql.db")
        cursor = connection.execute("SELECT * from videos")
        for row in cursor:
            print(row)
    finally:
        connection.close()
        
    return Response(status=200)

@app.route("/vote/<url>", methods=['POST'])
def vote(url):
    full_url = f"https://www.youtube.com/watch?v={url}"
    if validators.url(full_url):
        try:
            connection = sqlite3.connect("sql.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM videos WHERE url=?", (url, ))
            existing = cursor.fetchone()
            print(existing)
            if existing == None:
                cursor.execute("""INSERT INTO videos VALUES (?, ?)""", (url, 1))
            else:
                cursor.execute("UPDATE videos SET votes=? WHERE url=?", (existing[1] + 1, url))
            connection.commit()
        finally:
            connection.close()
        return Response(status=200)
    return Response(status=400)