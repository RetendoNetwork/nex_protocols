from enum import IntEnum

from nex.endpoint_interface import EndpointInterface
from nex.service_protocol import ServiceProtocol
from nex.packet_interface import PacketInterface
from nex.error import Error
from nex_protocols.globals import Globals


class MonitoringProtocol(IntEnum):
    PROTOCOL_ID = 0x13
    METHOD_PING_DAEMON = 0x1
    METHOD_GET_CLUSTER_MEMBERS = 0x2

    def __init__(self):
        self.endpoint = EndpointInterface()
        self.PingDaemon = None
        self.GetClusterMembers = None
        self.Patches = ServiceProtocol()
        self.PatchedMethods = []

    def endpoint(self) -> EndpointInterface:
        return self.endpoint

    def set_endpoint(self, endpoint: EndpointInterface):
        self.endpoint = endpoint

    def set_handler_ping_daemon(self, handler):
        self.PingDaemon = handler

    def set_handler_get_cluster_members(self, handler):
        self.GetClusterMembers = handler

    def handle_packet(self, packet: PacketInterface):
        globals = Globals()
        message = packet.rmc_message()

        if not message.is_request or message.protocol_id != self.PROTOCOL_ID:
            return

        if self.Patches and message.method_id in self.PatchedMethods:
            self.Patches.handle_packet(packet)
            return

        if message.method_id == self.METHOD_PING_DAEMON:
            Monitoring.ping_daemon(packet)
        elif message.method_id == self.METHOD_GET_CLUSTER_MEMBERS:
            Monitoring.get_cluster_members(packet)
        else:
            err_message = f"Unsupported Monitoring method ID: {message.method_id:#x}"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.respond_error(packet, self.PROTOCOL_ID, err)
            globals.logger.warning(err.message)


class Monitoring:
    def ping_daemon(packet: PacketInterface):
        globals = Globals()

        if MonitoringProtocol.PingDaemon is None:
            err_message = "Monitoring::PingDaemon not implemented"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.logger.warning(err.message)
            globals.respond_error(packet, MonitoringProtocol.PROTOCOL_ID, err)
            return

        request = packet.rmc_message()
        call_id = request.call_id

        rmc_message, rmc_error = MonitoringProtocol.PingDaemon(None, packet, call_id)
        if rmc_error:
            globals.respond_error(packet, MonitoringProtocol.PROTOCOL_ID, rmc_error)
            return

        globals.respond(packet, rmc_message)
        
    def get_cluster_members(packet: PacketInterface):
        globals = Globals()

        if MonitoringProtocol.GetClusterMembers is None:
            err_message = "Monitoring::GetClusterMembers not implemented"
            err = Error(1, err_message)
            globals.logger.warning(err.message)
            globals.respond_error(packet, MonitoringProtocol.PROTOCOL_ID, err)
            return

        request = packet.rmc_message()
        call_id = request.call_id

        rmc_message, rmc_error = MonitoringProtocol.GetClusterMembers(None, packet, call_id)
        if rmc_error:
            globals.respond_error(packet, MonitoringProtocol.PROTOCOL_ID, call_id)
            return

        globals.respond(packet, rmc_message)