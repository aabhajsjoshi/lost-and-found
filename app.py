import os
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
import uuid
from azure.storage.blob import BlobServiceClient, ContentSettings

load_dotenv()  # reads your .env file

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Connect to MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client["lost_found_db"]

users = db["users"]
items = db["items"]
claims = db["claims"]

# Limit uploads to 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# Connect to Azure Blob Storage
blob_service = BlobServiceClient.from_connection_string(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)
container_client = blob_service.get_container_client("item-images")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def upload_image(file):
    """Uploads a photo to Azure and returns its link.
    Returns "" if no photo was chosen, and None if the file type isn't allowed."""
    if not file or file.filename == "":
        return ""

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        return None

    # Random file name so two people uploading "photo.jpg" don't overwrite each other
    blob_name = f"{uuid.uuid4().hex}.{ext}"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(
        file.stream,
        content_settings=ContentSettings(content_type=file.content_type),
    )
    return blob_client.url

CATEGORIES = ["Wallet", "Phone", "ID Card", "Bag", "Keys", "Electronics", "Clothing", "Other"]

# Which status changes are allowed (current status -> allowed next statuses)
NEXT_STATUS = {
    "pending": ["approved", "rejected"],
    "approved": ["returned"],
}

@app.route("/")
def home():
    # Read what the user typed or picked (from the URL)
    q = request.args.get("q", "").strip()
    item_type = request.args.get("type", "")
    category = request.args.get("category", "")

    # Build the search: only active items, plus any filters the user chose
    query = {"status": "active"}

    if q:
        # re.escape makes special characters safe; "i" means ignore capital letters
        query["name"] = {"$regex": re.escape(q), "$options": "i"}
    if item_type in ("lost", "found"):
        query["type"] = item_type
    if category:
        query["category"] = category

    # Newest first
    results = list(items.find(query).sort("created_at", -1))

    return render_template(
        "index.html",
        items=results,
        q=q,
        selected_type=item_type,
        selected_category=category,
        categories=CATEGORIES,
    )


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

                # Upload the photo (if there is one)
        try:
            image_url = upload_image(request.files.get("photo"))
        except Exception:
            flash("Photo upload failed. Please try again.")
            return redirect(url_for("report"))

        if image_url is None:
            flash("Only PNG, JPG, GIF or WEBP photos are allowed.")
            return redirect(url_for("report"))

        items.insert_one({
            "name": name,
            "type": item_type,
            "category": category,
            "description": description,
            "location": location,
            "date": date,
            "image_url": image_url,      # filled in on Day 2 with Azure Blob Storage
            "status": "active",
            "created_at": datetime.utcnow()
        })

        flash("Your report was submitted!")
        return redirect(url_for("report"))

    return render_template("report.html")

@app.route("/item/<item_id>")
def item_detail(item_id):
    try:
        item = items.find_one({"_id": ObjectId(item_id)})
    except InvalidId:
        item = None  # the id in the address wasn't a real id

    if item is None:
        return render_template("item.html", item=None), 404

    return render_template("item.html", item=item)

@app.route("/item/<item_id>/claim", methods=["GET", "POST"])
def claim_item(item_id):
    try:
        item = items.find_one({"_id": ObjectId(item_id)})
    except InvalidId:
        item = None

    # Only active items can be claimed
    if item is None or item["status"] != "active":
        return render_template("item.html", item=None), 404

    if request.method == "POST":
        name = request.form.get("claimant", "").strip()
        contact = request.form.get("contact", "").strip()
        reason = request.form.get("reason", "").strip()

        if not name or not contact or not reason:
            flash("Please fill in all the fields.")
            return redirect(url_for("claim_item", item_id=item_id))

        claims.insert_one({
            "item_id": item["_id"],
            "claimant": name,
            "contact": contact,
            "reason": reason,
            "status": "pending",
            "created_at": datetime.utcnow()
        })

        flash("Your claim was submitted! The finder or admin will review it.")
        return redirect(url_for("item_detail", item_id=item_id))

    return render_template("claim.html", item=item)


@app.route("/admin/claims")
def admin_claims():
    all_claims = list(claims.find().sort("created_at", -1))
    for c in all_claims:
        c["item"] = items.find_one({"_id": c["item_id"]})  # attach the item so we can show its name
    return render_template("admin_claims.html", claims=all_claims)


@app.route("/admin/claims/<claim_id>/status", methods=["POST"])
def update_claim_status(claim_id):
    new_status = request.form.get("status")

    try:
        claim = claims.find_one({"_id": ObjectId(claim_id)})
    except InvalidId:
        claim = None

    if claim is None:
        flash("Claim not found.")
        return redirect(url_for("admin_claims"))

    # Only allow the changes listed in NEXT_STATUS
    if new_status not in NEXT_STATUS.get(claim["status"], []):
        flash("That status change isn't allowed.")
        return redirect(url_for("admin_claims"))

    claims.update_one({"_id": claim["_id"]}, {"$set": {"status": new_status}})

    # When the item is handed back, take it off the homepage
    if new_status == "returned":
        items.update_one({"_id": claim["item_id"]}, {"$set": {"status": "returned"}})

    flash(f"Claim marked as {new_status}.")
    return redirect(url_for("admin_claims"))

if __name__ == "__main__":
    app.run(debug=True)