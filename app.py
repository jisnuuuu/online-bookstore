from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Book, Order, OrderItem, CartItem, WishlistItem
import os

app = Flask(__name__)
# Secret key is required for sessions and flashing messages
app.secret_key = os.urandom(24)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind database to the Flask application
db.init_app(app)

# Automatically create tables if they do not exist
with app.app_context():
    db.create_all()

# Category Icon Mapping Helper
GENRE_ICONS = {
    'Classics': 'fa-scroll',
    'Dystopian': 'fa-eye',
    'Fantasy': 'fa-wand-magic-sparkles',
    'Self-Help': 'fa-lightbulb',
    'Fiction': 'fa-book-open-reader',
    'History': 'fa-landmark',
    'Sci-Fi': 'fa-rocket',
    'Romance': 'fa-heart',
    'Biography': 'fa-user-tie',
}

@app.context_processor
def inject_global_data():
    """Inject categories, cart counts, wishlist counts, and user wishlist IDs across all templates."""
    genre_counts = db.session.query(Book.genre, db.func.count(Book.id))\
        .filter(Book.genre.isnot(None))\
        .group_by(Book.genre)\
        .all()
    categories = []
    total_books = db.session.query(Book).count()
    for genre, count in sorted(genre_counts, key=lambda x: x[0] or ''):
        if genre:
            categories.append({
                'name': genre,
                'count': count,
                'icon': GENRE_ICONS.get(genre, 'fa-bookmark')
            })
            
    cart_count = 0
    wishlist_count = 0
    user_wishlist_ids = set()
    
    if 'user_id' in session:
        user_id = session['user_id']
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        cart_count = sum(item.quantity for item in cart_items)
        wishlist_items = WishlistItem.query.filter_by(user_id=user_id).all()
        wishlist_count = len(wishlist_items)
        user_wishlist_ids = {item.book_id for item in wishlist_items}
    else:
        cart = session.get('cart', {})
        cart_count = sum(cart.values())

    return dict(
        all_categories=categories, 
        total_books_count=total_books,
        cart_count=cart_count,
        wishlist_count=wishlist_count,
        user_wishlist_ids=user_wishlist_ids
    )

# --- ROUTES ---

@app.route('/')
def index():
    """
    Home Page / Book Catalog with Search & Genre Category Filter.
    """
    search_query = request.args.get('search', '').strip()
    selected_category = request.args.get('category', '').strip()
    
    query = Book.query

    if selected_category:
        query = query.filter(Book.genre == selected_category)

    if search_query:
        query = query.filter(
            Book.title.ilike(f'%{search_query}%') | 
            Book.author.ilike(f'%{search_query}%') |
            Book.genre.ilike(f'%{search_query}%')
        )

    books = query.all()

    return render_template(
        'index.html', 
        books=books, 
        search_query=search_query, 
        selected_category=selected_category
    )


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """
    Book Detail Page
    """
    book = db.session.get(Book, book_id)
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('index'))
    return render_template('book_detail.html', book=book)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Route
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
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
    User Login Route with Session Cart Merging.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            # Merge guest session cart into DB CartItem
            session_cart = session.pop('cart', {})
            if session_cart:
                for b_id_str, qty in session_cart.items():
                    b_id = int(b_id_str)
                    existing_item = CartItem.query.filter_by(user_id=user.id, book_id=b_id).first()
                    if existing_item:
                        existing_item.quantity += qty
                    else:
                        db.session.add(CartItem(user_id=user.id, book_id=b_id, quantity=qty))
                db.session.commit()

            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html', form_type='login')


@app.route('/logout')
def logout():
    """
    Clear login session.
    """
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


# --- CART ROUTES ---

