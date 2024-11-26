from fastapi import FastAPI, HTTPException
import requests
import sqlite3

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books (
        isbn TEXT PRIMARY KEY,
        title TEXT,
        author TEXT,
        cover_url TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

# Function to fetch book info from Open Library
def fetch_book_info(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    book_key = f"ISBN:{isbn}"
    if book_key in data:
        book_data = data[book_key]
        return {
            "isbn": isbn,
            "title": book_data.get("title", "Unknown"),
            "author": ", ".join([author["name"] for author in book_data.get("authors", [])]),
            "cover_url": book_data.get("cover", {}).get("medium", "")
        }
    return None

# API endpoint to scan and store book
@app.post("/scan")
def scan_book(isbn: str):
    book_info = fetch_book_info(isbn)
    if not book_info:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Save to database
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO books (isbn, title, author, cover_url)
        VALUES (?, ?, ?, ?)
    """, (book_info["isbn"], book_info["title"], book_info["author"], book_info["cover_url"]))
    conn.commit()
    conn.close()
    
    return book_info

# API endpoint to list books
@app.get("/books")
def list_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return [{"isbn": row[0], "title": row[1], "author": row[2], "cover_url": row[3]} for row in books]
