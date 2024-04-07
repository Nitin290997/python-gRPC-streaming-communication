"""
gRPC Server to run as network layer for inter-ecu communications
"""
__author__ = ["nitinsaini2909@gmail.com"]

import argparse
import sys
import os
import grpc
import logging
from pathlib import Path
from concurrent import futures

ROOT_DIR = Path(__file__).parent.parent
SERVER_LOG_FILE = ROOT_DIR / "logs/server.log"

if ROOT_DIR.__str__() not in sys.path:
    sys.path.append(ROOT_DIR.__str__())

from proto import vehicle_pb2_grpc

from services.comm_test.v1.comm_test import CommTestServicer
from services.dem.v1.client1 import DemCommunicationServicer
from services.dcm.v1.client2 import Client2CommunicationServicer


class NetworkServer:
    """
    Class implements method for starting and stopping its Network Server
    """

    def __init__(self, logger, serverHost: str = "0.0.0.0", securePort: int = 9010, port: int = 8010,
                 tls_Enabled: bool = False):
        """
        Initiates Network Server instance with required arguments
        """
        self._log = logger
        self.serverHost = serverHost
        self.securePort = securePort
        self.port = port
        # self.SERVER_CERTIFICATE = self._load_credential_from_file("certs/server.pem")
        # self.SERVER_CERTIFICATE_KEY = self._load_credential_from_file("certs/server.key")
        # self.ROOT_CERTIFICATE = self._load_credential_from_file("certs/network_ca.pem")
        self._server = None

    @staticmethod
    def _load_credential_from_file(filepath):
        real_path = os.path.join(os.path.dirname(__file__), filepath)
        with open(real_path, "rb") as f:
            return f.read()

    def RunServer(self):
        """
        Start gRPC server
        """
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        vehicle_pb2_grpc.add_CommTestServicer_to_server(CommTestServicer(), self._server)
        vehicle_pb2_grpc.add_DemCommunicationServicer_to_server(DemCommunicationServicer(), self._server)
        vehicle_pb2_grpc.add_DcmCommunicationServicer_to_server(Client2CommunicationServicer(), self._server)

        self._server.add_insecure_port(f"{self.serverHost}:{self.port}")
        self._log.info(f"Started gRPC Server on {self.serverHost}:{self.port}")

        self._server.start()
        self._server.wait_for_termination()


def main():
    """
    Main function for starting the ECU Server layer
    """
    parser = argparse.ArgumentParser(prog='gRPC Based ECU Service layer', description='Utility to start server')
    parser.add_argument("--serverHost", type=str, default="0.0.0.0", help="Address to start server on")
    parser.add_argument("--serverSecurePort", type=int, default=9010, help="Port to start secure server")
    parser.add_argument("--serverPort", type=int, default=8010, help="Port to server on")
    parser.add_argument("--logLevel", type=str, default="INFO", help="Logging level - INFO | DEBUG")
    args = parser.parse_args()

    log_level = logging.INFO
    if args.logLevel.lower() == "debug":
        log_level = logging.DEBUG

    logging.basicConfig(
        filename=SERVER_LOG_FILE.__str__(),
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level,
        datefmt="%H:%M:%S"
    )
    _log = logging.getLogger("Vehicle Network")

    server = NetworkServer(
        serverHost=args.serverHost,
        securePort=args.serverSecurePort,
        port=args.serverPort,
        logger=_log
    )
    server.RunServer()


if __name__ == "__main__":
    main()
