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
      return new Response(JSON.stringify({ error: "Only POST actions supported." }), { 
        status: 405, headers: { "Content-Type": "application/json" } 
      });
    }

    try {
      const payload = await request.json();
      const userMessages = payload.messages || [];
      
      // Enforce the Multi-Page System Instruction Prompts directly inside the Cloud Core Plane
      const cloudInstructions = {
        role: "system",
        content: (
          "You are the G-Man Multi-Page Web Builder Agent running natively on the Cloudflare Edge network. "
          "You must generate full code for THREE separate files: index.html, about.html, and contact.html matching the user request. "
          "You MUST output each file inside its own explicit block structure, preceded by its exact file marker line, like this:\n"
          "FILE:index.html\n```html\n(code here)\n```\n"
          "FILE:about.html\n```html\n(code here)\n```\n"
          "FILE:contact.html\n```html\n(code here)\n```"
        )
      };

      const consolidatedMessages = [cloudInstructions, ...userMessages];

      // Execute primary model tracking logic natively on Cloudflare AI matrix bindings
      const aiResponse = await env.AI.run("@cf/qwen/qwen3.8-27b", {
        messages: consolidatedMessages
      });

      const generatedText = aiResponse.response || aiResponse;

      // Output pristine OpenAI formatted JSON object payload directly to edge networks
      return new Response(JSON.stringify({
        id: `chatcmpl-${crypto.randomUUID()}`,
        object: "chat.completion",
        created: Math.floor(Date.now() / 1000),
        model: "qwen-3.8-27b-edge-multipage",
        choices: [{
          index: 0,
          message: { role: "assistant", content: generatedText },
          finish_reason: "stop"
        }]
      }), { headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });

    } catch (globalError) {
      return new Response(JSON.stringify({ 
        error: "OmniRoute Cloud Edge Exception", 
        details: globalError.message 
      }), { status: 500, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" } });
    }
  }
};
