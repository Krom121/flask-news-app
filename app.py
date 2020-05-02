import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient


app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route("/")
def index():
    # Init api
    newsapi = NewsApiClient(api_key='b855866438b64269ba90a58a73b28673')
    
    top_headlines = newsapi.get_top_headlines(sources='bbc-news, cnn, fox-news')

    articles = top_headlines['articles']
    desc = []
    aut = []
    news = []
    link = []
    img = []

    # ilitarate over the data in api with for loop
    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        aut.append(myarticles['author'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        link.append(myarticles['url'])

    mylist = zip(news, aut, desc, img, link)

    return render_template("index.html", context=mylist, title="News Feed")


# Post route for adding cities to database
@app.route("/weather", methods=['POST'])
def weather_post():
    # get the value from the from input by name 
    new_city = request.form.get('city')
    if new_city:
        new_city_obj = City(name=new_city)
        db.session.add(new_city_obj)
        # save new city to database
        db.session.commit()
    return redirect(url_for('weather_get'))

# get route for reciving the data from database and appending with api
@app.route("/weather")
def weather_get():
   
    # query database for all cities within the city table
    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6560b436a15d6c73ed06592ef82af38a'
    
    # create a list to hold all the weather for all the cities
    weather_data = []

    # ilitarate over the data in databse with for loop
    for city in cities:


        r = requests.get(url.format(city.name)).json()
        # print(r) print json response to test that api is working correctly

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        # Append weather to weather data for weather
        weather_data.append(weather)

    return render_template("weather.html", weather_data=weather_data, title="Weather")


@app.route("/sports")
def sports():
    return render_template("sports.html", title="Sports")


if __name__ == '__main__':
   app.run(debug=True) 