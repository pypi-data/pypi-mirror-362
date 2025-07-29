
from typing import List, Optional, Literal
from pydantic import BaseModel, ConfigDict
from enum import Enum

class TelemostConference(Enum):
    created = 'telemost_conference.created'
    access_level_changed = 'telemost_conference.access_level_changed'
    started = 'telemost_conference.started'
    ended = 'telemost_conference.ended'

    
    class Peer(Enum):
        joined = 'telemost_conference.peer.joined'
        kicked = 'telemost_conference.peer.kicked'
        role_changed = 'telemost_conference.peer.role_changed'

    class WaitingRoom(Enum):
        peer_joined = 'telemost_conference.waiting_room.peer.joined'
        peer_admitted = 'telemost_conference.waiting_room.peer.admitted'
        peer_left = 'telemost_conference.waiting_room.peer.left'

    class LiveStream(Enum):
        created = 'telemost_conference.live_stream.created'
        started = 'telemost_conference.live_stream.started'
        access_level_changed = 'telemost_conference.live_stream.access_level_changed'
        ended = 'telemost_conference.live_stream.ended'
        viewer_joined = 'telemost_conference.live_stream.viewer.joined'

class MessengerChat(Enum):
    created = 'messenger_chat.created'
    info_changed = 'messenger_chat.info_changed'
    invite_link_renewed = 'messenger_chat.invite_link_renewed'
    member_rights_changed = 'messenger_chat.member_rights_changed'
    group_added = 'messenger_chat.group_added'
    group_removed = 'messenger_chat.group_removed'
    department_added = 'messenger_chat.department_added'
    department_removed = 'messenger_chat.department_removed'
    file_sent = 'messenger_chat.file_sent'
    message_deleted = 'messenger_chat.message_deleted'
    call_started = 'messenger_chat.call_started'
    takeout_requested = 'messenger_chat.takeout_requested'

    class Member(Enum):
        added = 'messenger_chat.member.added'
        role_changed = 'messenger_chat.member.role_changed'
        removed = 'messenger_chat.member.removed'



class AuditLogEvent(BaseModel):
    """
    Audit log event
    Args:
        status (str): Request status& Success or Error
        idempotency_id (str): Event ID
        uid (int): ID of initiator User of the event
        service (str): Service name of the event. Possible values: Web, Desktop, Mobile, Api, Synchronization, ID, Internal, Unknown
        ip (str): User or source service IP address. For auto initiated events is localhost
        occurred_at (str): Occurred at of the event in ISO 8601 format
        org_id (str): Organization ID
        is_system (bool): Not in use. Always false
        meta (dict): Additional event data in JSON format
        request_id (str): ID of request
        type (str): Type of the event. See https://yandex.ru/dev/api360/doc/ru/audit-logs/get-logs#types for details
    """

    model_config = ConfigDict(coerce_numbers_to_str=True)
    
    status: str
    idempotency_id:str   
    uid: Optional[int] = 0
    service: Literal['Web', 'Desktop', 'Mobile', 'Api', 'Synchronization', 'ID', 'Internal', 'Unknown']
    ip: str
    occurred_at: str
    org_id: str
    is_system: bool = False
    meta: dict
    request_id: str
    type: str

class EnrichedEvent(BaseModel):
    """
    Audit log event with data
    Args:
        user_login (str): User login
        user_name (str): User name
        event (AuditLogEvent): Audit log event itself
    """
    user_login: str
    user_name: str
    event: AuditLogEvent

class AuditLogEventsPage(BaseModel):
    """
    Audit log events page
    Args:
        iteration_key (str): Next page iteration key
        items (list[EnrichedEvent]): List of audit log EnrichedEvents
    """
    iteration_key: Optional[str] = None
    items: List[EnrichedEvent]