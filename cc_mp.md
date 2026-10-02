Yep. Since you only have **2 days**, the goal is:

> **Working project → deployed on Azure → MongoDB Atlas connected → Azure Blob Storage working → screenshots/demo → report/viva ready.**

We're going to deliberately avoid anything that can derail us.

# 🚨 Project: Cloud-Based Lost & Found System

### Final architecture

```text
                 USER
                  │
                  ▼
        ┌──────────────────┐
        │   Azure Cloud    │
        │                  │
        │ Flask Application │
        └────────┬─────────┘
                 │
        ┌────────┴─────────┐
        ▼                  ▼
 MongoDB Atlas       Azure Blob Storage
     │                     │
     │                     │
 User data            Item images
 Lost items
 Found items
 Claims
```

**Cloud services:**

1. **Azure App Service** → hosts Flask
2. **MongoDB Atlas** → cloud database
3. **Azure Blob Storage** → cloud image storage

---

# 🟦 DAY 1 — BUILD EVERYTHING LOCALLY

## ⏰ Part 1 — Project setup

**~1 hour**

Create:

```text
lost-and-found/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── report.html
│   ├── item.html
│   └── login.html
│
└── static/
    ├── style.css
    └── script.js
```

Install:

```text
Python
Flask
PyMongo
python-dotenv
```

Get a basic Flask page running.

### Milestone 1

Open:

```text
http://127.0.0.1:5000
```

and see:

> **Lost & Found Portal**

If this doesn't work, **we stop here and fix it before moving on.**

---

# ⏰ Part 2 — MongoDB Atlas

**~1–1.5 hours**

Create the MongoDB Atlas database.

We'll have a database such as:

```text
lost_found_db
```

with collections:

```text
users
items
claims
```

### `items`

Something like:

```text
{
    name: "Black Wallet",
    type: "lost",
    category: "Wallet",
    description: "...",
    location: "CSE Block",
    date: "...",
    image_url: "...",
    status: "active"
}
```

### `claims`

```text
{
    item_id: "...",
    claimant: "...",
    reason: "...",
    status: "pending"
}
```

Connect Flask → MongoDB Atlas.

### Milestone 2

Submit an item through your Flask website and see it appear in MongoDB Atlas.

---

# ⏰ Part 3 — Report Lost/Found

**~2 hours**

Build one form that can handle both:

### Lost

```text
Report Type: LOST

Item name
Category
Description
Location
Date
Photo
```

### Found

```text
Report Type: FOUND

Item name
Category
Description
Location
Date
Photo
```

When submitted:

```text
HTML form
    ↓
Flask
    ↓
MongoDB
```

Don't worry about image uploads yet.

### Milestone 3

You can create:

> Lost iPhone

and

> Found Wallet

and both appear in your database.

---

# ⏰ Part 4 — Homepage + Search

**~2 hours**

Homepage:

```text
---------------------------------------
        CAMPUS LOST & FOUND
---------------------------------------

[ Search items... ]

[Lost] [Found]

---------------------------------------

Black Wallet
FOUND
CSE Block

---------------------------------------

Blue Backpack
LOST
Library

---------------------------------------
```

Implement:

* Display all active items
* Search by item name
* Filter Lost/Found
* Filter category

Keep the UI simple.

**Don't spend 3 hours making it pretty.**

---

# ⏰ Part 5 — Item details

**~1 hour**

Click an item:

```text
Black Wallet

Category: Wallet
Location: CSE Block
Date: 30 Sept 2026

Description:
Black leather wallet...

[ CLAIM ITEM ]
```

This gives us a proper user flow.

---

# ⏰ Part 6 — Claim system

**~1.5 hours**

When someone clicks:

> **Claim Item**

show:

```text
Why do you think this item belongs to you?

[________________________]

       [Submit Claim]
```

Store it in MongoDB.

Status:

```text
PENDING
```

Then provide a basic way to change:

```text
PENDING
   ↓
APPROVED
   ↓
RETURNED
```

or

```text
PENDING
   ↓
REJECTED
```

### 🎯 END OF DAY 1 TARGET

You should have:

```text
✅ Flask application
✅ MongoDB Atlas
✅ Report lost item
✅ Report found item
✅ Search
✅ Filters
✅ Item details
✅ Claim system
✅ Status system
```

And everything works **locally**.

---

# 🟩 DAY 2 — CLOUD + DEPLOYMENT

This is where we stop developing major features.

## ⏰ Part 7 — GitHub

**~30 minutes**

Create repository:

```text
lost-and-found
```

Push the working project.

Make sure `.env` is in `.gitignore`.

**VERY IMPORTANT:**

Never upload your MongoDB connection string/password to GitHub.

---

# ⏰ Part 8 — Azure account

**~30–45 minutes**

Set up your Azure student/free access.

Then create the resources needed for deployment.

Our main target:

> **Azure App Service**

This will run:

```text
Flask application
```

on the internet.

---

# ⏰ Part 9 — Azure Blob Storage

**~1 hour**

Create:

```text
Storage Account
       ↓
Blob Container
       ↓
item-images/
```

Now change our upload flow:

