from flask import Flask, render_template, request, jsonify, url_for
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
BASE_URL = "https://api.themoviedb.org/3"


@app.route('/')
def index():
    return render_template('index.html', movies=None, error=None)

@app.route('/search', methods=['POST'])
def search_movies():
    query = request.form.get('query')
    if query:
        headers = {
            'Authorization': f'Bearer {API_TOKEN}'
        }
        response = requests.get(f"{BASE_URL}/search/movie", params={
            'key': API_KEY,
            'query': query
        }, headers=headers)
        
        if response.status_code == 200:
            movies = response.json().get('results')
            return render_template('index.html', movies=movies, error=None)
        else:
            error_message = "Error fetching movies from the API."
            return render_template('index.html', movies=None, error=error_message)
    else:
        error_message = "Please enter a movie title!"
        return render_template('index.html', movies=None, error=error_message)


@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }
    response = requests.get(f"{BASE_URL}/movie/{movie_id}", params={
        'key': API_KEY,
        'query': query
    }, headers=headers)
    if response.status_code == 200:
            movie = response.json()
            return render_template('index.html', movie=movie, error=None)
    else:
        error_message = "Movie not found"
        return render_template('index.html', movies=None, error=error_message)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
