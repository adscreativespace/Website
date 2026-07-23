// api/auth.js
export default async function handler(req, res) {
  const { code } = req.query;

  if (!code) {
    return res.status(400).json({ error: "No code provided" });
  }

  // Exchange code for access token (GitHub OAuth)
  const response = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      client_id: "Ov23liCNUzULluARD3MQ",         // Replace with your Client ID
      client_secret: "afae482195b6bceefa13796e3a3585b90b9362c7", // Replace with your Client Secret
      code,
    }),
  });

  const data = await response.json();
  res.status(200).json(data);
}
