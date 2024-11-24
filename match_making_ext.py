from enum import IntEnum
from typing import List
import numpy as np

from nex.packet_interface import PacketInterface
from nex.nex_types.pid import PID
from nex.byte_stream_in import ByteStreamIn
from nex.endpoint_interface import EndpointInterface
from nex.service_protocol import ServiceProtocol
from nex.error import Error
from nex_protocols.globals import Globals


class MatchMakingExtProtocol(IntEnum):
    PROTOCOL_ID = 0x32
    METHOD_END_PARTICIPATION = 0x1
    METHOD_GET_PARTICIPANTS = 0x2
    METHOD_GET_DETAILED_PARTICIPANTS = 0x3
    METHOD_GET_PARTICIPANTS_URLS = 0x4
    METHOD_GET_GATHERING_RELATIONS = 0x5
    METHOD_DELETE_FROM_DELETIONS = 0x6

    def __init__(self):
        self.endpoint = EndpointInterface()
        self.EndParticipation = None
        self.GetParticipants = None
        self.GetDetailedParticipants = None
        self.GetParticipantsURLs = None
        self.GetGatheringRelations = None
        self.DeleteFromDeletions = None
        self.Patches = ServiceProtocol()
        self.PatchedMethods = []

    def endpoint(self) -> EndpointInterface:
        return self.endpoint
    
    def set_endpoint(self, endpoint: EndpointInterface):
        self.endpoint = endpoint

    def set_handler_end_participation(self, handler):
        self.EndParticipation = handler

    def set_handler_get_participants(self, handler):
        self.GetParticipants = handler

    def set_handler_get_detailed_participants(self, handler):
        self.GetDetailedParticipants = handler

    def set_handler_get_participants_urls(self, handler):
        self.GetParticipantsURLs = handler

    def set_handler_get_gathering_relations(self, handler):
        self.GetGatheringRelations = handler

    def set_handler_delete_from_deletions(self, handler):
        self.DeleteFromDeletions = handler

    def handle_packet(self, packet: PacketInterface):
        globals = Globals()
        message = packet.rmc_message()

        if not message.is_request or message.protocol_id != self.PROTOCOL_ID:
            return
        
        if self.Patches and message.method_id in self.PatchedMethods:
            self.Patches.handle_packet(packet)
            return
        
        if message.method_id == self.METHOD_END_PARTICIPATION:
            MatchMakingExt.end_participation(packet)
        elif message.method_id == self.METHOD_GET_PARTICIPANTS:
            MatchMakingExt.get_participants(packet)
        elif message.method_id == self.METHOD_GET_DETAILED_PARTICIPANTS:
            MatchMakingExt.get_detailed_participants(packet)
        elif message.method_id == self.METHOD_GET_PARTICIPANTS_URLS:
            MatchMakingExt.get_participants_urls(packet)
        elif message.method_id == self.METHOD_GET_GATHERING_RELATIONS:
            MatchMakingExt.get_gathering_relations(packet)
        elif message.method_id == self.METHOD_DELETE_FROM_DELETIONS:
            MatchMakingExt.delete_from_deletions(packet)
        else:
            err_message = f"Unsupported MatchMakingExt method ID: {message.method_id:#x}"
            err = Error(1, err_message) # TODO - Replace 1 to Core Implemented Error Code
            globals.respond_error(packet, self.PROTOCOL_ID, err)
            globals.logger.warning(err.message)


class MatchMakingExt:
    def end_participation(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        id_gathering = int
        str_message = str

        err = Error()

        rmc_message, rmc_error = MatchMakingExtProtocol.EndParticipation(None, packet, call_id, id_gathering, str_message)
        if rmc_error:
            globals.respond_error(packet, MatchMakingExtProtocol.PROTOCOL_ID, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    def get_participants(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        id_gathering = int
        b_only_active = bool

        err = Error()

        rmc_message, rmc_error = MatchMakingExtProtocol.GetParticipants(None, packet, call_id, id_gathering, b_only_active)
        if rmc_error:
            globals.respond_error(packet, MatchMakingExtProtocol.PROTOCOL_ID, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    def get_detailed_participants(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions, endpoint.byte_stream_settings())

        id_gathering = int
        b_only_active = bool

        rmc_message, rmc_error = MatchMakingExtProtocol.GetDetailedParticipants(None, packet, call_id, id_gathering, b_only_active)
        if rmc_error:
            globals.respond_error(packet, MatchMakingExtProtocol.PROTOCOL_ID, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    def get_participants_urls(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        lst_gatherings: List[int] = []

        rmc_message, rmc_error = MatchMakingExtProtocol.GetDetailedParticipants(None, packet, call_id, lst_gatherings)
        if rmc_error:
            globals.respond_error(packet, MatchMakingExtProtocol.PROTOCOL_ID, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    def get_gathering_relations(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        id = np.uint32 = np.uint32(0)
        descr: str = ""

        rmc_message, rmc_error = MatchMakingExtProtocol.GetDetailedParticipants(None, packet, call_id, id, descr)
        if rmc_error:
            globals.respond_error(packet, MatchMakingExtProtocol.PROTOCOL_ID, rmc_error)
            return
        
        globals.respond(packet, rmc_message)

    def delete_from_deletions(packet: PacketInterface):
        globals = Globals()
        request = packet.rmc_message()
        call_id = request.call_id
        parameters = request.parameters
        endpoint = packet.sender().endpoint()
        parameters_stream = ByteStreamIn(parameters, endpoint.library_versions(), endpoint.byte_stream_settings())

        lst_deletions = List[int] = []
        pid = PID()

        err = Error()

        rmc_message, rmc_error = MatchMakingExtProtocol.GetDetailedParticipants(None, packet, call_id, lst_deletions, pid)
        if rmc_error:
            globals.respond_error(packet, MatchMakingExtProtocol.PROTOCOL_ID, rmc_error)
            return
        
        globals.respond(packet, rmc_message)
