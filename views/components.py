# views/components.py
import customtkinter as ctk
from PIL import Image
try:
    from . import theme
except ImportError:
    import views.theme as theme

class AppHeader(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=0, height=70, border_width=1, border_color=theme.COLOR_BORDE)
        self.controller = controller
        try:
            # Tamaño más grande y proporcionado
            logo_img = ctk.CTkImage(light_image=Image.open("images/logo.png"), size=(160, 80))
            logo_button = ctk.CTkButton(self, image=logo_img, text="", fg_color="transparent", hover=False, command=controller.show_main_shop_page, width=170, height=90)
            logo_button.pack(side="left", padx=30, pady=8, anchor="center")
        except FileNotFoundError:
            logo_button = ctk.CTkButton(self, text="Flea Shop", text_color=theme.COLOR_TEXTO_PRINCIPAL, font=theme.FUENTE_SUBTITULO, fg_color="transparent", hover=False, command=controller.show_main_shop_page)
            logo_button.pack(side="left", padx=30, pady=8, anchor="center")
        right_frame = ctk.CTkFrame(self, fg_color="transparent"); right_frame.pack(side="right", padx=20, pady=10)
        btn_kwargs = {"font": theme.FUENTE_NORMAL, "fg_color": theme.COLOR_PRIMARIO, "hover_color": theme.COLOR_PRIMARIO_HOVER}
        ctk.CTkButton(right_frame, text="Carrito", command=controller.show_cart_page, **btn_kwargs).pack(side="left", padx=5)
        ctk.CTkButton(right_frame, text="Compras", command=controller.show_purchases_page, **btn_kwargs).pack(side="left", padx=5)
        ctk.CTkButton(right_frame, text="Mis Intercambios", command=controller.show_my_trades_page, **btn_kwargs).pack(side="left", padx=5)
        ctk.CTkButton(right_frame, text="Mi Perfil", command=controller.show_profile_page, **btn_kwargs).pack(side="left", padx=5)
        ctk.CTkButton(right_frame, text="Cerrar Sesión", fg_color="#D32F2F", hover_color="#B71C1C", command=controller.logout, font=theme.FUENTE_NORMAL).pack(side="left", padx=(5,0))
        search_frame = ctk.CTkFrame(self, fg_color="transparent"); search_frame.pack(side="left", fill="x", expand=True, padx=40)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar artículos...", font=theme.FUENTE_NORMAL, height=36, border_color=theme.COLOR_BORDE, text_color=theme.COLOR_TEXTO_PRINCIPAL)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<Return>", self.search_product)
        ctk.CTkButton(search_frame, text="Buscar", width=120, height=36, command=self.search_product, **btn_kwargs).pack(side="left", padx=10)
    def search_product(self, event=None): self.controller.show_main_shop_page(search_term=self.search_entry.get())

