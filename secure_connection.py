from enum import IntEnum

from nex.packet_interface import PacketInterface
from nex.byte_stream_in import ByteStreamIn
from nex_protocols.globals import Globals
from nex.error import Error


class SecureConnectionProtocol(IntEnum):
    PROTOCOL_ID = 0xB
    METHOD_REGISTER = 0x1
    METHOD_REQUEST_CONNECTION_DATA = 0x2
    METHOD_REQUEST_URLS = 0x3
    METHOD_REGISTER_EX = 0x4
    METHOD_TEST_CONNECTIVITY = 0x5
    METHOD_UPDATE_URLS = 0x6
    METHOD_REPLACE_URL = 0x7
    METHOD_SEND_REPORT = 0x8



class SecureConnection:
    def register(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parametersStream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())
        
        globals.respond(packet)

    def register_ex(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters =request.parameters
        endpoint = packet.sender().endpoint()
        parametersStream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        err = Error()

        globals.respond(packet)

