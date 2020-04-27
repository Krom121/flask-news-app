from flask import Flask, render_template, request, flash

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title="News Feed")



@app.route("/weather")
def weather():
    return render_template("weather.html", title="Weather")


@app.route("/sports")
def sports():
    return render_template("sports.html", title="Sports")


if __name__ == '__main__':
   app.run(debug=True) 