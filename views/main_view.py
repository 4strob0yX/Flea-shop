# views/main_view.py
import customtkinter as ctk
from . import theme
from .pages import LoginPage, RegisterPage, MainShopPage, ProductDetailPage, ProfilePage, ProductFormPage, ProposeTradePage, MyTradesPage, CartPage
from .components import ToastNotification

class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Flea Shop"); self.geometry("1280x800"); self.minsize(1024, 768)
        self.configure(fg_color=theme.COLOR_FONDO_APP)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1); container.grid_columnconfigure(0, weight=1)

        self._frames = {}
        from .pages import CartPage, PurchasesPage
        pages = (LoginPage, RegisterPage, MainShopPage, ProductDetailPage, ProfilePage, ProductFormPage, ProposeTradePage, MyTradesPage, CartPage, PurchasesPage)
        for F in pages:
            frame = F(container, self.controller)
            self._frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    def switch(self, page_name_str, **kwargs):
        page_name = "".join(word.capitalize() for word in page_name_str.split('_')) + "Page"
        if page_name in self._frames:
            frame = self._frames[page_name]
            if hasattr(frame, 'update_data'):
                frame.update_data(**kwargs)
            frame.tkraise()
        else:
            print(f"Error: La página '{page_name}' no existe.")

    def get_frame(self, page_name_str):
        page_name = "".join(word.capitalize() for word in page_name_str.split('_')) + "Page"
        return self._frames.get(page_name)

    def show_toast(self, message, bg_color=None, duration=3000):
        if bg_color is None: bg_color = theme.COLOR_PRIMARIO
        ToastNotification(self, message, bg_color=bg_color, duration=duration)