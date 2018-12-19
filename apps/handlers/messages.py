from typing import Dict
from carrier_client.manager import MessageManager
from carrier_client.message import OutgoingMessage
from django.conf import settings
from django_carrier_client.helpers import MessageManagerHelper

fs_push_manager = MessageManager(
    topics=["fs"],
    host=settings.CARRIER_HOST,
    port=settings.CARRIER_PORT,
    protocol=settings.CARRIER_PROTOCOL,
    auth=settings.CARRIER_TOKEN,
)

class MessageActions:
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class MessageSources:
    TEOS = "teos"
    UPLOADS = "uploads"
    
class MessageTypes:
    TEST_RESULT = "result"
    USER_MATERIAL = "user_material"

def push_to_carrier(topic, payload):
    fs_push_manager.send_one(
        OutgoingMessage(topic=topic, payload=payload)
    )
    
def carrier_start():
    teos_listening_manager = MessageManager(
        topics=["teos"],
        host=settings.CARRIER_HOST,
        port=settings.CARRIER_PORT,
        protocol=settings.CARRIER_PROTOCOL,
        auth=settings.CARRIER_TOKEN,
    )

    MessageManagerHelper.set_manager_to_listen(teos_listening_manager)

    from .handlers import TeosApiClient

    teos_listening_manager.register_event_handler(
        should_handle=TeosApiClient.is_message_about_test_result,
        handler=TeosApiClient.handle_message
    )