import unittest
import os
import tempfile
from app import app, db
from models import User, Book, CartItem, WishlistItem, Order, OrderItem

class BookstoreTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_fd, cls.test_db_path = tempfile.mkstemp(suffix='.db')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{cls.test_db_path}'
        app.config['WTF_CSRF_ENABLED'] = False

    @classmethod
    def tearDownClass(cls):
        os.close(cls.db_fd)
        try:
            os.remove(cls.test_db_path)
        except OSError:
            pass

    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            # Seed test books
            b1 = Book(title="Test Book 1", author="Author A", genre="Fiction", price=100.0, stock=5)
            b2 = Book(title="Test Book 2", author="Author B", genre="Fiction", price=200.0, stock=0)
            b3 = Book(title="Test Book 3", author="Author C", genre="Sci-Fi", price=300.0, stock=10)
            db.session.add_all([b1, b2, b3])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_routes_status(self):
        routes = ['/', '/catalog', '/catalog?search=Test', '/catalog?category=Fiction', '/catalog?genre=Fiction', '/login', '/register', '/cart']
        for r in routes:
            resp = self.client.get(r)
            self.assertEqual(resp.status_code, 200, f"Route {r} failed with status {resp.status_code}")

    def test_book_detail(self):
        resp = self.client.get('/book/1')
        self.assertEqual(resp.status_code, 200)
        # Non-existent book redirects to catalog
        resp2 = self.client.get('/book/999')
        self.assertEqual(resp2.status_code, 302)

    def test_registration_and_login(self):
        # Successful register
        resp = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        
        # Duplicate email
        resp_dup_email = self.client.post('/register', data={
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(resp_dup_email.status_code, 200)

        # Duplicate username (prevents 500)
        resp_dup_user = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'different@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(resp_dup_user.status_code, 200)

        # Empty fields
        resp_empty = self.client.post('/register', data={
            'username': '',
            'email': '',
            'password': ''
        }, follow_redirects=True)
        self.assertEqual(resp_empty.status_code, 200)

        # Successful login
        resp_login = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(resp_login.status_code, 200)

    def test_cart_operations(self):
        # Guest add to cart
        resp = self.client.post('/add-to-cart/1', data={'quantity': '2'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        resp_cart = self.client.get('/cart')
        self.assertIn(b"Test Book 1", resp_cart.data)

        # Invalid non-numeric quantity does not crash (falls back to 1)
        resp_inv = self.client.post('/add-to-cart/1', data={'quantity': 'abc'}, follow_redirects=True)
        self.assertEqual(resp_inv.status_code, 200)

        # Out of stock book cannot be added
        resp_oos = self.client.post('/add-to-cart/2', data={'quantity': '1'}, follow_redirects=True)
        self.assertEqual(resp_oos.status_code, 200)

        # Update cart: increase
        resp_up = self.client.post('/update-cart/1', data={'action': 'increase'}, follow_redirects=True)
        self.assertEqual(resp_up.status_code, 200)

        # Update cart: decrease
        resp_down = self.client.post('/update-cart/1', data={'action': 'decrease'}, follow_redirects=True)
        self.assertEqual(resp_down.status_code, 200)

        # Remove from cart
        resp_rem = self.client.post('/remove-from-cart/1', follow_redirects=True)
        self.assertEqual(resp_rem.status_code, 200)

    def test_checkout_and_razorpay(self):
        # Register and login
        self.client.post('/register', data={'username': 'buyer', 'email': 'buyer@example.com', 'password': 'pass'})
        self.client.post('/login', data={'email': 'buyer@example.com', 'password': 'pass'})

        # Add to cart
        self.client.post('/add-to-cart/1', data={'quantity': '2'})

        # Razorpay create order
        resp_rzp = self.client.post('/create-razorpay-order')
        self.assertEqual(resp_rzp.status_code, 200)
        data = resp_rzp.get_json()
        self.assertEqual(data['status'], 'success')
        db_order_id = data['db_order_id']

        # Razorpay verify payment
        resp_verify = self.client.post('/verify-razorpay-payment', json={
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': 'pay_test_12345',
            'razorpay_signature': 'dummy_sig',
            'db_order_id': db_order_id
        })
        self.assertEqual(resp_verify.status_code, 200)
        verify_data = resp_verify.get_json()
        self.assertEqual(verify_data['status'], 'success')

        # Idempotent second verification does not fail or deduct stock twice
        resp_verify_again = self.client.post('/verify-razorpay-payment', json={
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': 'pay_test_12345',
            'razorpay_signature': 'dummy_sig',
            'db_order_id': db_order_id
        })
        self.assertEqual(resp_verify_again.status_code, 200)

        # Account page shows completed order
        resp_acc = self.client.get('/account')
        self.assertEqual(resp_acc.status_code, 200)
        self.assertIn(b"Test Book 1", resp_acc.data)

    def test_wishlist(self):
        # Need login for wishlist
        self.client.post('/register', data={'username': 'wisher', 'email': 'wisher@example.com', 'password': 'pass'})
        self.client.post('/login', data={'email': 'wisher@example.com', 'password': 'pass'})

        # Add to wishlist
        resp = self.client.post('/add-to-wishlist/1', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        resp_w = self.client.get('/wishlist')
        self.assertEqual(resp_w.status_code, 200)
        self.assertIn(b"Test Book 1", resp_w.data)

        # Move to cart
        resp_move = self.client.post('/move-to-cart/1', follow_redirects=True)
        self.assertEqual(resp_move.status_code, 200)

if __name__ == '__main__':
    unittest.main()
