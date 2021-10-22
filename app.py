# Урок 14 SQL

import sqlite3
import json
from flask import Flask, render_template, request, Response, jsonify


def query_db(sqlite_query):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        # sqlite_query = ("SELECT DISTINCT director, title FROM netflix ")
        cursor.execute(sqlite_query)
        fields = [description[0] for description in cursor.description]
        result = []
        for item in cursor.fetchall():
            line = dict(zip(fields, item))
            result.append(line)
        return result


app = Flask(__name__)


@app.route('/movie')
def search_title():
    # Example: http://127.0.0.1:5000/movie?title=Tarzan
    title = request.args.get('title')
    result = query_db(f"SELECT title, country, release_year, listed_in, description FROM netflix WHERE title = '{title}' ORDER BY release_year DESC")
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


@app.route('/rating/family/')
def rating_family():
    result = query_db("SELECT title, rating, description FROM netflix WHERE rating = 'PG' OR rating = 'PG-13'")
    body = json.dumps(result)
    status = '200'
    response = Response(body, content_type='application/json', status=status)
    return response


@app.route('/rating/adult/')
def rating_adult():
    result = query_db("SELECT title, rating, description FROM netflix WHERE rating = 'R' OR rating = 'NC-17'")
    body = json.dumps(result)
    status = '200'
    response = Response(body, content_type='application/json', status=status)
    return response


if __name__ == '__main__':
    app.run()