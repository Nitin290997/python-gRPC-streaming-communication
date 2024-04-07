"""
Methods for resource management across all services
"""
__author__ = ["nitinsaini2909@gmail.com"]

import time
import json
import logging
from pathlib import Path

_log = logging.getLogger("RESOURCE_MANAGER")

ROOT_DIR = Path(__file__).parent.parent.parent


class NewVersionReceived(Exception):
    def __init__(self, version: int, message="Received resource version received"):
        self.version = version
        self.message = message
        super().__init__(self.message)


class ResourceManager:
    """
    Class implements methods for resource management
    """
    def __init__(self, resource_file):
        """
        Initializes resource manager
        """
        self.resource_file = resource_file
        self.current_version = 0

    def monitor_for_version_update(self):
        """
        checks if there is a new version update in the resources are available
        """
        _log.info(f"[Waiting for new resource version. Current applied version: {self.current_version}")
        while True:
            try:
                time.sleep(0.2)
                with open(self.resource_file, "r") as version_file:
                    version_available = json.load(version_file)["version"]
                if version_available == self.current_version:
                    continue
                else:
                    self.current_version = version_available
                    _log.info(f"[Received new resource Version: {self.current_version}")
                    raise NewVersionReceived(self.current_version)
            except KeyError as e:
                continue
            except json.JSONDecodeError as e:
                continue
