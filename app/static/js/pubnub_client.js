var message_payload = {
    "type" : "control",
    "mode" : "auto",
    "manual_lux": 500,
    "power_option": "reading",
    "min_lux" : 100,
    "max_lux" : 1000 
}

const pubnub = new PubNub({
    publishKey: "pub-c-1917ca54-c901-4ec2-a145-b0f197c3882e",
    subscribeKey: "sub-c-c5848d3f-0fce-45dd-b398-9147c61b581f",
    userId: "web-pi-light-controller" + Math.floor(Math.random() * 1000)
});


function publishMessage(payload) {
    pubnub.publish({
        channel: "iot.control",
        message: payload
    })
    .then((result) => {
        console.log("Published:", result.timetoken);
    })
    .catch((err) => {
        console.error("Publish failed:", err);
    });
}