### Description of the MQTT-Broker

**persistence true**
    - Enables persistant storage of messages, that means that the broker will save messages (e.g. for Qos 1 or Qos 2) and retransmit them even after a reboot.
    - This avoids loss of importent messages should the broker crash or get rebootet

**listener 1883**
    - Starts the broker on port 1883 (standardised port für unencryptet MQTT).
    - Clients must connect to this port.
    - If a different port is needed (e.g. for TLS), an additional listener-row could be neccessary (e.g. listener 8883 for encryptet MQTT).

**allow_anonymous false**
    - Disables anonymous connections, i.e. all clients have to autheticate themselves with username and passwort.
    - The user managment is done via [mosquitto_passwd](../../../../source/mqttBroker/mosquitto/passwd).
