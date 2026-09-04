export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
      });
    }
    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Use POST" }), { status: 405 });
    }
    try {
      const payload = await request.json();
      try {
        const aiResponse = await env.AI.run("@cf/qwen/qwen3.8-27b", {
          messages: payload.messages
        });
        return new Response(JSON.stringify({
          result: { response: aiResponse.response || aiResponse }
        }), { headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
      } catch (aiError) {
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
        const kimiText = kimiData.choices?.[0]?.message?.content || JSON.stringify(kimiData);
        return new Response(JSON.stringify({
          result: { response: kimiText }
        }), { headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
      }
    } catch (globalError) {
      return new Response(JSON.stringify({ error: globalError.message }), { status: 500 });
    }
  }
};
