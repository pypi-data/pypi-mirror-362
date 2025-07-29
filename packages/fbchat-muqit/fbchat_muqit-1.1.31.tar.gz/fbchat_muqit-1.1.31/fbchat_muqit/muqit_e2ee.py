# To do: Decrypt e2ee messages and establish connection to e2ee 

import aiomqtt

from . import State

class E2EEMqtt:
    _HOST = "web-chat-e2ee.facebook.com"

    @classmethod
    async def connect(cls, state: State):
        mqttClient = aiomqtt.Client(
            hostname=cls._HOST,
            identifier="mqttwsclient",
            clean_session=True,
            protocol=aiomqtt.ProtocolVersion.V31,
            transport="websockets",
            port=443,
            keepalive=60
        )
        mqttClient._client.tls_set()


