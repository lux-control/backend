let lux = 0;
let pubnub = null;

async function initPubNub() {
  const res = await fetch("/auth/pubnub/token", { credentials: "include" });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Token fetch failed: ${res.status} ${text}`);
  }

  const data = await res.json();

  pubnub = new PubNub({
    publishKey: "pub-c-1917ca54-c901-4ec2-a145-b0f197c3882e",
    subscribeKey: "sub-c-c5848d3f-0fce-45dd-b398-9147c61b581f",
    userId: data.authorized_uuid, // 🔑 must match authorized_uuid in token
  });

  pubnub.setToken(data.token);

  pubnub.addListener({
    message: function (event) {
      const msg = event.message;
      console.log("New message:", msg);

      if (msg && typeof msg.lux !== "undefined") {
        lux = msg.lux;
        console.log("Lux:", lux);

        const el = document.getElementById("lux-indicator");
        if (el) el.innerHTML = lux;
      }
    },
    status: function (event) {
      console.log("Status event:", event);

      if (event.category === "PNConnectedCategory") {
        console.log("Connected to PubNub channels!");
      } else if (event.category === "PNNetworkIssuesCategory") {
        console.log("Connection lost. Attempting to reconnect...");
      } else if (event.category === "PNAccessDeniedCategory") {
        console.error("Access denied (token/permissions/uuid mismatch).");
      }
    },
  });

  pubnub.subscribe({
    channels: ["iot.status"],
  });

  return pubnub;
}

initPubNub().catch((err) => {
  console.error("PubNub init failed:", err);
});

function publishMessage(payload) {
  if (!pubnub) {
    console.warn("PubNub not ready yet; cannot publish.");
    return;
  }

  pubnub
    .publish({
      channel: "iot.control",
      message: payload,
    })
    .then((result) => {
      console.log("Published:", result.timetoken);
    })
    .catch((err) => {
      console.error("Publish failed:", err);
    });
}