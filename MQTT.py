def connectMQTT():
    # replace HiveMQ server url, user, and password with own
    client = MQTTClient(client_id=b"Alan_PicoW", server=b"cluster_URL.hivemq.cloud", port=0, user=b"MQTT_username", password=b"MQTT_password",
                        keepalive=7200, ssl=True, ssl_params={'server_hostname':'cluster_URL.hivemq.cloud'}
                        )
    client.connect()
    return client
