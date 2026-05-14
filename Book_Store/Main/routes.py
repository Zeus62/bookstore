from Book_Store.Main import main
from Book_Store.models import Book
from Book_Store import db
from flask import render_template, request


@main.route('/')
@main.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html', title="Home")


@main.route("/about")
def about():
    return render_template('about.html', title="About")


@main.route("/books")
def books():
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    # Base query
    query = Book.query

    # Apply search filter
    if search_query:
        query = query.filter(
            (Book.title.ilike(f'%{search_query}%')) |
            (Book.author.ilike(f'%{search_query}%'))
        )

    # Apply category filter
    if category_filter:
        query = query.filter(Book.category == category_filter)

    # Get filtered books
    all_books = query.all()

    # Get unique categories for filter dropdown
    categories = sorted(set(b.category for b in Book.query.all()))

    return render_template('books.html', books=all_books, categories=categories,
                           current_search=search_query, current_category=category_filter)


@main.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    related_books = Book.query.filter(Book.category == book.category).filter(Book.id != book_id).limit(4).all()
    return render_template('book_detail.html', book=book, related_books=related_books)
