let lux = 0

const pubnub = new PubNub({
    publishKey: "pub-c-1917ca54-c901-4ec2-a145-b0f197c3882e",
    subscribeKey: "sub-c-c5848d3f-0fce-45dd-b398-9147c61b581f",
    userId: "web-pi-light-controller" + Math.floor(Math.random() * 1000)
});

pubnub.subscribe({
    channels: ["iot.status"]
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

pubnub.addListener({
    message: function(event) {
        msg = event.message
        console.log("New message:", msg);
        lux = msg.lux
        console.log("Lux: " + lux)

        span = document.getElementById("lux-indicator").innerHTML = lux
    },
    status: function(event) {
        console.log("Status event:", event);
        if (event.category === "PNConnectedCategory") {
            console.log("Connected to PubNub channels!");
        } else if (event.category === "PNNetworkIssuesCategory") {
            console.log("Connection lost. Attempting to reconnect...");
        }
    }
});
