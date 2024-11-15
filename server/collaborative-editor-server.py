import asyncio
import grpc
from concurrent import futures
import sys
import os
import datetime
from typing import Dict, Optional
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'protofiles'))
import collaborative_editor_pb2 as pb2
import collaborative_editor_pb2_grpc as pb2_grpc

class AuditLogger(pb2_grpc.AuditServiceServicer):
    def __init__(self, audit_file: str = "edit_history.log"):
        self.audit_file = audit_file

    async def RecordEdit(self, request: pb2.EditRecord, context) -> pb2.AuditResponse:
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"{timestamp} | Editor {request.editor_id} | {request.edit_type} at {request.offset}: {request.text}\n"
        
        with open(self.audit_file, "a") as f:
            f.write(log_entry)
        print(f"Audit: {log_entry.strip()}")
        return pb2.AuditResponse(recorded=True)

    async def record_edit(self, edit_request: pb2.EditRequest) -> None:
        edit_types = {0: "INSERT", 1: "MODIFY", 2: "REMOVE"}
        record = pb2.EditRecord(
            edit_type=edit_types[edit_request.type],
            text=edit_request.text,
            offset=edit_request.offset,
            editor_id=edit_request.editor_id
        )
        await self.RecordEdit(record, None)

class DocumentManager(pb2_grpc.DocumentServiceServicer):
    def __init__(self):
        self.content = ""
        self.audit_logger = AuditLogger()
        self.editor_queues: Dict[str, asyncio.Queue] = {}
        self.mutex = asyncio.Lock()

    async def notify_editors(self, editor_id: Optional[str] = None) -> None:
        state = pb2.DocumentState(text=self.content, editor_id=editor_id)
        offline_editors = []

        for eid, queue in self.editor_queues.items():
            if eid != editor_id:
                try:
                    await queue.put(state)
                except Exception:
                    offline_editors.append(eid)

        for eid in offline_editors:
            del self.editor_queues[eid]

    async def ModifyDocument(self, request_iterator, context) -> pb2.DocumentState:
        try:
            async for request in request_iterator:
                async with self.mutex:
                    try:
                        if request.type == pb2.EditRequest.INSERT:
                            self.content = (
                                self.content[:request.offset] +
                                request.text +
                                self.content[request.offset:]
                            )
                        elif request.type == pb2.EditRequest.MODIFY:
                            self.content = (
                                self.content[:request.offset] +
                                request.text +
                                self.content[request.offset + request.span:]
                            )
                        elif request.type == pb2.EditRequest.REMOVE:
                            self.content = (
                                self.content[:request.offset] +
                                self.content[request.offset + request.span:]
                            )

                        await self.audit_logger.record_edit(request)
                        await self.notify_editors(request.editor_id)
                        yield pb2.DocumentState(
                            text=self.content,
                            editor_id=request.editor_id
                        )

                        editor_queue = self.editor_queues.get(request.editor_id)
                        if editor_queue:
                            while not editor_queue.empty():
                                yield await editor_queue.get()

                    except Exception as e:
                        yield pb2.DocumentState(
                            has_error=True,
                            error_details=f"Failed to process edit: {str(e)}"
                        )

        except Exception as e:
            yield pb2.DocumentState(
                has_error=True,
                error_details=f"Stream error: {str(e)}"
            )
        finally:
            if request.editor_id in self.editor_queues:
                del self.editor_queues[request.editor_id]

    async def FetchDocument(self, request: pb2.DocumentQuery, context) -> pb2.DocumentState:
        return pb2.DocumentState(text=self.content)

    async def WatchDocumentChanges(self, request: pb2.DocumentQuery, context) -> pb2.DocumentState:
        editor_id = os.urandom(4).hex()
        editor_queue = asyncio.Queue()
        self.editor_queues[editor_id] = editor_queue

        try:
            yield pb2.DocumentState(text=self.content)
            while True:
                try:
                    state = await editor_queue.get()
                    yield state
                except Exception as e:
                    yield pb2.DocumentState(
                        has_error=True,
                        error_details=f"Update stream error: {str(e)}"
                    )
                    break
        finally:
            if editor_id in self.editor_queues:
                del self.editor_queues[editor_id]

async def main():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_DocumentServiceServicer_to_server(DocumentManager(), server)
    pb2_grpc.add_AuditServiceServicer_to_server(AuditLogger(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Collaborative editor server running on port 50051")
    print("Audit log: edit_history.log")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(main())
