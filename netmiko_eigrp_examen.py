from netmiko import ConnectHandler

dispositivo = {
    "device_type": "cisco_ios",
    "host": "192.168.56.101",
    "username": "admin",
    "password": "cisco123!",
    "secret": "cisco123!",
}

comandos_eigrp = [
    "ipv6 unicast-routing",
    "router eigrp EXAMEN-DRY7122",
    " address-family ipv4 unicast autonomous-system 100",
    "  af-interface GigabitEthernet1",
    "   passive-interface",
    "  exit-af-interface",
    "  network 0.0.0.0",
    " exit-address-family",
    "router eigrp EXAMEN-DRY7122",
    " address-family ipv6 unicast autonomous-system 100",
    "  af-interface GigabitEthernet1",
    "   passive-interface",
    "  exit-af-interface",
    " topology base",
    " exit-af-topology",
    " exit-address-family",
]

conexion = ConnectHandler(**dispositivo)
conexion.enable()

print("=== Configurando EIGRP Nombrado IPv4/IPv6 ===")
salida_config = conexion.send_config_set(comandos_eigrp)
print(salida_config)

print("\n=== Verificando configuracion EIGRP (show running-config | section eigrp) ===")
salida_eigrp = conexion.send_command("show running-config | section eigrp")
print(salida_eigrp)

print("\n=== Estado e IP de las interfaces (show ip interface brief) ===")
salida_interfaces = conexion.send_command("show ip interface brief")
print(salida_interfaces)

print("\n=== Running-config completo (show running-config) ===")
salida_running = conexion.send_command("show running-config")
print(salida_running)

print("\n=== Version del equipo (show version) ===")
salida_version = conexion.send_command("show version")
print(salida_version)

conexion.disconnect()
