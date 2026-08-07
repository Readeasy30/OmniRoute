
# Omniroute

A lightweight AI gateway and router that exposes a single OpenAI-compatible
endpoint and routes requests across multiple LLM providers with automatic
fallback, quota balancing, and context compression.

## Features

- **One universal endpoint** — connect your tools once at `http://localhost:20128/v1`
- **Automatic fallback** — if a provider hits a rate limit or fails, the next
  available node takes over
- **Multiple routing strategies** — priority, round-robin, fill-first,
  cost-optimized, and automatic scoring
- **Context compression** — reduce token usage before sending requests
- **Standard OpenAI format** — works with any OpenAI-compatible client

## Quick start

> **Review before you run.** Only install packages from sources you trust.
> Verify the publisher of any npm package before executing it on your machine.

### Node

```bash
npx omniroute start
