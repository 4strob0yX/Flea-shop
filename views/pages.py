# views/pages.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

try:
    from . import theme
    from .components import AppHeader, ProductCard
except ImportError:
    import theme
    from components import AppHeader, ProductCard

# Registrar CartPage en el sistema de vistas si es necesario

class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller): super().__init__(parent, fg_color=theme.COLOR_FONDO_APP); self.controller = controller
    def update_data(self, **kwargs): pass


# --- Página de Carrito de Compras ---
class CartPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(0, weight=1)
        AppHeader(self, controller).grid(row=0, column=0, sticky="ew")
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=(10,20))
        ctk.CTkButton(btn_frame, text="Comprar todo", font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.controller.handle_buy_cart).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).pack(side="left", padx=10)

    def update_data(self, products=None):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        if products:
            for i, product in enumerate(products):
                self.scrollable_frame.grid_columnconfigure(i % 4, weight=1, uniform="card")
                card = ProductCard(self.scrollable_frame, product, self.controller, show_cart_remove=True)
                card.grid(row=i//4, column=i%4, padx=15, pady=15, sticky="nsew")
        else:
            ctk.CTkLabel(self.scrollable_frame, text="Tu carrito está vacío.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True, padx=20, pady=50)

class PurchasesPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(0, weight=1)
        AppHeader(self, controller).grid(row=0, column=0, sticky="ew")
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).grid(row=2, column=0, pady=(10,20))
    def update_data(self, products=None):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        if products:
            for i, product in enumerate(products):
                self.scrollable_frame.grid_columnconfigure(i % 4, weight=1, uniform="card")
                ProductCard(self.scrollable_frame, product, self.controller).grid(row=i//4, column=i%4, padx=15, pady=15, sticky="nsew")
        else:
            ctk.CTkLabel(self.scrollable_frame, text="No has comprado productos aún.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True, padx=20, pady=50)

class LoginPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        frame = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=15, border_width=1, border_color=theme.COLOR_BORDE); frame.place(relx=0.5, rely=0.5, anchor="center")
        self.inner_frame = ctk.CTkFrame(frame, fg_color="transparent"); self.inner_frame.pack(padx=40, pady=40)
        ctk.CTkLabel(self.inner_frame, text="Inicia Sesión", font=theme.FUENTE_TITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(pady=(0, 30))
        ctk.CTkLabel(self.inner_frame, text="Correo Electrónico", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")
        self.email_entry = ctk.CTkEntry(self.inner_frame, width=350, height=45, font=theme.FUENTE_NORMAL, border_color=theme.COLOR_BORDE); self.email_entry.pack(pady=(5, 15))
        ctk.CTkLabel(self.inner_frame, text="Contraseña", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")
        self.password_entry = ctk.CTkEntry(self.inner_frame, show="*", width=350, height=45, font=theme.FUENTE_NORMAL, border_color=theme.COLOR_BORDE); self.password_entry.pack(pady=(5, 25))
        self.password_entry.bind("<Return>", self.login)
        ctk.CTkButton(self.inner_frame, text="Iniciar Sesión", height=45, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.login).pack(fill="x", pady=10)
        register_label = ctk.CTkLabel(self.inner_frame, text="¿No tienes cuenta? Regístrate", text_color=theme.COLOR_PRIMARIO, font=("Helvetica", 12, "underline"), cursor="hand2"); register_label.pack(pady=(20, 0))
        register_label.bind("<Button-1>", lambda e: self.controller.view.switch("register"))
    def login(self, event=None):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not email or not password:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Introduce un correo electrónico válido.")
            return
        self.controller.handle_login(email, password)
    def clear_fields(self): self.email_entry.delete(0, "end"); self.password_entry.delete(0, "end")

class RegisterPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.fields = {}
        frame = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=15, border_width=1, border_color=theme.COLOR_BORDE)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.inner_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent", width=420, height=500)
        self.inner_frame.pack(padx=40, pady=40, fill="both", expand=True)
        ctk.CTkLabel(self.inner_frame, text="Crear una Cuenta", font=theme.FUENTE_TITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(pady=(0, 30))
        # import os
        # import tkinter.filedialog as fd
        # self.selected_profile_image = None
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo Electrónico",
            "password": "Contraseña",
            "confirm_password": "Confirmar Contraseña"
        }
        for key, text in labels.items():
            ctk.CTkLabel(self.inner_frame, text=text, font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")
            entry = ctk.CTkEntry(self.inner_frame, width=350, height=45, font=theme.FUENTE_NORMAL, border_color=theme.COLOR_BORDE, show="*" if "Contraseña" in text else "")
            entry.pack(pady=(5, 15)); self.fields[key] = entry
        # Imagen de perfil eliminada del registro (solo editable en perfil)
        self.register_btn = ctk.CTkButton(self.inner_frame, text="Registrarse", height=45, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.register)
        self.register_btn.pack(fill="x", pady=10)
        self.login_label = ctk.CTkLabel(self.inner_frame, text="¿Ya tienes cuenta? Inicia Sesión", text_color=theme.COLOR_PRIMARIO, font=("Helvetica", 12, "underline"), cursor="hand2")
        self.login_label.pack(pady=(20, 0))
        self.login_label.bind("<Button-1>", lambda e: self.controller.view.switch("login"))
    # select_profile_image eliminado del registro
    def register(self):
        import os, shutil
        # Definir todos los campos relevantes del registro
        campos_registro = [
            "username", "email", "password", "confirm_password"
        ]
        # Obtener todos los campos, asegurando que todos estén presentes aunque estén vacíos
        data = {key: self.fields[key].get().strip() if key in self.fields else '' for key in campos_registro}
        pwd = data['password']
        conf_pwd = data['confirm_password']
        # Mensaje de depuración para ver los valores reales
        messagebox.showinfo("Debug", f"Password: '{pwd}'\nConfirm: '{conf_pwd}'\nIguales: {pwd == conf_pwd}")
        if not data['username'] or not data['email'] or not pwd or not conf_pwd:
            messagebox.showerror("Error", "Por favor, completa los campos obligatorios.")
            return
        if "@" not in data["email"] or "." not in data["email"]:
            messagebox.showerror("Error", "Introduce un correo electrónico válido.")
            return
        if pwd != conf_pwd:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        # No guardar imagen de perfil en el registro
        data['foto_perfil'] = ''  # Solo se podrá editar en la página de perfil
        # Eliminar confirm_password antes de enviar
        data.pop('confirm_password', None)
        # Asegurar que todos los campos relevantes estén presentes aunque estén vacíos
        campos_relevantes = [
            "nombre", "apellidos", "username", "email", "password", "telefono", "direccion", "fecha_nacimiento", "foto_perfil"
        ]
        for campo in campos_relevantes:
            if campo not in data:
                data[campo] = ''
        # Solo mostrar mensaje si el registro fue exitoso
        registro_ok = self.controller.handle_registration(data)
        if registro_ok:
            messagebox.showinfo("Éxito", "Registro exitoso. Ahora puedes iniciar sesión.")

class MainShopPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(0, weight=1)
        AppHeader(self, controller).grid(row=0, column=0, sticky="ew")
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
    def update_data(self, products=None):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        # Filtrar productos vendidos
        productos_disponibles = []
        if products:
            productos_disponibles = [p for p in products if not (p.get('vendido', 0) == 1 or p.get('vendido', False))]
        if productos_disponibles:
            for i, product in enumerate(productos_disponibles):
                self.scrollable_frame.grid_columnconfigure(i % 4, weight=1, uniform="card")
                ProductCard(self.scrollable_frame, product, self.controller).grid(row=i//4, column=i%4, padx=15, pady=15, sticky="nsew")
        else:
            ctk.CTkLabel(self.scrollable_frame, text="No hay productos disponibles.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True, padx=20, pady=50)

class ProductDetailPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(0, weight=1)
        AppHeader(self, controller).grid(row=0, column=0, sticky="ew")
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent"); self.content_frame.grid(row=1, column=0, sticky="nsew", padx=60, pady=30)
        ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).grid(row=2, column=0, pady=(10,20))
    def update_data(self, product=None):
        import os
        for widget in self.content_frame.winfo_children(): widget.destroy()
        if not product: return
        self.content_frame.grid_columnconfigure(0, weight=2); self.content_frame.grid_columnconfigure(1, weight=3); self.content_frame.grid_rowconfigure(0, weight=1)
        img_frame = ctk.CTkFrame(self.content_frame, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=12, border_color=theme.COLOR_BORDE, border_width=1); img_frame.grid(row=0, column=0, sticky="nsew")
        img_path = product.get('imagen_path', '')
        if img_path:
            abs_img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', img_path))
        else:
            abs_img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', 'placeholder.png'))
        if os.path.exists(abs_img_path) and os.path.isfile(abs_img_path):
            img = Image.open(abs_img_path)
        else:
            img = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', 'placeholder.png')))
        ctk.CTkLabel(img_frame, image=ctk.CTkImage(light_image=img, size=(450, 450)), text="").pack(expand=True, padx=20, pady=20)
        details_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent"); details_frame.grid(row=0, column=1, sticky="nw", padx=(40, 0), pady=20)
        ctk.CTkLabel(details_frame, text=product['nombre'], font=theme.FUENTE_TITULO, wraplength=500, justify="left", text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")
        ctk.CTkLabel(details_frame, text=f"Vendido por: {product.get('owner_name', 'N/A')}", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_SECUNDARIO).pack(anchor="w", pady=5)
        ctk.CTkLabel(details_frame, text=f"Precio: ${product.get('precio', 'N/A')}", font=theme.FUENTE_BOLD, text_color=theme.COLOR_PRIMARIO, anchor="w").pack(anchor="w", pady=5)
        ctk.CTkLabel(details_frame, text="Descripción", font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(details_frame, text=product['descripcion'], font=theme.FUENTE_NORMAL, wraplength=500, justify="left", text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")

        # Overlay de vendido
        if product.get('vendido', 0) == 1 or product.get('vendido', False):
            overlay = ctk.CTkLabel(img_frame, text="VENDIDO", font=theme.FUENTE_BOLD, fg_color="#D32F2F", text_color="white", corner_radius=8)
            overlay.place(relx=0.5, rely=0.5, anchor="center")

        # Botones de acción para usuarios logueados que no son dueños
        if self.controller.current_user and product['owner_user_id'] != self.controller.current_user['id']:
            btn_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            btn_frame.pack(anchor="w", pady=30)
            # Botón de carrito solo si NO es del usuario actual
            is_owner = product['owner_user_id'] == self.controller.current_user['id']
            if not is_owner:
                in_cart = False
                if hasattr(self.controller, 'get_cart_status'):
                    try:
                        in_cart = self.controller.get_cart_status(product['id'])
                    except Exception:
                        in_cart = False
                cart_btn = ctk.CTkButton(
                    btn_frame, text=("En carrito" if in_cart else "Agregar al carrito"), width=140, height=46,
                    font=theme.FUENTE_BOLD,
                    fg_color=(theme.COLOR_PRIMARIO if not in_cart else "#AAAAAA"),
                    hover_color=(theme.COLOR_PRIMARIO_HOVER if not in_cart else "#888888"),
                    state=("disabled" if in_cart or product.get('vendido', 0) == 1 or product.get('vendido', False) else "normal"),
                    command=lambda: self.controller.handle_add_to_cart(product['id'])
                )
                cart_btn.pack(side="left", padx=(0, 20))
            # Comprar
            buy_btn = ctk.CTkButton(
                btn_frame, text="Comprar", font=theme.FUENTE_BOLD, height=46,
                fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER,
                state=("disabled" if product.get('vendido', 0) == 1 or product.get('vendido', False) else "normal"),
                command=lambda: self.controller.handle_buy_product(product['id'])
            )
            buy_btn.pack(side="left", padx=(0, 20))
            # Proponer intercambio (solo si no está vendido)
            ctk.CTkButton(
                btn_frame,
                text="Proponer Intercambio",
                font=theme.FUENTE_BOLD,
                height=46,
                fg_color=theme.COLOR_PRIMARIO,
                hover_color=theme.COLOR_PRIMARIO_HOVER,
                state=("disabled" if product.get('vendido', 0) == 1 or product.get('vendido', False) else "normal"),
                command=lambda p=product: self.controller.show_propose_trade_page(p)
            ).pack(side="left")

class ProfilePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # Layout horizontal: perfil a la izquierda, productos a la derecha
        self.user_entries = {}
        # Botón volver fijo abajo
        self.menu_btn = None
        self._ensure_menu_btn()

    def _ensure_menu_btn(self):
        if not hasattr(self, 'menu_btn') or self.menu_btn is None or not self.menu_btn.winfo_exists():
            self.menu_btn = ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page)
            self.menu_btn.pack(side="bottom", fill="x", pady=(10, 20))
    def update_data(self, user=None, products=None):
        # Destruye el container anterior si existe
        if hasattr(self, 'container') and self.container is not None:
            self.container.destroy()
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        # No destruir el botón fijo de menú
        for widget in self.winfo_children():
            if widget is not self.container and widget is not self.menu_btn:
                widget.destroy()
        self._ensure_menu_btn()
        self.user_entries.clear()  # Limpia referencias a entradas antiguas
        if not user:
            return
        # Si products no viene como argumento, lo obtenemos del modelo
        if products is None and hasattr(self.controller, 'model') and hasattr(self.controller, 'current_user_id'):
            products = self.controller.model.get_user_products(self.controller.current_user_id)
        profile_panel = ctk.CTkFrame(self.container, fg_color=theme.COLOR_FONDO_SIDEBAR, corner_radius=0, width=480)
        profile_panel.pack(side="left", fill="y")
        self.inner_profile_frame = ctk.CTkScrollableFrame(profile_panel, fg_color="transparent", width=420, height=600)
        self.inner_profile_frame.pack(padx=30, pady=30, fill="both", expand=True)
        ctk.CTkLabel(self.inner_profile_frame, text="Mi Perfil", font=theme.FUENTE_SUBTITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(0, 20))
        import os
        import tkinter.filedialog as fd
        from PIL import Image
        self.selected_profile_image = None
        labels = {
            "nombre": "Nombre:", "apellidos": "Apellidos:", "username": "Nombre de usuario:", "email": "Correo electrónico:",
            "telefono": "Teléfono:", "direccion": "Dirección:", "fecha_nacimiento": "Fecha de nacimiento (YYYY-MM-DD):",
            "nivel": "Nivel:", "reputacion": "Reputación:", "estado": "Estado:", "verificado": "Verificado (0/1):"
        }
        for key, text in labels.items():
            ctk.CTkLabel(self.inner_profile_frame, text=text, font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(10,0))
            value = user.get(key, '') if user else ''
            entry = ctk.CTkEntry(self.inner_profile_frame, font=theme.FUENTE_NORMAL, height=40, state="disabled" if key in ["email"] else "normal", fg_color="#FFFFFF", border_color=theme.COLOR_BORDE, text_color=theme.COLOR_TEXTO_PRINCIPAL)
            entry.insert(0, str(value) if value is not None else '')
            entry.pack(fill="x", pady=(5,0))
            self.user_entries[key] = entry
        # Imagen de perfil y botones (dentro del ámbito correcto)
        self.img_label = ctk.CTkLabel(self.inner_profile_frame, text="No se ha seleccionado imagen de perfil", font=("Arial", 12), text_color=theme.COLOR_TEXTO_PRINCIPAL)
        self.img_label.pack(pady=(10, 5))
        self.img_preview = ctk.CTkLabel(self.inner_profile_frame, text="", image=None)
        self.img_preview.pack(pady=(0, 10))
        if user and user.get('foto_perfil'):
            abs_img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', user['foto_perfil']))
            if os.path.exists(abs_img_path):
                try:
                    img = Image.open(abs_img_path)
                    img.thumbnail((120, 120))
                    self._img_preview_obj = ctk.CTkImage(light_image=img, size=(120, 120))
                    self.img_preview.configure(image=self._img_preview_obj, text="")
                    self.img_label.configure(text=os.path.basename(user['foto_perfil']), text_color=theme.COLOR_PRIMARIO)
                except Exception:
                    self.img_preview.configure(image=None, text="Error al cargar imagen")
        ctk.CTkButton(self.inner_profile_frame, text="Seleccionar Imagen de Perfil", font=theme.FUENTE_NORMAL, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.select_profile_image).pack(fill="x", pady=(0, 10))
        self.edit_button = ctk.CTkButton(self.inner_profile_frame, text="Editar Perfil", height=40, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.toggle_edit_mode)
        self.edit_button.pack(pady=30, fill="x")
        # (El botón de volver ya está fijo abajo, no se agrega aquí)
        # Panel de productos (derecha)
        self.products_panel = ctk.CTkFrame(self.container, fg_color="transparent")
        self.products_panel.pack(side="left", fill="both", expand=True, padx=30, pady=20)
        top_bar = ctk.CTkFrame(self.products_panel, fg_color="transparent")
        top_bar.pack(fill="x", pady=(10,0))
        ctk.CTkLabel(top_bar, text="Mis Artículos en Venta", font=theme.FUENTE_SUBTITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(side="left")
        ctk.CTkButton(top_bar, text="+ Vender Artículo", font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.controller.show_add_product_form).pack(side="right")
        self.products_list = ctk.CTkScrollableFrame(self.products_panel, fg_color=theme.COLOR_FONDO_FRAME, border_color=theme.COLOR_BORDE, border_width=1, corner_radius=8)
        self.products_list.pack(fill="both", expand=True, pady=20)
        # Mostrar productos
        if products:
            for p in products:
                p_frame = ctk.CTkFrame(self.products_list, fg_color=theme.COLOR_FONDO_FRAME, border_width=1, border_color=theme.COLOR_BORDE)
                p_frame.pack(fill="x", pady=8, padx=8)
                ctk.CTkLabel(p_frame, text=p['nombre'], font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(side="left", padx=15, pady=15)
                ctk.CTkButton(
                    p_frame,
                    text="Eliminar",
                    width=80,
                    font=theme.FUENTE_NORMAL,
                    fg_color="#D32F2F",
                    hover_color="#B71C1C",
                    command=lambda p_id=p['id']: self.confirm_delete_product(p_id)
                ).pack(side="right", padx=(10,15))
                ctk.CTkButton(
                    p_frame,
                    text="Editar",
                    width=80,
                    font=theme.FUENTE_NORMAL,
                    fg_color="#AAAAAA",
                    hover_color="#888888",
                    command=lambda prod=p: self.controller.show_edit_product_form(prod)
                ).pack(side="right")
        else:
            ctk.CTkLabel(self.products_list, text="Aún no tienes artículos en venta.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True, padx=20, pady=50)
    def select_profile_image(self):
        import os
        import tkinter.filedialog as fd
        from PIL import Image
        filetypes = [("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")]
        filename = fd.askopenfilename(title="Seleccionar imagen de perfil", filetypes=filetypes)
        if filename:
            self.selected_profile_image = filename
            self.img_label.configure(text=os.path.basename(filename), text_color=theme.COLOR_PRIMARIO)
            try:
                img = Image.open(filename)
                img.thumbnail((120, 120))
                self._img_preview_obj = ctk.CTkImage(light_image=img, size=(120, 120))
                self.img_preview.configure(image=self._img_preview_obj, text="")
            except Exception:
                self.img_preview.configure(image=None, text="Error al cargar imagen")
        else:
            self.selected_profile_image = None
            self.img_label.configure(text="No se ha seleccionado imagen de perfil", text_color=theme.COLOR_TEXTO_PRINCIPAL)
            self.img_preview.configure(image=None, text="")
        self.edit_button = ctk.CTkButton(self.inner_profile_frame, text="Editar Perfil", height=40, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.toggle_edit_mode); self.edit_button.pack(pady=30, fill="x")
        # Botón Volver al menú principal
        ctk.CTkButton(self.inner_profile_frame, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).pack(fill="x", pady=(0, 10))
        self.products_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.products_panel.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.products_panel.grid_rowconfigure(1, weight=1)
        self.products_panel.grid_columnconfigure(0, weight=1)
        top_bar = ctk.CTkFrame(self.products_panel, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(10,0))
        ctk.CTkLabel(top_bar, text="Mis Artículos en Venta", font=theme.FUENTE_SUBTITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(side="left")
        ctk.CTkButton(top_bar, text="+ Vender Artículo", font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.controller.show_add_product_form).pack(side="right")
        self.products_list = ctk.CTkScrollableFrame(self.products_panel, fg_color=theme.COLOR_FONDO_FRAME, border_color=theme.COLOR_BORDE, border_width=1, corner_radius=8)
        self.products_list.grid(row=1, column=0, sticky="nsew", pady=20)
        # Asegura que products esté definido correctamente
        if products is None and hasattr(self.controller, 'model') and hasattr(self.controller, 'current_user'):
            products = self.controller.model.get_user_products(self.controller.current_user['id'])
        if products:
            for p in products:
                p_frame = ctk.CTkFrame(self.products_list, fg_color=theme.COLOR_FONDO_FRAME, border_width=1, border_color=theme.COLOR_BORDE)
                p_frame.pack(fill="x", pady=8, padx=8)
                ctk.CTkLabel(p_frame, text=p['nombre'], font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(side="left", padx=15, pady=15)
                ctk.CTkButton(
                    p_frame,
                    text="Eliminar",
                    width=80,
                    font=theme.FUENTE_NORMAL,
                    fg_color="#D32F2F",
                    hover_color="#B71C1C",
                    command=lambda p_id=p['id']: self.confirm_delete_product(p_id)
                ).pack(side="right", padx=(10,15))
                ctk.CTkButton(
                    p_frame,
                    text="Editar",
                    width=80,
                    font=theme.FUENTE_NORMAL,
                    fg_color="#AAAAAA",
                    hover_color="#888888",
                    command=lambda prod=p: self.controller.show_edit_product_form(prod)
                ).pack(side="right")
        else:
            ctk.CTkLabel(self.products_list, text="Aún no tienes artículos en venta.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True, padx=20, pady=50)

    def confirm_delete_product(self, product_id):
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este producto? Esta acción no se puede deshacer."):
            self.controller.handle_delete_product(product_id)
    def toggle_edit_mode(self):
        for key, entry in self.user_entries.items():
            if key != "email":
                entry.configure(state="normal")
        self.edit_button.configure(text="Guardar Cambios", command=self.save_profile)
    def save_profile(self):
        import os, shutil
        data = {key: entry.get().strip() for key, entry in self.user_entries.items()}
        # Guardar imagen de perfil si se seleccionó una nueva
        if self.selected_profile_image:
            images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))
            os.makedirs(images_dir, exist_ok=True)
            ext = os.path.splitext(self.selected_profile_image)[1]
            dest_filename = f"perfil_{data['username']}{ext}"
            dest_path = os.path.join(images_dir, dest_filename)
            try:
                shutil.copy2(self.selected_profile_image, dest_path)
                data['foto_perfil'] = f"images/{dest_filename}"
            except Exception:
                data['foto_perfil'] = ''
        self.controller.handle_update_profile(data)
        messagebox.showinfo("Éxito", "Perfil actualizado correctamente.")

class ProductFormPage(BasePage):
    def __init__(self, parent, controller):
        import os
        import shutil
        import tkinter.filedialog as fd
        super().__init__(parent, controller)
        self.product_id, self.fields = None, {}
        self.selected_image_path = None
        frame = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=15, border_width=1, border_color=theme.COLOR_BORDE); frame.place(relx=0.5, rely=0.5, anchor="center")
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent"); inner_frame.pack(padx=40, pady=40)
        self.title_label = ctk.CTkLabel(inner_frame, text="", font=theme.FUENTE_TITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL); self.title_label.pack(pady=(0, 30))
        labels = {"nombre": "Nombre del Artículo", "precio": "Precio (MXN)", "descripcion": "Descripción"}
        for key, text in labels.items():
            ctk.CTkLabel(inner_frame, text=text, font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")
            entry = ctk.CTkTextbox(inner_frame, width=400, height=120, font=theme.FUENTE_NORMAL, border_color=theme.COLOR_BORDE, text_color=theme.COLOR_TEXTO_PRINCIPAL, border_width=1) if key == "descripcion" else ctk.CTkEntry(inner_frame, width=400, height=45, font=theme.FUENTE_NORMAL, border_color=theme.COLOR_BORDE)
            entry.pack(pady=(5,15)); self.fields[key] = entry
        # Botón para seleccionar imagen
        self.img_label = ctk.CTkLabel(inner_frame, text="No se ha seleccionado imagen", font=("Arial", 12), text_color=theme.COLOR_TEXTO_PRINCIPAL)
        self.img_label.pack(pady=(10, 5))
        self.img_preview = ctk.CTkLabel(inner_frame, text="", image=None)
        self.img_preview.pack(pady=(0, 10))
        ctk.CTkButton(inner_frame, text="Seleccionar Imagen", font=theme.FUENTE_NORMAL, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.select_image).pack(fill="x", pady=(0, 10))
        ctk.CTkButton(inner_frame, text="Guardar Producto", height=45, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.save).pack(fill="x", pady=10)
        ctk.CTkButton(inner_frame, text="Cancelar", height=45, font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=controller.show_profile_page).pack(fill="x", pady=(5,0))
        ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).pack(side="bottom", pady=(10,20))

    def select_image(self):
        import os
        import tkinter.filedialog as fd
        from PIL import Image
        filetypes = [("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp;*.tiff;*.tif")]
        filename = fd.askopenfilename(title="Seleccionar imagen", filetypes=filetypes)
        if filename:
            self.selected_image_path = filename
            self.img_label.configure(text=os.path.basename(filename), text_color=theme.COLOR_PRIMARIO)
            try:
                img = Image.open(filename)
                img.thumbnail((200, 200))
                img_preview_obj = ctk.CTkImage(light_image=img, size=(200, 200))
                self.img_preview.configure(image=img_preview_obj, text="")
                self.img_preview.image = img_preview_obj  # Mantener referencia
            except Exception:
                self.img_preview.configure(image=None, text="Error al cargar imagen")
                self.img_preview.image = None
        else:
            self.selected_image_path = None
            self.img_label.configure(text="No se ha seleccionado imagen", text_color=theme.COLOR_TEXTO_PRINCIPAL)
            self.img_preview.configure(image=None, text="")
            self.img_preview.image = None

    def update_data(self, product=None):
        import os
        from PIL import Image
        for entry in self.fields.values():
            if isinstance(entry, ctk.CTkTextbox):
                entry.delete("1.0", "end")
            else:
                entry.delete(0, "end")
        self.selected_image_path = None
        self.img_label.configure(text="No se ha seleccionado imagen", text_color=theme.COLOR_TEXTO_PRINCIPAL)
        self.img_preview.configure(image=None, text="")
        self.img_preview.image = None
        # Siempre crea un nuevo objeto de imagen para evitar errores de referencia
        if product:
            self.title_label.configure(text="Editar Producto"); self.product_id = product['id']
            self.fields['nombre'].insert(0, product.get('nombre', ''))
            self.fields['precio'].insert(0, str(product.get('precio', '')))
            self.fields['descripcion'].insert("1.0", product.get('descripcion', ''))
            if product.get('imagen_path'):
                self.selected_image_path = product['imagen_path']
                self.img_label.configure(text=os.path.basename(product['imagen_path']), text_color=theme.COLOR_PRIMARIO)
                try:
                    abs_img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', product['imagen_path']))
                    if os.path.exists(abs_img_path):
                        img = Image.open(abs_img_path)
                        img.thumbnail((200, 200))
                        img_preview_obj = ctk.CTkImage(light_image=img, size=(200, 200))
                        self.img_preview.configure(image=img_preview_obj, text="")
                        self.img_preview.image = img_preview_obj  # Mantener referencia
                    else:
                        self.img_preview.configure(image=None, text="No se encontró la imagen")
                        self.img_preview.image = None
                except Exception:
                    self.img_preview.configure(image=None, text="Error al cargar imagen")
                    self.img_preview.image = None
        else:
            self.title_label.configure(text="Vender un Artículo"); self.product_id = None
            self.img_preview.configure(image=None, text="")
            self.img_preview.image = None
    def save(self):
        import os
        import shutil
        nombre = self.fields['nombre'].get().strip()
        precio = self.fields['precio'].get().strip()
        descripcion = self.fields['descripcion'].get("1.0", "end-1c").strip()
        if not nombre or not precio or not descripcion:
            messagebox.showerror("Error", "Por favor, completa todos los campos del producto.")
            return
        try:
            precio_float = float(precio)
            if precio_float < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número positivo.")
            return
        data = {
            'nombre': nombre,
            'precio': precio_float,
            'descripcion': descripcion
        }
        # Guardar imagen en carpeta images y guardar ruta relativa
        if self.selected_image_path:
            images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))
            os.makedirs(images_dir, exist_ok=True)
            ext = os.path.splitext(self.selected_image_path)[1]
            dest_filename = f"{data['nombre'].replace(' ', '_')}_{self.product_id or 'nuevo'}{ext}"
            dest_path = os.path.join(images_dir, dest_filename)
            try:
                shutil.copy2(self.selected_image_path, dest_path)
                # Guardar siempre como 'images/nombre_archivo.ext'
                data['imagen_path'] = f"images/{dest_filename}"
            except Exception as e:
                data['imagen_path'] = ''
        else:
            data['imagen_path'] = ''
        self.controller.handle_save_product(data, self.product_id)
        messagebox.showinfo("Éxito", "Producto guardado correctamente.")

class ProposeTradePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.target_product, self.user_products_map = None, {}
        frame = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=15, border_width=1, border_color=theme.COLOR_BORDE); frame.place(relx=0.5, rely=0.5, anchor="center")
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent"); inner_frame.pack(padx=40, pady=40, fill="x")
        ctk.CTkLabel(inner_frame, text="Proponer Intercambio", font=theme.FUENTE_TITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(pady=(0, 20))
        self.target_label = ctk.CTkLabel(inner_frame, text="Artículo deseado: ", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL); self.target_label.pack(anchor="w")
        ctk.CTkLabel(inner_frame, text="\nOfrecer a cambio:", font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(10,5))
        self.offer_menu = ctk.CTkOptionMenu(
            inner_frame,
            height=45,
            font=theme.FUENTE_NORMAL,
            fg_color="white",
            button_color=theme.COLOR_PRIMARIO,
            button_hover_color=theme.COLOR_PRIMARIO_HOVER,
            dropdown_font=theme.FUENTE_NORMAL,
            text_color=theme.COLOR_TEXTO_PRINCIPAL
        );
        self.offer_menu.pack(fill="x")
        ctk.CTkButton(inner_frame, text="Enviar Propuesta", height=45, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.propose).pack(fill="x", pady=(30,10))
        ctk.CTkButton(inner_frame, text="Cancelar", height=45, font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).pack(fill="x")
        ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).pack(side="bottom", pady=(10,20))
    def update_data(self, target_product=None, user_products=None):
        if not target_product or not user_products: return
        self.target_product = target_product
        self.target_label.configure(text=f"Artículo deseado: {target_product['nombre']}")
        # Filtrar solo productos NO vendidos
        disponibles = [p for p in user_products if not (p.get('vendido', 0) == 1 or p.get('vendido', False))]
        self.user_products_map = {p['nombre']: p['id'] for p in disponibles}
        product_names = list(self.user_products_map.keys())
        if product_names:
            self.offer_menu.configure(values=product_names)
            self.offer_menu.set(product_names[0])
        else:
            self.offer_menu.configure(values=["No tienes artículos disponibles"])
            self.offer_menu.set("No tienes artículos disponibles")
    def propose(self):
        selected_product_name = self.offer_menu.get()
        proposer_product_id = self.user_products_map.get(selected_product_name)
        if proposer_product_id and self.target_product: self.controller.handle_create_trade(proposer_product_id, self.target_product)

class MyTradesPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(0, weight=1)
        AppHeader(self, controller).grid(row=0, column=0, sticky="ew")
        tabview = ctk.CTkTabview(self, fg_color=theme.COLOR_FONDO_FRAME, segmented_button_selected_color=theme.COLOR_PRIMARIO, segmented_button_selected_hover_color=theme.COLOR_PRIMARIO_HOVER, border_color=theme.COLOR_BORDE, border_width=1); tabview.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.received_tab, self.sent_tab = tabview.add("Propuestas Recibidas"), tabview.add("Propuestas Enviadas")
        ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).grid(row=2, column=0, pady=(10,20))
    def update_data(self, trades=None):
        for tab in [self.received_tab, self.sent_tab]:
            for widget in tab.winfo_children(): widget.destroy()
        received_scroll = ctk.CTkScrollableFrame(self.received_tab, fg_color="transparent"); received_scroll.pack(fill="both", expand=True)
        sent_scroll = ctk.CTkScrollableFrame(self.sent_tab, fg_color="transparent"); sent_scroll.pack(fill="both", expand=True)
        if not trades:
            ctk.CTkLabel(received_scroll, text="No has recibido ninguna propuesta.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True)
            ctk.CTkLabel(sent_scroll, text="No has enviado ninguna propuesta.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True)
            return
        current_user_id, received_count, sent_count = self.controller.current_user['id'], 0, 0
        status_colors = {"pendiente": "#333333", "aceptado": "#2ECC71", "rechazado": "#E74C3C", "cancelado": "#95A5A6", "completado": theme.COLOR_PRIMARIO}
        for trade in trades:
            parent_tab, text = (None, "")
            if trade['receiver_user_id'] == current_user_id: parent_tab, received_count, text = received_scroll, received_count + 1, f"{trade['proposer_name']} te ofrece '{trade['proposer_product_name']}' por tu '{trade['receiver_product_name']}'"
            else: parent_tab, sent_count, text = sent_scroll, sent_count + 1, f"Le ofreciste a {trade['receiver_name']} tu '{trade['proposer_product_name']}' por su '{trade['receiver_product_name']}'"
            card = ctk.CTkFrame(parent_tab, fg_color="white", border_width=1, border_color=theme.COLOR_BORDE); card.pack(fill="x", padx=10, pady=8)
            ctk.CTkLabel(card, text=text, font=theme.FUENTE_NORMAL, wraplength=700, justify="left", text_color="#222222").pack(side="left", padx=15, pady=15)
            button_frame = ctk.CTkFrame(card, fg_color="transparent"); button_frame.pack(side="right", padx=15, pady=10)
            status = trade['status']
            # Mejorar visibilidad del estado
            bg_map = {
                "pendiente": "#FFFBE0",
                "aceptado": "#E0FFE0",
                "rechazado": "#FFE0E0",
                "cancelado": "#F0F0F0",
                "completado": "#D0F5E0"
            }
            ctk.CTkLabel(
                button_frame,
                text=status.capitalize(),
                font=("Arial", 16, "bold"),
                text_color=status_colors.get(status, "#333333"),  # Asegura color visible
                fg_color=bg_map.get(status, "white"),
                corner_radius=8,
                width=120,
                height=30
            ).pack(pady=5)
            if status == 'pendiente':
                if trade['receiver_user_id'] == current_user_id:
                    ctk.CTkButton(button_frame, text="Aceptar", fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, width=100, command=lambda t_id=trade['id']: self.controller.handle_update_trade(t_id, 'aceptado')).pack(side="left", padx=5)
                    ctk.CTkButton(button_frame, text="Rechazar", fg_color="#D32F2F", hover_color="#B71C1C", width=100, command=lambda t_id=trade['id']: self.controller.handle_update_trade(t_id, 'rechazado')).pack(side="left")
                else:
                    ctk.CTkButton(button_frame, text="Cancelar", fg_color="#AAAAAA", hover_color="#888888", width=100, command=lambda t_id=trade['id']: self.controller.handle_update_trade(t_id, 'cancelado')).pack(side="left")
        if received_count == 0: ctk.CTkLabel(received_scroll, text="No has recibido ninguna propuesta.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True)
        if sent_count == 0: ctk.CTkLabel(sent_scroll, text="No has enviado ninguna propuesta.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True)