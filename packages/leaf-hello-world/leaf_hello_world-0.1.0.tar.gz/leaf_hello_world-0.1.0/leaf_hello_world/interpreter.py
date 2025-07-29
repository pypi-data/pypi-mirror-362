import logging
import os
import random
from datetime import datetime, timezone
from typing import Any

from influxobject import InfluxPoint
from leaf.adapters.equipment_adapter import AbstractInterpreter
from leaf.utility.logger.logger_utils import get_logger

# logger = get_logger(__name__, log_file="app.log", log_level=logging.DEBUG)

from leaf.start import logger

current_dir = os.path.dirname(os.path.abspath(__file__))
metadata_fn = os.path.join(current_dir, "device.json")


class HelloWorldInterpreter(AbstractInterpreter):
    # '<institute>/<equipment_id>/<instance_id>/details'
    def __init__(self, metadata_manager: Any) -> None:
        super().__init__()
        self.data = {}
        self.metadata_manager = metadata_manager
        logger.info("Initializing DEMO Interpreter")

    def retrieval(self) -> dict[str, Any]:
        logger.debug(f"Retrieval...")
        return {"measurement": "some data?", "start": None, "stop": None}

    def measurement(self, ignore) -> InfluxPoint:
        logger.debug("A hello world measurement is being prepared.")
        # Prepare the data
        influx_object = InfluxPoint()
        influx_object.measurement = "bioreactor_example"
        for key, value in self.metadata_manager.get_instance_data().items():
            key = key.lower().split("(")[0].strip().replace(" ", "_")
            if isinstance(value, (str, int, float)):
                influx_object.add_tag(key, value)

        # Add example fields such as temperature, pH, and agitation speed with random values
        temperature = round(random.uniform(25.0, 30.0), 2)
        pH = round(random.uniform(6.5, 7.5), 1)
        agitation_speed = round(random.uniform(100, 200), 0)
        # Add the fields to the InfluxPoint object
        influx_object.add_field("temperature", temperature)
        influx_object.add_field("pH", pH)
        influx_object.add_field("agitation_speed", agitation_speed)
        influx_object.time = datetime.now(timezone.utc)

        logger.info(f"Measurement: {influx_object}")

        return influx_object

    def metadata(self, data: Any) -> None:
        print(f"Metadata: {data}")
