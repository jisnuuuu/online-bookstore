from app import app
from models import db, Book

def seed_database():
    books = [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            genre="Fiction",
            price=399.00,
            stock=15,
            image_url="https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=500&auto=format&fit=crop&q=60",
            description="The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan, set in the roaring twenties."
        ),
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre="Classics",
            price=499.00,
            stock=8,
            image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500&auto=format&fit=crop&q=60",
            description="The Pulitzer Prize-winning masterpiece about a Southern lawyer defending a Black man accused of a crime he did not commit."
        ),
        Book(
            title="1984",
            author="George Orwell",
            genre="Dystopian",
            price=449.00,
            stock=22,
            image_url="https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500&auto=format&fit=crop&q=60",
            description="A dystopian novel about totalitarianism, mass surveillance, and repressive regimentation of persons and behaviors within society."
        ),
        Book(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre="Fantasy",
            price=599.00,
            stock=5,
            image_url="https://images.unsplash.com/photo-1618666012174-83b441c0bc76?w=500&auto=format&fit=crop&q=60",
            description="A classic fantasy novel following the quest of home-loving hobbit Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon."
        ),
        Book(
            title="Atomic Habits",
            author="James Clear",
            genre="Self-Help",
            price=699.00,
            stock=30,
            image_url="https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500&auto=format&fit=crop&q=60",
            description="Tiny Changes, Remarkable Results. An easy and proven way to build good habits and break bad ones."
        )
    ]
    
    # Check if books already exist to prevent duplicate seeding
    if Book.query.first() is None:
        db.session.bulk_save_objects(books)
        db.session.commit()
        print("Database successfully seeded with 5 books!")
    else:
        print("Database already contains books. Skipping seeding.")

if __name__ == '__main__':
    with app.app_context():
        seed_database()
