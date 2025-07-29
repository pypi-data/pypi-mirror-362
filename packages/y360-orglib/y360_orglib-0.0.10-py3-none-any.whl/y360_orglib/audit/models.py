from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class MailEvent(BaseModel):
    """
    Audit logs mail Event
    Details https://yandex.ru/dev/api360/doc/ru/ref/AuditLogService/AuditLogService_Mail#v1mailevent

    Attributes:
        client_ip (str): Client IP
        date (str): Event date
        event_type (Literal): Event type (mailbox_send, message_receive, message_seen, message_unseen, message_forward, message_purge, message_trash, message_spam, message_unspam, message_move, message_copy, message_answer)
        org_id (int): Organization ID
        request_id (str): System request ID (may be Not unique)
        source (str): Event source (server, imap, pop3, native)
        uniq_id (str): Unique event ID
        user_login (str): User login
        user_name (str): User name
        user_uid (str): User ID
        actor_uid (Optional[str]): Mailbox Actor ID (if exists)
        bcc (Optional[str]): BCC address (if exists)
        cc (Optional[str]): CC address (if exists)
        to (Optional[str]): To address (if exists)
        dest_mid (Optional[str]): New email id on copy (if exists)
        folder_name (Optional[str]): Personal folder name (if exists)
        folder_type (Optional[Literal]): Folder type (inbox, sent, trash, spam, drafts, outbox, archive, discount, restored, reply_later, user)
        from_s (Optional[str]): From address (if exists)
        labels (Optional[List[str]]): System email labels (if exists) (seen, attached, undo, delayed)
        mid (Optional[str]): Email Id (if exists)
        msg_id (Optional[str]): Message-ID header value (if exists)
    
    """

    client_ip: str = Field(alias="clientIp")
    date: str  # ISO формат даты
    event_type: Literal[
        'mailbox_send',
        'message_receive',
        'message_seen',
        'message_unseen',
        'message_forward',
        'message_purge',
        'message_trash',
        'message_spam',
        'message_unspam',
        'message_move',
        'message_copy',
        'message_answer'
        ] = Field(alias='eventType')
    org_id: int = Field(alias="orgId")
    request_id: str = Field(alias="requestId")
    source: str
    uniq_id: str = Field(alias="uniqId")
    user_login: str = Field(alias="userLogin")
    user_name: str = Field(alias="userName")
    user_uid: str = Field(alias="userUid")
    actor_uid: Optional[str] = Field(alias="actorUid", default=None)
    bcc: Optional[str] = None
    cc: Optional[str] = None
    to: Optional[str] = None
    dest_mid: Optional[str] = Field(alias="destMid", default=None)
    folder_name: Optional[str] = Field(alias="folderName", default=None)
    folder_type: Optional[
        Literal[
            'inbox',
            'sent',
            'trash',
            'spam',
            'drafts',
            'outbox',
            'archive',
            'template_',
            'discount',
            'restored',
            'reply_later',
            'user'
            ]
        ] = Field(alias="folderType", default=None)
    from_s: Optional[str] = Field(alias="from", default=None)
    labels: Optional[List[str]] = None
    mid: Optional[str] = None
    msg_id: Optional[str] = Field(alias="msgId", default=None)
    # Todo: add subject

class MailEventsPage(BaseModel):
    """
    Audit logs mail Events page
    Details https://yandex.ru/dev/api360/doc/ru/ref/AuditLogService/AuditLogService_Mail

    Attributes:
        events (List[MailEvent]): List of events
        nextPageToken (Optional[str]): Next page token (if exists)

    """
    events: List[MailEvent]
    nextPageToken: Optional[str] = ''
