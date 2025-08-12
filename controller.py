# controller.py
from tkinter import messagebox
from views import utils # Importar el nuevo módulo de utilidades

class Controller:

    # --- Carrito de compras ---
    def show_cart_page(self):
        if not self.current_user:
            self.view.show_toast("Debes iniciar sesión para ver tu carrito.", bg_color="#D32F2F")
            return
        cart_products = self.model.get_cart_products(self.current_user['id'])
        self.view.switch("cart", products=cart_products)

    def show_purchases_page(self):
        if not self.current_user:
            self.view.show_toast("Debes iniciar sesión para ver tus compras.", bg_color="#D32F2F")
            return
        purchases = self.model.get_user_purchases(self.current_user['id'])
        self.view.switch("purchases", products=purchases)

    def handle_add_to_cart(self, product_id):
        if not self.current_user:
            self.view.show_toast("Debes iniciar sesión para agregar al carrito.", bg_color="#D32F2F")
            return
        user_id = self.current_user['id']
        added = self.model.add_to_cart(user_id, product_id)
        if added:
            self.view.show_toast("Agregado al carrito.")
        else:
            self.view.show_toast("Error al agregar al carrito.", bg_color="#D32F2F")
        self.show_product_detail(product_id)

    def handle_remove_from_cart(self, product_id):
        if not self.current_user:
            self.view.show_toast("Debes iniciar sesión para modificar el carrito.", bg_color="#D32F2F")
            return
        user_id = self.current_user['id']
        removed = self.model.remove_from_cart(user_id, product_id)
        if removed:
            self.view.show_toast("Eliminado del carrito.")
        else:
            self.view.show_toast("Error al quitar del carrito.", bg_color="#D32F2F")
        self.show_cart_page()

    def handle_buy_cart(self):
        if not self.current_user:
            self.view.show_toast("Debes iniciar sesión para comprar.", bg_color="#D32F2F")
            return
        user_id = self.current_user['id']
        cart = self.model.get_user_cart(user_id)
        if not cart:
            self.view.show_toast("El carrito está vacío.")
            return
        success = True
        for product_id in cart:
            result = self.model.buy_product(user_id, product_id)
            if not result:
                success = False
        self.model.clear_cart(user_id)
        if success:
            self.view.show_toast("¡Compra realizada con éxito!")
        else:
            self.view.show_toast("Algunos productos no se pudieron comprar.", bg_color="#D32F2F")
        self.show_main_shop_page()

    def get_cart_status(self, product_id):
        if not self.current_user:
            return False
        cart = self.model.get_user_cart(self.current_user['id'])
        return product_id in cart

    # --- Compra directa ---
    def handle_buy_product(self, product_id):
        if not self.current_user:
            self.view.show_toast("Debes iniciar sesión para comprar.", bg_color="#D32F2F")
            return
        user_id = self.current_user['id']
        result = self.model.buy_product(user_id, product_id)
        if result:
            self.view.show_toast("¡Compra realizada con éxito!")
            self.show_main_shop_page()
        else:
            self.view.show_toast("No se pudo completar la compra.", bg_color="#D32F2F")
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_user = None

    def start(self):
        self.view.switch("login")
        self.view.mainloop()

    def handle_login(self, email, password):
        if not email or not password:
            self.view.show_toast("Correo y contraseña son requeridos.", bg_color="#D32F2F")
            return
        user = self.model.check_user(email, password)
        if user:
            self.current_user = user
            self.view.show_toast(f"¡Bienvenido, {user['nombre']}!")
            self.show_main_shop_page()
        else:
            messagebox.showerror("Error de Sesión", "Correo o contraseña incorrectos.")
    
    def handle_registration(self, data):
        errors = utils.validate_registration_data(data)
        if errors:
            messagebox.showerror("Error de Registro", "\n".join(errors))
            return False

        if self.model.get_user_by_email(data['email']):
            messagebox.showerror("Error de Registro", "El correo electrónico ya está en uso.")
            return False

        data.pop('confirm_password', None)
        if self.model.create_user(data):
            self.logout()
            return True
        else:
            messagebox.showerror("Error de Registro", "Ocurrió un error inesperado al crear el usuario.")
            return False

    def logout(self):
        self.current_user = None
        if login_frame := self.view.get_frame("login"): login_frame.clear_fields()
        self.view.switch("login")

    def show_main_shop_page(self, search_term=None):
        products = self.model.get_all_products(search_term)
        self.view.switch("main_shop", products=products)
    
    def show_product_detail(self, product_id):
        product = self.model.get_product_by_id(product_id)
        if product: self.view.switch("product_detail", product=product)

    def show_profile_page(self):
        if not self.current_user: return
        user_data = self.model.get_user_by_id(self.current_user['id'])
        user_products = self.model.get_user_products(self.current_user['id'])
        self.view.switch("profile", user=user_data, products=user_products)

    def handle_update_profile(self, data):
        if self.model.update_user_profile(self.current_user['id'], data):
            self.view.show_toast("Perfil actualizado")
            self.current_user['nombre'] = data['nombre']
            self.show_profile_page()
        else:
            self.view.show_toast("Error al actualizar el perfil", bg_color="#D32F2F")

    def show_add_product_form(self):
        self.view.switch("product_form", product=None)

    def show_edit_product_form(self, product):
        if self.current_user and product['owner_user_id'] == self.current_user['id']:
            self.view.switch("product_form", product=product)
        else:
            messagebox.showerror("Acción denegada", "No tienes permiso para editar este producto.")

    def handle_save_product(self, data, product_id=None):
        if not self.current_user or not self.current_user.get('id'):
            messagebox.showerror("Error", "Debes iniciar sesión antes de agregar o editar un producto.")
            return

        errors = utils.validate_product_data(data)
        if errors:
            messagebox.showerror("Error de Validación", "\n".join(errors))
            return

        if product_id:
            success = self.model.update_product(data, product_id, self.current_user['id'])
            self.view.show_toast("Producto actualizado con éxito" if success else "Error al actualizar", bg_color=None if success else "#D32F2F")
        else:
            owner_id = self.current_user['id']
            print("ID de usuario actual:", owner_id)  # DEPURACIÓN
            if not isinstance(owner_id, int):
                try:
                    owner_id = int(owner_id)
                except Exception:
                    messagebox.showerror("Error", "ID de usuario inválido. No se puede agregar el producto.")
                    return
            data['owner_user_id'] = owner_id
            data['imagen_path'] = ""
            success = self.model.add_product(data)
            self.view.show_toast("Producto agregado con éxito" if success else "Error al agregar", bg_color=None if success else "#D32F2F")

        self.show_profile_page()

    def handle_delete_product(self, product_id):
        if messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que quieres eliminar este producto?"):
            if self.model.delete_product(product_id, self.current_user['id']):
                self.view.show_toast("Producto eliminado"); self.show_profile_page()
            else:
                self.view.show_toast("Error al eliminar", bg_color="#D32F2F")

    def show_my_trades_page(self):
        if not self.current_user: return
        trades = self.model.get_trades_for_user(self.current_user['id'])
        self.view.switch("my_trades", trades=trades)

    def show_propose_trade_page(self, target_product):
        if not self.current_user: messagebox.showerror("Error", "Debes iniciar sesión para proponer un intercambio."); return
        user_products = self.model.get_user_products(self.current_user['id'])
        if not user_products: messagebox.showinfo("Información", "No tienes artículos para intercambiar."); return
        self.view.switch("propose_trade", target_product=target_product, user_products=user_products)

    def handle_create_trade(self, proposer_product_id, target_product):
        success = self.model.create_trade(self.current_user['id'], proposer_product_id, target_product['owner_user_id'], target_product['id'])
        if success: self.view.show_toast("Propuesta de intercambio enviada.")
        else: self.view.show_toast("Error al enviar la propuesta.", bg_color="#D32F2F")
        self.show_main_shop_page()
            
    def handle_update_trade(self, trade_id, new_status):
        if new_status == 'aceptado':
            if self.model.execute_trade(trade_id): self.view.show_toast("¡Intercambio aceptado y completado!")
            else: self.view.show_toast("Error al procesar el intercambio.", bg_color="#D32F2F")
        else:
            if self.model.update_trade_status(trade_id, new_status): self.view.show_toast(f"Propuesta {new_status}.")
            else: self.view.show_toast("Error al actualizar la propuesta.", bg_color="#D32F2F")
        self.show_my_trades_page()