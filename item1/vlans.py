while True:
    entrada = input("Ingrese número de VLAN (o 's' para salir): ").strip().lower()

    if entrada == "s":
        print("Saliendo del programa.")
        break

    if not entrada.isdigit():
        print("Debe ingresar un número válido.")
        continue

    vlan = int(entrada)

    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} corresponde al rango normal.")
    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} corresponde al rango extendido.")
    else:
        print(f"La VLAN {vlan} está fuera de rango válido.")