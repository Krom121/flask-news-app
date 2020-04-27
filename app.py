from flask import Flask, render_template, request, flash
from newsapi import NewsApiClient


app = Flask(__name__)


@app.route("/")
def index():
    # Init api
    newsapi = NewsApiClient(api_key='b855866438b64269ba90a58a73b28673')
    
    top_headlines = newsapi.get_top_headlines(sources='bbc-news')

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
    return render_template("weather.html", title="Weather")


@app.route("/sports")
def sports():
    return render_template("sports.html", title="Sports")


if __name__ == '__main__':
   app.run(debug=True) 