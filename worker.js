export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    const proxyTask = async () => {
      const incomingData = await request.json();
      
      const kimiResponse = await fetch("https://kimi.ai", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.KIMI_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "kimi-k2.7-code-highspeed",
          messages: incomingData.messages,
          temperature: 0.1
        })
      });

      return kimiResponse;
    };

    return ctx.waitUntil(proxyTask());
  }
}
