from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Book, Order, OrderItem
import os

app = Flask(__name__)
# Secret key is required for sessions and flashing messages
app.secret_key = os.urandom(24)

# Database Configuration
# This will create a database.db file in your project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind database to the Flask application
db.init_app(app)

# Automatically create tables if they do not exist
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def index():
    """
    Home Page / Book Catalog
    Person A: Retrieve books from the database.
    Person B: Render index.html with list of books and search query input.
    """
    search_query = request.args.get('search', '')
    
    # Placeholder: Retrieve all books. Person A can expand this for searching.
    books = Book.query.all()
    
    if search_query:
        books = Book.query.filter(Book.title.contains(search_query) | Book.author.contains(search_query)).all()

    return render_template('index.html', books=books, search_query=search_query)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """
    Book Detail Page
    Person A: Retrieve single book by book_id.
    Person B: Design premium details layout.
    """
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Route
    Person A: Capture form inputs, hash password, check duplicate email, insert User in DB.
    Person B: Display elegant form UI and success/error alert banners.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Basic validation placeholder (Person A will enhance)
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
            
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('login.html', form_type='register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Route
    Person A: Verify password hash against database record, store user session data.
    Person B: Display login form, manage redirects.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html', form_type='login')


@app.route('/logout')
def logout():
    """
    Clear login sessions.
    """
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


@app.route('/cart')
def view_cart():
    """
    Shopping Cart Details
    Person A: Retrieve cart contents from session['cart'] (stores product_id: quantity).
    Person B: Style the table and display grand total pricing dynamically.
    """
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for book_id, quantity in cart.items():
        book = Book.query.get(int(book_id))
        if book:
            subtotal = book.price * quantity
            total_price += subtotal
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'subtotal': subtotal
            })
            
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/add-to-cart/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    """
    Add item to session-based cart.
    """
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', 1))
    
    # Convert key to string because Flask session keys must be strings
    book_id_str = str(book_id)
    cart[book_id_str] = cart.get(book_id_str, 0) + quantity
    session['cart'] = cart
    
    flash('Book added to cart!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Convert cart into order history.
    Person A: Create Order and OrderItem records, deduct inventory stock, clear cart.
    Person B: Create checkout form and success receipt page.
    """
    if 'user_id' not in session:
        flash('Please login to place an order.', 'warning')
        return redirect(url_for('login'))
        
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('index'))
        
    # Calculate total and process
    total = 0
    order_items = []
    
    # Start transaction
    for book_id, quantity in cart.items():
        book = Book.query.get(int(book_id))
        if book:
            if book.stock < quantity:
                flash(f'Sorry, only {book.stock} units of {book.title} are in stock.', 'danger')
                return redirect(url_for('view_cart'))
            total += book.price * quantity
            order_items.append((book, quantity))

    # Save to db
    order = Order(user_id=session['user_id'], total_amount=total)
    db.session.add(order)
    db.session.flush() # Gets the generated order.id
    
    for book, quantity in order_items:
        # Deduct stock
        book.stock -= quantity
        # Create item
        item = OrderItem(order_id=order.id, book_id=book.id, quantity=quantity, price=book.price)
        db.session.add(item)
        
    db.session.commit()
    session.pop('cart', None) # Clear cart
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
