import asyncio
import grpc
import sys
import os
import uuid
from typing import Optional, Set
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'protofiles'))
import collaborative_editor_pb2 as pb2
import collaborative_editor_pb2_grpc as pb2_grpc
class DocumentEditor:
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('localhost:50051')
        self.stub = pb2_grpc.DocumentServiceStub(self.channel)
        self.content = ""
        self.update_queue = asyncio.Queue()
        self.editor_id = uuid.uuid4().hex[:8]
        print(f"\nEditor ID: {self.editor_id}")
        self.active = True
        self.tasks: Set[asyncio.Task] = set()

    def show_content(self, prefix: str = "Document content"):
        print("\n" + "-" * 50)
        print(f"{prefix}:")
        print(f"'{self.content}'")
        print("-" * 50 + "\n")

    async def initialize_document(self):
        try:
            response = await self.stub.FetchDocument(pb2.DocumentQuery())
            self.content = response.text
            self.show_content("Initial document state")
        except grpc.RpcError as e:
            print(f"Failed to fetch document: {str(e)}")

    async def monitor_changes(self):
        try:
            async for state in self.stub.WatchDocumentChanges(pb2.DocumentQuery()):
                if not self.active:
                    break
                if not state.has_error:
                    if state.editor_id != self.editor_id:
                        self.content = state.text
                        await self.update_queue.put(state)
                else:
                    print(f"Change stream error: {state.error_details}")
        except grpc.RpcError as e:
            if self.active:
                print(f"Change monitoring error: {str(e)}")
        except asyncio.CancelledError:
            pass

    async def process_changes(self):
        try:
            while self.active:
                try:
                    state = await asyncio.wait_for(self.update_queue.get(), timeout=0.1)
                    self.content = state.text
                    if state.editor_id and state.editor_id != self.editor_id:
                        self.show_content(f"Updated by editor {state.editor_id}")
                except asyncio.TimeoutError:
                    break
        except asyncio.CancelledError:
            pass
        except Exception as e:
            if self.active:
                print(f"Change processing error: {str(e)}")

    async def get_command(self) -> Optional[pb2.EditRequest]:
        while self.active:
            print("\nAvailable commands:")
            print("1. insert - Insert text at position")
            print("2. modify - Replace text at position")
            print("3. remove - Remove text at position")
            print("4. show - Display current document")
            print("5. exit - Close editor")
            
            await self.process_changes()
            
            try:
                command = input("\nEnter command: ").lower()
                
                if command in ['exit', '5']:
                    self.active = False
                    return None
                
                if command in ['show', '4']:
                    self.show_content("Current document")
                    continue

                offset = int(input("Enter position: "))
                
                if command in ['insert', '1']:
                    text = input("Text to insert: ")
                    return pb2.EditRequest(
                        type=pb2.EditRequest.INSERT,
                        offset=offset,
                        text=text,
                        editor_id=self.editor_id
                    )
                elif command in ['modify', '2']:
                    text = input("New text: ")
                    span = int(input("Length to replace: "))
                    return pb2.EditRequest(
                        type=pb2.EditRequest.MODIFY,
                        offset=offset,
                        text=text,
                        span=span,
                        editor_id=self.editor_id
                    )
                elif command in ['remove', '3']:
                    span = int(input("Length to remove: "))
                    return pb2.EditRequest(
                        type=pb2.EditRequest.REMOVE,
                        offset=offset,
                        span=span,
                        editor_id=self.editor_id
                    )
                else:
                    print("Invalid command. Please try again.")
            except ValueError:
                print("Invalid input. Please try again.")

    async def edit_document(self):
        async def request_generator():
            generated = False
            while self.active:
                request = await self.get_command()
                if request is None:
                    if not generated:
                        yield pb2.EditRequest(
                            type=pb2.EditRequest.INSERT,
                            offset=0,
                            text="",
                            editor_id=self.editor_id
                        )
                    break
                generated = True
                yield request

        try:
            monitor_task = asyncio.create_task(self.monitor_changes())
            self.tasks.add(monitor_task)
            
            async for state in self.stub.ModifyDocument(request_generator()):
                if not self.active:
                    break
                if state.has_error:
                    print(f"Error: {state.error_details}")
                else:
                    self.content = state.text
                    if state.editor_id == self.editor_id and state.text:
                        self.show_content("Document updated (by you)")
                    await self.process_changes()

        except grpc.RpcError as e:
            if "EOF" not in str(e) and self.active:
                print(f"Edit stream error: {str(e)}")
                await self.initialize_document()
        finally:
            monitor_task.cancel()
            self.tasks.remove(monitor_task)
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass

    async def cleanup(self):
        self.active = False
        
        for task in self.tasks:
            task.cancel()
        
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        
        while not self.update_queue.empty():
            try:
                self.update_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        
        await self.channel.close()

async def main():
    print("\nCollaborative Document Editor")
    print("-" * 28)
    
    editor = DocumentEditor()
    try:
        await editor.initialize_document()
        await editor.edit_document()
    finally:
        await editor.cleanup()
        print("\nEditor closed successfully!")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEditor terminated by user")
