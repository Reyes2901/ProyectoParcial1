from flask import Blueprint, render_template, request, redirect, url_for
import pymysql

admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='ecommerce',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# DASHBOARD ADMIN
@admin_bp.route('/')
def dashboard():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total_products FROM products")
    products = cur.fetchone()

    cur.execute("SELECT COUNT(*) AS total_users FROM users WHERE role='client'")
    users = cur.fetchone()

    cur.execute("SELECT COUNT(*) AS total_orders FROM orders")
    orders = cur.fetchone()

    conn.close()
    return render_template('dashboard.html', products=products, users=users, orders=orders)

# LISTAR PRODUCTOS
@admin_bp.route('/products')
def products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    conn.close()
    return render_template('products.html', products=data)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        image_url = request.form['image_url']
        
        # Validación simple
        if not name or not description or not price or not stock or not image_url:
            flash('Por favor, completa todos los campos.', 'error')
            return render_template('add_product.html')
        
        try:
            price = float(price)  # Asegurarse de que el precio sea un número
            stock = int(stock)    # Asegurarse de que el stock sea un número entero
        except ValueError:
            flash('El precio y el stock deben ser números válidos.', 'error')
            return render_template('add_product.html')

        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO products (name, description, price, stock, image_url) VALUES (%s, %s, %s, %s, %s)",
                        (name, description, price, stock, image_url))
            conn.commit()
            flash('Producto agregado con éxito.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al agregar el producto: {str(e)}', 'error')
        finally:
            conn.close()

        return redirect(url_for('admin.products'))

    return render_template('add_product.html')

# EDITAR PRODUCTO
@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        image_url = request.form['image_url']

        cur.execute("""
            UPDATE products 
            SET name=%s, description=%s, price=%s, stock=%s, image_url=%s 
            WHERE id=%s
        """, (name, description, price, stock, image_url, id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin.products'))

    cur.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cur.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

# ELIMINAR PRODUCTO
@admin_bp.route('/products/delete/<int:id>')
def delete_product(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.products'))
