import os
from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Connect to MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client["lost_found_db"]

users = db["users"]
items = db["items"]
claims = db["claims"]


@app.route("/")
def home():
    return render_template("index.html")


# Temporary route just to test the database connection
@app.route("")
def test_db():
    client.admin.command("ping")
    result = items.insert_one({
        "name": "Test Wallet",
        "type": "found",
        "status": "active"
    })
    return f"Connected! Inserted item with id: {result.inserted_id}"


if __name__ == "__main__":
    app.run(debug=True)