import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient


app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisismysecret'

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&appid=6560b436a15d6c73ed06592ef82af38a'
    r = requests.get(url).json()
    return r


# Init api for news headlines
newsapi = NewsApiClient(api_key='b855866438b64269ba90a58a73b28673')

@app.route("/")
def index():
    #add sources from api
    top_headlines = newsapi.get_top_headlines(sources='bbc-news, cnn, fox-news, reuters, usa-today')

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
    err_msg = ''
    # get the value from the from input by name city
    new_city = request.form.get('city')
    if new_city:
        # check if there is a duplicate city name
        dup_city = City.query.filter_by(name=new_city).first()
        if not dup_city:
            # check that city exists
            dup_city_data = get_weather_data(new_city)
            if dup_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                # save new city to database
                db.session.commit()
            else:
                err_msg = 'City does not exist on earth'
        else:
           err_msg = 'Your City is Already Avaiable'

    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('City added successfully') 
    return redirect(url_for('weather_get'))

# get route for reciving the data from database and appending with api
# get by default no need to put method in app.route
@app.route("/weather")
def weather_get():
   
    # query database for all cities within the city table
    cities = City.query.all()

    # create a list to hold all the weather for all the cities
    weather_data = []

    # ilitarate over the city name in databse with for loop
    for city in cities:
        r = get_weather_data(city.name)
        # print(r) print json response to test that api is working correctly

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        # Append city to weather data for weather
        weather_data.append(weather)

    return render_template("weather.html", weather_data=weather_data, title="Weather")


# delete route for removing city from database by name
@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    flash(f'Successfully removed { city.name }', 'success')
    return redirect(url_for('weather_get'))


@app.route("/sports")
def sports():
    #add sources from api
    sports_headlines = newsapi.get_top_headlines(sources='nhl-news')
    #print(sports_headlines)
    sports = sports_headlines['articles']
    desc = []
    aut = []
    news = []
    link = []
    img = []

    # ilitarate over the data in api with for loop
    for i in range(len(sports)):
        mysports = sports[i]

        news.append(mysports['title'])
        aut.append(mysports['author'])
        desc.append(mysports['description'])
        img.append(mysports['urlToImage'])
        link.append(mysports['url'])

        sportslist = zip(news, aut, desc, img, link)

    return render_template("sports.html", context=sportslist, title="Sports")


if __name__ == '__main__':
   app.run(debug=True) 