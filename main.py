# main.py
from model import Model
from views.main_view import MainView
from controller import Controller

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'root', 
        'password': '', # <--- CAMBIA ESTO
        'database': 'flea_shop_db'
    }

    model = Model(db_config)
    controller = Controller(model=model, view=None)
    view = MainView(controller)
    controller.view = view 
    controller.start()
    