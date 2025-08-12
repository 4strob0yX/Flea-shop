# views/pages.py (VERSIÓN FINAL Y COMPLETA)
import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os
import shutil
from pathlib import Path

try:
    from . import theme
    from .components import AppHeader, ProductCard
except ImportError:
    import theme
    from components import AppHeader, ProductCard

class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.COLOR_FONDO_APP)
        self.controller = controller
    def update_data(self, **kwargs):
        pass

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
        self.register_btn = ctk.CTkButton(self.inner_frame, text="Registrarse", height=45, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.register)
        self.register_btn.pack(fill="x", pady=10)
        self.login_label = ctk.CTkLabel(self.inner_frame, text="¿Ya tienes cuenta? Inicia Sesión", text_color=theme.COLOR_PRIMARIO, font=("Helvetica", 12, "underline"), cursor="hand2")
        self.login_label.pack(pady=(20, 0))
        self.login_label.bind("<Button-1>", lambda e: self.controller.view.switch("register"))
    def register(self):
        campos_registro = ["username", "email", "password", "confirm_password"]
        data = {key: self.fields[key].get().strip() if key in self.fields else '' for key in campos_registro}
        if not all(data.values()):
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return
        if "@" not in data["email"] or "." not in data["email"]:
            messagebox.showerror("Error", "Introduce un correo electrónico válido.")
            return
        if data['password'] != data['confirm_password']:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        data['foto_perfil'] = ''
        data.pop('confirm_password', None)
        campos_relevantes = ["nombre", "apellidos", "username", "email", "password", "telefono", "direccion", "fecha_nacimiento", "foto_perfil"]
        for campo in campos_relevantes:
            if campo not in data: data[campo] = ''
        if self.controller.handle_registration(data):
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
        productos_disponibles = [p for p in products if not p.get('vendido')] if products else []
        if productos_disponibles:
            for i, product in enumerate(productos_disponibles):
                self.scrollable_frame.grid_columnconfigure(i % 4, weight=1, uniform="card")
                ProductCard(self.scrollable_frame, product, self.controller).grid(row=i//4, column=i%4, padx=15, pady=15, sticky="nsew")
        else:
            ctk.CTkLabel(self.scrollable_frame, text="No hay productos disponibles.", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(expand=True, padx=20, pady=50)

class ProductDetailPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(0, weight=1)
        AppHeader(self, controller).grid(row=0, column=0, sticky="ew")
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent"); self.content_frame.grid(row=1, column=0, sticky="nsew", padx=60, pady=30)
        ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).grid(row=2, column=0, pady=(10,20))

    def update_data(self, product=None):
        for widget in self.content_frame.winfo_children(): widget.destroy()
        if not product: return
        self.content_frame.grid_columnconfigure(0, weight=2); self.content_frame.grid_columnconfigure(1, weight=3); self.content_frame.grid_rowconfigure(0, weight=1)
        img_frame = ctk.CTkFrame(self.content_frame, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=12, border_color=theme.COLOR_BORDE, border_width=1); img_frame.grid(row=0, column=0, sticky="nsew")
        
        base_path = Path(__file__).parent.parent
        image_path_str = product.get("imagen_path", "")
        placeholder_path = base_path / "images" / "placeholder.png"
        abs_img_path = base_path / image_path_str if image_path_str else placeholder_path
        if not abs_img_path.is_file(): abs_img_path = placeholder_path

        try:
            img = Image.open(abs_img_path)
            self.img_preview_ref = ctk.CTkImage(light_image=img, size=(450, 450))
            ctk.CTkLabel(img_frame, image=self.img_preview_ref, text="").pack(expand=True, padx=20, pady=20)
        except Exception as e:
            print(f"Error loading image in detail view: {e}")
            ctk.CTkLabel(img_frame, text="Imagen no disponible").pack(expand=True)
            
        details_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent"); details_frame.grid(row=0, column=1, sticky="nw", padx=(40, 0), pady=20)
        ctk.CTkLabel(details_frame, text=product['nombre'], font=theme.FUENTE_TITULO, wraplength=500, justify="left", text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")
        ctk.CTkLabel(details_frame, text=f"Vendido por: {product.get('owner_name', 'N/A')}", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_SECUNDARIO).pack(anchor="w", pady=5)
        ctk.CTkLabel(details_frame, text=f"Precio: ${product.get('precio', 0.0):.2f}", font=theme.FUENTE_BOLD, text_color=theme.COLOR_PRIMARIO, anchor="w").pack(anchor="w", pady=5)
        ctk.CTkLabel(details_frame, text=f"Ubicación: {product.get('direccion', 'No especificada')}", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_SECUNDARIO).pack(anchor="w", pady=5)
        ctk.CTkLabel(details_frame, text="Descripción", font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(details_frame, text=product['descripcion'], font=theme.FUENTE_NORMAL, wraplength=500, justify="left", text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")

        if product.get('vendido'):
            overlay = ctk.CTkLabel(img_frame, text="VENDIDO", font=theme.FUENTE_BOLD, fg_color="#D32F2F", text_color="white", corner_radius=8)
            overlay.place(relx=0.5, rely=0.5, anchor="center")

        if self.controller.current_user and product['owner_user_id'] != self.controller.current_user['id']:
            btn_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            btn_frame.pack(anchor="w", pady=30)
            in_cart = self.controller.get_cart_status(product['id'])
            cart_btn = ctk.CTkButton(btn_frame, text=("En carrito" if in_cart else "Agregar al carrito"), width=140, height=46, font=theme.FUENTE_BOLD, fg_color=(theme.COLOR_PRIMARIO if not in_cart else "#AAAAAA"), hover_color=(theme.COLOR_PRIMARIO_HOVER if not in_cart else "#888888"), state=("disabled" if in_cart or product.get('vendido') else "normal"), command=lambda: self.controller.handle_add_to_cart(product['id']))
            cart_btn.pack(side="left", padx=(0, 10))
            buy_btn = ctk.CTkButton(btn_frame, text="Comprar", font=theme.FUENTE_BOLD, height=46, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, state=("disabled" if product.get('vendido') else "normal"), command=lambda: self.controller.show_payment_page(product['id']))
            buy_btn.pack(side="left", padx=(0, 10))
            ctk.CTkButton(btn_frame, text="Proponer Intercambio", font=theme.FUENTE_BOLD, height=46, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, state=("disabled" if product.get('vendido') else "normal"), command=lambda p=product: self.controller.show_propose_trade_page(p)).pack(side="left", padx=(0,10))
            ctk.CTkButton(btn_frame, text="Contactar Vendedor", font=theme.FUENTE_NORMAL, height=46, command=lambda: self.controller.show_chat_page(product['owner_user_id'])).pack(side="left")

class ProfilePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.user_entries = {}
        self.selected_profile_image = None
        self._img_preview_obj = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        profile_panel = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_SIDEBAR, corner_radius=0, width=480)
        profile_panel.grid(row=0, column=0, sticky="ns")
        
        self.inner_profile_frame = ctk.CTkScrollableFrame(profile_panel, fg_color="transparent", width=420)
        self.inner_profile_frame.pack(padx=30, pady=30, fill="both", expand=True)
        
        self.products_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.products_panel.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        self.products_panel.grid_rowconfigure(1, weight=1)
        self.products_panel.grid_columnconfigure(0, weight=1)

        self.menu_btn = ctk.CTkButton(self, text="Volver al menú principal", font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page)
        self.menu_btn.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 20))

        self._build_profile_widgets()
        self._build_products_panel_widgets()

    def _build_profile_widgets(self):
        ctk.CTkLabel(self.inner_profile_frame, text="Mi Perfil", font=theme.FUENTE_SUBTITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(0, 20))
        
        labels = {
            "nombre": "Nombre:", "apellidos": "Apellidos:", "username": "Nombre de usuario:", "email": "Correo electrónico:",
            "telefono": "Teléfono:", "direccion": "Dirección:", "fecha_nacimiento": "Fecha de nacimiento (YYYY-MM-DD):"
        }
        for key, text in labels.items():
            ctk.CTkLabel(self.inner_profile_frame, text=text, font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(10,0))
            entry = ctk.CTkEntry(self.inner_profile_frame, font=theme.FUENTE_NORMAL, height=40, border_color=theme.COLOR_BORDE, text_color=theme.COLOR_TEXTO_PRINCIPAL)
            entry.pack(fill="x", pady=(5,0))
            self.user_entries[key] = entry

        self.img_preview = ctk.CTkLabel(self.inner_profile_frame, text="", image=None)
        self.img_preview.pack(pady=(10, 10))
        
        ctk.CTkButton(self.inner_profile_frame, text="Seleccionar Imagen de Perfil", font=theme.FUENTE_NORMAL, command=self.select_profile_image).pack(fill="x", pady=(0, 10))
        
        self.edit_button = ctk.CTkButton(self.inner_profile_frame, text="Guardar Cambios", height=40, font=theme.FUENTE_BOLD, command=self.save_profile)
        self.edit_button.pack(pady=30, fill="x")

    def _build_products_panel_widgets(self):
        top_bar = ctk.CTkFrame(self.products_panel, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(10,0))
        ctk.CTkLabel(top_bar, text="Mis Artículos en Venta", font=theme.FUENTE_SUBTITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(side="left")
        ctk.CTkButton(top_bar, text="+ Vender Artículo", font=theme.FUENTE_BOLD, command=self.controller.show_add_product_form).pack(side="right")
        
        self.products_list_frame = ctk.CTkScrollableFrame(self.products_panel, fg_color=theme.COLOR_FONDO_FRAME, border_color=theme.COLOR_BORDE, border_width=1, corner_radius=8)
        self.products_list_frame.grid(row=1, column=0, sticky="nsew", pady=20)

    def update_data(self, user=None, products=None):
        if not user: return
        
        for key, entry in self.user_entries.items():
            entry.delete(0, "end")
            entry.insert(0, str(user.get(key, '')))
            entry.configure(state="disabled" if key == "email" else "normal")

        if user.get('foto_perfil'):
            try:
                img_path = Path(__file__).parent.parent / user['foto_perfil']
                if img_path.is_file():
                    img = Image.open(img_path)
                    img.thumbnail((120, 120))
                    self._img_preview_obj = ctk.CTkImage(light_image=img, size=img.size)
                    self.img_preview.configure(image=self._img_preview_obj)
            except Exception as e:
                print(f"Error al cargar imagen de perfil: {e}")
                self.img_preview.configure(image=None)

        for widget in self.products_list_frame.winfo_children(): widget.destroy()
        
        if products:
            for p in products:
                p_frame = ctk.CTkFrame(self.products_list_frame, fg_color="transparent")
                p_frame.pack(fill="x", pady=5, padx=5)
                ctk.CTkLabel(p_frame, text=p['nombre'], font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(side="left", padx=10)
                ctk.CTkButton(p_frame, text="Eliminar", width=80, fg_color="#D32F2F", hover_color="#B71C1C", command=lambda p_id=p['id']: self.confirm_delete_product(p_id)).pack(side="right", padx=5)
                ctk.CTkButton(p_frame, text="Editar", width=80, fg_color="#AAAAAA", hover_color="#888888", command=lambda prod=p: self.controller.show_edit_product_form(prod)).pack(side="right")
        else:
            ctk.CTkLabel(self.products_list_frame, text="Aún no tienes artículos en venta.", font=theme.FUENTE_NORMAL).pack(expand=True, padx=20, pady=50)

    def select_profile_image(self):
        filename = filedialog.askopenfilename(title="Seleccionar imagen de perfil", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if filename:
            self.selected_profile_image = filename
            img = Image.open(filename)
            img.thumbnail((120, 120))
            self._img_preview_obj = ctk.CTkImage(light_image=img, size=img.size)
            self.img_preview.configure(image=self._img_preview_obj)

    def save_profile(self):
        data = {key: entry.get().strip() for key, entry in self.user_entries.items()}
        if self.selected_profile_image:
            try:
                base_path = Path(__file__).parent.parent
                images_dir = base_path / "images"
                images_dir.mkdir(exist_ok=True)
                source_path = Path(self.selected_profile_image)
                dest_filename = f"perfil_{data['username']}{source_path.suffix}"
                dest_path = images_dir / dest_filename
                shutil.copy2(source_path, dest_path)
                data['foto_perfil'] = f"images/{dest_filename}"
            except Exception as e:
                print(f"Error al guardar imagen de perfil: {e}")
        self.controller.handle_update_profile(data)

    def confirm_delete_product(self, product_id):
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este producto?"):
            self.controller.handle_delete_product(product_id)

class ProductFormPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.product_id = None
        self.fields = {}
        self.selected_image_path = None
        self._original_image_path = None

        frame = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=15, border_width=1, border_color=theme.COLOR_BORDE)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        inner_frame = ctk.CTkFrame(frame, fg_color="transparent")
        inner_frame.pack(padx=40, pady=40)

        self.title_label = ctk.CTkLabel(inner_frame, text="", font=theme.FUENTE_TITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL)
        self.title_label.pack(pady=(0, 30))

        labels = {"nombre": "Nombre del Artículo", "precio": "Precio (MXN)", "direccion": "Ubicación (Ciudad, Estado)", "descripcion": "Descripción"}
        for key, text in labels.items():
            ctk.CTkLabel(inner_frame, text=text, font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w")
            if key == "descripcion":
                entry = ctk.CTkTextbox(inner_frame, width=400, height=120, font=theme.FUENTE_NORMAL, border_color=theme.COLOR_BORDE, text_color=theme.COLOR_TEXTO_PRINCIPAL, border_width=1)
            else:
                entry = ctk.CTkEntry(inner_frame, width=400, height=45, font=theme.FUENTE_NORMAL, border_color=theme.COLOR_BORDE)
            entry.pack(pady=(5,15))
            self.fields[key] = entry

        self.img_label = ctk.CTkLabel(inner_frame, text="No se ha seleccionado imagen", font=("Arial", 12), text_color=theme.COLOR_TEXTO_PRINCIPAL)
        self.img_label.pack(pady=(10, 5))
        self.img_preview = ctk.CTkLabel(inner_frame, text="")
        self.img_preview.pack(pady=(0, 10))

        ctk.CTkButton(inner_frame, text="Seleccionar Imagen", font=theme.FUENTE_NORMAL, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.select_image).pack(fill="x", pady=(0, 10))
        ctk.CTkButton(inner_frame, text="Guardar Producto", height=45, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.save).pack(fill="x", pady=10)
        ctk.CTkButton(inner_frame, text="Cancelar", height=45, font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=controller.show_profile_page).pack(fill="x", pady=(5,0))
    
    def select_image(self):
        filename = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])
        if filename:
            self.selected_image_path = filename
            self.img_label.configure(text=os.path.basename(filename))
            try:
                img = Image.open(filename)
                img.thumbnail((200, 200))
                ctk_image = ctk.CTkImage(light_image=img, size=img.size)
                self.img_preview.configure(image=ctk_image)
                self.img_preview.image = ctk_image
            except Exception as e:
                self.img_preview.configure(image=None, text="Error al cargar imagen")
                print(f"Error en select_image: {e}")

    def update_data(self, product=None):
        for field in self.fields.values():
            if isinstance(field, ctk.CTkTextbox): field.delete("1.0", "end")
            else: field.delete(0, "end")
        
        self.selected_image_path = None
        self._original_image_path = None
        self.img_label.configure(text="No se ha seleccionado imagen")
        self.img_preview.configure(image=None)
        self.img_preview.image = None

        if product:
            self.product_id = product.get('id')
            self.title_label.configure(text="Editar Producto")
            self.fields['nombre'].insert(0, product.get('nombre', ''))
            self.fields['precio'].insert(0, str(product.get('precio', '')))
            self.fields['descripcion'].insert("1.0", product.get('descripcion', ''))
            self.fields['direccion'].insert(0, product.get('direccion', ''))
            
            image_path = product.get('imagen_path')
            if image_path:
                self._original_image_path = image_path
                full_image_path = Path(__file__).parent.parent / image_path
                if full_image_path.is_file():
                    self.img_label.configure(text=full_image_path.name)
                    try:
                        img = Image.open(full_image_path)
                        img.thumbnail((200, 200))
                        ctk_image = ctk.CTkImage(light_image=img, size=img.size)
                        self.img_preview.configure(image=ctk_image)
                        self.img_preview.image = ctk_image
                    except Exception as e:
                        print(f"Error al cargar imagen en update_data: {e}")
        else:
            self.product_id = None
            self.title_label.configure(text="Vender un Artículo")

    def save(self):
        nombre = self.fields['nombre'].get().strip()
        precio = self.fields['precio'].get().strip()
        descripcion = self.fields['descripcion'].get("1.0", "end-1c").strip()
        direccion = self.fields['direccion'].get().strip()

        if not nombre or not precio:
            messagebox.showerror("Error", "El nombre y el precio son obligatorios.")
            return
        try:
            precio_float = float(precio)
            if precio_float < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido y positivo.")
            return

        data = {'nombre': nombre, 'precio': precio_float, 'descripcion': descripcion, 'direccion': direccion}

        if self.selected_image_path:
            try:
                base_path = Path(__file__).parent.parent
                images_dir = base_path / "images"
                images_dir.mkdir(exist_ok=True)
                
                source_path = Path(self.selected_image_path)
                safe_nombre = "".join(c for c in nombre if c.isalnum() or c in (' ', '_')).rstrip()
                
                import time
                timestamp = int(time.time())
                
                new_filename = f"{safe_nombre.replace(' ', '_')}_{self.product_id or timestamp}{source_path.suffix}"

                dest_path = images_dir / new_filename
                shutil.copy2(source_path, dest_path)
                data['imagen_path'] = f"images/{new_filename}"
            except Exception as e:
                print(f"Error al guardar la imagen: {e}")
                data['imagen_path'] = self._original_image_path or ''
        else:
            data['imagen_path'] = self._original_image_path or ''

        self.controller.handle_save_product(data, self.product_id)

class ProposeTradePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.target_product, self.user_products_map = None, {}
        frame = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=15, border_width=1, border_color=theme.COLOR_BORDE); frame.place(relx=0.5, rely=0.5, anchor="center")
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent"); inner_frame.pack(padx=40, pady=40, fill="x")
        ctk.CTkLabel(inner_frame, text="Proponer Intercambio", font=theme.FUENTE_TITULO, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(pady=(0, 20))
        self.target_label = ctk.CTkLabel(inner_frame, text="Artículo deseado: ", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL); self.target_label.pack(anchor="w")
        ctk.CTkLabel(inner_frame, text="\nOfrecer a cambio:", font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(10,5))
        self.offer_menu = ctk.CTkOptionMenu(inner_frame, height=45, font=theme.FUENTE_NORMAL, fg_color="white", button_color=theme.COLOR_PRIMARIO, button_hover_color=theme.COLOR_PRIMARIO_HOVER, dropdown_font=theme.FUENTE_NORMAL, text_color=theme.COLOR_TEXTO_PRINCIPAL)
        self.offer_menu.pack(fill="x")
        ctk.CTkButton(inner_frame, text="Enviar Propuesta", height=45, font=theme.FUENTE_BOLD, fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, command=self.propose).pack(fill="x", pady=(30,10))
        ctk.CTkButton(inner_frame, text="Cancelar", height=45, font=theme.FUENTE_NORMAL, fg_color="#AAAAAA", hover_color="#888888", command=self.controller.show_main_shop_page).pack(fill="x")

    def update_data(self, target_product=None, user_products=None):
        if not target_product or user_products is None: return
        self.target_product = target_product
        self.target_label.configure(text=f"Artículo deseado: {target_product['nombre']}")
        disponibles = [p for p in user_products if not p.get('vendido')]
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
        tabview = ctk.CTkTabview(self, fg_color=theme.COLOR_FONDO_FRAME, segmented_button_selected_color=theme.COLOR_PRIMARIO, segmented_button_selected_hover_color=theme.COLOR_PRIMARIO_HOVER, border_color=theme.COLOR_BORDE, border_width=1)
        tabview.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.received_tab = tabview.add("Recibidas")
        self.sent_tab = tabview.add("Enviadas")
        self.completed_tab = tabview.add("Completadas")
        ctk.CTkButton(self, text="Volver al menú principal", command=self.controller.show_main_shop_page).grid(row=2, column=0, pady=(10,20))

    def update_data(self, trades=None):
        for tab in [self.received_tab, self.sent_tab, self.completed_tab]:
            for widget in tab.winfo_children(): widget.destroy()

        received_scroll = ctk.CTkScrollableFrame(self.received_tab, fg_color="transparent"); received_scroll.pack(fill="both", expand=True)
        sent_scroll = ctk.CTkScrollableFrame(self.sent_tab, fg_color="transparent"); sent_scroll.pack(fill="both", expand=True)
        completed_scroll = ctk.CTkScrollableFrame(self.completed_tab, fg_color="transparent"); completed_scroll.pack(fill="both", expand=True)

        if not trades:
            ctk.CTkLabel(received_scroll, text="No has recibido ninguna propuesta.").pack(expand=True)
            ctk.CTkLabel(sent_scroll, text="No has enviado ninguna propuesta.").pack(expand=True)
            ctk.CTkLabel(completed_scroll, text="No tienes intercambios completados.").pack(expand=True)
            return

        current_user_id = self.controller.current_user['id']
        status_colors = {"pendiente": "#333333", "aceptado": "#2ECC71", "rechazado": "#E74C3C", "cancelado": "#95A5A6", "completado": theme.COLOR_PRIMARIO}
        
        received_count, sent_count, completed_count = 0, 0, 0

        for trade in trades:
            is_receiver = trade['receiver_user_id'] == current_user_id
            
            if trade['status'] == 'completado':
                parent_tab = completed_scroll
                completed_count += 1
                text = f"Intercambio de '{trade['proposer_product_name']}' por '{trade['receiver_product_name']}'"
            elif is_receiver and trade['status'] == 'pendiente':
                parent_tab = received_scroll
                received_count += 1
                text = f"{trade['proposer_name']} te ofrece '{trade['proposer_product_name']}' por tu '{trade['receiver_product_name']}'"
            elif not is_receiver and trade['status'] == 'pendiente':
                parent_tab = sent_scroll
                sent_count += 1
                text = f"Le ofreciste a {trade['receiver_name']} tu '{trade['proposer_product_name']}' por su '{trade['receiver_product_name']}'"
            else:
                continue

            card = ctk.CTkFrame(parent_tab, fg_color="white", border_width=1, border_color=theme.COLOR_BORDE); card.pack(fill="x", padx=10, pady=8)
            ctk.CTkLabel(card, text=text, font=theme.FUENTE_NORMAL, wraplength=700, justify="left", text_color="#222222").pack(side="left", padx=15, pady=15)
            button_frame = ctk.CTkFrame(card, fg_color="transparent"); button_frame.pack(side="right", padx=15, pady=10)
            status = trade['status']
            ctk.CTkLabel(button_frame, text=status.capitalize(), font=("Arial", 16, "bold"), text_color=status_colors.get(status, "#333333")).pack(pady=5)
            if status == 'pendiente':
                if is_receiver:
                    ctk.CTkButton(button_frame, text="Aceptar", fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER, width=100, command=lambda t_id=trade['id']: self.controller.handle_update_trade(t_id, 'aceptado')).pack(side="left", padx=5)
                    ctk.CTkButton(button_frame, text="Rechazar", fg_color="#D32F2F", hover_color="#B71C1C", width=100, command=lambda t_id=trade['id']: self.controller.handle_update_trade(t_id, 'rechazado')).pack(side="left")
                else:
                    ctk.CTkButton(button_frame, text="Cancelar", fg_color="#AAAAAA", hover_color="#888888", width=100, command=lambda t_id=trade['id']: self.controller.handle_update_trade(t_id, 'cancelado')).pack(side="left")

        if received_count == 0: ctk.CTkLabel(received_scroll, text="No has recibido ninguna propuesta.").pack(expand=True)
        if sent_count == 0: ctk.CTkLabel(sent_scroll, text="No has enviado ninguna propuesta.").pack(expand=True)
        if completed_count == 0: ctk.CTkLabel(completed_scroll, text="No tienes intercambios completados.").pack(expand=True)

class AllChatsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(0, weight=1)
        AppHeader(self, controller).grid(row=0, column=0, sticky="ew")

        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)

    def update_data(self, conversations=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not conversations:
            ctk.CTkLabel(self.scrollable_frame, text="No tienes conversaciones.", font=theme.FUENTE_NORMAL).pack(expand=True)
            return
        
        for conv in conversations:
            # CORRECCIÓN: Usar un CTkFrame como contenedor y un botón dentro (o manejar el clic en el frame)
            chat_card = ctk.CTkFrame(self.scrollable_frame, fg_color=theme.COLOR_FONDO_FRAME, border_width=1, border_color=theme.COLOR_BORDE, corner_radius=10, cursor="hand2")
            chat_card.pack(fill="x", pady=5, padx=10)
            
            chat_card.bind("<Button-1>", lambda event, other_id=conv['other_user_id']: self.controller.show_chat_page(other_id))
            
            # Crear un frame interno para usar pack sin conflictos
            inner_card_frame = ctk.CTkFrame(chat_card, fg_color="transparent")
            inner_card_frame.pack(padx=15, pady=10, fill="x")

            label_name = ctk.CTkLabel(inner_card_frame, text=conv.get('other_user_name', 'Usuario'), font=theme.FUENTE_BOLD)
            label_name.pack(side="top", anchor="w")
            label_name.bind("<Button-1>", lambda event, other_id=conv['other_user_id']: self.controller.show_chat_page(other_id))

            label_msg = ctk.CTkLabel(inner_card_frame, text=conv.get('last_message', '')[:60] + "...", font=theme.FUENTE_NORMAL)
            label_msg.pack(side="top", anchor="w")
            label_msg.bind("<Button-1>", lambda event, other_id=conv['other_user_id']: self.controller.show_chat_page(other_id))


class ChatPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(0, weight=1)
        self.other_user = None

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        main_frame.grid_rowconfigure(1, weight=1); main_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_header = ctk.CTkLabel(main_frame, text="Chat", font=theme.FUENTE_SUBTITULO)
        self.chat_header.grid(row=0, column=0, sticky="ew", pady=(0,10))

        self.chat_messages_frame = ctk.CTkScrollableFrame(main_frame, fg_color=theme.COLOR_FONDO_FRAME)
        self.chat_messages_frame.grid(row=1, column=0, sticky="nsew")

        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.grid(row=2, column=0, sticky="ew", pady=(10,0))
        input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = ctk.CTkEntry(input_frame, placeholder_text="Escribe un mensaje...")
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(0,10))
        self.message_entry.bind("<Return>", self.send_message)

        ctk.CTkButton(input_frame, text="Enviar", command=self.send_message).grid(row=0, column=1)
        ctk.CTkButton(self, text="Volver a Mis Chats", command=self.controller.show_all_chats_page).grid(row=1, column=0, sticky="sw", padx=30, pady=20)

    def send_message(self, event=None):
        message = self.message_entry.get()
        if self.other_user and message.strip():
            self.controller.handle_send_message(self.other_user['id'], message)
            self.message_entry.delete(0, "end")

    def update_data(self, conversation=None, other_user=None):
        for widget in self.chat_messages_frame.winfo_children():
            widget.destroy()
        
        self.other_user = other_user
        if other_user:
            self.chat_header.configure(text=f"Chat con {other_user.get('username', 'Usuario')}")

        if conversation:
            current_user_id = self.controller.current_user['id']
            for msg in conversation:
                align = "e" if msg['sender_id'] == current_user_id else "w"
                bubble_color = theme.COLOR_PRIMARIO if align == "e" else "#E5E5EA"
                text_color = "white" if align == "e" else "black"
                
                msg_frame = ctk.CTkFrame(self.chat_messages_frame, fg_color="transparent")
                msg_frame.pack(fill="x", padx=10, pady=5)

                label = ctk.CTkLabel(msg_frame, text=msg['message_text'], fg_color=bubble_color, text_color=text_color, corner_radius=10, wraplength=400)
                if align == 'e':
                    label.pack(anchor="e")
                else:
                    label.pack(anchor="w")

class PaymentConfirmationPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.product = None
        frame = ctk.CTkFrame(self, fg_color=theme.COLOR_FONDO_FRAME); frame.place(relx=0.5, rely=0.5, anchor="center")
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent"); inner_frame.pack(padx=40, pady=40)
        
        self.title_label = ctk.CTkLabel(inner_frame, text="Confirmar Compra", font=theme.FUENTE_TITULO)
        self.title_label.pack(pady=20)
        self.product_label = ctk.CTkLabel(inner_frame, text="", font=theme.FUENTE_NORMAL)
        self.product_label.pack(pady=10)
        self.price_label = ctk.CTkLabel(inner_frame, text="", font=theme.FUENTE_BOLD)
        self.price_label.pack(pady=10)
        
        ctk.CTkButton(inner_frame, text="Confirmar Pago", command=self.confirm_payment, font=theme.FUENTE_BOLD).pack(pady=20)
        ctk.CTkButton(inner_frame, text="Cancelar", command=controller.show_main_shop_page, fg_color="transparent", text_color="gray").pack()

    def update_data(self, product=None):
        self.product = product
        if product:
            self.product_label.configure(text=f"Artículo: {product['nombre']}")
            self.price_label.configure(text=f"Precio Total: ${product['precio']:.2f}")

    def confirm_payment(self):
        if self.product:
            messagebox.showinfo("Pago Simulado", "El pago se ha procesado con éxito.")
            self.controller.handle_buy_product(self.product['id'])