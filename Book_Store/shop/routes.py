from flask import render_template, url_for, redirect, request
from flask_login import current_user, login_required
from Book_Store import db
from Book_Store.models import Book, Cart, CartItem, Order, OrderItem
from Book_Store.shop import shop

@shop.app_context_processor
def inject_cart_count():
    count = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            count = sum(item.quantity for item in cart.items)
    return dict(cart_count=count)

@shop.route('/add_to_cart/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
        
    cart_item = CartItem.query.filter_by(cart_id=cart.id, book_id=book.id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, book_id=book.id, quantity=1)
        db.session.add(cart_item)
        
    db.session.commit()
    return redirect(request.referrer or url_for('main.home'))

@shop.route('/cart')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    items = []
    total = 0
    if cart:
        items = cart.items
        total = sum(item.book.price * item.quantity for item in items)
    return render_template('cart.html', title='Cart', items=items, total=total)

@shop.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.cart.user_id != current_user.id:
        return redirect(url_for('shop.view_cart'))
    
    action = request.form.get('action')
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
    elif action == 'remove':
        db.session.delete(item)
        
    db.session.commit()
    return redirect(url_for('shop.view_cart'))

@shop.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        return redirect(url_for('shop.view_cart'))
        
    total = sum(item.book.price * item.quantity for item in cart.items)
    
    order = Order(user_id=current_user.id, total_price=total)
    db.session.add(order)
    db.session.flush() # get order.id
    
    for item in cart.items:
        order_item = OrderItem(order_id=order.id, book_id=item.book_id, quantity=item.quantity, price=item.book.price)
        db.session.add(order_item)
        db.session.delete(item)
        
    db.session.commit()
    return redirect(url_for('shop.receipt', order_id=order.id))

@shop.route('/receipt/<int:order_id>')
@login_required
def receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return redirect(url_for('main.home'))
    return render_template('receipt.html', title='Receipt', order=order)
