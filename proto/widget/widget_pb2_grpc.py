# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from proto.widget import widget_pb2 as proto_dot_widget_dot_widget__pb2


class WidgetsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/widget.Widgets/Get',
                request_serializer=proto_dot_widget_dot_widget__pb2.WidgetRequest.SerializeToString,
                response_deserializer=proto_dot_widget_dot_widget__pb2.Widget.FromString,
                )
        self.Create = channel.unary_unary(
                '/widget.Widgets/Create',
                request_serializer=proto_dot_widget_dot_widget__pb2.Widget.SerializeToString,
                response_deserializer=proto_dot_widget_dot_widget__pb2.Widget.FromString,
                )
        self.List = channel.unary_stream(
                '/widget.Widgets/List',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_widget_dot_widget__pb2.Widget.FromString,
                )
        self.Delete = channel.unary_unary(
                '/widget.Widgets/Delete',
                request_serializer=proto_dot_widget_dot_widget__pb2.WidgetRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class WidgetsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WidgetsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=proto_dot_widget_dot_widget__pb2.WidgetRequest.FromString,
                    response_serializer=proto_dot_widget_dot_widget__pb2.Widget.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=proto_dot_widget_dot_widget__pb2.Widget.FromString,
                    response_serializer=proto_dot_widget_dot_widget__pb2.Widget.SerializeToString,
            ),
            'List': grpc.unary_stream_rpc_method_handler(
                    servicer.List,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=proto_dot_widget_dot_widget__pb2.Widget.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=proto_dot_widget_dot_widget__pb2.WidgetRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'widget.Widgets', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Widgets(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/widget.Widgets/Get',
            proto_dot_widget_dot_widget__pb2.WidgetRequest.SerializeToString,
            proto_dot_widget_dot_widget__pb2.Widget.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/widget.Widgets/Create',
            proto_dot_widget_dot_widget__pb2.Widget.SerializeToString,
            proto_dot_widget_dot_widget__pb2.Widget.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/widget.Widgets/List',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            proto_dot_widget_dot_widget__pb2.Widget.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/widget.Widgets/Delete',
            proto_dot_widget_dot_widget__pb2.WidgetRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
