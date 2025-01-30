def obtener_datos_personales():
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")

    # Validación de la edad
    while True:
        edad = input("Ingrese su edad: ")
        if edad.isdigit():
            edad = int(edad)
            break
        else:
            print("Por favor, ingrese una edad válida.")

    sede = input("Ingrese su sede: ")

    return nombre, apellido, edad, sede

def imprimir_datos_personales(nombre, apellido, edad, sede):
    print("\nDatos personales:")
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"Edad: {edad}")
    print(f"Sede: {sede}")

if __name__ == "__main__":
    nombre, apellido, edad, sede = obtener_datos_personales()
    imprimir_datos_personales(nombre, apellido, edad, sede)

