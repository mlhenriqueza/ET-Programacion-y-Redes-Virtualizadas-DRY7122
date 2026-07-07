from ncclient import manager

HOST = "192.168.56.101"
PORT = 830
USER = "admin"
PASS = "cisco123!"

config_xml = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
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
    print("Resultado de creación de Loopback11:")
    print(respuesta)
