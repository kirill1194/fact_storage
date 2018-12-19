from django.test import TestCase
from carrier_client.message import IncomingMessage
from django_carrier_client.helpers import MessageManagerHelper
from .messages import MessageActions, MessageTypes, MessageSources, carrier_start
from .handlers import TeosApiClient

class TeosMessageTestCase(TestCase):
    
    # message = """
    #     {"action":"create","timestamp":"2018-12-10T10:00:00+00:00","source":"teos","type":"result",
    #     "id":{"test":{"uuid":"a69ed2f7-ac5e-45ea-9f1c-4635657e2970"},"user":{"unti_id":141}},
    #     "title":"Заголовок теста"}"""

    # def test_carrier_start(self):
    #     carrier_start()
    #     for message_manager in MessageManagerHelper.get_message_managers_to_listen():
    #         incoming_message = IncomingMessage()
    #         incoming_message._value = self.message
    #         message_manager.handle_message(incoming_message)

class TeosApiClientTestCase(TestCase):

    class Message():
        
        def __init__(self, action, type, source):
            self.action = action
            self.type = type
            self.source = source

        def get_payload(self):
            return {
                "action": self.action,
                "type": self.type,
                "source": self.source
            }

    def test_is_message_about_test_result(self):

        valid_message = self.Message(
            MessageActions.CREATE, 
            MessageTypes.TEST_RESULT, 
            MessageSources.TEOS
        )

        invalid_action_message = self.Message(
            MessageActions.UPDATE, 
            MessageTypes.TEST_RESULT, 
            MessageSources.TEOS
        )

        invalid_type_message = self.Message(
            MessageActions.CREATE, 
            MessageTypes.USER_MATERIAL, 
            MessageSources.TEOS
        )

        invalid_source_message = self.Message(
            MessageActions.CREATE, 
            MessageTypes.TEST_RESULT, 
            MessageSources.UPLOADS
        )

        self.assertTrue(TeosApiClient.is_message_about_test_result(valid_message))
        self.assertFalse(TeosApiClient.is_message_about_test_result(invalid_action_message))
        self.assertFalse(TeosApiClient.is_message_about_test_result(invalid_type_message))
        self.assertFalse(TeosApiClient.is_message_about_test_result(invalid_source_message))
