# serializacion_json.py
# Semana 4 - Serializacion y deserializacion (JSON)
# El "viaje" de los datos:  Objeto Python  <->  Diccionario  <->  Texto JSON
# Para ejecutar:  python serializacion_json.py

import json


# Clase base (la del enunciado de la actividad)
class Transaccion:
    def __init__(self, cliente_id, tipo, monto):
        self.cliente_id = cliente_id
        self.tipo = tipo
        self.monto = monto

    def __str__(self):
        return f"Transaccion [{self.tipo}] - ID: {self.cliente_id}, Monto: {self.monto}"


# ---------- SERIALIZACION:  Objeto -> Diccionario -> Texto JSON ----------
def objeto_a_json(transaccion):
    # Paso 1: el Objeto se convierte en un DICCIONARIO simple
    como_dict = {
        "cliente_id": transaccion.cliente_id,
        "tipo": transaccion.tipo,
        "monto": transaccion.monto,
    }
    # Paso 2: el Diccionario se convierte en una CADENA DE TEXTO JSON
    return json.dumps(como_dict)


# ---------- DESERIALIZACION:  Texto JSON -> Diccionario -> Objeto ----------
def json_a_objeto(texto_json):
    # Paso 1: la cadena JSON se convierte de nuevo en un DICCIONARIO
    como_dict = json.loads(texto_json)
    # Paso 2: usamos las claves del diccionario para LLAMAR AL CONSTRUCTOR
    return Transaccion(como_dict["cliente_id"], como_dict["tipo"], como_dict["monto"])


# ---------- Demostracion ----------
def ejecutar():
    original = Transaccion("C002", "CREDITO", 500000)
    print("1) Objeto original :", original)

    texto = objeto_a_json(original)
    print("2) Serializado     :", texto)
    print("   Tipo de dato    :", type(texto).__name__, "(es TEXTO)")

    reconstruido = json_a_objeto(texto)
    print("3) Deserializado   :", reconstruido)


if __name__ == "__main__":
    ejecutar()
