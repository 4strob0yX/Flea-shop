# views/utils.py
import re

def is_valid_email(email):
    """Verifica si el formato de un email es válido usando una expresión regular simple."""
    if not email: return False
    # Expresión regular para validar un email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def validate_registration_data(data):
    """Valida todos los campos del formulario de registro."""
    errors = []
    required_fields = {"username": "Nombre de usuario", "email": "Email", "password": "Contraseña"}
    
    for key, name in required_fields.items():
        if not data.get(key):
            errors.append(f"El campo '{name}' no puede estar vacío.")

    if data.get("email") and not is_valid_email(data["email"]):
        errors.append("El formato del email no es válido.")

    if data.get("password") and len(data["password"]) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres.")

    # La comparación de contraseñas se realiza en la vista, no aquí
        
    return errors

def validate_product_data(data):
    """Valida los campos del formulario de producto."""
    errors = []
    if not data.get("nombre"):
        errors.append("El nombre del producto no puede estar vacío.")
    if not data.get("precio"):
        errors.append("El precio no puede estar vacío.")
    else:
        try:
            float(data["precio"])
        except ValueError:
            errors.append("El precio debe ser un número válido.")
    return errors