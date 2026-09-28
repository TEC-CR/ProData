import data_loader
import distributions
import survival
import censored
import visualization
import utils
import inference

def seleccionar_modo():
    print("\n=== Selección de modo ===")
    print("1. Una muestra (columna B)")
    print("2. Dos muestras (columnas B y D)")
    return input("Seleccione: ")

def menu():
    print("\n=== ProData ===")
    print("1. Ajustar distribución")
    print("2. Graficar densidad")
    print("3. Supervivencia / falla / riesgo")
    print("4. Datos censurados")
    print("5. Percentil o tiempo")
    print("6. Prueba de hipótesis (dos muestras)")
    print("7. Intervalo de confianza")
    print("8. Comparar confiabilidad (dos muestras)")
    print("0. Salir")

def main():
    modo = seleccionar_modo()
    archivo = input("Ingrese ruta del archivo Excel: ")
    datos = data_loader.cargar_excel(archivo)

    datos1 = datos["muestra1"].dropna()
    datos2 = datos["muestra2"].dropna() if modo == "2" else None

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "6" and modo == "2":
            print(inference.prueba_medias(datos1, datos2))
        elif opcion == "7":
            print(inference.intervalo_confianza(datos1))
        elif opcion == "8" and modo == "2":
            print(inference.comparar_confiabilidad(datos1, datos2))
        elif opcion == "0":
            break
        else:
            print("Función aún no implementada o requiere dos muestras.")

if __name__ == "__main__":
    main()
