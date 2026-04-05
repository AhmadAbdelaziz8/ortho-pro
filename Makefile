# Makefile
PROTO_DIR=proto
SERVER_DIR=server/pb
CLIENT_DIR=client/src/pb

# Create directories if they don't exist
init:
	mkdir -p $(SERVER_DIR)
	mkdir -p $(CLIENT_DIR)

# Generate Go and gRPC-Web stubs
generate: init
	# 1. Generate Go Code (Server)
	protoc -I=$(PROTO_DIR) \
		--go_out=$(SERVER_DIR) --go_opt=paths=source_relative \
		--go-grpc_out=$(SERVER_DIR) --go-grpc_opt=paths=source_relative \
		$(PROTO_DIR)/*.proto

	# 2. Generate JavaScript/gRPC-Web Code (Client)
	protoc -I=$(PROTO_DIR) \
		--js_out=import_style=commonjs:$(CLIENT_DIR) \
		--grpc-web_out=import_style=commonjs,mode=grpcwebtext:$(CLIENT_DIR) \
		$(PROTO_DIR)/*.proto

	@echo "Protobuf compilation successful."