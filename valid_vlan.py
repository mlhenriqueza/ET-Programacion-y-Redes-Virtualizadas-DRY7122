vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} corresponde al rango NORMAL (1-1005).")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} corresponde al rango EXTENDIDO (1006-4094).")
else:
    print(f"La VLAN {vlan} no es un valor válido (rango permitido 1-4094).")
