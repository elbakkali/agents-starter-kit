# Nuxt web frontend — multi-stage for dev and prod.
# Requires a standard Nuxt app in web/ (package.json, nuxt.config, etc.).

FROM node:20-alpine AS base
WORKDIR /app

FROM base AS dev
COPY package.json package-lock.json* ./
RUN npm ci || npm install
COPY . .
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM base AS prod
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build
CMD ["node", ".output/server/index.mjs"]
