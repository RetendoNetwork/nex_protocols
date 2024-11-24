from enum import IntEnum
from typing import List

from nex.packet_interface import PacketInterface
from nex.byte_stream_in import ByteStreamIn
from nex.endpoint_interface import EndpointInterface
from nex.service_protocol import ServiceProtocol
from nex.error import Error
from nex_protocols.globals import Globals


class NatTraversalProtocol(IntEnum):
    PROTOCOL_ID = 0x13
    METHOD_REQUEST_PROBE_INITIATION = 0x1
    METHOD_INITIATE_PROBE = 0x2
    METHOD_REQUEST_PROBE_INITIATION_EXT = 0x3
    METHOD_REPORT_NAT_TRAVERSAL_RESULT = 0x4
    METHOD_REPORT_NAT_PROPERTIES = 0x5
    METHOD_GET_RELAY_SIGNATURE_KEY = 0x6
    METHOD_REPORT_NAT_TRAVERSAL_RESULT_DETAIL = 0x7

    def __init__(self):
        self.endpoint = EndpointInterface()
        self.RequestProbeInitiation = None
        self.InitiateProbe = None
        self.RequestProbeInitiationExt = None
        self.ReportNATTraversalResult = None
        self.ReportNATProperties = None
        self.GetRelaySignatureKey = None
        self.ReportNATTraversalResultDetail = None
        self.Patches = ServiceProtocol()
        self.PatchedMethods = []

    def endpoint(self) -> EndpointInterface:
        return self.endpoint
    
    def set_endpoint(self, endpoint: EndpointInterface):
        self.endpoint = endpoint

    def set_handler_request_probe_initiation(self, handler):
        self.RequestProbeInitiation = handler

    def set_handler_initiate_probe(self, handler):
        self.ProbeInitiation = handler

    def set_handler_request_probe_initiation_ext(self, handler):
        self.RequestProbeInitiationExt  = handler

    def set_handler_report_nat_traversal_result(self, handler):
        self.ReportNATTraversalResult = handler

    def set_handler_report_nat_properties(self, handler):
        self.ReportNATProperties = handler

    def set_handler_get_relay_signature_key(self, handler):
        self.GetRelaySignatureKey = handler

    def set_handler_report_nat_traversal_result_detail(self, handler):
        self.ReportNATTraversalResultDetail = handler

    def handle_packet(self, packet: PacketInterface):
        globals = Globals()

        message = packet.rmc_message()

        if not message.is_request or message.protocol_id != self.PROTOCOL_ID:
            return
        
        if self.Patches and message.method_id in self.PatchedMethods:
            self.Patches.handle_packet(packet)
            return
        
        if message.method_id == self.METHOD_REQUEST_PROBE_INITIATION:
            NatTraversal.request_probe_initiation(packet)
        else:
            err_message = f"Unsupported NatTraversal method ID: {message.method_id:#x}"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.respond_error(packet, self.PROTOCOL_ID, err)
            globals.logger.warning(err.message)


class NatTraversal:
    def request_probe_initiation(packet: PacketInterface):
        globals = Globals()

        if NatTraversalProtocol.RequestProbeInitiation is None:
            err_message = "NATTraversal::RequestProbeInitiation not implemented"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.logger.warning(err.message)
            globals.respond_error(packet, NatTraversalProtocol.PROTOCOL_ID, err)
            return
        
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        url_target_list = List

        rmc_message, rmc_error = NatTraversalProtocol.RequestProbeInitiation(None, packet, call_id, url_target_list)
        if rmc_error:
            globals.respond_error(packet, NatTraversalProtocol.PROTOCOL_ID, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

        # TODO - Add more stuff for Nat Traversal