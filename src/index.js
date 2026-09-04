export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type, Authorization" } });
    }
    try {
      const payload = await request.json();
      const userMessages = payload.messages || [];
      const targetEndpointType = payload.module_target || "factory";

      let systemPrompt = "";
      if (targetEndpointType === "business") {
        systemPrompt = "You are the TopShelf Business OS SEO Optimizer Agent. Output highly targeted schema matrices, optimized landing page HTML copy, and metadata sets for Readeasy30, Matheasy30, and Ozark Webmasters pipelines.";
      } else if (targetEndpointType === "finance") {
        systemPrompt = "You are the High-Velocity Financial Autotrader Oracle. Analyze SPX option premium risk vectors, calculate ATR trailing target markers, and return programmatic mathematical signals.";
      } else {
        systemPrompt = "You are the G-Man Autonomous Website Generator Agent. Output full multi-page file sets containing interconnected code wrappers labeled clearly with FILE:filename design guidelines.";
      }

      const aiResponse = await env.AI.run("@cf/qwen/qwen3.8-27b", {
        messages: [{ role: "system", content: systemPrompt }, ...userMessages]
      });

      return new Response(JSON.stringify({
        id: `chatcmpl-${crypto.randomUUID()}`,
        object: "chat.completion",
        created: Math.floor(Date.now() / 1000),
        model: "omniroute-unified-production-v4",
        choices: [{ index: 0, message: { role: "assistant", content: aiResponse.response || aiResponse }, finish_reason: "stop" }]
      }), { headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
    } catch (err) {
      return new Response(JSON.stringify({ error: "Unified Cluster Error", details: err.message }), { status: 500, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
    }
  }
};
