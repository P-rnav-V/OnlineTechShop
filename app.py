from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from DatabaseScript import db, Item
from DatabaseScript import Review 
from flask import make_response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'yesyesnono'

db.init_app(app)

@app.route('/')
def loginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if len(password) < 8:
        return render_template('login.html', error="Password must be at least 8 characters.")
    session['username'] = username
    return redirect(url_for('galleryPage'))

@app.route('/gallery')
def galleryPage():
    if 'username' not in session:
        return redirect(url_for('loginPage'))

    search_query = request.args.get('search', '').lower()
    sort_order = request.args.get('sort')

    itemsForSale = Item.query.all()

    if search_query:
        itemsForSale = [item for item in itemsForSale if search_query in item.name.lower()]

    if sort_order == 'price_asc':
        itemsForSale.sort(key=lambda item: item.price)
    elif sort_order == 'price_desc':
        itemsForSale.sort(key=lambda item: item.price, reverse=True)
    elif sort_order == 'name_asc':
        itemsForSale.sort(key=lambda item: item.name.lower())
    elif sort_order == 'name_desc':
        itemsForSale.sort(key=lambda item: item.name.lower(), reverse=True)
    elif sort_order == 'env_LowToHigh':
        itemsForSale.sort(key=lambda item: item.envImpactsValue)
    elif sort_order == 'env_HighToLow':
        itemsForSale.sort(key=lambda item: item.envImpactsValue,reverse=True)
        

    return render_template("index.html", itemsForSale=itemsForSale, username=session['username'], sort_order=sort_order)

@app.route('/add-to-basket/<int:item_id>', methods=['POST'])
def addToBasket(item_id):
    if 'username' not in session:
        return redirect(url_for('loginPage'))

    quantity = int(request.form.get('quantity', 1))
    basket = session.get('basket', {})
    item_key = str(item_id)
    basket[item_key] = basket.get(item_key, 0) + quantity
    session['basket'] = basket
    return redirect(url_for('galleryPage'))


@app.route('/item/<int:itemId>', methods=['GET', 'POST'])
def singleProductPage(itemId):
    item = Item.query.get(itemId)
    quantity = request.args.get('quantity')

    if request.method == 'POST':
        if 'quantity' in request.form:
            quantity = int(request.form.get('quantity'))
            basket = session.get('basket', {})
            basket[str(item.id)] = basket.get(str(item.id), 0) + quantity
            session['basket'] = basket
            return redirect(url_for('singleProductPage', itemId=itemId, quantity=quantity))
        elif 'review' in request.form:
            content = request.form.get('review')
            if content:
                new_review = Review(item_id=item.id, username=session.get('username'), content=content)
                db.session.add(new_review)
                db.session.commit()
                return redirect(url_for('singleProductPage', itemId=itemId))

    reviews = Review.query.filter_by(item_id=itemId).order_by(Review.timestamp.desc()).all()
    return render_template('SingleTech.html', item=item, quantity=quantity, username=session.get('username'), reviews=reviews)


@app.route('/basket')
def basketPage():
    basket = session.get('basket', {})
    basket_items = []
    total_price = 0
    for item_id, quantity in basket.items():
        item = Item.query.get(int(item_id))
        if item:
            item_total = item.price * quantity
            total_price += item_total
            basket_items.append({
                'item': item,
                'quantity': quantity,
                'total_price': item_total
            })
    return render_template('basket.html', basket_items=basket_items, total_price=total_price, username=session.get('username'))


@app.route('/remove/<int:item_id>')
def removeFromBasket(item_id):
    basket = session.get('basket', {})
    item_key = str(item_id)
    if item_key in basket:
        if basket[item_key] > 1:
            basket[item_key] -= 1
        else:
            del basket[item_key]
    session['basket'] = basket
    return redirect(url_for('basketPage'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkoutPage():
    if request.method == 'POST':        
        session['basket'] = {} 
        return render_template('thankyou.html', username=session.get('username'))
    return render_template('checkout.html', username=session.get('username'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('loginPage'))

@app.route('/shipping-label')
def shippingLabel():
    username = session.get('username')
    label = f"Shipping Label\nRecipient: {username}\nThank you for your purchase from TechMart!"
    response = make_response(label)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = 'attachment; filename=shipping_label.txt'
    return response

@app.route('/invoice')
def invoice():
    basket = session.get('basket', {})
    total = 0
    lines = []
    for item_id, quantity in basket.items():
        item = Item.query.get(int(item_id))
        if item:
            subtotal = item.price * quantity
            lines.append(f"{item.name} x{quantity} - ${subtotal:.2f}")
            total += subtotal

    content = f"INVOICE\nCustomer: {session.get('username')}\n" + "\n".join(lines) + f"\n\nTotal: ${total:.2f}"
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = 'attachment; filename=invoice.txt'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
