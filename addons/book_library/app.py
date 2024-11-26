
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pyzbar.pyzbar import decode
from PIL import Image
import requests
import os

app = Flask(__name__)
CORS(app)

# Serve the HTML interface
@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/scan', methods=['POST'])
def scan_barcode():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image = Image.open(file)
    decoded_objects = decode(image)
    
    if not decoded_objects:
        return jsonify({"error": "No barcode found"}), 400

    barcode = decoded_objects[0].data.decode("utf-8")

    # Example: Query Google Books API with the barcode (ISBN)
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{barcode}")
    book_data = response.json()

    if 'items' not in book_data:
        return jsonify({"error": "Book not found"}), 404

    book = book_data['items'][0]['volumeInfo']
    return jsonify({
        "title": book.get("title", "Unknown"),
        "authors": book.get("authors", []),
        "publisher": book.get("publisher", "Unknown"),
        "publishedDate": book.get("publishedDate", "Unknown")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
