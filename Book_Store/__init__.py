from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bookstore_secret_key_2025'
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Use DATABASE_URI from environment variables if running in Docker, else fallback to a default local MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI',
    'mysql+pymysql://root:bookstore2025@localhost:3306/BookStore'
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def init_db():
    from Book_Store.models import Book
    with app.app_context():
        db.create_all()

        if Book.query.count() == 0:
            books = [
                Book(title="The Great Gatsby", author="F. Scott Fitzgerald", description="A story of the fabulously wealthy Jay Gatsby and his love for Daisy Buchanan.", price=12.99, category="Fiction"),
                Book(title="To Kill a Mockingbird", author="Harper Lee", description="A novel about racial injustice in the Deep South through the eyes of a child.", price=14.99, category="Fiction"),
                Book(title="1984", author="George Orwell", description="A dystopian novel set in a totalitarian society under constant surveillance.", price=11.99, category="Science Fiction"),
                Book(title="Pride and Prejudice", author="Jane Austen", description="A romantic novel about the Bennet family and the proud Mr. Darcy.", price=10.99, category="Romance"),
                Book(title="The Catcher in the Rye", author="J.D. Salinger", description="A story about teenage rebellion and alienation in 1950s America.", price=13.99, category="Fiction"),
                Book(title="Harry Potter", author="J.K. Rowling", description="A young wizard discovers his magical heritage and attends Hogwarts.", price=15.99, category="Fantasy"),
                Book(title="The Lord of the Rings", author="J.R.R. Tolkien", description="An epic fantasy adventure to destroy the One Ring and save Middle-earth.", price=19.99, category="Fantasy"),
                Book(title="The Alchemist", author="Paulo Coelho", description="A shepherd boy travels from Spain to Egypt in search of treasure.", price=12.49, category="Philosophy"),
            ]
            db.session.add_all(books)
            db.session.commit()


# Initialize database
init_db()


from Book_Store.Main.routes import main
from Book_Store.users.routes import users
from Book_Store.reviews.routes import reviews_bp
from Book_Store.shop.routes import shop

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(reviews_bp)
app.register_blueprint(shop)

# Delay user loader to break circular dependency
def set_user_loader():
    from Book_Store.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

set_user_loader()
