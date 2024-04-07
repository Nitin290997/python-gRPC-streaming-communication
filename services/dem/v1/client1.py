"""
Extends proto.vehicle_pb2_grpc.Client1CommunicationServicer to implement method
"""
__author__ = ["nitinsaini2909@gmail.com"]

import json
import logging
import threading
from pathlib import Path

_log = logging.getLogger("CLIENT1")

from services.common.resource_management import ResourceManager, NewVersionReceived
from proto import schema_pb2_grpc, schema_pb2
from google.protobuf.json_format import MessageToDict

ROOT_DIR = Path(__file__).parent.parent.parent.parent
RESOURCE_FILE = ROOT_DIR / "resources/client1.json"


def generate_resources(resources_to_stream: list, resources: dict) -> list:
    def __get_resource_mapping(module: str) -> list:
        returnable_resource = list()
        for error in resources[module]:
            returnable_resource.append(schema_pb2.resources(resource={error['error_code']: error['error_message']}))
        return returnable_resource

    responseData = list()
    for module in resources_to_stream:
        moduleData = __get_resource_mapping(module)
        if len(moduleData) > 0:
            responseData.extend(moduleData)

    return responseData


class Client1CommunicationServicer(schema_pb2_grpc.Client1CommunicationServicer):
    """
    Class that Diagnostic Error Manager Network Communication
    """
    current_version = 0
    nonce = str()

    def __init__(self) -> None:
        """
        Function to initialize client1 operator
        """
        self.monitor_thread = threading.Thread
        self.resource_manager = ResourceManager(resource_file=RESOURCE_FILE.__str__())

    def build_response(self, request_data, version_available):
        """
        Builds response to be sent back
        """
        resources_to_stream = list()

        with open(RESOURCE_FILE.__str__(), "r") as f:
            resource = json.load(f)

        for resource_module in request_data['resourceLocators']:
            if resource_module in resource["modules"]:
                resources_to_stream.append(resource_module)

        Client1CommunicationServicer.nonce = str(f"{version_available}A")

        response_data = schema_pb2.Response(
            version_info=str(version_available),
            resources=generate_resources(resources_to_stream, resource['modules']),
            nonce=Client1CommunicationServicer.nonce,
            ServerId="Network Server"
        )
        return response_data

    def StreamResources(self, request_iterator, context):
        """
        Function accepts node requests and responds with requested resources
        """
        request_data = dict
        try:
            for request in request_iterator:
                request_data = MessageToDict(request)
                _log.info(f"[{context.peer()}] | REQUEST | CLIENT1 Data Request")
                _log.debug(f"request data - {request_data}")

                self.monitor_thread = threading.Thread(
                    daemon=True,
                    target=self.resource_manager.monitor_for_version_update()
                )
                self.monitor_thread.start()
                self.monitor_thread.join()

        except NewVersionReceived as e:
            Client1CommunicationServicer.current_version = e.version
            responseData = self.build_response(
                request_data=request_data,
                version_available=Client1CommunicationServicer.current_version
            )
            _log.info(f"[{context.peer()}] | RESPONSE | CLIENT1 Data Response")
            _log.debug(f"response data - {responseData}")
            yield responseData
