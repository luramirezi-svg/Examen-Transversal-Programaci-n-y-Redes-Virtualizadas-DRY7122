import requests

API_KEY = "47a609d5-c1a5-4eb2-8178-42e62a1acb0d"

def geocodificar(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()

    if "hits" in data and len(data["hits"]) > 0:
        punto = data["hits"][0]["point"]
        return punto["lat"], punto["lng"]
    return None

def obtener_ruta(origen, destino, vehiculo):
    coord_origen = geocodificar(origen)
    coord_destino = geocodificar(destino)

    if not coord_origen or not coord_destino:
        print("No se pudo encontrar alguna de las ciudades.")
        return

    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{coord_origen[0]},{coord_origen[1]}", f"{coord_destino[0]},{coord_destino[1]}"],
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    r = requests.get(url, params=params)
    data = r.json()

    if "paths" not in data:
        print("No se pudo calcular la ruta.")
        print(data)
        return

    path = data["paths"][0]
    distancia_metros = path["distance"]
    duracion_ms = path["time"]

    km = distancia_metros / 1000
    horas = duracion_ms / 1000 / 60 / 60

    print(f"\nOrigen: {origen}")
    print(f"Destino: {destino}")
    print(f"Medio de transporte: {vehiculo}")
    print(f"Distancia: {km:.2f} km")
    print(f"Duración estimada: {horas:.2f} horas")
    print("\nNarrativa del viaje:")

    for instruccion in path["instructions"]:
        print("-", instruccion["text"])

while True:
    origen = input("\nCiudad de Origen (o 's' para salir): ").strip()
    if origen.lower() == "s":
        break

    destino = input("Ciudad de Destino (o 's' para salir): ").strip()
    if destino.lower() == "s":
        break

    vehiculo = input("Medio de transporte (car, bike, foot): ").strip().lower()
    if vehiculo == "s":
        break

    if vehiculo not in ["car", "bike", "foot"]:
        print("Transporte no válido.")
        continue

    obtener_ruta(origen, destino, vehiculo)