"""
Audit Log module for interacting with the Y360 audit log API.

Details
https://yandex.ru/dev/api360/doc/ru/ref/AuditLogService/
https://yandex.ru/dev/api360/doc/ru/audit-logs/

"""

__version__ = "0.1.0"

from y360_orglib.audit.audit_mail import AuditMail
from y360_orglib.audit.audit_events import AuditEvents
from y360_orglib.audit.models import MailEventsPage, MailEvent
from y360_orglib.audit.event_models import AuditLogEventsPage, AuditLogEvent, EnrichedEvent, TelemostConference, MessengerChat

__all__ = [
    "AuditMail",
    "MailEventsPage",
    "MailEvent",
    "AuditEvents",
    "AuditLogEventsPage",
    "AuditLogEvent",
    "EnrichedEvent",
    "TelemostConference",
    "MessengerChat"
    ]
