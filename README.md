# Sistema de Inventario — Tienda de Zapatos

Estudiante: Juan Carlos Tejeda Lara  
*Asignatura:* Acceso a Datos / Programación  

# Descripción del Proyecto
Aplicación de consola desarrollada en Python para la gestión del inventario de una tienda de zapatos. Implementa persistencia de datos permanente utilizando **SQLite** como motor de base de datos y **SQLAlchemy 2.0** como ORM (Object-Relational Mapping) para ejecutar las operaciones CRUD (Crear, Consultar, Actualizar y Eliminar).

# Documentación Técnica — Respuestas a las Preguntas

### Pregunta 1. ¿Qué clase de Python representa la tabla de la base de datos? Explica cómo SQLAlchemy identifica el nombre de la tabla y sus columnas.
La clase de Python que representa la tabla es `Zapato`, definida en `datos.py`, la cual hereda de `Base` (que a su vez hereda de `DeclarativeBase`).
* *Nombre de la tabla:* SQLAlchemy lo identifica mediante el atributo especial `__tablename__ = "zapatos"`.
* *Columnas:* Se mapean mediante atributos de clase anotados con `Mapped` y `mapped_column()`. En nuestra implementación:
  * `id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)` define la clave primaria entera y autoincremental.
  * `modelo: Mapped[str] = mapped_column(String(100), nullable=False)` define la columna de texto obligatorio.
  * `talla: Mapped[int] = mapped_column(Integer, nullable=False)` define la columna numérica entera para la talla.
  * `precio: Mapped[float] = mapped_column(Float, nullable=False)` define la columna decimal/real para el precio.

# Pregunta 2. ¿Qué ocurre cuando ejecutas el programa por primera vez? Explica cómo se crea la base de datos `zapateria.db` y la tabla `zapatos`.
Al iniciar `main.py`, lo primero que se ejecuta es `inicializar_db()`, función que invoca a `Base.metadata.create_all(engine)`.

 SQLAlchemy solicita al motor de SQLite abrir ese archivo. Al no existir previamente en la carpeta del proyecto, SQLite crea automáticamente el archivo físico `zapateria.db`. Inmediatamente después, `metadata.create_all()` lee la estructura de la clase `Zapato` registrada en `Base` y crea la tabla `zapatos` con sus cuatro columnas si aún no existe.

# Pregunta 3. Cuando seleccionas la opción de registrar un zapato, ¿qué recorrido siguen los datos desde el menú hasta quedar almacenados en SQLite? Identifica las funciones utilizadas.

1. En `main.py`, dentro de `main()`, al elegir la opción `1`, se capturan por consola los valores `modelo`, `talla` y `precio`.

2. `main()` llama a la función `crear_zapato(modelo, talla, precio)` ubicada en `datos.py`.

3. `crear_zapato()` construye un objeto de Python: `nuevo_zapato = Zapato(modelo=modelo, talla=talla, precio=precio)`.

4. Abre una sesión con `with Session(engine) as session:`, añade el objeto mediante `session.add(nuevo_zapato)` y confirma la escritura física en `zapateria.db` con `session.commit()`. Por último, `session.refresh(nuevo_zapato)` sincroniza el objeto en memoria con el `id` generado automáticamente por SQLite.

### Pregunta 4. ¿Para qué se utiliza una sesión de SQLAlchemy? ¿Qué ocurriría si agregas o modificas un objeto, pero no confirmas la transacción con `commit()`?

La sesión (`Session(engine)`) actúa como intermediario y área de trabajo transaccional (patrón *Unit of Work*) entre los objetos Python en memoria RAM y la base de datos SQLite, rastreando qué registros se crean, modifican o eliminan.
Si se agrega un zapato con `session.add()` o se cambia su precio sin ejecutar `session.commit()`, los cambios permanecen únicamente en la memoria temporal de la sesión y nunca se escriben en el archivo `zapateria.db`. Al salir del bloque `with`, la sesión se cierra automáticamente y ejecuta un *rollback*, descartando todas las operaciones pendientes.

# Pregunta 5. ¿Cómo funciona la búsqueda de zapatos por ID? Explica qué devuelve tu función cuando encuentra el registro y qué devuelve cuando no existe.

La función `buscar_zapato(zapato_id)` utiliza el método `session.get(Zapato, zapato_id)`, diseñado para consultar directamente por clave primaria en la tabla `zapatos`.
* *Cuando encuentra el registro:* Devuelve una instancia del objeto `Zapato` con sus atributos cargados (`id`, `modelo`, `talla`, `precio`), lo que permite imprimir sus detalles en consola (por ejemplo, al buscar el ID `1` en la Prueba 3).
* *Cuando no existe:* Devuelve `None`. Al probar con un ID inexistente (como `99`), `main.py` evalúa ese `None` e informa al usuario que: "no existe ningún zapato con ese ID", evitando errores de ejecución.

# Pregunta 6. ¿Cómo se actualiza el precio de un zapato mediante el ORM? Explica cómo se obtiene el objeto, cómo se modifica su atributo y cómo se guarda el cambio.

En `actualizar_precio(zapato_id, nuevo_precio)` el proceso se realiza en tres pasos dentro de la sesión:

1. *Obtención:* Se busca la instancia con `zapato = session.get(Zapato, zapato_id)`. Si retorna `None` (caso de ID inexistente), la función devuelve `False`.
2. *Modificación:* Al estar el objeto rastreado por la sesión activa, se modifica directamente su atributo en Python: `zapato.precio = nuevo_precio`.
3. *Guardado:* Al ejecutar `session.commit()`, SQLAlchemy detecta que el atributo `precio` del objeto cambió y persiste el nuevo valor en `zapateria.db`, devolviendo `True`.

# Pregunta 7. ¿Qué ocurre cuando eliminas un zapato? Explica cómo compruebas que el registro ya no existe en la base de datos.

En `eliminar_zapato(zapato_id)` se recupera primero el objeto mediante `session.get(Zapato, zapato_id)`. Si existe, se marca para eliminación con `session.delete(zapato)` y se confirma con `session.commit()`, borrando definitivamente la fila de `zapateria.db` (si el ID no existe, retorna `False` sin afectar la base de datos).
Para comprobar que el registro fue eliminado:
* Al ejecutar la opción **2 (Listar todos los zapatos)** (`listar_zapatos()`), el zapato eliminado (ID `2` en la Prueba 5) ya no aparece en el inventario.

* Al intentar buscarlo, actualizarlo o volver a eliminarlo por su ID, `session.get()` devuelve `None` y el sistema avisa que el registro no existe.

# Pregunta 8. ¿Qué sucede con los zapatos registrados cuando cierras y vuelves a ejecutar el programa? Explica por qué permanecen almacenados.

Al cerrar la aplicación con la opción `6` y volver a ejecutar `python main.py` (Prueba 6), los registros que no fueron eliminados siguen apareciendo exactamente con sus últimos valores guardados.
Esto sucede porque SQLite almacena la base de datos en un archivo binario persistente en el disco duro (`zapateria.db`), y cada operación confirmada mediante `session.commit()` graba los datos físicamente en el almacenamiento permanente, de modo que no dependen de la memoria RAM del proceso de Python.