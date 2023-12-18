# slug
    from flask import Flask, render_template, request, redirect, url_for
    import sqlite3

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

# Database initialization
    def init_db():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create 'books' table if it doesn't exist
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

    init_db()  # Initialize the database when the app starts

# Helper function to generate a slug
    def generate_slug(author):
       return author.lower().replace(' ', '-')  # Converts author name to a URL-friendly slug

# Create a new book
     @app.route('/add', methods=['POST', 'GET'])
     def add_book():
     if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        slug = generate_slug(author)  # Generate slug from author's name

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insert new book details into the database
        cursor.execute('INSERT INTO books (title, author, slug) VALUES (?, ?, ?)', (title, author, slug))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))  # Redirect to the book list page

    return render_template('add.html')  # Render the add book form

# Read (list) books
    @app.route('/')
    def index():
     conn = sqlite3.connect('database.db')
     cursor = conn.cursor()

    # Fetch all books from the database
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    return render_template('index.html', books=books)  # Render the book list page with fetched books

# Update a book
    @app.route('/edit/<string:slug>', methods=['POST', 'GET'])
    def edit_book(slug):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        # Update book details in the database based on slug
        cursor.execute('UPDATE books SET title=?, author=? WHERE slug=?', (title, author, slug))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))  # Redirect to the book list page after updating

    # Fetch book details for editing
    cursor.execute('SELECT * FROM books WHERE slug=?', (slug,))
    book = cursor.fetchone()
    conn.close()

    return render_template('edit.html', book=book)  # Render the edit book form with book details

# Delete a book
    @app.route('/delete/<string:slug>')
    def delete_book(slug):
     conn = sqlite3.connect('database.db')
     cursor = conn.cursor()

    # Delete a book from the database based on slug
    cursor.execute('DELETE FROM books WHERE slug=?', (slug,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))  # Redirect to the book list page after deletion

    if __name__ == '__main__':
        app.run(debug=True)  # Run the Flask app in debug mode
