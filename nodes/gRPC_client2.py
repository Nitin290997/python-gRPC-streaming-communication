"""
gRPC Client to run as a node or ecu with specific functionality
"""
__author__ = ["nitinsaini2909@gmail.com"]

import time
import sys
import argparse
import logging
from pathlib import Path

import grpc

ROOT_DIR = Path(__file__).parent.parent
if ROOT_DIR.__str__() not in sys.path:
    sys.path.append(ROOT_DIR.__str__())

from proto import vehicle_pb2_grpc
from proto import vehicle_pb2

from google.protobuf.json_format import MessageToDict


class DemClient:
    """
    Class implements method for starting and stopping client
    """

    def __init__(self, logger, serverHost: str = "0.0.0.0", securePort: int = 9010, port: int = 8010,
                 tls_Enabled: bool = False, frequency: int = 5):
        """
        Initiates Client instance with required arguments
        """
        self._log = logger
        self._channel = grpc.insecure_channel
        self.serverHost = serverHost
        self.securePort = securePort
        self.port = port
        self.frequency = frequency
        self.service_stub = None

    def RunClient(self):
        """
        Start gRPC Client
        """
        self._channel = grpc.insecure_channel(f"{self.serverHost}:{self.port}")
        self._log.info(f"Started gRPC DCM Client on {self.serverHost}:{self.port}")

        # comm test
        self._log.info(f"Beginning com test")
        comm_test_stub = vehicle_pb2_grpc.CommTestStub(self._channel)
        server_identity = comm_test_stub.Identify(vehicle_pb2.ClientHello(
            message="DCM Client",
            client_data="No Diagnostic Data"
        ))
        self._log.info(f"Com test response - {MessageToDict(server_identity)}")

        # Dem Service Stub
        self.service_stub = vehicle_pb2_grpc.DcmCommunicationStub(self._channel)

    def start_dcm_service(self):
        """
        Starts dcm service with dcm communication rpc
        """

        def request_generator(version: int):
            request = vehicle_pb2.Request(
                version=f"{version}",
                node="DCM_CLIENT",
                resource_names="DCM",
                resource_locators=["obd", "ota"],
                response_nonce="",
                error_detail=None
            )
            yield request

        version = 0

        while True:
            try:
                for response in self.service_stub.StreamResources(request_generator(version=version)):
                    self._log.info(f"Server Response: {MessageToDict(response)}")
                    version = int(response.version_info)

            except grpc.RpcError as e:
                self._log.error(e.details())
            except Exception as e:
                self._log.error(str(e))
            time.sleep(self.frequency)


def main():
    """
    Main function for starting the ECU client
    """
    parser = argparse.ArgumentParser(prog='gRPC Based ECU client', description='Utility to start client')
    parser.add_argument("--serverHost", type=str, default="0.0.0.0", help="Address to start server on")
    parser.add_argument("--serverSecurePort", type=int, default=9010, help="Port to start secure server")
    parser.add_argument("--serverPort", type=int, default=8010, help="Port to server on")
    parser.add_argument("--frequency", type=int, default=5, help="Sleep duration before attempting to reconnect")
    parser.add_argument("--logLevel", type=str, default="INFO", help="Logging level - INFO | DEBUG")
    args = parser.parse_args()

    log_level = logging.INFO
    if args.logLevel.lower() == "debug":
        log_level = logging.DEBUG

    CLIENT_LOG_FILE = ROOT_DIR / "logs/client2.log"
    logging.basicConfig(
        filename=CLIENT_LOG_FILE.__str__(),
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level,
        datefmt="%H:%M:%S"
    )
    _log = logging.getLogger("Dcm Client")

    client = DemClient(
        serverHost=args.serverHost,
        securePort=args.serverSecurePort,
        port=args.serverPort,
        logger=_log,
        frequency=args.frequency
    )
    client.RunClient()
    client.start_dcm_service()


if __name__ == "__main__":
    main()
