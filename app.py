from Book_Store import app, init_db

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=3000, ssl_context='adhoc')