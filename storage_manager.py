from enum import IntEnum

from nex.endpoint_interface import EndpointInterface
from nex.byte_stream_in import ByteStreamIn
from nex.service_protocol import ServiceProtocol
from nex.packet_interface import PacketInterface
from nex.error import Error
from nex_protocols.globals import Globals


class StorageManagerProtocol(IntEnum):
    PROTOCOL_ID = 0x6E
    METHOD_ACQUIRE_CARD_ID = 0x4
    METHOD_ACTIVATE_WITH_CARD_ID = 0x5

    def __init__(self):
        self.endpoint = EndpointInterface()
        self.AcquireCardID = None
        self.ActivateWithCardID = None
        self.Patches = ServiceProtocol()
        self.PatchedMethods = []

    def endpoint(self) -> EndpointInterface:
        return self.endpoint

    def set_endpoint(self, endpoint: EndpointInterface):
        self.endpoint = endpoint

    def set_handler_acquire_card_id(self, handler):
        self.AcquireCardID = handler

    def set_handler_activate_with_card_id(self, handler):
        self.ActivateWithCardID = handler

    def handle_packet(self, packet: PacketInterface):
        globals = Globals()
        message = packet.rmc_message()

        if not message.is_request or message.protocol_id != self.PROTOCOL_ID:
            return

        if self.Patches and message.method_id in self.PatchedMethods:
            self.Patches.handle_packet(packet)
            return

        if message.method_id == self.METHOD_ACQUIRE_CARD_ID:
            StorageManager.acquire_card_id(packet)
        elif message.method_id == self.METHOD_ACTIVATE_WITH_CARD_ID:
            StorageManager.activate_with_card_id(packet)
        else:
            err_message = f"Unsupported Health method ID: {message.method_id:#x}"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.respond_error(packet, self.PROTOCOL_ID, err)
            globals.logger.warning(err.message)


class StorageManager:
    def acquire_card_id(packet: PacketInterface):
        globals = Globals()

        if StorageManagerProtocol.AcquireCardID is None:
            err_message = "StorageManager::AcquireCardID not implemented"
            err = Error(1, err_message)  # TODO - Replace 1 to Core Implemented Error Code
            globals.logger.warning(err.message)
            globals.respond_error(packet, StorageManagerProtocol.PROTOCOL_ID, err)
            return

        request = packet.rmc_message()
        call_id = request.call_id

        rmc_message, rmc_error = StorageManagerProtocol.AcquireCardID(None, packet, call_id)
        if rmc_error:
            globals.respond_error(packet, StorageManagerProtocol.PROTOCOL_ID, rmc_error)
            return

        globals.respond(packet, rmc_message)

    def activate_with_card_id(packet: PacketInterface):
        globals = Globals()

        if StorageManagerProtocol.ActivateWithCardID is None:
            err_message = "StorageManager::ActivateWithCardID not implemented"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.respond_error(packet, StorageManagerProtocol.PROTOCOL_ID, err)
            return
        
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        unknown = None
        card_id = None

        rmc_message, rmc_error = StorageManagerProtocol.ActivateWithCardID(None, packet, call_id, unknown, card_id)
        if rmc_error:
            globals.respond_error(packet, rmc_error)
            return

        globals.respond(packet, rmc_message)