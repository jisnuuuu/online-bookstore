from app import app
from models import db, Book

def seed_database():
    books = [
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre="Classics",
            price=12.49,
            stock=8,
            image_url="https://covers.openlibrary.org/b/id/14817209-L.jpg",
            description="The Pulitzer Prize-winning masterpiece about a Southern lawyer defending a Black man accused of a crime he did not commit."
        ),
        Book(
            title="1984",
            author="George Orwell",
            genre="Dystopian",
            price=10.99,
            stock=22,
            image_url="https://covers.openlibrary.org/b/id/12693610-L.jpg",
            description="A dystopian novel about totalitarianism, mass surveillance, and repressive regimentation of persons and behaviors within society."
        ),
        Book(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre="Fantasy",
            price=14.99,
            stock=5,
            image_url="https://covers.openlibrary.org/b/id/15223072-L.jpg",
            description="A classic fantasy novel following the quest of home-loving hobbit Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon."
        ),
        Book(
            title="Atomic Habits",
            author="James Clear",
            genre="Self-Help",
            price=16.99,
            stock=30,
            image_url="https://m.media-amazon.com/images/I/81wgcld4wxL._AC_UF1000,1000_QL80_.jpg",
            description="Tiny Changes, Remarkable Results. An easy and proven way to build good habits and break bad ones."
        ),
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            genre="Fiction",
            price=10.99,
            stock=20,
            image_url="https://covers.openlibrary.org/b/id/14635758-L.jpg",
            description="The exemplary novel of the Jazz Age, capturing the glamour, opulence, and ultimate disillusionment of the American Dream."
        ),
        Book(
            title="Sapiens",
            author="Yuval Noah Harari",
            genre="History",
            price=19.99,
            stock=25,
            image_url="https://covers.openlibrary.org/b/id/8284312-L.jpg",
            description="A groundbreaking narrative of humanity's creation and evolution that explores how biology and history have defined us."
        ),
        Book(
            title="Dune",
            author="Frank Herbert",
            genre="Sci-Fi",
            price=15.99,
            stock=12,
            image_url="https://m.media-amazon.com/images/I/81ym3QUd3KL._AC_UF1000,1000_QL80_.jpg",
            description="A stunning blend of adventure, mysticism, environmentalism, and politics, set on the dangerous desert planet Arrakis."
        ),
        Book(
            title="Pride and Prejudice",
            author="Jane Austen",
            genre="Romance",
            price=9.99,
            stock=22,
            image_url="https://covers.openlibrary.org/b/id/8090214-L.jpg",
            description="A romantic comedy of manners detailing the emotional development of Elizabeth Bennet as she learns the error of hasty judgments."
        ),
        Book(
            title="Educated",
            author="Tara Westover",
            genre="Biography",
            price=14.95,
            stock=14,
            image_url="https://covers.openlibrary.org/b/id/15216613-L.jpg",
            description="An unforgettable memoir about a young girl who leaves her survivalist family in rural Idaho to earn a PhD from Cambridge University."
        ),
        Book(
            title="Deep Work",
            author="Cal Newport",
            genre="Self-Help",
            price=16.00,
            stock=35,
            image_url="https://covers.openlibrary.org/b/id/15150797-L.jpg",
            description="Rules for focused success in a distracted world, presenting a rigorous training regimen to transform your mind and habits."
        ),
        Book(
            title="The Catcher in the Rye",
            author="J.D. Salinger",
            genre="Fiction",
            price=11.99,
            stock=10,
            image_url="https://covers.openlibrary.org/b/id/15172466-L.jpg",
            description="The classic novel of teenage angst and alienation, tracking a few days in the life of sixteen-year-old Holden Caulfield."
        ),
        Book(
            title="The Alchemist",
            author="Paulo Coelho",
            genre="Fiction",
            price=13.50,
            stock=30,
            image_url="https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1654371463i/18144590.jpg",
            description="A magical story about Santiago, an Andalusian shepherd boy who travels in search of a worldly treasure, finding something deeper."
        )
    ]
    
    if Book.query.first() is None:
        db.session.bulk_save_objects(books)
        db.session.commit()
        print("Database successfully seeded with 12 books!")
    else:
        print("Database already contains books. Skipping seeding.")

if __name__ == '__main__':
    with app.app_context():
        seed_database()
