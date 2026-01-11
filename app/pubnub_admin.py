import os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

def build_pubnub_admin() -> PubNub:
    pnconfig = PNConfiguration()
    pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
    pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
    pnconfig.secret_key = os.getenv("PUBNUB_SECRET_KEY")
    pnconfig.user_id = "server-token-issuer"
    return PubNub(pnconfig)