```text
User uploads image
       ↓
Flask
       ↓
Azure Blob Storage
       ↓
Image URL
       ↓
MongoDB
```

MongoDB stores the **URL**, not the actual image.

Example:

```text
item:
    name = "Black Wallet"
    image_url = "https://...."
```

### Milestone 4

Upload an image and confirm:

**Azure Blob Storage → image exists**

**MongoDB → image URL exists**

---

# ⏰ Part 10 — Deploy Flask to Azure

**~2 hours**

Deploy the GitHub project to:

> **Azure App Service**

Configure environment variables such as:

```text
MONGO_URI
SECRET_KEY
AZURE_STORAGE_CONNECTION_STRING
```

Then test the public Azure URL.

### Milestone 5 🎉

You can open:

```text
https://your-project.azurewebsites.net
```

and see your Lost & Found website.

---

# ⏰ Part 11 — Connect everything

**~1 hour**

Test the **actual cloud flow**:

```text
Browser
   ↓
Azure Flask
   ↓
MongoDB Atlas
```

and:

```text
Browser
   ↓
Azure Flask
   ↓
Azure Blob Storage
```

Test:

### Test 1

Report lost item.

→ MongoDB contains it.

### Test 2

Report found item + image.

→ Image appears in Blob Storage.

→ MongoDB contains image URL.

### Test 3

Search item.

→ Correct item appears.

### Test 4

Claim item.

→ Claim appears in MongoDB.

---

# ⏰ Part 12 — UI cleanup

**~1 hour MAX**

Only now make it look decent.

Add:

* Navigation bar
* Cards
* Buttons
* Consistent spacing
* Status badges
* Simple responsive layout

Don't fall into:

> "Oooo I can redesign the whole website."

💀

You have a deadline.

---

# 🟨 FINAL 2–3 HOURS — PROJECT SUBMISSION

This is important.

## 📸 Take screenshots

Get screenshots of:

### 1. Homepage

```text
Lost & Found portal
```

### 2. Report form

### 3. Lost/found items

### 4. Item details

### 5. Claim form

### 6. MongoDB Atlas

Show your collections/data.

### 7. Azure

Show your deployed App Service.

### 8. Azure Blob Storage

Show uploaded images.

### 9. Final deployed website

This is especially important.

---

# 📊 Architecture diagram

Your final diagram can be:

```text
                         USER
                          │
                          ▼
                ┌──────────────────┐
                │   Azure App      │
                │    Service       │
                │                  │
                │ Flask + HTML/CSS │
                │      + JS        │
                └────────┬─────────┘
                         │
                 ┌───────┴────────┐
                 │                │
                 ▼                ▼
          ┌─────────────┐  ┌──────────────┐
          │  MongoDB    │  │ Azure Blob   │
          │    Atlas    │  │   Storage    │
          │             │  │              │
          │ Users       │  │ Item images  │
          │ Items       │  │              │
          │ Claims      │  │              │
          └─────────────┘  └──────────────┘
```

This will make your **"two cloud services" requirement extremely obvious.**

---

# 🎤 Viva preparation

You should be able to answer these:

### Why Flask?

> Flask is a lightweight Python web framework used to build the backend and API of our application.

### Why MongoDB?

> MongoDB is a NoSQL database that stores data in flexible JSON-like documents.

### Why MongoDB Atlas?

> MongoDB Atlas is the cloud-hosted version of MongoDB, so our database can be accessed by the deployed application.

### Why Azure?

> Azure provides the cloud infrastructure for deploying and running our web application.

### Why Blob Storage?

> Images are better stored as files in object storage rather than directly inside the database. We store their URLs in MongoDB.

### What happens when a user reports an item?

> The frontend sends the form data to Flask. Flask stores the item information in MongoDB and uploads the image to Azure Blob Storage. The image URL is then associated with the item.

### Why use two cloud services?

> They perform different roles: Azure hosts the application, while MongoDB Atlas provides the cloud database. Azure Blob Storage additionally handles image files.

---

# 🚨 Scope freeze

This is **VERY important** for your two-day deadline.

### MUST HAVE

```text
🟢 Flask
🟢 MongoDB Atlas
🟢 Azure deployment
🟢 Azure Blob Storage
🟢 Lost reports
🟢 Found reports
🟢 Search/filter
🟢 Item details
🟢 Claims
🟢 Basic status
```

### ONLY IF EVERYTHING ABOVE WORKS

```text
🟡 Login
🟡 Admin dashboard
🟡 Better UI
🟡 Email notifications
```

### DO NOT TOUCH

```text
🔴 AI image matching
🔴 Maps
🔴 React
🔴 Docker
🔴 Microservices
🔴 Real-time chat
🔴 Recommendation system
```

---

## The key strategy

**Don't spend Day 1 trying to make a cloud application.**

Make a **working Flask + MongoDB application first**.

Then Day 2:

> **"Take the thing that already works → put it on Azure → add Blob Storage."**

That is much safer than trying to learn Flask, MongoDB, Azure, and Blob Storage simultaneously.

And because you said you're short on time, I'd recommend we work **step-by-step rather than planning the entire implementation at once**. Start with **Part 1: Flask project setup**, get that working, then move to MongoDB.
