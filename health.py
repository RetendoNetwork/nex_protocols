from enum import IntEnum

from nex.packet_interface import PacketInterface
from nex_protocols.globals import Globals


class HealthProtocol(IntEnum):
    PROTOCOL_ID = 0x12
    METHOD_PING_DAEMON = 0x1
    METHOD_PING_DATABASE = 0x2
    METHOD_RUN_SANITY_CHECK = 0x3
    METHOD_FIX_SANITY_ERRORS = 0x4


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

