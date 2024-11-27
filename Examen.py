import csv
from datetime import datetime

def leer_archivo(nombre_archivo):
    """Lee los datos existentes del archivo CSV."""
    datos = []
    try:
        with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for linea in lector:
                datos.append(linea)
    except FileNotFoundError:
        pass  # Si el archivo no existe, simplemente devuelve una lista vacía.
    return datos

def escribir_archivo(nombre_archivo, datos):
    """Escribe datos en un archivo CSV."""
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        campos = ["Nombre", "Presentaciones", "Fechas"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)

def orden_insercion(datos):
    """Ordena los datos ascendentemente por fecha usando el método de inserción."""
    for i in range(1, len(datos)):
        key = datos[i]
        j = i - 1
        while j >= 0 and datetime.strptime(datos[j]["Fechas"].split(",")[0], "%Y-%m-%d") > datetime.strptime(key["Fechas"].split(",")[0], "%Y-%m-%d"):
            datos[j + 1] = datos[j]
            j -= 1
        datos[j + 1] = key

def intercalar_archivos(archivos):
    """Intercala los datos de tres archivos y los ordena por fecha."""
    datos_combinados = []
    
    # Leer todos los archivos y agregar los datos
    for archivo in archivos:
        datos_combinados.extend(leer_archivo(archivo))
    
    # Ordenar los datos combinados por fecha
    orden_insercion(datos_combinados)
    
    # Escribir los datos combinados y ordenados en el archivo RECITALES.csv
    escribir_archivo("RECITALES.csv", datos_combinados)
    print("Archivos intercalados y ordenados con éxito en RECITALES.csv.")

def agregar_datos(nombre_archivo):
    """Permite al usuario ingresar datos y los guarda en el archivo especificado sin borrar el contenido previo."""
    datos_existentes = leer_archivo(nombre_archivo)
    nuevos_datos = []

    print(f"\nAgregando datos al archivo {nombre_archivo}:")
    while True:
        nombre = input("Nombre del cantante u orquesta (o 'fin' para terminar): ")
        if nombre.lower() == "fin":
            break
        presentaciones = input("Número de presentaciones: ")
        fechas = input("Fechas de las presentaciones (formato YYYY-MM-DD, separadas por comas): ")
        fechas_lista = [fecha.strip() for fecha in fechas.split(",")]
        
        # Validar formato de fechas
        try:
            fechas_validas = sorted([datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d") for fecha in fechas_lista])
            nuevos_datos.append({"Nombre": nombre, "Presentaciones": presentaciones, "Fechas": ", ".join(fechas_validas)})
        except ValueError:
            print("Error: Una o más fechas tienen un formato incorrecto. Intente nuevamente.")
            continue

    # Combinar datos existentes con los nuevos
    todos_los_datos = datos_existentes + nuevos_datos

    # Ordenar los datos con el algoritmo de inserción
    orden_insercion(todos_los_datos)
    
    # Guardar los datos ordenados en el archivo
    escribir_archivo(nombre_archivo, todos_los_datos)
    print(f"Datos guardados y ordenados exitosamente en {nombre_archivo}.")

def mostrar_archivo(nombre_archivo):
    """Muestra el contenido de un archivo CSV."""
    datos = leer_archivo(nombre_archivo)
    if not datos:
        print(f"El archivo {nombre_archivo} está vacío o no existe.")
        return
    print(f"\nContenido del archivo {nombre_archivo}:")
    for registro in datos:
        print(f"Nombre: {registro['Nombre']}, Presentaciones: {registro['Presentaciones']}, Fechas: {registro['Fechas']}")

def mostrar_recitales():
    """Muestra el contenido del archivo RECITALES.csv."""
    datos = leer_archivo("RECITALES.csv")
    if not datos:
        print(f"El archivo RECITALES.csv está vacío o no existe.")
        return
    print(f"\nContenido del archivo RECITALES.csv (ordenado por fechas):")
    for registro in datos:
        print(f"Nombre: {registro['Nombre']}, Presentaciones: {registro['Presentaciones']}, Fechas: {registro['Fechas']}")

def menu():
    """Menú principal del programa."""
    archivos = ["A1.csv", "A2.csv", "A3.csv"]
    
    while True:
        print("\n--- Menú Principal ---")
        print("1. Agregar datos al archivo A1")
        print("2. Agregar datos al archivo A2")
        print("3. Agregar datos al archivo A3")
        print("4. Mostrar archivo A1")
        print("5. Mostrar archivo A2")
        print("6. Mostrar archivo A3")
        print("7. Intercalar y ordenar los tres archivos (A1, A2, A3) en RECITALES")
        print("8. Mostrar los recitales ordenados (RECITALES.csv)")
        print("9. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_datos(archivos[0])
        elif opcion == "2":
            agregar_datos(archivos[1])
        elif opcion == "3":
            agregar_datos(archivos[2])
        elif opcion == "4":
            mostrar_archivo(archivos[0])
        elif opcion == "5":
            mostrar_archivo(archivos[1])
        elif opcion == "6":
            mostrar_archivo(archivos[2])
        elif opcion == "7":
            intercalar_archivos(archivos)
        elif opcion == "8":
            mostrar_recitales()  # Mostrar el archivo RECITALES.csv
        elif opcion == "9":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar el menú
menu()
