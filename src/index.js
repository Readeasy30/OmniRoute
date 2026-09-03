/**
 * OmniRoute Edge Gateway - Enterprise Serverless Architecture
 * Replaces: omniroute-watchdog.ps1, maintain-db.ps1, rotate-logs.ps1
 */
export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
      });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed. Use POST." }), { 
        status: 405, headers: { "Content-Type": "application/json" } 
      });
    }

    try {
      const payload = await request.json();

      // Route to Qwen 3.8-27B natively hosted on Cloudflare's Edge Grid
      try {
        const qwenResult = await env.AI.run('@cf/qwen/qwen3.8-27b', {
          messages: payload.messages,
          stream: false
        });

        return new Response(JSON.stringify({
          choices: [{ message: { role: "assistant", content: qwenResult.response } }],
          model: "qwen-3.8-27b-edge"
        }), { headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });

      } catch (qwenError) {
        // Fallback Circuit Breaker: If Cloudflare's Qwen drops, instantly use Kimi K3 via Fireworks
        const fireworksResponse = await fetch("https://fireworks.ai", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${env.FIREWORKS_API_KEY}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: "accounts/fireworks/models/kimi-k3",
            messages: payload.messages
          })
        });

        const kimiData = await fireworksResponse.json();
        return new Response(JSON.stringify(kimiData), {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }

    } catch (globalError) {
      return new Response(JSON.stringify({ error: "OmniRoute Gateway Failure", details: globalError.message }), { 
        status: 500, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } 
      });
    }
  }
};
