import bcrypt
import numpy as np
import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from psycopg2.extras import RealDictCursor
from sklearn.metrics.pairwise import cosine_similarity
from config import DB_CONFIG

client_bp = Blueprint('client', __name__, template_folder='templates/client')


def get_db():
    # Asumiendo que DB_CONFIG es un diccionario que contiene las credenciales de la DB
    config = DB_CONFIG.copy()  # Hacemos una copia para evitar modificar el original
    config.pop('cursor_factory', None)  # Nos aseguramos de que no esté en DB_CONFIG

    return psycopg2.connect(cursor_factory=RealDictCursor, **config)


def require_login():
    if 'user_id' not in session:
        flash('Debes iniciar sesión.', 'error')
        return redirect(url_for('client.login'))
    return None


@client_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'error')
            return redirect(url_for('client.register'))

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
                    if cur.fetchone():
                        flash('Este correo ya está registrado.', 'error')
                        return redirect(url_for('client.register'))

                    cur.execute("""
                        INSERT INTO users (username, email, password, role)
                        VALUES (%s, %s, %s, %s)
                    """, (username, email, hashed_password.decode(), 'client'))
                    conn.commit()

            flash('Registro exitoso. Inicia sesión.', 'success')
            return redirect(url_for('client.login'))

        except Exception as e:
            flash('Error en el registro: ' + str(e), 'error')

    return render_template('register.html')


@client_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                    user = cur.fetchone()

                    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                        session['user_id'] = user['id']
                        session['username'] = user['username']
                        return redirect(url_for('client.index'))

        except Exception as e:
            flash('Error en inicio de sesión: ' + str(e), 'error')

        flash('Correo o contraseña incorrectos.', 'error')
        return redirect(url_for('client.login'))

    return render_template('login.html')


@client_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('client.login'))


@client_bp.route('/')
def index():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM products")
                products = cur.fetchall()
        return render_template('index.html', products=products)
    except:
        flash('No se pudieron cargar los productos.', 'error')
        return render_template('index.html', products=[])



@client_bp.route('/ranking')
def ranking():
    try:
        # Conexión a la base de datos
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, description, price, image_url FROM products")
                all_products = cur.fetchall()

                user_id = session.get("user_id", 1)  # Obtener el ID del usuario desde la sesión
                cur.execute("SELECT product_id FROM cart WHERE user_id = %s", (user_id,))
                cart_product_ids = {row[0] for row in cur.fetchall()}  # Usar set para optimizar la búsqueda

        # Si hay productos en el carrito
        if cart_product_ids:
            texts = [f"{prod[1]} {prod[2]}" for prod in all_products]
            product_ids = [prod[0] for prod in all_products]

            # Vectorización y cálculo de similitudes
            vectorizer = TfidfVectorizer(stop_words='spanish')
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Obtener los índices de los productos en el carrito
            cart_indices = [i for i, pid in enumerate(product_ids) if pid in cart_product_ids]
            cart_vectors = tfidf_matrix[cart_indices]

            # Calcular similitud entre los productos del carrito y todos los productos
            similarity_scores = cosine_similarity(cart_vectors, tfidf_matrix)
            avg_similarity = np.mean(similarity_scores, axis=0)
            ranked_indices = np.argsort(avg_similarity)[::-1]

            # Generar los productos recomendados
            recommended = []
            similarity_data = []
            for i in ranked_indices:
                if product_ids[i] not in cart_product_ids:
                    product = all_products[i]
                    recommended.append(product)
                    similarity_data.append({
                        'name': product[1],
                        'score': round(float(avg_similarity[i]), 3)
                    })
                if len(recommended) >= 4:  # Limitar a 4 productos recomendados
                    break

            mean_score = float(np.max(avg_similarity))  # Promedio de la similitud
        else:
            recommended = []
            similarity_data = []
            mean_score = 0.0

        return render_template(
            'index.html',
            products=recommended,
            similarity_data=similarity_data,
            mean_score=mean_score
        )

    except Exception as e:
        print(f"Error en /ranking: {e}")
        flash('No se pudieron cargar los productos.', 'error')
        return render_template('index.html', products=[], similarity_data=[], mean_score=0.0)


@client_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if not session.get('user_id'):
        return redirect(url_for('client.login'))

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                product = cur.fetchone()
                if not product:
                    flash('Producto no encontrado.', 'error')
                    return redirect(url_for('client.index'))

                cur.execute("""
                    SELECT 1 FROM cart WHERE user_id = %s AND product_id = %s
                """, (session['user_id'], product_id))

                if cur.fetchone():
                    cur.execute("""
                        UPDATE cart SET quantity = quantity + 1
                        WHERE user_id = %s AND product_id = %s
                    """, (session['user_id'], product_id))
                else:
                    cur.execute("""
                        INSERT INTO cart (user_id, product_id, quantity)
                        VALUES (%s, %s, 1)
                    """, (session['user_id'], product_id))

                conn.commit()
        flash('Producto agregado al carrito.', 'success')

    except Exception as e:
        flash(f'Error al agregar producto: {e}', 'error')

    return redirect(url_for('client.cart'))


@client_bp.route('/cart')
def cart():
    if not session.get('user_id'):
        return redirect(url_for('client.login'))

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.name, p.price, c.quantity, 
                           (p.price * c.quantity) AS total_price, c.product_id
                    FROM cart c
                    JOIN products p ON c.product_id = p.id
                    WHERE c.user_id = %s
                """, (session['user_id'],))
                items = cur.fetchall()
        total = sum(item['total_price'] for item in items)
        return render_template('cart.html', cart_items=items, total=total)
    except:
        flash('No se pudo cargar el carrito.', 'error')
        return render_template('cart.html', cart_items=[], total=0)


@client_bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if not session.get('user_id'):
        return redirect(url_for('client.login'))

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s",
                            (session['user_id'], product_id))
                conn.commit()
        flash('Producto eliminado.', 'success')
    except:
        flash('No se pudo eliminar el producto.', 'error')

    return redirect(url_for('client.cart'))


@client_bp.route('/checkout')
def checkout():
    if not session.get('user_id'):
        return redirect(url_for('client.login'))

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Obtener los productos del carrito
                cur.execute("""
                    SELECT p.price, c.quantity
                    FROM cart c
                    JOIN products p ON c.product_id = p.id
                    WHERE c.user_id = %s
                """, (session['user_id'],))
                items = cur.fetchall()

                # Calcular el total de la compra
                total = sum(i['price'] * i['quantity'] for i in items)

                # Insertar la orden en la base de datos
                cur.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id",
                            (session['user_id'], total))
                order_id = cur.fetchone()['id']

                # Eliminar los productos del carrito después de la compra
                cur.execute("DELETE FROM cart WHERE user_id = %s", (session['user_id'],))
                conn.commit()

        flash('¡Compra realizada con éxito!', 'success')
        return redirect(url_for('client.order_summary', order_id=order_id))

    except Exception as e:
        flash(f'Error al realizar compra: {e}', 'error')
        return redirect(url_for('client.cart'))



@client_bp.route('/order_summary/<int:order_id>')
def order_summary(order_id):
    if not session.get('user_id'):
        return redirect(url_for('client.login'))

    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                # Obtener los detalles de la orden
                cur.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s",
                            (order_id, session['user_id']))
                order = cur.fetchone()

        if not order:
            flash('Orden no encontrada.', 'error')
            return redirect(url_for('client.index'))

        return render_template('order_summary.html', order=order)

    except Exception as e:
        flash(f'Error al cargar orden: {e}', 'error')
        return redirect(url_for('client.index'))

