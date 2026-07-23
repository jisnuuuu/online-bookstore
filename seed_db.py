from app import app
from models import db, Book

def seed_database():
    books = [
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre="Classics",
            price=499.00,
            stock=8,
            image_url="https://covers.openlibrary.org/b/id/14817209-L.jpg",
            description="The Pulitzer Prize-winning masterpiece about a Southern lawyer defending a Black man accused of a crime he did not commit.Set in the racially divided American South during the Great Depression, this novel is narrated by young Scout Finch. Her father, Atticus Finch, is a principled lawyer who bravely defends a Black man falsely accused of a crime. The story explores themes of empathy, racial injustice, and the loss of innocence."
        ),
        Book(
            title="1984",
            author="George Orwell",
            genre="Dystopian",
            price=449.00,
            stock=22,
            image_url="https://covers.openlibrary.org/b/id/12693610-L.jpg",
            description="A dystopian novel about totalitarianism, mass surveillance, and repressive regimentation of persons and behaviors within society.A seminal dystopian novel set in a totalitarian superstate ruled by the omnipresent 'Big Brother'. The story follows Winston Smith, a low-ranking party member who dares to express independent thought and forbidden love, ultimately leading him into a terrifying struggle against a government that seeks to control reality, memory, and truth"
        ),
        Book(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre="Fantasy",
            price=599.00,
            stock=5,
            image_url="https://covers.openlibrary.org/b/id/15223072-L.jpg",
            description="A classic fantasy novel following the quest of home-loving hobbit Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon.A beloved fantasy precursor to The Lord of the Rings, this book follows Bilbo Baggins, an unassuming, home-loving hobbit who is unexpectedly whisked away on an adventure by the wizard Gandalf and a company of dwarves. Together, they journey across treacherous lands to reclaim a lost kingdom and its treasure from the fearsome dragon, Smaug."
        ),
        Book(
            title="Atomic Habits",
            author="James Clear",
            genre="Self-Help",
            price=699.00,
            stock=30,
            image_url="https://m.media-amazon.com/images/I/81wgcld4wxL._AC_UF1000,1000_QL80_.jpg",
            description="Tiny Changes, Remarkable Results. An easy and proven way to build good habits and break bad ones.Atomic Habits by James Clear is a practical guide on how tiny, daily improvements compound into massive, life-altering results. Instead of focusing on massive goals, it teaches you to build robust systems using the 'Four Laws of Behavior Change' to effortlessly adopt good habits and shed destructive ones."
        ),
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            genre="Fiction",
            price=399.00,
            stock=20,
            image_url="https://covers.openlibrary.org/b/id/14635758-L.jpg",
            description="The exemplary novel of the Jazz Age, capturing the glamour, opulence, and ultimate disillusionment of the American Dream.Set in the decadent 'Jazz Age' of the 1920s, this tragic novel is narrated by Nick Carraway, who moves next door to the enigmatic, self-made millionaire Jay Gatsby. The story uncovers Gatsby's lavish lifestyle and his obsessive, tragic pursuit of his former lover, Daisy Buchanan, exploring themes of love, greed, and the illusion of the American Dream."
        ),
        Book(
            title="Sapiens",
            author="Yuval Noah Harari",
            genre="History",
            price=599.00,
            stock=25,
            image_url="https://covers.openlibrary.org/b/id/8284312-L.jpg",
            description="A groundbreaking narrative of humanity's creation and evolution that explores how biology and history have defined us. This sweeping non-fiction book spans the entirety of human history, from the Stone Age to the modern day. Blending the natural and social sciences, the book explores how Homo sapiens evolved from an insignificant animal into the ruler of the Earth, driven by monumental developments like the Cognitive and Agricultural Revolutions."
        ),
        Book(
            title="Dune",
            author="Frank Herbert",
            genre="Sci-Fi",
            price=449.00,
            stock=12,
            image_url="https://m.media-amazon.com/images/I/81ym3QUd3KL._AC_UF1000,1000_QL80_.jpg",
            description="A stunning blend of adventure, mysticism, environmentalism, and politics, set on the dangerous desert planet Arrakis.Set in the far future, this epic sci-fi masterwork is centered on Arrakis, an inhospitable desert planet and the universe's only source of 'melange' (spice)—a drug vital for interstellar travel. The story follows young Paul Atreides as his noble family is betrayed, forcing him into the desert where he aligns with the indigenous Fremen to reclaim his destiny."
        ),
        Book(
            title="Pride and Prejudice",
            author="Jane Austen",
            genre="Romance",
            price=299.00,
            stock=22,
            image_url="https://covers.openlibrary.org/b/id/8090214-L.jpg",
            description="A romantic comedy of manners detailing the emotional development of Elizabeth Bennet as she learns the error of hasty judgments. First published in 1813, this beloved romantic comedy follows the quick-witted Elizabeth Bennet as she navigates issues of manners, marriage, and social standing in 19th-century England. The story centers on her tumultuous relationship with the wealthy and haughty Mr. Darcy, as both must overcome their biases to find true love."
        ),
        Book(
            title="Deep Work",
            author="Cal Newport",
            genre="Self-Help",
            price=349.00,
            stock=35,
            image_url="https://covers.openlibrary.org/b/id/15150797-L.jpg",
            description="Rules for focused success in a distracted world, presenting a rigorous training regimen to transform your mind and habits. A productivity and self-help book that defines 'deep work' as the ability to focus without distraction on a cognitively demanding task. Cal Newport argues that this ability is a dying superpower in the modern, distracted age and provides a rigorous training regimen to help readers eliminate digital noise and improve concentration."
        ),
        Book(
            title="The Catcher in the Rye",
            author="J.D. Salinger",
            genre="Fiction",
            price=299.00,
            stock=10,
            image_url="https://covers.openlibrary.org/b/id/15172466-L.jpg",
            description="The classic novel of teenage angst and alienation, tracking a few days in the life of sixteen-year-old Holden Caulfield. This classic coming-of-age novel is narrated by Holden Caulfield, a disillusioned, rebellious 16-year-old who has just been expelled from his prep school. Wandering through New York City, Holden struggles with the 'phoniness' of the adult world and attempts to hold onto the innocence of childhood"
        ),
        Book(
            title="The Alchemist",
            author="Paulo Coelho",
            genre="Fiction",
            price=249.00,
            stock=30,
            image_url="https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1654371463i/18144590.jpg",
            description="A magical story about Santiago, an Andalusian shepherd boy who travels in search of a worldly treasure, finding something deeper."
            "The Alchemist by Paulo Coelho is a celebrated modern fable that follows Santiago, an Andalusian shepherd boy who leaves Spain to seek a hidden treasure at the Egyptian pyramids."
        ),
    ]
    
    if Book.query.first() is None:
        db.session.bulk_save_objects(books)
        db.session.commit()
        print(f"Database successfully seeded with {len(books)} books!")
    else:
        print("Database already contains books. Skipping seeding.")

if __name__ == '__main__':
    with app.app_context():
        seed_database()
