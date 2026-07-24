# Semana 4 — Gestión de errores y excepciones

En la Semana 3 los objetos se protegían a sí mismos (lanzaban `ValueError` en el *setter*). Pero
si el programa principal intentaba crear un objeto con un dato malo, **todo colapsaba**. Esta
semana le damos al sistema la capacidad de **recuperarse** con `try/except`, y sentamos las bases
de la **persistencia** con la serialización a **JSON**.

## Archivos

| Archivo | Actividad | Para qué sirve |
|---------|-----------|----------------|
| [`robustez_try_except.py`](./robustez_try_except.py) | **Actividad 1** | Lectura tolerante a fallos: procesa un archivo con datos corruptos sin detenerse. |
| [`transacciones_corruptas.txt`](./transacciones_corruptas.txt) | **Actividad 1** | 7 registros, **3 con errores intencionales**. |
| [`serializacion_json.py`](./serializacion_json.py) | **Actividad 2** | Demuestra Objeto → Diccionario → JSON y el camino inverso. |

---

## Actividad 1 — Recuperación con `try/except`

El archivo `transacciones_corruptas.txt` tiene 3 errores a propósito:

| Línea | Dato | Error que provoca |
|------|------|-------------------|
| C003 | `DEBITO,texto_invalido` | **ValueError** — no se puede convertir `"texto_invalido"` a número |
| C004 | `CREDITO,-200000` | **ValueError** — el *setter* rechaza montos negativos (validación de la Semana 3) |
| C006 | `DEBITO` (falta el monto) | **TypeError** — al constructor le faltan argumentos |

`cargar_transacciones()` envuelve la creación del objeto en un `try` y atrapa cada fallo con un
`except` específico, imprime el error con el número de línea y **continúa** con el siguiente
registro.

### Salida esperada
```
  [Linea 3] ValueError: invalid literal for int() with base 10: 'texto_invalido'  ->  se ignora: C003,DEBITO,texto_invalido
  [Linea 4] ValueError: el monto no puede ser negativo  ->  se ignora: C004,CREDITO,-200000
  [Linea 6] TypeError: datos insuficientes  ->  se ignora: C006,DEBITO

Se procesaron 4 transacciones validas:
   C001 | DEBITO | $150000
   C002 | CREDITO | $500000
   C005 | DEBITO | $45000
   C007 | CREDITO | $10000
```

> 💡 El programa lee un archivo **lleno de datos corruptos** y aun así procesa **todos los datos
> válidos**, dejando un registro (log) de los errores, sin detenerse. Eso es un sistema
> **tolerante a fallos**.

---

## Actividad 2 — Serialización y persistencia (JSON)

Los objetos viven en la **memoria** de Python; para **guardarlos** o **enviarlos** hay que
convertirlos a un formato de texto universal: **JSON**.

- **Serializar** = Objeto → Diccionario → texto JSON (`json.dumps`).
- **Deserializar** = texto JSON → Diccionario → Objeto (`json.loads` + constructor).

> 🧳 Analogía: serializar es **empacar** tus cosas en una caja para un viaje (el objeto se vuelve
> texto que viaja por internet o al disco); deserializar es **desempacar** al llegar.

### Salida esperada
```
1) Objeto original : Transaccion [CREDITO] - ID: C002, Monto: 500000
2) Serializado     : {"cliente_id": "C002", "tipo": "CREDITO", "monto": 500000}
3) Deserializado   : Transaccion [CREDITO] - ID: C002, Monto: 500000
```

---

## Cómo ejecutar
```bash
python robustez_try_except.py     # Actividad 1
python serializacion_json.py      # Actividad 2
```
