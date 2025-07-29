import logging
import os
import time
from threading import Thread
from typing import Optional

from leaf.adapters.core_adapters.discrete_experiment_adapter import DiscreteExperimentAdapter
from leaf.error_handler.error_holder import ErrorHolder
from leaf.modules.input_modules.polling_watcher import PollingWatcher
from leaf.modules.input_modules.simple_watcher import SimpleWatcher
from leaf.modules.input_modules.external_event_watcher import ExternalEventWatcher
from leaf.utility.logger.logger_utils import get_logger
from leaf_register.metadata import MetadataManager

from leaf_hello_world.interpreter import HelloWorldInterpreter

logger = get_logger(__name__, log_file="app.log", log_level=logging.DEBUG)
current_dir = os.path.dirname(os.path.abspath(__file__))
metadata_fn = os.path.join(current_dir, 'device.json')

class HelloWorldAdapter(DiscreteExperimentAdapter):
    def __init__(
        self,
        instance_data,
        output,
        interval: int = 100,
        maximum_message_size: Optional[int] = 1,
        error_holder: Optional[ErrorHolder] = None,
        experiment_timeout: int|None=None,
        external_watcher: ExternalEventWatcher = None
        ) -> None:

        if instance_data is None or instance_data == {}:
            raise ValueError("Instance data cannot be empty")

        logger.info(f"Interval: {interval}")

        metadata_manager = MetadataManager()
        watcher: PollingWatcher = SimpleWatcher(metadata_manager=metadata_manager,interval=interval)

        self.interpreter = HelloWorldInterpreter(metadata_manager=metadata_manager)
        # Set instance data
        # self.interpreter.instance_data = instance_data

        super().__init__(instance_data=instance_data,
                         watcher=watcher,
                         output=output,
                         interpreter=self.interpreter,
                         maximum_message_size=maximum_message_size,
                         error_holder=error_holder,
                         metadata_manager=metadata_manager,
                         experiment_timeout=experiment_timeout,
                         external_watcher=external_watcher)

        self._metadata_manager.add_equipment_data(metadata_fn)

    def simulate(self, filename, interval) -> None:
        logger.info("Simulating adapter")
        # Start the proxy thread for the adapter
        proxy_thread = Thread(target=self.start)
        proxy_thread.start()

        with open(filename, "r") as f:
            header = f.readline().split(",")
            for line in f:
                line_split = line.strip().split(",")
                # Combine header and line_split into a dictionary
                line_dict = {header[i]: line_split[i] for i in range(len(header))}
                self.interpreter.data = line_dict
                logger.info(line)
                logger.info("Sleeping for %s seconds", interval)
                time.sleep(interval)
