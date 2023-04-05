def connectMQTT():
    # replace HiveMQ server url, user, and password with own
    client = MQTTClient(client_id=b"Alan_PicoW", server=b"********.hivemq.cloud", port=0, user=b"********", password=b"********",
                        keepalive=7200, ssl=True, ssl_params={'server_hostname':'********.hivemq.cloud'}
                        )
    client.connect()
    return client
