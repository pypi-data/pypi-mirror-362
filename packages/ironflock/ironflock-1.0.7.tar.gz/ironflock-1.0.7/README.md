# ironflock

## About

With this library you can publish data from your apps on your IoT edge hardware to the fleet data storage of the [IronFlock](https://studio.ironflock.com) devops platform.
When this library is used on a certain device the library automatically uses the private messaging realm (Unified Name Space)
of the device's fleet and the data is collected in the respective fleet database.

So if you use the library in your app, the data collection will always be private to the app user's fleet.

For more information on the IronFlock IoT Devops Platform for engineers and developers visit our [IronFlock](https://www.ironflock.com) home page.
## Usage

```python
import asyncio
from ironflock import IronFlock

# create an IronFlock instance to connect to the IronFlock platform data infrastructure.
# The IronFlock instance handles authentication when run on a device registered in IronFlock.
ironflock = IronFlock()

async def main():
    while True:
        # publish an event (if connection is not established the publish is skipped)
        publication = await ironflock.publish("test.publish.com", {"temperature": 20})
        print(publication)
        await asyncio.sleep(3)


if __name__ == "__main__":
    ironflock = IronFlock(mainFunc=main)
    ironflock.run()
```

## Options

The `IronFlock` `__init__` function can be configured with the following options:

```ts
{
    serial_number: string;
}
```

**serial_number**: Used to set the serial_number of the device if the `DEVICE_SERIAL_NUMBER` environment variable does not exist. It can also be used if the user wishes to authenticate as another device.

## Advanced Usage

If you need more control, e.g. acting on lifecycle events (`onJoin`, `onLeave`) take a look at
the [examples](https://github.com/RecordEvolution/ironflock-py/tree/main/examples) folder.


## Development

Install the necessary components if you don't have them already:

```shell
pip install --upgrade setuptools wheel twine
```

Build and publish a new pypi package:

```shell
make publish
```

Check the package at https://pypi.org/project/ironflock/.