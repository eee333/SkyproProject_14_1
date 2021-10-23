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
def search():
    result = []
    status = '200'
    type_ = request.args.get('type') # Example: http://127.0.0.1:5000/movie?type=Movie
    title = request.args.get('title') # Example: http://127.0.0.1:5000/movie?title=Tarzan
    year = request.args.get('year') # Example: /movie?year=1973-1975 or /movie?year=1975
    genre = request.args.get('genre')  # Example: http://127.0.0.1:5000/movie?genre=Children & Family Movies
    if type_ and year and genre: # Example: /movie?genre=Dramas&type=Movie&year=1973
        year = int(year)
        result = query_db(
            f"SELECT title, description FROM netflix WHERE type = '{type_}' AND release_year = {year} AND listed_in LIKE '%{genre}%' ORDER BY title")
    elif title:
        result = query_db(f"SELECT title, country, release_year, listed_in, description FROM netflix WHERE title = '{title}' ORDER BY release_year DESC")
    elif year:
        if '-' in year:
            years = year.split('-')
            years[0] = int(years[0])
            years[1] = int(years[1])
            result = query_db(
                f"SELECT title, release_year FROM netflix WHERE release_year BETWEEN {years[0]} AND {years[1]} ORDER BY release_year DESC LIMIT 100")
        else:
            year = int(year)
            result = query_db(
                f"SELECT title, release_year FROM netflix WHERE release_year = {year}  ORDER BY release_year DESC LIMIT 100")
    elif genre:
        result = query_db(f"SELECT title, description FROM netflix WHERE listed_in LIKE '%{genre}%' ORDER BY release_year DESC LIMIT 10")

    if not result:
        result = {"error": "Not found"}
        status = '404'
    body = json.dumps(result)
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


@app.route('/cast')
def cast_search():
    actor_dic = {} # Return actors and count {'Randall Duk Kim': 2, ...}
    status = '200'
    cast = request.args.get('cast')  # Example: http://127.0.0.1:5000/cast?cast=Jack Black, Dustin Hoffman
    if cast:
        cast_pair = cast.split(', ')
        result = query_db(f"SELECT \"cast\" FROM netflix WHERE \"cast\" LIKE '%{cast_pair[0]}%' AND \"cast\" LIKE '%{cast_pair[1]}%'")

        actor_dic = {}
        i = 1
        for item in result[:-1]: # all items, but not last
            for actor in item['cast'].split(', '):
                if actor not in cast_pair:
                    for rest_item in result[i:]: # all next items
                        if actor in rest_item['cast']:
                            if actor in actor_dic.keys():
                                actor_dic[actor] += 1
                            else:
                                actor_dic[actor] = 2
            i += 1

    if not actor_dic:
        actor_dic = {"error": "Not found"}
        status = '404'
    body = json.dumps(actor_dic)
    response = Response(body, content_type='application/json', status=status)
    return response


if __name__ == '__main__':
    app.run()