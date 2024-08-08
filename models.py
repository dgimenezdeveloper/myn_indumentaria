from flask_mysqldb import MySQL

mysql = MySQL()

def get_all_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return products

def get_product_by_id(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", [product_id])
    product = cur.fetchone()
    cur.close()
    return product

def add_product(name, description, price, category, image):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products (name, description, price, category, image) VALUES (%s, %s, %i, %s, %s)",
                (name, description, price, category, image))
    mysql.connection.commit()
    cur.close()

def update_product(product_id, name, description, price, category, image):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE products SET name = %s, description = %s, category = %s, image = %s WHERE id = %s",
                (name, description, price, category, image, product_id))
    mysql.connection.commit()
    cur.close()

def delete_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", [product_id])
    mysql.connection.commit()
    cur.close()
