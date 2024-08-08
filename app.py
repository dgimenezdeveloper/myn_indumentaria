from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import mysql, get_all_products, get_product_by_id, add_product, update_product, delete_product
from forms import ProductForm

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

@app.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = get_product_by_id(product_id)
    return render_template('product.html', product=product)

@app.route('/add', methods=['GET', 'POST'])
def add_product_view():
    form = ProductForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        category = form.category.data
        image = form.image.data.filename
        add_product(name, description, price, category, image)
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product_view(product_id):
    product = get_product_by_id(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        category = form.category.data
        image = form.image.data.filename if form.image.data else product['image']
        update_product(product_id, name, description, price, category, image)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_product.html', form=form, product=product)

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product_view(product_id):
    delete_product(product_id)
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items, get_product_by_id=get_product_by_id)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart.remove(product_id)
    session['cart'] = cart
    flash('Product removed from cart!', 'success')
    return redirect(url_for('cart'))

# Rutas para las categorias
@app.route('/category/<category_name>')
def category(category_name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE category = %s", (category_name,))
    products = cursor.fetchall()
    cursor.close()
    return render_template('category.html', products=products, category_name=category_name)


if __name__ == '__main__':
    app.run(debug=True)
