# Build stage: use Node to install and build the Vite app
FROM node:18-alpine AS builder

# Create app directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json .
RUN npm install

# Copy source and build
COPY . .
RUN npm run build

# Production stage: use nginx to serve static files
FROM nginx:stable-alpine

# Remove default nginx html
RUN rm -rf /usr/share/nginx/html/*

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
