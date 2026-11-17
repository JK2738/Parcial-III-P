from datos import (
    actualizar_precio,
    buscar_zapato,
    crear_zapato,
    eliminar_zapato,
    inicializar_db,
    listar_zapatos,
)


def mostrar_menu() -> None:
    print("\n=== INVENTARIO TIENDA DE ZAPATOS ===")
    print("1. Registrar zapato")
    print("2. Listar todos los zapatos")
    print("3. Buscar zapato por ID")
    print("4. Actualizar precio de un zapato")
    print("5. Eliminar zapato")
    print("6. Salir")


def main() -> None:
    inicializar_db()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            modelo = input("Modelo del zapato: ").strip()
            try:
                talla = int(input("Talla: ").strip())
                precio = float(input("Precio: ").strip())
            except ValueError:
                print("Error: La talla debe ser un entero y el precio un número válido.")
                continue

            zapato = crear_zapato(modelo, talla, precio)
            print(f"Zapato registrado correctamente con ID: {zapato.id}")

        elif opcion == "2":
            zapatos = listar_zapatos()
            if not zapatos:
                print("No hay zapatos registrados en el inventario.")
            else:
                print("\n--- LISTADO DE ZAPATOS ---")
                for z in zapatos:
                    print(f"ID: {z.id} | Modelo: {z.modelo} | Talla: {z.talla} | Precio: ${z.precio:,.2f}")

        elif opcion == "3":
            try:
                zapato_id = int(input("Ingrese el ID del zapato a buscar: ").strip())
            except ValueError:
                print("Error: El ID debe ser un número entero.")
                continue

            zapato = buscar_zapato(zapato_id)
            if zapato:
                print(f"Encontrado -> ID: {zapato.id} | Modelo: {zapato.modelo} | Talla: {zapato.talla} | Precio: ${zapato.precio:,.2f}")
            else:
                print(f"No existe ningún zapato con el ID {zapato_id}.")

        elif opcion == "4":
            try:
                zapato_id = int(input("Ingrese el ID del zapato a actualizar: ").strip())
                nuevo_precio = float(input("Ingrese el nuevo precio: ").strip())
            except ValueError:
                print("Error: Ingrese valores numéricos válidos.")
                continue

            if actualizar_precio(zapato_id, nuevo_precio):
                print("Precio actualizado correctamente.")
            else:
                print(f"No se pudo actualizar: no existe un zapato con el ID {zapato_id}.")

        elif opcion == "5":
            try:
                zapato_id = int(input("Ingrese el ID del zapato a eliminar: ").strip())
            except ValueError:
                print("Error: El ID debe ser un número entero.")
                continue

            if eliminar_zapato(zapato_id):
                print("Zapato eliminado correctamente.")
            else:
                print(f"No se pudo eliminar: no existe un zapato con el ID {zapato_id}.")

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
