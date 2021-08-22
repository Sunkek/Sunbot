FROM golang:alpine AS builder

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /build

RUN apk update && apk upgrade && apk add --no-cache ca-certificates
RUN update-ca-certificates

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY . .

RUN go build -o main .

WORKDIR /dist

RUN cp /build/main .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /dist/main /
EXPOSE 80
ENTRYPOINT ["/main"]