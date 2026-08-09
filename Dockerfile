FROM node:20-alpine AS base
WORKDIR /app
RUN apk add --no-cache libc6-compat git
COPY package*.json ./

FROM base AS dependencies
RUN npm install --prefer-online --no-audit --no-fund --legacy-peer-deps

FROM base AS builder
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
ENV NODE_ENV=production
RUN npm run build

FROM base AS runner
ENV NODE_ENV=production
ENV PORT=20128
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

USER nextjs
EXPOSE 20128
CMD ["npm", "run", "start"]

# Stage 1: Build Caddy with the required external DNS modules
FROM caddy:2.8.4-builder AS builder

# Inject Cloudflare and AWS Route53 DNS validation providers
RUN xcaddy build \
    --with ://github.com \
    --with ://github.com

# Stage 2: Produce the minimal, hardened runtime image
FROM caddy:2.8.4-alpine

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
