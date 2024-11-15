# Collaborative Text Editor

A distributed text editing system built with gRPC that enables multiple users to collaboratively edit documents in real-time. The system uses bidirectional streaming for instant synchronization of changes across all connected clients.

## System Architecture

```
collaborative_editor/
│
├── client/
│   └── collaborative-editor-client.py         # Client implementation
│
├── server/
│   └── collaborative-editor-server.py        # Server implementation
│
├── proto/
│   ├── collaborative-editor.proto    # Protocol definition
│   ├── collaborative_editor_pb2.py   # Generated code
│   └── collaborative_editor_pb2_grpc.py
│
├── toBuild.sh             # Build automation script
└── README.md
```

## System Requirements

The following components are required to run the system:

- Python 3.7 or newer
- pip package manager
- gRPC framework and tools

## Setup Instructions

1. Clone this repository to your local machine

2. Give execution permissions to the build script:
   ```bash
   chmod +x build.sh
   ```

3. Run the build script to set up the environment:
   ```bash
   ./build.sh
   ```

## Running the Application

1. Start the document service:
   ```bash
   python3 collaborative-editor-server.py
   ```

2. Launch client instances (in separate terminals):
   ```bash
   python3 collaborative-editor-client.py
   ```

## Core Features

- Real-time collaborative editing
- Immediate synchronization across clients
- Basic text operations (insert, modify, remove)
- Automatic conflict resolution
- Operation logging and audit trail
- Error recovery and graceful degradation

## Client Commands

The editor supports the following operations:

1. `insert` - Add new text at specified position
2. `modify` - Replace existing text at position
3. `remove` - Delete text at position
4. `show` - Display current document state
5. `exit` - Close the editor

## Technical Details

- Uses gRPC bidirectional streaming for real-time updates
- Implements asynchronous operation logging
- Maintains document consistency across clients
- Handles network failures and client disconnections
- Provides unique client identification

## Development Notes

- Server maintains single source of truth
- Changes are propagated to all connected clients
- Operations are logged for audit purposes
- Error handling covers network and input validation
- Clean shutdown protocol for graceful termination

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Future Roadmap

Planned enhancements include:

- Cursor position tracking
- Undo/redo functionality
- User authentication
- Document persistence
- Rich text formatting
- Multiple document support

## License

This project is available under the MIT License. See the LICENSE file for details.
