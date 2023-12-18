from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            slug TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper function to generate a slug
def generate_slug(author):
    return author.lower().replace(' ', '-')

# Create a new book
@app.route('/add', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        slug = generate_slug(author)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, slug) VALUES (?, ?, ?)', (title, author, slug))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add.html')

# Read (list) books
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    return render_template('index.html', books=books)

# Update a book
@app.route('/edit/<string:slug>', methods=['POST', 'GET'])
def edit_book(slug):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        cursor.execute('UPDATE books SET title=?, author=? WHERE slug=?', (title, author, slug))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM books WHERE slug=?', (slug,))
    book = cursor.fetchone()
    conn.close()

    return render_template('edit.html', book=book)

# Delete a book
@app.route('/delete/<string:slug>')
def delete_book(slug):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE slug=?', (slug,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
