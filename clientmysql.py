import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import pymysql
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client_bp = Blueprint('client', __name__, template_folder='templates/client')

# ----------------------------
# Configuración de conexión a base de datos
# ----------------------------
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='ecommerce',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# ----------------------------
# Registro de usuario
# ----------------------------
@client_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Comprobar si la contraseña tiene una longitud mínima
        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'error')
            return redirect(url_for('client.register'))

        # Usamos bcrypt para generar el hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            flash('Este correo electrónico ya está registrado.', 'error')
            conn.close()
            return redirect(url_for('client.register'))

        cur.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_password, 'client')
        )
        conn.commit()
        conn.close()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('client.login'))

    return render_template('register.html')

# ----------------------------
# Inicio de sesión
# ----------------------------
@client_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('client.index'))

        flash('Correo o contraseña incorrectos.', 'error')
        return redirect(url_for('client.login'))

    return render_template('login.html')

# ----------------------------
# Cierre de sesión
# ----------------------------
@client_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('client.login'))

# ----------------------------
# Página principal
# ----------------------------
@client_bp.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@client_bp.route('/ranking')
def ranking():
    conn = get_db()
    cur = conn.cursor()

    user_id = session.get('user_id')

    if not user_id:
        flash('Debes iniciar sesión para ver tus recomendaciones.', 'error')
        return redirect(url_for('client.login'))

    # ----------------------------
    # 1. Obtener productos en el carrito del usuario actual
    # ----------------------------
    cur.execute("""
        SELECT DISTINCT p.id, p.name, p.price, p.image_url, p.category
        FROM products p
        JOIN cart c ON p.id = c.product_id
        WHERE c.user_id = %s
    """, (user_id,))
    
    cart_products = cur.fetchall()

    if not cart_products:
        flash('Agrega productos al carrito para ver recomendaciones.', 'info')
        return render_template('ranking.html', products=[])

    # ----------------------------
    # 2. Buscar productos recomendados por categoría (complementarios)
    # ----------------------------
    cur.execute("""
        SELECT DISTINCT p.id, p.name, p.price, p.image_url
        FROM products p
        WHERE p.category IN (
            SELECT DISTINCT p2.category
            FROM products p2
            JOIN cart c ON p2.id = c.product_id
            WHERE c.user_id = %s
        )
        AND p.id NOT IN (
            SELECT product_id FROM cart WHERE user_id = %s
        )
        LIMIT 20
    """, (user_id, user_id))

    complementary_products = cur.fetchall()
    recommended_products = complementary_products

    # ----------------------------
    # 3. Si hay pocos, completar con similares por precio
    # ----------------------------
    if len(recommended_products) < 5:
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity

        product_data = [
            {'id': p['id'], 'name': p['name'], 'price': p['price'], 'image_url': p['image_url']}
            for p in cart_products
        ]
        product_features = np.array([[p['price']] for p in product_data])
        if product_features.ndim == 1:
            product_features = product_features.reshape(-1, 1)

        similarity_matrix = cosine_similarity(product_features)

        similar_products = []
        seen_ids = set(p['id'] for p in complementary_products)

        for i, product in enumerate(cart_products):
            similarities = similarity_matrix[i]
            similar_indices = similarities.argsort()[-6:-1][::-1]

            for index in similar_indices:
                similar_product = cart_products[index]
                if similar_product['id'] not in seen_ids:
                    seen_ids.add(similar_product['id'])
                    similar_products.append({
                        'id': similar_product['id'],
                        'name': similar_product['name'],
                        'price': similar_product['price'],
                        'image_url': similar_product['image_url']
                    })

        recommended_products += similar_products

    conn.close()
    return render_template('ranking.html', products=recommended_products[:20])

# ----------------------------
# Agregar producto al carrito
# ----------------------------
@client_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('client.login'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()

    if not product:
        conn.close()
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('client.index'))

    # Verifica si el producto ya está en el carrito
    cur.execute(
        "SELECT * FROM cart WHERE user_id = %s AND product_id = %s",
        (session['user_id'], product_id)
    )
    item = cur.fetchone()

    if item:
        cur.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE user_id = %s AND product_id = %s",
            (session['user_id'], product_id)
        )
    else:
        cur.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, 1)",
            (session['user_id'], product_id)
        )

    conn.commit()
    conn.close()

    flash('Producto agregado al carrito.', 'success')
    return redirect(url_for('client.cart'))

# ----------------------------
# Ver carrito de compras
# ----------------------------
@client_bp.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('client.login'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name, p.price, c.quantity, (p.price * c.quantity) AS total_price, c.product_id
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (session['user_id'],))
    items = cur.fetchall()
    conn.close()

    total = sum(item['total_price'] for item in items)
    return render_template('cart.html', cart_items=items, total=total)

# ----------------------------
# Eliminar producto del carrito
# ----------------------------
@client_bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('client.login'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (session['user_id'], product_id))
    conn.commit()
    conn.close()

    flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('client.cart'))

# ----------------------------
# Finalizar compra
# ----------------------------
@client_bp.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('client.login'))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (session['user_id'],))
    items = cur.fetchall()

    total = sum(item['price'] * item['quantity'] for item in items)

    cur.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s)", (session['user_id'], total))
    order_id = cur.lastrowid

    cur.execute("DELETE FROM cart WHERE user_id = %s", (session['user_id'],))
    conn.commit()
    conn.close()

    flash('¡Compra completada con éxito!', 'success')
    return redirect(url_for('client.order_summary', order_id=order_id))

# ----------------------------
# Resumen de orden
# ----------------------------
@client_bp.route('/order_summary/<int:order_id>')
def order_summary(order_id):
    if 'user_id' not in session:
        return redirect(url_for('client.login'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, session['user_id']))
    order = cur.fetchone()
    conn.close()

    if not order:
        flash('Orden no encontrada.', 'error')
        return redirect(url_for('client.index'))

    return render_template('order_summary.html', order=order)
