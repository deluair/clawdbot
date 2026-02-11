#!/usr/bin/env node
// OVHcloud API helper - proper signature generation
import crypto from "crypto";

const AK = process.env.OVH_APPLICATION_KEY || "9c65880a73f14a01";
const AS = process.env.OVH_APPLICATION_SECRET || "071e3ff8a766d98bb8e4c077ccb6021a";
const CK = process.env.OVH_CONSUMER_KEY || "e307b675f120aba45c7194a183699a37";

// OVHcloud US endpoint
const BASE = "https://api.us.ovhcloud.com/1.0";

async function getTimeDelta() {
  const res = await fetch(`${BASE}/auth/time`);
  const serverTime = await res.json();
  return serverTime - Math.floor(Date.now() / 1000);
}

async function ovhRequest(method, path, body = null) {
  const timeDelta = await getTimeDelta();
  const timestamp = Math.floor(Date.now() / 1000) + timeDelta;
  const url = `${BASE}${path}`;

  const toSign = [
    AS,
    CK,
    method.toUpperCase(),
    url,
    body ? JSON.stringify(body) : "",
    String(timestamp),
  ].join("+");
  const signature = "$1$" + crypto.createHash("sha1").update(toSign).digest("hex");

  const headers = {
    "X-Ovh-Application": AK,
    "X-Ovh-Consumer": CK,
    "X-Ovh-Signature": signature,
    "X-Ovh-Timestamp": String(timestamp),
    "Content-Type": "application/json",
  };

  const res = await fetch(url, {
    method: method.toUpperCase(),
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  return res.json();
}

// Main
const action = process.argv[2] || "list";

if (action === "list") {
  const vpsList = await ovhRequest("GET", "/vps");
  console.log("VPS list:", JSON.stringify(vpsList, null, 2));

  if (Array.isArray(vpsList) && vpsList.length > 0) {
    for (const vpsName of vpsList) {
      const details = await ovhRequest("GET", `/vps/${vpsName}`);
      console.log(`\nVPS details for ${vpsName}:`, JSON.stringify(details, null, 2));
    }
  }
} else if (action === "ip") {
  const vpsName = process.argv[3];
  const ips = await ovhRequest("GET", `/vps/${vpsName}/ips`);
  console.log("IPs:", JSON.stringify(ips, null, 2));
}
