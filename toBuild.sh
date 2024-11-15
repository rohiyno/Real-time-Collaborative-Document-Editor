#!/bin/bash

echo "Start...."

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install required packages
echo "Dependencies..."
pip3 install grpcio 
pip3 install grpcio-tools


# Generate Python code from proto
python3 -m grpc_tools.protoc \
    -I./protofiles \
    --python_out=. \
    --grpc_python_out=. \
    ./protofiles/collaborative-editor.proto

# Move generated files to appropriate locations
mv collaborative_editor_pb2.py collaborative_editor_pb2_grpc.py protofiles/



echo "Build completed successfully!"
