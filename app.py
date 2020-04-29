import requests
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient


app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

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

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        aut.append(myarticles['author'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        link.append(myarticles['url'])

    mylist = zip(news, aut, desc, img, link)

    return render_template("index.html", context=mylist, title="News Feed")



@app.route("/weather")
def weather():

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6560b436a15d6c73ed06592ef82af38a'
    city = 'Edinburgh'
    r = requests.get(url.format(city)).json()
    # print(r) print json response to test that api is working correctly

    weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    

    return render_template("weather.html", weather=weather, title="Weather")


@app.route("/sports")
def sports():
    return render_template("sports.html", title="Sports")


if __name__ == '__main__':
   app.run(debug=True) 