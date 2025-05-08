# FastAPI?
FastAPI is a modern and fast (high-performance) Python web framework used to build REST APIs.

The name says it all:

Fast: It works very quickly (uses Python's async features).

API: Application Programming Interface – a way for apps or users to interact with software or systems.

## What Can You Do with FastAPI?
### If you're using Python and want to:

Build web applications

Create backend APIs

Show AI/ML model results on a web page (like taking input from a form and showing model output)
Then FastAPI is a great tool!

## Key Features of FastAPI:
✅ Async support – Gives fast responses using async/await
✅ Type hints – Uses Python's type system for automatic data checks
✅ Auto documentation – Creates docs using Swagger UI and ReDoc automatically
✅ Easy to learn – Feels like Flask, but with modern features

##Example Code (Small “Hello World” API):

## Step 1:
Create a Project Folder and Set Up a Virtual Environment
🔧 First, make a project folder:
```
uv init fastdca-p1
cd fastdca-p1
```
👉 This command creates a new folder named fastdca-p1 and goes inside it.

## Step 2: 
Create and Activate a Virtual Environment
Windows:
```
uv venv
.venv\Scripts\activate
```
👉 This creates a virtual environment where only the libraries for this project will be installed.

## Step 3: 
Install Required Libraries
```
uv add "fastapi[standard]"
```
## This installs:

-fastapi: API framework

-uvicorn: For running the server

-httpx: For testing

## Step 4:
Create a "Hello World" API
Create the file:``` main.py ```
And write this code in it:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

```
### To Understand:
@app.get("/"):
When someone opens / in the browser, it will return:
{"Hello": "World"}

@app.get("/items/{item_id}"):
When someone opens /items/10 (or any number), it will return the item ID in the response.
If there's an extra query string like ?q=abc, that will also be included in the response.