import os
class ProductCard(ctk.CTkFrame):
    def __init__(self, parent, product, controller, show_cart_remove=False):
        super().__init__(parent, fg_color=theme.COLOR_FONDO_FRAME, corner_radius=12, border_width=2, border_color=theme.COLOR_BORDE)
        self.product = product
        self.controller = controller

        # Imagen del producto
        image_path = product.get("imagen_path", "")
        abs_img_path = None
        if image_path:
            # Si es absoluta y existe, úsala directo
            if os.path.isabs(image_path) and os.path.exists(image_path):
                abs_img_path = image_path
            else:
                # Si es relativa, busca desde la raíz del proyecto
                abs_img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', image_path))
                if not os.path.exists(abs_img_path):
                    abs_img_path = None
        if not abs_img_path or not os.path.exists(abs_img_path):
            abs_img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', 'placeholder.png'))
        try:
            img = Image.open(abs_img_path)
        except Exception:
            img = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', 'placeholder.png')))
        img = img.resize((120, 120))
        ctk_img = ctk.CTkImage(light_image=img, size=(120, 120))
        self.image_label = ctk.CTkLabel(self, image=ctk_img, text="")
        self.image_label.pack(pady=5)

        # Nombre y precio
        ctk.CTkLabel(self, text=product.get('nombre', ''), font=theme.FUENTE_BOLD, text_color=theme.COLOR_TEXTO_PRINCIPAL).pack(pady=(0,2))
        ctk.CTkLabel(self, text=f"Precio: ${product.get('precio', 'N/A')}", font=theme.FUENTE_NORMAL, text_color=theme.COLOR_PRIMARIO).pack()

        # Botones de acción
        btns_frame = ctk.CTkFrame(self, fg_color="transparent")
        btns_frame.pack(pady=5)
        # Botón de carrito (agregar/quitar)
        # Ocultar botón de carrito si el producto es del usuario actual
        is_owner = False
        if hasattr(controller, 'current_user') and controller.current_user:
            is_owner = product.get('owner_user_id') == controller.current_user.get('id')
        if not is_owner:
            in_cart = False
            if hasattr(controller, 'get_cart_status'):
                try:
                    in_cart = controller.get_cart_status(product['id'])
                except Exception:
                    in_cart = False
            if show_cart_remove:
                cart_btn = ctk.CTkButton(
                    btns_frame, text="Quitar del carrito", width=120, height=36,
                    font=theme.FUENTE_NORMAL, fg_color="#D32F2F", hover_color="#B71C1C",
                    command=lambda: controller.handle_remove_from_cart(product['id'])
                )
                cart_btn.pack(side="left", padx=(0, 8))
            else:
                cart_btn = ctk.CTkButton(
                    btns_frame, text=("En carrito" if in_cart else "Agregar al carrito"), width=120, height=36,
                    font=theme.FUENTE_NORMAL,
                    fg_color=(theme.COLOR_PRIMARIO if not in_cart else "#AAAAAA"),
                    hover_color=(theme.COLOR_PRIMARIO_HOVER if not in_cart else "#888888"),
                    state=("disabled" if in_cart or product.get('vendido', 0) == 1 or product.get('vendido', False) else "normal"),
                    command=lambda: controller.handle_add_to_cart(product['id'])
                )
                cart_btn.pack(side="left", padx=(0, 8))
        # Botón comprar solo si el producto NO es del usuario actual
        show_buy_btn = True
        if hasattr(controller, 'current_user') and controller.current_user:
            if product.get('owner_user_id') == controller.current_user.get('id'):
                show_buy_btn = False
        if show_buy_btn:
            buy_btn = ctk.CTkButton(
                btns_frame, text="Comprar", font=theme.FUENTE_BOLD,
                fg_color=theme.COLOR_PRIMARIO, hover_color=theme.COLOR_PRIMARIO_HOVER,
                state=("disabled" if product.get('vendido', 0) == 1 or product.get('vendido', False) else "normal"),
                command=lambda: controller.handle_buy_product(product['id'])
            )
            buy_btn.pack(side="left", padx=(0, 8))

        # Overlay de vendido
        if product.get('vendido', 0) == 1 or product.get('vendido', False):
            overlay = ctk.CTkLabel(self, text="VENDIDO", font=theme.FUENTE_BOLD, fg_color="#D32F2F", text_color="white", corner_radius=8)
            overlay.place(relx=0.5, rely=0.5, anchor="center")

        # Click para detalle
        self.bind("<Button-1>", self.on_click)
        for widget in self.winfo_children():
            widget.bind("<Button-1>", self.on_click)
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    child.bind("<Button-1>", self.on_click)
    def on_click(self, event):
        self.controller.show_product_detail(self.product['id'])

class ToastNotification(ctk.CTkToplevel):
    def __init__(self, parent, message, bg_color, duration=2500):
        super().__init__(parent)
        self.overrideredirect(True); self.attributes("-alpha", 0.95)
        ctk.CTkLabel(self, text=message, text_color="white", font=theme.FUENTE_BOLD, corner_radius=10, fg_color=bg_color, padx=20, pady=10).pack()
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()//2) - (self.winfo_reqwidth()//2)
        y = parent.winfo_y() + parent.winfo_height() - 100
        self.geometry(f"+{x}+{y}"); self.after(duration, self.destroy_fade_out)
    def destroy_fade_out(self):
        alpha = self.attributes("-alpha")
        if alpha > 0: self.attributes("-alpha", alpha - 0.1); self.after(20, self.destroy_fade_out)
        else: self.destroy()