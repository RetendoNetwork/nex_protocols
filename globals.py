from nex.packet_interface import PacketInterface
from nex.rmc import RMC
from nex.error import Error
from nex_logger.logger import Logger


class Globals:
    logger = Logger()

    def respond(packet: PacketInterface, message: RMC):
        sender = packet.sender()
        responsePacket = PacketInterface()

        # TODO - Add other code for respond function.

        sender.endpoint().send(responsePacket)

    def respond_error(packet: PacketInterface, protocol_id, error: Error):
        sender = packet.sender()
        request = packet.rmc_message()
        errorCode = request

        rmcResponse = RMC.new_rmc_error(sender.endpoint(), errorCode)
        rmcResponse.protocol_id = request.protocol_id
        rmcResponse.call_id = request.call_id

        responsePacket = PacketInterface()

        sender.endpoint().send(responsePacket)