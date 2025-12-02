# Build stage: compile the Go binary
FROM golang:1.20-alpine AS builder

# Install git (if modules need it) and set working dir
RUN apk add --no-cache git
WORKDIR /src

# Copy go.mod and go.sum to enable dependency caching
COPY go.mod go.sum* ./

# Download modules
RUN go mod download

# Copy remaining source
COPY . .

# Build the binary statically
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /order-service ./

# Final stage: small runtime image
FROM alpine:3.18

# Add CA certs for outbound HTTPS calls
RUN apk add --no-cache ca-certificates

# Copy binary from builder
COPY --from=builder /order-service /order-service

# Expose the service port
EXPOSE 5003

# Default command to run the service
CMD ["/order-service"]
