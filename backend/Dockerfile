# Stage 1: Build the Go binary
FROM golang:1.22-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy module metadata first (layer cache when deps unchanged)
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the server code (including the generated pb folder)
COPY . .

# Build the executable
RUN CGO_ENABLED=0 GOOS=linux go build -o backend .

# Stage 2: Create the lightweight runtime image
FROM alpine:latest

WORKDIR /root/

# Copy only the compiled binary from the builder stage
COPY --from=builder /app/backend .

# Expose the gRPC port
EXPOSE 50051

# Run the server
CMD ["./backend"]