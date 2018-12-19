import hashlib
import requests
from django.conf import settings
from apps.storage.models import Fact
from .messages import MessageActions, MessageTypes, MessageSources

def get_fact_hash(fact):
    # TODO add actor, created_at
    return "{}{}{}{}".format(
        fact.type, 
        fact.result,
        fact.source, 
        fact.handler
    )

class ApiClient():
    pass

class TeosApiClient(ApiClient):

    __handler_name = "teos_test_result"

    @staticmethod
    def get_test_result(test_id, unti_id):
        protocol = getattr(settings, "TEOS_PROTOCOL", None)
        base_url = getattr(settings, "TEOS_BASE_URL", None)
        api_key = getattr(settings, "TEOS_API_KEY", None)

        if not base_url or not api_key or not protocol:
            raise ValueError("improperly configured: need TEOS_BASE_URL, TEOS_API_KEY, TEOS_PROTOCOL")

        result_url = "{}://{}/api/v1/test/{}/result?app_token={}&unti_id={}".format(
            protocol, base_url, test_id, api_key, unti_id
        )
        
        response = requests.get(result_url)
        return response.json()

    @staticmethod
    def is_message_about_test_result(message):
        payload = message.get_payload()
        if payload["action"] == MessageActions.CREATE and \
           payload["type"] == MessageTypes.TEST_RESULT and \
           payload["source"] == MessageSources.TEOS:
           return True   

        return False

    @staticmethod
    def handle_message(message):

        payload = message.get_payload()
        test_result = TeosApiClient.get_test_result(
            payload["id"]["test"]["uuid"], payload["id"]["user"]["unti_id"]
        )

        meta = {
            "test": {"uuid": payload["id"]["test"]["uuid"]}
        }

        fact = Fact(
            actor=[test_result["unti_id"]],
            type="teos.test.result",
            source=MessageSources.TEOS,
            handler=TeosApiClient.__handler_name,
            meta=meta
        )

        fact_result = {}

        for result in test_result["results"]:
            for scale in result["scales"]:
                scale_group = scale["scale_group"]["uuid"]
                if scale_group in fact_result:
                    if scale["uuid"] in fact_result[scale_group]:
                        value = int(fact_result[scale_group][scale["uuid"]]) + int(scale["value"])
                        fact_result[scale_group][scale["uuid"]] = value
                    else:
                        kv = {scale["uuid"]: int(scale["value"])}
                        fact_result[scale_group].update(kv)                
                else:
                    kv = {scale["uuid"]: int(scale["value"])}
                    fact_result.update({scale_group: kv})

        for k in fact_result.keys():
            fact.result = {
                "scale_group": {
                    "uuid": k,
                    "scales": fact_result[k]
                }
            }
            fact.hash=hashlib.sha256(get_fact_hash(fact).encode()).hexdigest()
            fact.save()