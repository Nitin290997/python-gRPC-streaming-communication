"""
Extends proto.vehicle_pb2_grpc.CommTestServicer to implement method
"""
__author__ = ["nitinsaini2909@gmail.com"]

import logging

_log = logging.getLogger("COMM_TEST")

from proto import vehicle_pb2_grpc, vehicle_pb2
from google.protobuf.json_format import MessageToDict


class CommTestServicer(vehicle_pb2_grpc.CommTestServicer):

    def Identify(self, request, context):
        """
        Function accepts node communication test identifies rpc and responds accordingly
        """
        request_data = MessageToDict(request)
        _log.info(f"[{context.peer()}] | REQUEST | IDENTIFY")
        _log.debug(f"request data - {request_data}")
        ResponseData = vehicle_pb2.ServerHello(
            ack="Identified",
            response_string="Network Server"
        )
        _log.info(f"[{context.peer()}] | RESPONSE | IDENTIFY ACK SERVER")
        _log.debug(f"response data - {ResponseData}")
        return ResponseData
