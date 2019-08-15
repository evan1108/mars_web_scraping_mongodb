from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_app = mongo.db.mars_app.find_one()
    return render_template('index.html', mars_dict=mars_app)


@app.route("/scrape")
def scrape():
    mars_app = mongo.db.mars_app
    mars_data = scrape_mars.scrape()
    mars_app.update({}, mars_data, upsert=True)
# after scrape.py fixes, look at return statement
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

