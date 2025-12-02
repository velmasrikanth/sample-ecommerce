# Use official Node.js LTS image (alpine variant for smaller size)
FROM node:18-alpine

# Create and set working directory
WORKDIR /app

# Copy package manifest(s) first to install deps (cache optimization)
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --production

# Copy application source
COPY . .

# Expose service port
EXPOSE 5002

# Default command to start the Node.js app
CMD ["node", "index.js"]
