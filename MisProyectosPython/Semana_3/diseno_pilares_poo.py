# # robustez_try_except.py
# Actividad Semana 4 - Implementacion de recuperacion try-except
# Objetivo: leer transacciones_corruptas.txt sin que un dato malo detenga el programa.
# Cada linea valida tiene:  ID, TIPO, MONTO
# Para ejecutar:  python robustez_try_except.py
 
 
# ---------------------------------------------------------------
# 1) CLASE BASE: encapsulamiento del monto (igual que semana 3)
# ---------------------------------------------------------------
 
class TransaccionBase:
    """Clase base que encapsula el monto y define el comportamiento comun."""
 
    def __init__(self, id_transaccion, monto):
        self.id_transaccion = id_transaccion
        self.monto = monto  # usa el setter para validar
 
    # GETTER: permite leer el monto de forma segura
    @property
    def monto(self):
        return self._monto
 
    # SETTER: valida que el monto no sea negativo antes de guardarlo
    @monto.setter
    def monto(self, nuevo_monto):
        if int(nuevo_monto) < 0:
            raise ValueError("El monto no puede ser negativo.")
        self._monto = int(nuevo_monto)
 
    def calcular_impacto(self):
        raise NotImplementedError("Cada tipo de transaccion define su impacto.")
 
    def obtener_informacion(self):
        return f"{self.id_transaccion} | {type(self).__name__} | ${self.monto}"
 
 
# ---------------------------------------------------------------
# 2) CLASES HIJAS: herencia + polimorfismo
# ---------------------------------------------------------------
 
class TransaccionCredito(TransaccionBase):
    """Credito: impacto = 2% del monto (tasa de interes)."""
 
    def calcular_impacto(self):
        return round(self.monto * 0.02, 2)
 
 
class TransaccionDebito(TransaccionBase):
    """Debito: impacto = comision fija de $1500."""
 
    def calcular_impacto(self):
        return 1500
 
 
# ---------------------------------------------------------------
# 3) CREAR EL OBJETO CORRECTO SEGUN EL TIPO
# ---------------------------------------------------------------
 
def crear_transaccion(id_transaccion, tipo, monto):
    """Crea y devuelve el objeto de transaccion segun el tipo recibido."""
    if tipo == "CREDITO":
        return TransaccionCredito(id_transaccion, monto)
    if tipo == "DEBITO":
        return TransaccionDebito(id_transaccion, monto)
    raise ValueError(f"tipo desconocido '{tipo}'")
 
 
# ---------------------------------------------------------------
# 4) LECTURA ROBUSTA CON try-except
#    Este es el unico punto donde vive el bloque try-except.
#    Si un registro falla, se registra el error y el bucle
#    continua con el siguiente registro sin detenerse.
# ---------------------------------------------------------------
 
def leer_transacciones(nombre_archivo):
    """Lee el archivo linea por linea y devuelve solo las transacciones validas.
 
    Errores atrapados:
    - ValueError: monto con texto invalido o monto negativo.
    - TypeError: linea con datos insuficientes (menos de 3 columnas).
    """
    transacciones = []
 
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
 
            # Ignorar lineas en blanco
            if not linea.strip():
                continue
 
            try:
                # PASO 1: separar los campos de la linea
                # Si la linea tiene menos de 3 columnas, el desempaquetado
                # lanzara un ValueError (no un TypeError como podria esperarse)
                partes = linea.strip().split(",")
                id_transaccion, tipo, monto = partes  # puede fallar aqui
 
                # PASO 2: crear el objeto (puede fallar si monto es texto o negativo)
                transaccion = crear_transaccion(id_transaccion.strip(),
                                                tipo.strip(),
                                                monto.strip())
                transacciones.append(transaccion)
 
            except ValueError as error:
                # Atrapa: conversion fallida (texto_invalido -> int)
                #         monto negativo (raise ValueError del Setter)
                #         desempaquetado fallido por columnas insuficientes
                print(f"  [ERROR ValueError] Linea {numero_linea} "
                      f"({linea.strip()}) -> {error}")
 
            except TypeError as error:
                # Atrapa: si se pasa un tipo de dato inesperado al constructor
                print(f"  [ERROR TypeError] Linea {numero_linea} "
                      f"({linea.strip()}) -> {error}")
 
    return transacciones
 
 
# ---------------------------------------------------------------
# 5) FUNCION PRINCIPAL
# ---------------------------------------------------------------
 
def ejecutar_sistema():
    print("Leyendo transacciones_corruptas.txt...\n")
    transacciones = leer_transacciones("transacciones_corruptas.txt")
 
    print("\n--- Transacciones validas cargadas ---")
    for t in transacciones:
        print(t.obtener_informacion(), "-> impacto:", t.calcular_impacto())
 
    print(f"\nTotal transacciones validas: {len(transacciones)}")
 
 
if __name__ == "__main__":
    ejecutar_sistema()
 
