# Урок 14 SQL

import sqlite3
import json
from flask import Flask, render_template, request, Response, jsonify


def query_db(sqlite_query):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        # sqlite_query = ("SELECT DISTINCT director, title FROM netflix ")  # TODO измените код запроса
        cursor.execute(sqlite_query)
        fields = [description[0] for description in cursor.description]
        result = []
        for item in cursor.fetchall():
            line = dict(zip(fields, item))
            result.append(line)
        return result


app = Flask(__name__)


@app.route('/movie/<title>/')
def search_title(title):
    result = query_db("SELECT DISTINCT director FROM netflix")
    body = json.dumps(result)
    status = '200'
    response = Response(body, content_type='application/json', status=status)
    return response


@app.route('/rating/children/')
def rating_children():
    result = query_db("SELECT title, rating, description FROM netflix WHERE rating = 'G'")
    body = json.dumps(result)
    status = '200'
    response = Response(body, content_type='application/json', status=status)
    return response


if __name__ == '__main__':
    app.run()