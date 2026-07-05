import requests
import json

API_KEY = "488ea978-11ea-44e0-8191-1fd519a536ca"


def geocodificar(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    try:
        respuesta = requests.get(url, params=params)
        respuesta.raise_for_status()
        datos = respuesta.json()

        if "message" in datos:
            print(f"\nError de la API: {datos['message']}")
            return None

        if "hits" not in datos or len(datos["hits"]) == 0:
            print(f"\nNo se encontró la ciudad '{ciudad}'.")
            return None

        punto = datos["hits"][0]["point"]
        return punto["lat"], punto["lng"]

    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}")
        return None


def elegir_medio_transporte():
    print("\nSeleccione el medio de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. A pie")

    opciones = {
        "1": "car",
        "2": "bike",
        "3": "foot"
    }

    while True:
        opcion = input("Opción: ").strip()

        if opcion in opciones:
            return opciones[opcion]

        print("Opción inválida. Intente nuevamente.")


def calcular_ruta(origen, destino, medio):
    url = "https://graphhopper.com/api/1/route"

    params = {
        "point": [
            f"{origen[0]},{origen[1]}",
            f"{destino[0]},{destino[1]}"
        ],
        "vehicle": medio,
        "locale": "es",
        "instructions": "true",
        "key": API_KEY
    }

    try:
        respuesta = requests.get(url, params=params)
        respuesta.raise_for_status()
        return respuesta.json()

    except requests.exceptions.RequestException as e:
        print(f"\nError al calcular la ruta: {e}")
        return None


def mostrar_resultado(datos):
    if not datos or "paths" not in datos or len(datos["paths"]) == 0:
        print("\nNo fue posible calcular la ruta.")
        return

    path = datos["paths"][0]

    distancia_km = path["distance"] / 1000
    distancia_millas = distancia_km * 0.621371

    tiempo_seg = path["time"] / 1000
    horas = int(tiempo_seg // 3600)
    minutos = int((tiempo_seg % 3600) // 60)

    print("\n========================================")
    print("      RESULTADO DEL VIAJE")
    print("========================================")
    print(f"Distancia : {distancia_km:.2f} km")
    print(f"           {distancia_millas:.2f} millas")
    print(f"Duración  : {horas} h {minutos} min")

    print("\nNarrativa del viaje:")

    for paso in path["instructions"]:
        print(f"• {paso['text']}")


def main():
    print("==============================================")
    print(" Calculadora de Distancia Chile - Argentina")
    print("==============================================")

    while True:
        origen_texto = input("\nIngrese Ciudad de Origen (o 's' para salir): ").strip()

        if origen_texto.lower() == "s":
            print("\nPrograma finalizado.")
            break

        destino_texto = input("Ingrese Ciudad de Destino: ").strip()

        if destino_texto.lower() == "s":
            print("\nPrograma finalizado.")
            break

        origen = geocodificar(origen_texto)
        destino = geocodificar(destino_texto)

        if origen is None or destino is None:
            print("\nNo fue posible obtener las coordenadas de alguna ciudad.")
            continue

        medio = elegir_medio_transporte()

        datos_ruta = calcular_ruta(origen, destino, medio)

        mostrar_resultado(datos_ruta)


if __name__ == "__main__":
    main()
