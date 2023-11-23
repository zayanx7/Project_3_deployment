from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import json

app = Flask(__name__, static_url_path='/static')

# Connect to SQLite database
engine = create_engine('sqlite:///imdb.db')


# Connect to the new SQLite database
engine_landldata = create_engine('sqlite:///bmo.db')

@app.route('/')
def home():
    # Connect to SQLite database
    conn = sqlite3.connect('imdb.db')

    # Query the data from the 'imdb_data' table
    query = 'SELECT * FROM imdb_data'
    movies_df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    # Convert DataFrame to a list of dictionaries for rendering in the template
    movies = movies_df.to_dict(orient='records')

    return render_template('index.html', movies=movies)

@app.route('/movie/<series_title>')
def movie_details(series_title):
    # Connect to SQLite database
    conn = sqlite3.connect('imdb.db')

    # Query the data for the specific Series Title
    query = f"SELECT * FROM imdb_data WHERE Series_Title = '{series_title}'"
    movie_df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    # Convert DataFrame to a dictionary for rendering in the template
    movie_data = movie_df.to_dict(orient='records')[0] if not movie_df.empty else None

    return render_template('movie_details.html', movie_data=movie_data)

@app.route('/search')
def search():
    search_query = request.args.get('search', '')
    
    # Connect to SQLite database
    conn = sqlite3.connect('imdb.db')

    # Query the data from the 'imdb_data' table based on the search query
    query = f"SELECT * FROM imdb_data WHERE Series_Title LIKE '%{search_query}%'"
    search_results_df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    # Convert DataFrame to a list of dictionaries for rendering in the template
    search_results = search_results_df.to_dict(orient='records')

    return render_template('search_results.html', search_results=search_results, search_query=search_query)

@app.route('/dashboard')
def dashboard():
    # Connect to SQLite database
    conn = sqlite3.connect('imdb.db')

    # Query the data for IMDb Ratings Distribution
    ratings_distribution_query = 'SELECT IMDB_Rating, COUNT(*) AS Count FROM imdb_data GROUP BY IMDB_Rating'
    ratings_distribution_data = pd.read_sql_query(ratings_distribution_query, conn).to_dict(orient='records')
    
    

    # Query the data for IMDb Ratings vs. Gross Revenue
    ratings_vs_revenue_query = 'SELECT IMDB_Rating, Gross FROM imdb_data WHERE Gross IS NOT NULL'
    ratings_vs_revenue_data = pd.read_sql_query(ratings_vs_revenue_query, conn).to_dict(orient='records')

    # Query the data for Votes vs. Ratings
    votes_vs_ratings_query = 'SELECT No_of_Votes, IMDB_Rating FROM imdb_data WHERE No_of_Votes IS NOT NULL'
    votes_vs_ratings_data = pd.read_sql_query(votes_vs_ratings_query, conn).to_dict(orient='records')

    # Close the connection
    conn.close()


    return render_template('dashboard.html',
                           ratings_distribution_data=ratings_distribution_data,
                           ratings_vs_revenue_data=ratings_vs_revenue_data,
                           votes_vs_ratings_data=votes_vs_ratings_data)


@app.route('/map')
def map_visualization():
    # Connect to the new SQLite database
    conn_landldata = sqlite3.connect('bmo.db')

    # Query data with latitude and longitude from the 'landldata' table
    query_landldata = 'SELECT Area, Latitude, Longitude, "#1 Release", "Weekend Gross" FROM landldata WHERE Latitude IS NOT NULL AND Longitude IS NOT NULL'
    location_data = pd.read_sql_query(query_landldata, conn_landldata).to_dict(orient='records')

    # Close the connection
    conn_landldata.close()

    return render_template('map.html', location_data=location_data)

if __name__ == '__main__':
    app.run(debug=True)
