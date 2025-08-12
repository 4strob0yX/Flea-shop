-- Agrega el campo cart_items a la tabla users para el carrito persistente
ALTER TABLE users ADD COLUMN cart_items TEXT DEFAULT '[]';