@app.route('/cart')
def view_cart():
    """
    Shopping Cart Details (Database persisted for user, session for guest).
    """
    cart_items = []
    total_price = 0
    
    if 'user_id' in session:
        items = CartItem.query.filter_by(user_id=session['user_id']).all()
        for item in items:
            if item.book:
                subtotal = item.book.price * item.quantity
                total_price += subtotal
                cart_items.append({
                    'id': item.id,
                    'book': item.book,
                    'quantity': item.quantity,
                    'subtotal': subtotal
                })
    else:
        cart = session.get('cart', {})
        for book_id_str, quantity in cart.items():
            book = db.session.get(Book, int(book_id_str))
            if book:
                subtotal = book.price * quantity
                total_price += subtotal
                cart_items.append({
                    'id': None,
                    'book': book,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
            
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/add-to-cart/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    """
    Add item to cart (DB for logged-in user, session for guest).
    """
    book = db.session.get(Book, book_id)
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('index'))

    quantity = int(request.form.get('quantity', 1))
    
    if 'user_id' in session:
        user_id = session['user_id']
        cart_item = CartItem.query.filter_by(user_id=user_id, book_id=book_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(user_id=user_id, book_id=book_id, quantity=quantity)
            db.session.add(cart_item)
        db.session.commit()
    else:
        cart = session.get('cart', {})
        book_id_str = str(book_id)
        cart[book_id_str] = cart.get(book_id_str, 0) + quantity
        session['cart'] = cart
    
    flash(f'"{book.title}" added to your cart!', 'success')
    next_url = request.referrer or url_for('view_cart')
    return redirect(next_url)


@app.route('/update-cart/<int:book_id>', methods=['POST'])
def update_cart(book_id):
    """
    Update item quantity in cart.
    """
    action = request.form.get('action')
    quantity_input = request.form.get('quantity')

    if 'user_id' in session:
        user_id = session['user_id']
        cart_item = CartItem.query.filter_by(user_id=user_id, book_id=book_id).first()
        if cart_item:
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease':
                cart_item.quantity -= 1
            elif quantity_input and quantity_input.isdigit():
                cart_item.quantity = int(quantity_input)
            
            if cart_item.quantity <= 0:
                db.session.delete(cart_item)
            db.session.commit()
    else:
        cart = session.get('cart', {})
        book_id_str = str(book_id)
        if book_id_str in cart:
            if action == 'increase':
                cart[book_id_str] += 1
            elif action == 'decrease':
                cart[book_id_str] -= 1
            elif quantity_input and quantity_input.isdigit():
                cart[book_id_str] = int(quantity_input)
                
            if cart[book_id_str] <= 0:
                cart.pop(book_id_str)
            session['cart'] = cart

    return redirect(url_for('view_cart'))


@app.route('/remove-from-cart/<int:book_id>', methods=['POST', 'GET'])
def remove_from_cart(book_id):
    """
    Remove item from cart.
    """
    if 'user_id' in session:
        cart_item = CartItem.query.filter_by(user_id=session['user_id'], book_id=book_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
    else:
        cart = session.get('cart', {})
        cart.pop(str(book_id), None)
        session['cart'] = cart

    flash('Item removed from cart.', 'info')
    return redirect(url_for('view_cart'))


@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    """
    Clear all items in cart.
    """
    if 'user_id' in session:
        CartItem.query.filter_by(user_id=session['user_id']).delete()
        db.session.commit()
    else:
        session.pop('cart', None)
        
    flash('Cart cleared.', 'info')
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Convert cart into order history.
    """
    if 'user_id' not in session:
        flash('Please login to place an order.', 'warning')
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('index'))
        
    total = 0
    order_items_data = []
    
    for item in cart_items:
        book = item.book
        if book:
            if book.stock < item.quantity:
                flash(f'Sorry, only {book.stock} units of "{book.title}" are in stock.', 'danger')
                return redirect(url_for('view_cart'))
            total += book.price * item.quantity
            order_items_data.append((book, item.quantity))

    # Create Order
    order = Order(user_id=user_id, total_amount=total)
    db.session.add(order)
    db.session.flush()
    
    for book, quantity in order_items_data:
        book.stock -= quantity
        order_item = OrderItem(order_id=order.id, book_id=book.id, quantity=quantity, price=book.price)
        db.session.add(order_item)
        
    # Clear DB cart
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    flash('Order placed successfully! Thank you for your purchase.', 'success')
    return redirect(url_for('index'))


# --- WISHLIST ROUTES ---

@app.route('/wishlist')
def wishlist():
    """
    Display User Wishlist
    """
    if 'user_id' not in session:
        flash('Please login to view your saved wishlist.', 'warning')
        return redirect(url_for('login'))
        
    wishlist_items = WishlistItem.query.filter_by(user_id=session['user_id']).order_by(WishlistItem.created_at.desc()).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)


@app.route('/add-to-wishlist/<int:book_id>', methods=['POST', 'GET'])
def add_to_wishlist(book_id):
    """
    Add or toggle book in Wishlist.
    """
    if 'user_id' not in session:
        flash('Please login to save books to your wishlist.', 'warning')
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    book = db.session.get(Book, book_id)
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('index'))
        
    existing = WishlistItem.query.filter_by(user_id=user_id, book_id=book_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f'"{book.title}" removed from your wishlist.', 'info')
    else:
        wishlist_item = WishlistItem(user_id=user_id, book_id=book_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash(f'"{book.title}" saved to your wishlist!', 'success')
        
    next_url = request.referrer or url_for('wishlist')
    return redirect(next_url)


@app.route('/remove-from-wishlist/<int:book_id>', methods=['POST', 'GET'])
def remove_from_wishlist(book_id):
    """
    Remove item from Wishlist.
    """
    if 'user_id' not in session:
        flash('Please login.', 'warning')
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    item = WishlistItem.query.filter_by(user_id=user_id, book_id=book_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from your wishlist.', 'info')
        
    next_url = request.referrer or url_for('wishlist')
    return redirect(next_url)


@app.route('/move-to-cart/<int:book_id>', methods=['POST', 'GET'])
def move_to_cart(book_id):
    """
    Move book from Wishlist to Cart.
    """
    if 'user_id' not in session:
        flash('Please login to manage your cart.', 'warning')
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    book = db.session.get(Book, book_id)
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('wishlist'))
        
    # Add to DB cart
    cart_item = CartItem.query.filter_by(user_id=user_id, book_id=book_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        db.session.add(CartItem(user_id=user_id, book_id=book_id, quantity=1))
        
    # Remove from wishlist
    wishlist_item = WishlistItem.query.filter_by(user_id=user_id, book_id=book_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        
    db.session.commit()
    flash(f'Moved "{book.title}" to your shopping cart!', 'success')
    return redirect(url_for('view_cart'))


if __name__ == '__main__':
    app.run(debug=True)
