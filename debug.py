from enum import IntEnum

from nex.packet_interface import PacketInterface
from nex.endpoint_interface import EndpointInterface
from nex.service_protocol import ServiceProtocol
from nex.error import Error
from nex_protocols.globals import Globals


class DebugProtocol(IntEnum):
    PROTOCOL_ID = 0x74
    METHOD_ENABLE_API_RECORDER = 0x1
    METHOD_DISABLE_API_RECORDER = 0x2
    METHOD_IS_API_RECORDER_ENABLED = 0x3
    METHOD_GET_API_CALLS = 0x4
    METHOD_SET_EXCLUDE_JOINED_MATCHMAKE_SESSION = 0x5
    METHOD_GET_EXCLUDE_JOINED_MATCHMAKE_SESSION = 0x6
    METHOD_GET_API_CALL_SUMMARY = 0x7

    def __init__(self):
        self.endpoint = EndpointInterface
        self.EnableAPIRecorder = None
        self.DisableAPIRecorder = None
        self.IsAPIRecorderEnabled = None
        self.GetAPICalls = None
        self.SetExcludeJoinedMatchmakeSession = None
        self.GetExcludeJoinedMatchmakeSession = None
        self.GetAPICallSummary = None
        self.Patches = ServiceProtocol()
        self.PatchedMethods = []

    def endpoint(self) -> EndpointInterface:
        return self.endpoint
    
    def set_endpoint(self, endpoint: EndpointInterface):
        self.endpoint = endpoint

    def set_handler_enable_api_recorder(self, handler):
        self.EnableAPIRecorder = handler

    def set_handler_disable_api_recorder(self, handler):
        self.DisableAPIRecorder = handler

    def set_handler_is_api_recorder_enabled(self, handler):
        self.IsAPIRecorderEnabled = handler

    def set_handler_get_api_calls(self, handler):
        self.GetAPICalls = handler

    def set_handler_set_exclude_joined_matchmake_session(self, handler):
        self.SetExcludeJoinedMatchmakeSession = handler

    def set_handler_get_exclude_joined_matchmake_session(self, handler):
        self.GetExcludeJoinedMatchmakeSession = handler

    def set_handler_get_api_calls_summary(self, handler):
        self.GetAPICallSummary = handler

    def handle_packet(self, packet: PacketInterface):
        globals = Globals()
        message = packet.rmc_message()

        if not message.is_request or message.protocol_id != self.PROTOCOL_ID:
            return
        
        if self.Patches and message.method_id in self.PatchedMethods:
            self.Patches.handle_packet(packet)
            return
        
        if message.method_id == self.METHOD_ENABLE_API_RECORDER:
            Debug.enable_api_recorder(packet)
        elif message.method_id == self.METHOD_DISABLE_API_RECORDER:
            Debug.disable_api_recorder(packet)
        elif message.method_id == self.METHOD_IS_API_RECORDER_ENABLED:
            Debug.is_api_recorder_enabled(packet)
        else:
            err_message = f"Unsupported MatchMakingExt Debug ID: {message.method_id:#x}"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.respond_error(packet, self.PROTOCOL_ID, err)
            globals.logger.warning(err.message)


class Debug:
    def enable_api_recorder(packet: PacketInterface):
        globals = Globals()

        if DebugProtocol.EnableAPIRecorder is None:
            err_message = "Debug::EnableAPIRecorder not implemented"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.logger.warning(err.message)
            globals.respond_error(packet, DebugProtocol.PROTOCOL_ID, err)
            return

        request = packet.rmc_message()
        call_id = request.call_id

        rmc_message, rmc_error = DebugProtocol.EnableAPIRecorder(None, packet, call_id)
        if rmc_error:
            globals.respond_error(packet, DebugProtocol.METHOD_ENABLE_API_RECORDER, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    def disable_api_recorder(packet: PacketInterface):
        globals = Globals()

        if DebugProtocol.DisableAPIRecorder is None:
            err_message = "Debug::DisableAPIRecorder not implemented"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.logger.warning(err.message)
            globals.respond_error(packet, DebugProtocol.PROTOCOL_ID, err)
            return

        request = packet.rmc_message()
        call_id = request.call_id

        rmc_message, rmc_error = DebugProtocol.DisableAPIRecorder(None, packet, call_id)
        if rmc_error:
            globals.respond_error(packet, DebugProtocol.METHOD_DISABLE_API_RECORDER, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    def is_api_recorder_enabled(packet: PacketInterface):
        globals = Globals()

        if DebugProtocol.IsAPIRecorderEnabled is None:
            err_message = "Debug::IsAPIRecorderEnabled not implemented"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.logger.warning(err.message)
            globals.respond_error(packet, DebugProtocol.PROTOCOL_ID, err)
            return

        request = packet.rmc_message()
        call_id = request.call_id

        rmc_message, rmc_error = DebugProtocol.IsAPIRecorderEnabled(None, packet, call_id)
        if rmc_error:
            globals.respond_error(packet, DebugProtocol.METHOD_IS_API_RECORDER_ENABLED, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    # TODO - Add other stuff later