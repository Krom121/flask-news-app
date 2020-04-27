from flask import Flask, render_template, request, flash



@app.route("/")
def index():
    return render_template("index.html", tittle="News Feed")



@app.route("/weather")
def weather():
    return render_template("weather.html", tittle="Weather")


@app.route("/sports")
def sports():
    return render_template("sports.html", tittle="Sports")