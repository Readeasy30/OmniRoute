[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

> **One OpenAI-compatible endpoint to rule them all.** Aggregate 60+ AI providers, pool free & paid quotas, and never hit a rate limit again.

**OmniRoute** is a lightweight, zero-overhead AI gateway and router. It provides a unified local endpoint (`http://localhost:20128/v1`) that connects all your AI coding tools—like **Cursor, Claude Code, OpenClaw, Codex, and Cline**—to dozens of LLM providers with automatic fallback, quota balancing, and context compression.

---

## ✨ Why OmniRoute?

* **🆓 $0/Month Tech Stack:** Easily stack documented free tiers across providers to run coding assistants endlessly without cost.
* **🔌 One Universal Endpoint:** Connect once at `http://localhost:20128/v1`. Swap models and providers on the fly using standard OpenAI client formats.
* **⚡ Smart Auto-Fallback:** If your primary account or provider hits a rate limit or goes down, OmniRoute instantly routes your prompt to the next available account.
* **🗜️ Context & Token Saver:** Built-in compression strategies reduce context windows and token usage by **15–95%**, drastically slashing costs and staying under quota boundaries.
* **🔀 13+ Routing Strategies:** Choose from Priority, Round Robin, Fill First, Cost Optimized, P2C, or hands-off **Auto 6-factor scoring** (latency, quota, task fit, and cost).
* **💻 Zero Key Setup Available:** Supports friction-free, keyless providers out of the box so you can start right away.

---

## ⚡ Quick Start

### 1. Run with Docker (Recommended)

```bash
docker run -d \
  --name omniroute \
  -p 20128:20128 \
  -v ./omniroute.yaml:/etc/omniroute/omniroute.yaml \
  --restart unless-stopped \
  diegosouzapw/omniroute:latest

npx omniroute start

version: "1.0"
server:
  port: 20128

combos:
  - name: free-coding-stack
    strategy: auto # auto, priority, round_robin, cost_optimized, etc.
    nodes:
      - provider: anthropic
        model: claude-3-5-sonnet
      - provider: openai
        model: gpt-4o
      - provider: deepseek
        model: deepseek-coder

providers:
  pollinations:
    enabled: true # Keyless provider

MIT License

Copyright (c) 2026 Omniroute Authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Contributing to Omniroute

Thank you for considering contributing to Omniroute! 

## How to Contribute

1. **Report Bugs:** Open an issue on GitHub detailing the bug and steps to reproduce.
2. **Suggest Features:** Create an issue outlining your proposed idea.
3. **Submit Code:**
   - Fork the repo and create a branch from `main`.
   - Ensure code conforms to standard formatting tools (e.g., `gofmt`, `prettier`).
   - Add tests covering your changes.
   - Open a Pull Request referencing the related issue.

version: '3.8'

services:
  omniroute:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./omniroute.yaml:/etc/omniroute/omniroute.yaml
    environment:
      - CONFIG_PATH=/etc/omniroute/omniroute.yaml
    restart: always

version: "1.0"
server:
  port: 8080

routes:
  - path: /api/v1/users
    target: http://user-service:3000
    timeout: 5s
    rate_limit:
      requests_per_minute: 100

  - path: /api/v1/ai
    type: llm_router
    strategy: lowest_latency
    providers:
      - name: openai
        endpoint: https://api.openai.com/v1
      - name: anthropic
        endpoint: https://api.anthropic.com/v1

omniroute/
├── README.md             <-- The README generated above
├── omniroute.yaml        <-- Your configuration file
├── docker-compose.yml    <-- For containerized running
├── LICENSE               <-- Your license text (e.g., MIT)
└── CONTRIBUTING.md       <-- Contribution guidelines
