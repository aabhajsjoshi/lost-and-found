import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
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
#@app.route("/test-db")
#def test_db():
#    client.admin.command("ping")
#    result = items.insert_one({
#        "name": "Test Wallet",
#        "type": "found",
#        "status": "active"
#    })
#    return f"Connected! Inserted item with id: {result.inserted_id}"

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        item_type = request.form.get("type")
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        date = request.form.get("date", "").strip()

        # Basic checks so we don't save empty or broken reports
        if item_type not in ("lost", "found") or not name or not location:
            flash("Please fill in all the required fields.")
            return redirect(url_for("report"))

        items.insert_one({
            "name": name,
            "type": item_type,
            "category": category,
            "description": description,
            "location": location,
            "date": date,
            "image_url": "",      # filled in on Day 2 with Azure Blob Storage
            "status": "active",
            "created_at": datetime.utcnow()
        })

        flash("Your report was submitted!")
        return redirect(url_for("report"))

    return render_template("report.html")

if __name__ == "__main__":
    app.run(debug=True)