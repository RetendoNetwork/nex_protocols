from enum import IntEnum

from nex.endpoint_interface import EndpointInterface
from nex.service_protocol import ServiceProtocol
from nex.packet_interface import PacketInterface
from nex.error import Error
from nex_protocols.globals import Globals


class HealthProtocol(IntEnum):
    PROTOCOL_ID = 0x12
    METHOD_PING_DAEMON = 0x1
    METHOD_PING_DATABASE = 0x2
    METHOD_RUN_SANITY_CHECK = 0x3
    METHOD_FIX_SANITY_ERRORS = 0x4

    def __init__(self):
        self.endpoint = EndpointInterface()
        self.PingDaemon = None
        self.PingDatabase = None
        self.RunSanityCheck = None
        self.FixSanityErrors = None
        self.Patches = ServiceProtocol()
        self.PatchedMethods = []

    def endpoint(self) -> EndpointInterface:
        return self.endpoint

    def set_endpoint(self, endpoint: EndpointInterface):
        self.endpoint = endpoint

    def set_handler_ping_daemon(self, handler):
        self.PingDaemon = handler

    def set_handler_ping_database(self, handler):
        self.PingDatabase = handler

    def set_handler_run_sanity_check(self, handler):
        self.RunSanityCheck = handler

    def set_handler_fix_sanity_errors(self, handler):
        self.FixSanityErrors = handler

    def handle_packet(self, packet: PacketInterface):
        globals = Globals()
        message = packet.rmc_message()

        if not message.is_request or message.protocol_id != self.PROTOCOL_ID:
            return

        if self.Patches and message.method_id in self.PatchedMethods:
            self.Patches.handle_packet(packet)
            return

        if message.method_id == self.METHOD_PING_DAEMON:
            Health.ping_daemon(packet)
        elif message.method_id == self.METHOD_PING_DATABASE:
            Health.ping_database(packet)
        elif message.method_id == self.METHOD_RUN_SANITY_CHECK:
            Health.run_sanity_check(packet)
        elif message.method_id == self.METHOD_FIX_SANITY_ERRORS:
            Health.fix_sanity_errors(packet)
        else:
            err_message = f"Unsupported Health method ID: {message.method_id:#x}"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.respond_error(packet, self.PROTOCOL_ID, err)
            globals.logger.warning(err.message)


class Health:
    def ping_daemon(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id

        globals.respond(packet)

    def ping_database(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id

        globals.respond(packet)

    def run_sanity_check(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id

        globals.respond(packet)

    def fix_sanity_errors(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id

        globals.respond(packet)