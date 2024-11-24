from enum import IntEnum

from nex.endpoint_interface import EndpointInterface
from nex.service_protocol import ServiceProtocol
from nex.nex_types.pid import PID


class NintendoNotificationsProtocol(IntEnum):
    PROTOCOL_ID = 0x64
    METHOD_PROCESS_NINTENDO_NOTIFICATIONS_EVENT_1 = 0x1
    METHOD_PROCESS_NINTENDO_NOTIFICATIONS_EVENT_2 = 0x2

    def __init__(self):
        self.endpoint = EndpointInterface()
        self.Patches = ServiceProtocol()
        self.PatchedMethods = []

    def endpoint(self) -> EndpointInterface:
        return self.endpoint
    
    def set_endpoint(self, endpoint: EndpointInterface):
        self.endpoint = endpoint


class NotificationTypes(IntEnum):
    FriendPresenceUpdated3DS = 1
    FriendFavoriteGameUpdated3DS = 2
    FriendCommentUpdated3DS = 3
    FriendMiiChanged3DS = 5
    FriendshipCompleted3DS = 7
    FriendOffline = 10
    FriendMiiChanged = 21
    Unknown1MiiRelated = 22
    FriendPreferencesChanged = 23
    FriendStartedTitle = 24
    Unknown2FriendRequestRelated = 25
    FriendRemoved = 26
    FriendRequestCanceled = 26
    FriendRequestReceived = 27
    Unknown3FriendRequestRelated = 28
    Unknown4BlacklistRelated = 29
    FriendRequestAccepted = 30
    Unknown5BlacklistRelated = 31
    Unknown6BlacklistRelated = 32
    FriendStatusMessageChanged = 33
    Unknown7 = 34
    Unknown8FriendshipRelated = 35
    Unknown9PersistentNotificationsRelated = 36


class NintendoNotificationEvent:
    pass # TODO - Do Nintendo Notification Event


class NintendoNotificationEventGeneral:
    pass # TODO - Do Nintendo Notification Event General