import os
from typing import Tuple
from autobahn.asyncio.component import Component
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth

try:
    SWARM_KEY = os.environ["SWARM_KEY"]
except:
    raise Exception("Environment variable SWARM_KEY not set!")

try:
    APP_KEY = os.environ["APP_KEY"]
except:
    raise Exception("Environment variable APP_KEY not set!")

try:
    ENV = os.environ["ENV"].lower()
except:
    raise Exception("Environment variable ENV not set!")

# CB_REALM = "userapps"
CB_REALM = f"realm-{SWARM_KEY}-{APP_KEY}-{ENV}"

DATAPODS_WS_URI = "wss://cbw.datapods.io/ws-ua-usr"
STUDIO_WS_URI_OLD = "wss://cbw.record-evolution.com/ws-ua-usr"
STUDIO_WS_URI = "wss://cbw.ironflock.com/ws-ua-usr"
LOCALHOST_WS_URI = "ws://localhost:8080/ws-ua-usr"

socketURIMap = {
    "https://studio.datapods.io": DATAPODS_WS_URI,
    "https://studio.record-evolution.com": STUDIO_WS_URI_OLD,
    "https://studio.ironflock.com": STUDIO_WS_URI,
    "http://localhost:8085": LOCALHOST_WS_URI,
}


def getWebSocketURI():
    reswarm_url = os.environ.get("RESWARM_URL")
    if not reswarm_url:
        return STUDIO_WS_URI
    return socketURIMap.get(reswarm_url)


def getSerialNumber(serial_number: str = None) -> str:
    if serial_number is None:
        s_num = os.environ.get("DEVICE_SERIAL_NUMBER")
        if s_num is None:
            raise Exception("ENV Variable 'DEVICE_SERIAL_NUMBER' is not set!")
    else:
        s_num = serial_number
    return s_num


class AppSession(ApplicationSession):
    serial_number: str = None

    def onConnect(self):
        print('onConnect called')
        if self.serial_number is None:
            raise Exception("serial_number missing on AppSession")

        self.join(CB_REALM, ["wampcra"], self.serial_number)

    def onChallenge(self, challenge):
        print('challenge requested for {}'.format(challenge.method))
        if challenge.method == "wampcra":
            if self.serial_number is None:
                raise Exception("serial_number missing on AppSession")

            signature = auth.compute_wcs(
                self.serial_number, challenge.extra["challenge"]
            )
            return signature

        raise Exception("Invalid authmethod {}".format(challenge.method))


def create_application_session(
    serial_number: str = None,
) -> Tuple[ApplicationSession, ApplicationRunner]:
    """Creates an Autobahn ApplicationSession and ApplicationRunner, which connects to the IronFlock Platform

    Args:
        serial_number (str, optional): serial_number of device.
        Defaults to None, in which case the environment variable DEVICE_SERIAL_NUMBER is used.

    Returns:
        Tuple[ApplicationSession, ApplicationRunner]
    """
    AppSession.serial_number = getSerialNumber(serial_number)

    runner = ApplicationRunner(
        url=getWebSocketURI(),
        realm=CB_REALM,
    )

    print('Application runner created')

    return AppSession, runner


def create_application_component(serial_number: str = None) -> Component:
    """Creates an Autobahn Component, which connects to the IronFlock Platform

    Args:
        serial_number (str, optional): serial_number of device.
        Defaults to None, in which case the environment variable DEVICE_SERIAL_NUMBER is used.

    Returns:
        Component
    """
    appSession, _ = create_application_session(serial_number)

    comp = Component(
        transports=[{
            "url": getWebSocketURI(),
            "serializers": ['msgpack'],
            }],
        realm=CB_REALM,
        session_factory=appSession,
    )
    print('WAMP Component created')

    return comp