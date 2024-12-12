FROM golang:alpine AS builder

WORKDIR /app
COPY ../ ./

RUN go mod download
RUN go build -o internal-microservice ./cmd/internal-microservice.go

FROM alpine:latest

COPY --from=builder /app/internal-microservice ./

CMD ["./internal-microservice"]