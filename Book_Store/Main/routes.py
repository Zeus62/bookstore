from Book_Store.Main import main
from Book_Store.models import Book
from Book_Store import db
from flask import render_template, request, session, redirect, url_for


@main.route('/')
@main.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html', title="Home")


@main.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ar', 'fr', 'de']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.home'))



@main.route("/books")
def books():
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    # Start with all books
    all_books = Book.query.all()

    # Apply category filter first (DB-level match)
    if category_filter:
        all_books = [b for b in all_books if b.category == category_filter]

    # Apply search filter with translation support
    if search_query:
        from flask_babel import gettext
        search_lower = search_query.lower()
        results = []
        for b in all_books:
            # Search in original English fields
            if (search_lower in b.title.lower() or
                search_lower in b.author.lower() or
                (b.description and search_lower in b.description.lower())):
                results.append(b)
                continue
            # Search in translated fields
            translated_title = gettext(b.title).lower()
            translated_desc = gettext(b.description).lower() if b.description else ""
            if search_lower in translated_title or search_lower in translated_desc:
                results.append(b)
        all_books = results

    # Get ALL categories for the dropdown (not filtered)
    categories = sorted(set(b.category for b in Book.query.all()))

    return render_template('books.html', books=all_books, categories=categories,
                           current_search=search_query, current_category=category_filter)


@main.route('/book/<int:book_id>')
def book_detail(book_id):
    from Book_Store.reviews.forms import ReviewForm
    book = Book.query.get_or_404(book_id)
    related_books = Book.query.filter(Book.category == book.category).filter(Book.id != book_id).limit(4).all()
    form = ReviewForm()
    return render_template('book_detail.html', book=book, related_books=related_books, form=form)
