import os
import asyncio
from typing import Optional
from autobahn.asyncio.component import Component, run
from autobahn.wamp.interfaces import ISession
from autobahn.wamp.types import PublishOptions, RegisterOptions
from autobahn.wamp.request import Publication

from ironflock.AutobahnConnection import getSerialNumber, create_application_component


class IronFlock:
    """Conveniance class for easy-to-use message publishing in the IronFlock platform.

    Example:

        async def main():
            while True:
                publication = await ironFlock.publish("test.publish.pw", 1, "two", 3, foo="bar")
                print(publication)
                await asyncio.sleep(3)


        if __name__ == "__main__":
            ironflock = IronFlock(mainFunc=main)
            ironFlock.run()
    """

    def __init__(self, serial_number: str = None, mainFunc=None) -> None:
        """Creates IronFlock Instance

        Args:
            serial_number (str, optional): serial_number of device.
            Defaults to None, in which case the environment variable DEVICE_SERIAL_NUMBER is used.
        """
        self._serial_number = getSerialNumber(serial_number)
        self._device_name = os.environ.get("DEVICE_NAME")
        self._device_key = os.environ.get("DEVICE_KEY")
        self._component = create_application_component(serial_number)
        self._session: ISession = None
        self.mainFunc = mainFunc

        @self._component.on_join
        async def onJoin(session, details):
            print("component joined")
            self._session = session
            if self.mainFunc: 
                self._main_task = asyncio.create_task(mainFunc())

        @self._component.on_disconnect
        @self._component.on_leave
        async def onLeave(*args, **kwargs):
            print("component left")
            if self._main_task:
                self._main_task.cancel()
                try:
                    await self._main_task
                except asyncio.CancelledError:
                    pass
                self._main_task = None
            self._session = None

    @property
    def component(self) -> Component:
        """The Autobahn Component

        Returns:
            Component
        """
        return self._component

    @property
    def session(self) -> Optional[ISession]:
        """The Autobahn Session

        Returns:
            Optional[ISession]
        """
        return self._session

    async def publish(self, topic: str, *args, **kwargs) -> Optional[Publication]:
        """Publishes to the IronFlock Platform Message Router

        Args:
            topic (str): The URI of the topic to publish to, e.g. "com.myapp.mytopic1"

        Returns:
            Optional[Publication]: Object representing a publication
            (feedback from publishing an event when doing an acknowledged publish)
        """

        extra = {
            "DEVICE_SERIAL_NUMBER": self._serial_number,
            "DEVICE_KEY": self._device_key,
            "DEVICE_NAME": self._device_name,
            "options": PublishOptions(acknowledge=True),
        }

        if self._session is not None:
            pub = await self._session.publish(topic, *args, **kwargs, **extra)
            return pub
        else:
            print("cannot publish, not connected")
            
    async def set_device_location(self, long: float, lat: float):
        """Update the location of the device registered in the platform
            This will update the device's location in the master data of the platform.
            The maps in the device or group overviews will reflect the new device location in realtime.
            The location history will not be stored in the platform. 
            If you need location history, then create a dedicated table for it.
        """

        payload = {
            "long": long,
            "lat": lat
        }
        
        extra = {
            "DEVICE_SERIAL_NUMBER": self._serial_number,
            "DEVICE_KEY": self._device_key,
            "DEVICE_NAME": self._device_name
        }
        
        if hasattr(self, "_session") and hasattr(self._session, "call"):
            res = await self._session.call('ironflock.location_service.update', payload, **extra)
        return res
    
    async def register_function(self, topic: str, func):
        """Registers a function to be called when a message is received on the given topic.
        
        Args:
            topic (str): The URI of the topic to register the function for, e.g. "example.mytopic1".
            func (callable): The function to call when a message is received on the topic.
        """
        swarm_key = os.environ.get("SWARM_KEY")
        app_key = os.environ.get("APP_KEY")
        env_value = os.environ.get("ENV")
        
        topic = f"{swarm_key}.{self._device_key}.{app_key}.{env_value}.{topic}"
        
        if self._session is not None:
            await self._session.register(topic, func, options=RegisterOptions(force_reregister=True))
        else:
            print("cannot register function, not connected")

    async def publish_to_table(
        self, tablename: str, *args, **kwargs
    ) -> Optional[Publication]:
        """Publishes Data to a Table in the IronFlock Platform. This is a conveniance function.
            You can achieve the same results by simply publishing a payload to the topic
            
            [SWARM_KEY].[APP_KEY].[your_table_name]
            
            The SWARM_KEY and APP_KEY are provided as environment variables to the device container.
            The also provided ENV variable holds either PROD or DEV to decide which topic to use, above.
            This function automatically detects the environment and publishes to the correct table.
        Args:
            tablename (str): The table name of the table to publish to, e.g. "sensordata"

        Returns:
            Optional[Publication]: Object representing a publication
            (feedback from publishing an event when doing an acknowledged publish)
        """

        if not tablename:
            raise Exception("Tablename must not be None or empty string!")

        swarm_key = os.environ.get("SWARM_KEY")
        app_key = os.environ.get("APP_KEY")
        env_value = os.environ.get("ENV")

        if swarm_key is None:
            raise Exception("Environment variable SWARM_KEY not set!")

        if app_key is None:
            raise Exception("Environment variable APP_KEY not set!")

        topic = f"{swarm_key}.{app_key}.{tablename}"

        pub = await self.publish(topic, *args, **kwargs)
        return pub

    def run(self, wait=True):
        """Runs the Component in the asyncio event loop."""
        if wait:
            run([self._component])
        else:
            return self._component.start()
