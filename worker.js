export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    const locations = [
      "https://kimi.ai",
      "https://kimi.ai",
      "http://localhost:20128/v1",
      "https://workers.dev"
    ];

    const proxyTask = async () => {
      const incomingData = await request.json();
      
      for (const targetUrl of locations) {
        try {
          const kimiResponse = await fetch(targetUrl, {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${env.KIMI_API_KEY}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              model: "kimi-k2.7-code-highspeed",
              messages: incomingData.messages,
              temperature: 0.1
            }),
            signal: AbortSignal.timeout(5000)
          });

          if (kimiResponse.ok) return kimiResponse;
        } catch (err) {
          console.log(`Connection failed for path: ${targetUrl}. Trying next location.`);
        }
      }
      return new Response('All 4 network path resolutions exhausted.', { status: 504 });
    };

    return ctx.waitUntil(proxyTask());
  }
}
