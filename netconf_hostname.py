from ncclient import manager

HOST = "192.168.56.101"
PORT = 830
USER = "admin"
PASS = "cisco123!"

nuevo_hostname = "Reyes-Urra-Fernandez-Henriquez" 

config_xml = f"""
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>{nuevo_hostname}</hostname>
  </native>
</config>
"""

with manager.connect(
    host=HOST,
    port=PORT,
    username=USER,
    password=PASS,
    hostkey_verify=False,
    device_params={"name": "csr"},
    look_for_keys=False,
    allow_agent=False
) as m:
    respuesta = m.edit_config(target="running", config=config_xml)
    print("Resultado del cambio de hostname:")
    print(respuesta)
