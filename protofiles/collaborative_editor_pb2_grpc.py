# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import collaborative_editor_pb2 as collaborative__editor__pb2

GRPC_GENERATED_VERSION = '1.67.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in collaborative_editor_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DocumentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ModifyDocument = channel.stream_stream(
                '/collaborativeeditor.DocumentService/ModifyDocument',
                request_serializer=collaborative__editor__pb2.EditRequest.SerializeToString,
                response_deserializer=collaborative__editor__pb2.DocumentState.FromString,
                _registered_method=True)
        self.FetchDocument = channel.unary_unary(
                '/collaborativeeditor.DocumentService/FetchDocument',
                request_serializer=collaborative__editor__pb2.DocumentQuery.SerializeToString,
                response_deserializer=collaborative__editor__pb2.DocumentState.FromString,
                _registered_method=True)
        self.WatchDocumentChanges = channel.unary_stream(
                '/collaborativeeditor.DocumentService/WatchDocumentChanges',
                request_serializer=collaborative__editor__pb2.DocumentQuery.SerializeToString,
                response_deserializer=collaborative__editor__pb2.DocumentState.FromString,
                _registered_method=True)


class DocumentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ModifyDocument(self, request_iterator, context):
        """Bidirectional stream for document modifications
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FetchDocument(self, request, context):
        """Get current document state
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WatchDocumentChanges(self, request, context):
        """Subscribe to document changes
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DocumentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ModifyDocument': grpc.stream_stream_rpc_method_handler(
                    servicer.ModifyDocument,
                    request_deserializer=collaborative__editor__pb2.EditRequest.FromString,
                    response_serializer=collaborative__editor__pb2.DocumentState.SerializeToString,
            ),
            'FetchDocument': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchDocument,
                    request_deserializer=collaborative__editor__pb2.DocumentQuery.FromString,
                    response_serializer=collaborative__editor__pb2.DocumentState.SerializeToString,
            ),
            'WatchDocumentChanges': grpc.unary_stream_rpc_method_handler(
                    servicer.WatchDocumentChanges,
                    request_deserializer=collaborative__editor__pb2.DocumentQuery.FromString,
                    response_serializer=collaborative__editor__pb2.DocumentState.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'collaborativeeditor.DocumentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('collaborativeeditor.DocumentService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DocumentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ModifyDocument(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/collaborativeeditor.DocumentService/ModifyDocument',
            collaborative__editor__pb2.EditRequest.SerializeToString,
            collaborative__editor__pb2.DocumentState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def FetchDocument(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/collaborativeeditor.DocumentService/FetchDocument',
            collaborative__editor__pb2.DocumentQuery.SerializeToString,
            collaborative__editor__pb2.DocumentState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def WatchDocumentChanges(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/collaborativeeditor.DocumentService/WatchDocumentChanges',
            collaborative__editor__pb2.DocumentQuery.SerializeToString,
            collaborative__editor__pb2.DocumentState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class AuditServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RecordEdit = channel.unary_unary(
                '/collaborativeeditor.AuditService/RecordEdit',
                request_serializer=collaborative__editor__pb2.EditRecord.SerializeToString,
                response_deserializer=collaborative__editor__pb2.AuditResponse.FromString,
                _registered_method=True)


class AuditServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RecordEdit(self, request, context):
        """Asynchronous audit logging
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuditServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RecordEdit': grpc.unary_unary_rpc_method_handler(
                    servicer.RecordEdit,
                    request_deserializer=collaborative__editor__pb2.EditRecord.FromString,
                    response_serializer=collaborative__editor__pb2.AuditResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'collaborativeeditor.AuditService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('collaborativeeditor.AuditService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AuditService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RecordEdit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/collaborativeeditor.AuditService/RecordEdit',
            collaborative__editor__pb2.EditRecord.SerializeToString,
            collaborative__editor__pb2.AuditResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)