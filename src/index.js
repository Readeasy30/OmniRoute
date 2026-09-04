export default {
  async fetch(request, env) {
    // 1. Universal Edge CORS Handshake Matrix
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
      return new Response(JSON.stringify({ error: "Only POST actions are supported on this edge routing vector." }), { 
        status: 405, headers: { "Content-Type": "application/json" } 
      });
    }

    try {
      const payload = await request.json();
      const userMessages = payload.messages || [];

      // 2. Strict Architectural Prompts - Forcing clear markdown multi-page boundary generation
      const designGuardrails = {
        role: "system",
        content: (
          "You are the G-Man Autonomous Multi-Page Web Builder Agent running natively on the Cloudflare Edge network. "
          "Your job is to write full code for THREE separate files: index.html, about.html, and contact.html matching the user prompt. "
          "You MUST output each file inside its own explicit block structure, preceded by its exact file marker line, like this:\n"
          "FILE:index.html\n```html\n(code here)\n```\n"
          "FILE:about.html\n```html\n(code here)\n```\n"
          "FILE:contact.html\n```html\n(code here)\n```"
        )
      };

      const systemInputPayload = [designGuardrails, ...userMessages];

      // 3. Native Model Execution Context Bindings
      const aiResponse = await env.AI.run("@cf/qwen/qwen3.8-27b", {
        messages: systemInputPayload
      });

      const extractedCoreResponseText = aiResponse.response || aiResponse;

      // 4. OpenAI Chat Completions Standard Serialization Delivery Protocol
      return new Response(JSON.stringify({
        id: `chatcmpl-${crypto.randomUUID()}`,
        object: "chat.completion",
        created: Math.floor(Date.now() / 1000),
        model: "qwen-3.8-27b-edge-multipage-production",
        choices: [{
          index: 0,
          message: { role: "assistant", content: extractedCoreResponseText },
          finish_reason: "stop"
        }]
      }), { headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });

    } catch (globalClusterError) {
      return new Response(JSON.stringify({ 
        error: "OmniRoute Infrastructure Server Exception", 
        details: globalClusterError.message 
      }), { status: 500, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
    }
  }
};
