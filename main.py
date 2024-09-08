import urllib.parse
from flask import Flask, request, Response, jsonify
import os
import validators
import sqlite3
import urllib
import yt_dlp

sqliteConnection = sqlite3.connect('sql.db')
cursor = sqliteConnection.cursor()
print("DB Init")

query = 'select sqlite_version();'
cursor.execute(query)

result = cursor.fetchall()
print(f"SQLite Version is {result}")

cursor.execute('''CREATE TABLE IF NOT EXISTS videos
               (url TEXT, votes integer, title TEXT, thumbnail TEXT)''')

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
    results = []
    try:
        connection = sqlite3.connect("sql.db")
        cursor = connection.execute("""SELECT * 
                                    FROM videos 
                                    ORDER BY votes DESC 
                                    LIMIT 5""")
        results = cursor.fetchall()
    finally:
        connection.close()
        
    return jsonify(results)

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
                with yt_dlp.YoutubeDL() as ydl:
                    info_dict = ydl.extract_info(full_url, download=False)
                    # print(info_dict.keys())
                    title = info_dict['title']
                    thumbnail = info_dict['thumbnail']
                cursor.execute("""INSERT INTO videos VALUES (?, ?, ?, ?)""", 
                               (url, 1, title, thumbnail))
            else:
                cursor.execute("UPDATE videos SET votes=? WHERE url=?", (existing[1] + 1, url))
            connection.commit()
        finally:
            connection.close()
        return Response(status=200)
    return Response(status=400)