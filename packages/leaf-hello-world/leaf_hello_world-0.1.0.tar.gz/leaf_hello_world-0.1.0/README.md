# Laboratory Equipment Adapter Framework - LEAF

This is a demo adapter for the Laboratory Equipment Adapter Framework (LEAF). It is a simple adapter that will be used to showcase how an adapter can be created and integrated into the LEAF framework.

## Installation

To install the adapter, you can use the following command:

```bash
# Clone the repository...

# Install the adapter into your python environment
poetry build
pip install dist/leaf_hello_world-0.1.0.tar.gz
```

## Usage

Once installed within `leaf` you can add a new equipment to the (minimal) config file.

```
EQUIPMENT_INSTANCES:
  - equipment:
      adapter: hello_world
      data:
        instance_id: example_equipment_id1
        institute: example_equipment_institute1
      requirements:
        interval: 11
OUTPUTS:
  - plugin: MQTT
    broker: test.mosquitto.org
    port: 1883
```

You can then start the leaf program and it should sent a 'hello world' message every 11 seconds.
