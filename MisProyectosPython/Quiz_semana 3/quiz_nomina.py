# quiz_nomina.py
# Quiz Semana 3 - Fundamentos de Programacion (Pilares de POO)
# Estudiante: Liliana Betancur
 
import pandas as pd
 
 
# ---------------------------------------------------------------
# 1) CLASE BASE: datos comunes + ENCAPSULAMIENTO del salario
# ---------------------------------------------------------------
 
class EmpleadoBase:
    """Clase base que encapsula el salario y define el comportamiento comun."""
 
    def __init__(self, nombre, salario_base, ciudad):
        self.nombre = nombre          # nombre del empleado
        self.ciudad = ciudad          # ciudad donde trabaja
        self.salario_base = salario_base  # usamos el setter para validar
 
    # GETTER: permite leer el salario de forma segura
    @property
    def salario_base(self):
        """Devuelve el salario base almacenado de forma privada."""
        return self._salario_base
 
    # SETTER: valida que el salario no sea negativo antes de guardarlo
    @salario_base.setter
    def salario_base(self, nuevo_salario):
        """Valida y guarda el salario base."""
        if int(nuevo_salario) < 0:
            raise ValueError("El salario no puede ser negativo.")
        self._salario_base = int(nuevo_salario)
 
    # Metodo que cada clase hija sobreescribe con su propia logica
    def calcular_pago(self):
        raise NotImplementedError("Cada tipo de empleado calcula su pago.")
 
    def obtener_informacion(self):
        """Devuelve los datos del empleado como texto legible."""
        tipo = type(self).__name__
        return f"{self.nombre} | {tipo} | {self.ciudad} | base ${self.salario_base}"
 
 
# ---------------------------------------------------------------
# 2) CLASES HIJAS (HERENCIA)
# ---------------------------------------------------------------
 
class EmpleadoPlanta(EmpleadoBase):
    """Empleado de planta: recibe salario base mas 30% de prestaciones."""
 
    def calcular_pago(self):
        """Devuelve el salario base mas el 30% de prestaciones."""
        return self.salario_base * 1.30
 
 
class EmpleadoContratista(EmpleadoBase):
    """Contratista: recibe unicamente su salario base, sin prestaciones."""
 
    def calcular_pago(self):
        """Devuelve el salario base sin ningun adicional."""
        return self.salario_base
 
 
# ---------------------------------------------------------------
# 3) CREAR EL OBJETO CORRECTO SEGUN EL TIPO
# ---------------------------------------------------------------
 
def crear_empleado(nombre, tipo, salario_base, ciudad):
    """Crea y devuelve el objeto de empleado segun el tipo recibido."""
    if tipo == "PLANTA":
        return EmpleadoPlanta(nombre, salario_base, ciudad)
    elif tipo == "CONTRATISTA":
        return EmpleadoContratista(nombre, salario_base, ciudad)
    else:
        raise ValueError(f"tipo desconocido '{tipo}'")
 
 
# ---------------------------------------------------------------
# 4) LECTURA DEL EXCEL (ya estaba lista, no se modifica)
# ---------------------------------------------------------------
 
def leer_empleados_excel(nombre_archivo):
    """Lee empleados desde un Excel y devuelve una lista de objetos Empleado."""
    empleados = []
    df = pd.read_excel(nombre_archivo)
    df.columns = [str(c).strip().lower() for c in df.columns]
 
    columnas_necesarias = {"nombre", "tipo", "salario_base"}
    if not columnas_necesarias.issubset(df.columns):
        faltan = columnas_necesarias - set(df.columns)
        print(f"  [Error] Al Excel le faltan columnas: {faltan}")
        return empleados
 
    for _, fila in df.iterrows():
        if pd.isna(fila["nombre"]) or pd.isna(fila["tipo"]) or pd.isna(fila["salario_base"]):
            print("  [Aviso] Fila incompleta ignorada.")
            continue
 
        nombre = str(fila["nombre"]).strip()
        tipo = str(fila["tipo"]).strip().upper()
        salario = fila["salario_base"]
        ciudad = str(fila["ciudad"]).strip() if "ciudad" in df.columns and not pd.isna(fila["ciudad"]) else ""
 
        try:
            empleado = crear_empleado(nombre, tipo, salario, ciudad)
            if empleado is not None:
                empleados.append(empleado)
        except ValueError as error:
            print(f"  [Aviso] Se ignoro {nombre}: {error}")
 
    return empleados


# =====================================================================
# 5) RETO EXTRA: ¡CREA TU PROPIA FUNCION!
#    Inventa una funcion util que trabaje con la lista de empleados.
#    Elige UNA de estas ideas (o propon la tuya) y programala aqui abajo:

#       * salario_promedio(empleados): promedio de salario_base
#       * empleados_por_ciudad(empleados, ciudad): cuantos hay en esa ciudad
#       * empleado_mejor_pagado(empleados): el de mayor calcular_pago()

#    Documentala con un docstring y luego llamala dentro de ejecutar_quiz().
# =====================================================================
def salario_promedio(empleados):
    # TODO: escribe aqui tu propia logica
    pass


# 6) Funcion principal
def ejecutar_quiz():
    empleados = leer_empleados_excel("empleados.xlsx")
 
    print("--- Nomina ---")
    for empleado in empleados:
        print(empleado.obtener_informacion(), "-> pago:", empleado.calcular_pago())
 
    mejor = mi_funcion(empleados)
    if mejor is not None:
        print("\nEmpleado mejor pagado:", mejor.obtener_informacion())
 
 
ejecutar_quiz()

