# model.py
import mysql.connector
from mysql.connector import Error
import bcrypt
import json

class Model:
    def __init__(self, db_config):
        self.db_config = db_config

    def _execute_query(self, query, params=None, fetch=None, is_commit=False):
        result = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            if conn.is_connected():
                cursor = conn.cursor(dictionary=(fetch in ['one', 'all']))
                cursor.execute(query, params or ())
                if is_commit:
                    conn.commit()
                    result = cursor.lastrowid if 'INSERT' in query.upper() else cursor.rowcount > 0
                elif fetch:
                    result = cursor.fetchone() if fetch == 'one' else cursor.fetchall()
        except Error as e:
            print(f"Error de base de datos: {e}")
            if 'conn' in locals() and conn.is_connected(): conn.rollback()
            result = False if is_commit else (None if fetch else [])
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
        return result

    # --- NUEVO: Lógica para la página de todos los chats ---
    def get_user_conversations(self, user_id):
        query = """
            SELECT 
                other_user.id as other_user_id,
                other_user.username as other_user_name,
                last_msg.message_text as last_message,
                last_msg.created_at as last_message_time
            FROM (
                SELECT
                    CASE
                        WHEN sender_id = %s THEN receiver_id
                        ELSE sender_id
                    END as other_user_id,
                    MAX(id) as max_message_id
                FROM messages
                WHERE sender_id = %s OR receiver_id = %s
                GROUP BY
                    CASE
                        WHEN sender_id = %s THEN receiver_id
                        ELSE sender_id
                    END
            ) as conversations
            JOIN users as other_user ON other_user.id = conversations.other_user_id
            JOIN messages as last_msg ON last_msg.id = conversations.max_message_id
            ORDER BY last_msg.created_at DESC;
        """
        return self._execute_query(query, (user_id, user_id, user_id, user_id), fetch='all')

    def send_message(self, sender_id, receiver_id, message_text):
        query = "INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (%s, %s, %s)"
        return self._execute_query(query, (sender_id, receiver_id, message_text), is_commit=True)

    def get_conversation(self, user1_id, user2_id):
        query = """
            SELECT m.*, u.username as sender_name 
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE (m.sender_id = %s AND m.receiver_id = %s) OR (m.sender_id = %s AND m.receiver_id = %s)
            ORDER BY m.created_at ASC
        """
        return self._execute_query(query, (user1_id, user2_id, user2_id, user1_id), fetch='all')

    def add_product(self, data):
        query = """
            INSERT INTO products (owner_user_id, nombre, descripcion, precio, imagen_path, direccion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['owner_user_id'], data['nombre'], data.get('descripcion', ''),
            float(data['precio']), data.get('imagen_path', ''), data.get('direccion', '')
        )
        return self._execute_query(query, params, is_commit=True)
        
    def update_product(self, data, product_id, user_id):
        query = """
            UPDATE products SET nombre=%s, descripcion=%s, precio=%s, imagen_path=%s, direccion=%s 
            WHERE id=%s AND owner_user_id=%s
        """
        params = (
            data['nombre'], data['descripcion'], data['precio'], 
            data.get('imagen_path', ''), data.get('direccion', ''), product_id, user_id
        )
        return self._execute_query(query, params, is_commit=True)

    def get_user_cart(self, user_id):
        query = "SELECT cart_items FROM users WHERE id = %s"
        result = self._execute_query(query, (user_id,), fetch='one')
        if result and result.get('cart_items'):
            try:
                return json.loads(result['cart_items'])
            except Exception:
                return []
        return []

    def add_to_cart(self, user_id, product_id):
        cart = self.get_user_cart(user_id)
        if product_id not in cart:
            cart.append(product_id)
        query = "UPDATE users SET cart_items = %s WHERE id = %s"
        return self._execute_query(query, (json.dumps(cart), user_id), is_commit=True)

    def remove_from_cart(self, user_id, product_id):
        cart = self.get_user_cart(user_id)
        if product_id in cart:
            cart.remove(product_id)
        query = "UPDATE users SET cart_items = %s WHERE id = %s"
        return self._execute_query(query, (json.dumps(cart), user_id), is_commit=True)

    def clear_cart(self, user_id):
        query = "UPDATE users SET cart_items = '[]' WHERE id = %s"
        return self._execute_query(query, (user_id,), is_commit=True)

    def get_cart_products(self, user_id):
        cart = self.get_user_cart(user_id)
        if not cart:
            return []
        placeholders = ','.join(['%s'] * len(cart))
        query = f"SELECT p.*, u.nombre as owner_name FROM products p JOIN users u ON p.owner_user_id = u.id WHERE p.id IN ({placeholders})"
        return self._execute_query(query, tuple(cart), fetch='all')

    def buy_product(self, user_id, product_id):
        query = "UPDATE products SET vendido = 1, comprador_user_id = %s WHERE id = %s AND vendido = 0"
        return self._execute_query(query, (user_id, product_id), is_commit=True)

    def get_user_purchases(self, user_id):
        query = '''
            SELECT p.*, u.nombre as owner_name
            FROM products p
            JOIN users u ON p.owner_user_id = u.id
            WHERE p.comprador_user_id = %s
        '''
        return self._execute_query(query, (user_id,), fetch='all')
    
    def hash_password(self, p): return bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt())
    def check_password(self, p, h): return bcrypt.checkpw(p.encode('utf-8'), h.encode('utf-8'))

    def create_user(self, data):
        data['password_hash'] = self.hash_password(data.pop('password')).decode('utf-8')
        campos = [
            'nombre', 'apellidos', 'email', 'password_hash', 'telefono', 'username', 'foto_perfil', 'direccion',
            'fecha_nacimiento', 'is_admin', 'estado', 'ultimo_login', 'verificado', 'reputacion', 'nivel'
        ]
        insert_campos = [c for c in campos if c in data]
        insert_values = [data[c] for c in insert_campos]
        query = f"INSERT INTO users ({', '.join(insert_campos)}) VALUES ({', '.join(['%s']*len(insert_campos))})"
        return self._execute_query(query, tuple(insert_values), is_commit=True)

    def check_user(self, email, password):
        user = self._execute_query("SELECT * FROM users WHERE email = %s", (email,), fetch='one')
        if user and user.get('password_hash') and self.check_password(password, user['password_hash']):
            return user
        return None

    def get_user_by_email(self, email):
        return self._execute_query("SELECT id FROM users WHERE email = %s", (email,), fetch='one')

    def get_user_by_id(self, user_id):
        return self._execute_query(
            "SELECT id, nombre, apellidos, email, telefono, username, foto_perfil, direccion, fecha_nacimiento, is_admin, estado, ultimo_login, verificado, reputacion, nivel FROM users WHERE id = %s",
            (user_id,), fetch='one')

    def update_user_profile(self, user_id, data):
        campos_actualizables = [
            'nombre', 'apellidos', 'telefono', 'username', 'foto_perfil', 'direccion',
            'fecha_nacimiento', 'is_admin', 'estado', 'ultimo_login', 'verificado', 'reputacion', 'nivel'
        ]
        sets = [f"{c}=%s" for c in campos_actualizables if c in data]
        values = [data[c] for c in campos_actualizables if c in data]
        if not sets: return False
        query = f"UPDATE users SET {', '.join(sets)} WHERE id=%s"
        values.append(user_id)
        return self._execute_query(query, tuple(values), is_commit=True)

    def delete_product(self, product_id, user_id):
        query = "DELETE FROM products WHERE id=%s AND owner_user_id=%s"
        return self._execute_query(query, (product_id, user_id), is_commit=True)

    def get_all_products(self, search_term=None):
        query = "SELECT p.*, u.nombre as owner_name FROM products p JOIN users u ON p.owner_user_id = u.id"
        params = ()
        if search_term:
            query += " WHERE p.nombre LIKE %s"
            params = (f"%{search_term}%",)
        return self._execute_query(query, params, fetch='all')

    def get_product_by_id(self, product_id):
        query = "SELECT p.*, u.nombre as owner_name FROM products p JOIN users u ON p.owner_user_id = u.id WHERE p.id = %s"
        return self._execute_query(query, (product_id,), fetch='one')

    def get_user_products(self, user_id):
        return self._execute_query("SELECT * FROM products WHERE owner_user_id = %s", (user_id,), fetch='all')

    def create_trade(self, proposer_user_id, proposer_product_id, receiver_user_id, receiver_product_id):
        query = "INSERT INTO trades (proposer_user_id, proposer_product_id, receiver_user_id, receiver_product_id) VALUES (%s, %s, %s, %s)"
        params = (proposer_user_id, proposer_product_id, receiver_user_id, receiver_product_id)
        return self._execute_query(query, params, is_commit=True)

    def get_trades_for_user(self, user_id):
        query = """
        SELECT t.id, t.status, t.proposer_user_id, up.nombre as proposer_name, pp.nombre as proposer_product_name, pp.id as proposer_product_id,
        t.receiver_user_id, ur.nombre as receiver_name, rp.nombre as receiver_product_name, rp.id as receiver_product_id
        FROM trades t
        JOIN users up ON t.proposer_user_id = up.id JOIN products pp ON t.proposer_product_id = pp.id
        JOIN users ur ON t.receiver_user_id = ur.id JOIN products rp ON t.receiver_product_id = rp.id
        WHERE t.proposer_user_id = %s OR t.receiver_user_id = %s ORDER BY t.created_at DESC
        """
        return self._execute_query(query, (user_id, user_id), fetch='all')

    def update_trade_status(self, trade_id, new_status):
        query = "UPDATE trades SET status = %s WHERE id = %s"
        return self._execute_query(query, (new_status, trade_id), is_commit=True)

    def execute_trade(self, trade_id):
        conn = self._create_connection()
        if not conn: return False
        try:
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction()
            cursor.execute("SELECT * FROM trades WHERE id = %s AND status = 'pendiente' FOR UPDATE", (trade_id,))
            trade = cursor.fetchone()
            if not trade: raise Error("Trade no encontrado o no está pendiente")
            p_user, p_prod = trade['proposer_user_id'], trade['proposer_product_id']
            r_user, r_prod = trade['receiver_user_id'], trade['receiver_product_id']
            cursor.execute("UPDATE products SET owner_user_id = %s WHERE id = %s", (r_user, p_prod))
            cursor.execute("UPDATE products SET owner_user_id = %s WHERE id = %s", (p_user, r_prod))
            cursor.execute("UPDATE trades SET status = 'completado' WHERE id = %s", (trade_id,))
            cursor.execute("UPDATE trades SET status = 'cancelado' WHERE (proposer_product_id = %s OR receiver_product_id = %s OR proposer_product_id = %s OR receiver_product_id = %s) AND status = 'pendiente' AND id != %s",
                           (p_prod, p_prod, r_prod, r_prod, trade_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Error en la transacción del trade: {e}")
            conn.rollback()
            return False
        finally:
            if conn.is_connected(): cursor.close(); conn.close()