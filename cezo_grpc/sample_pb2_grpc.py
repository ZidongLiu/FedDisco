# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from cezo_grpc import sample_pb2 as cezo__grpc_dot_sample__pb2

GRPC_GENERATED_VERSION = '1.66.1'
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
        + f' but the generated code in cezo_grpc/sample_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SampleServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Connect = channel.unary_unary(
                '/sample_server.SampleServer/Connect',
                request_serializer=cezo__grpc_dot_sample__pb2.EmptyRequest.SerializeToString,
                response_deserializer=cezo__grpc_dot_sample__pb2.ConnectResponse.FromString,
                _registered_method=True)
        self.TryToJoinIteration = channel.unary_unary(
                '/sample_server.SampleServer/TryToJoinIteration',
                request_serializer=cezo__grpc_dot_sample__pb2.TryToJoinIterationRequest.SerializeToString,
                response_deserializer=cezo__grpc_dot_sample__pb2.TryToJoinIterationResponse.FromString,
                _registered_method=True)
        self.PullGradsAndSeeds = channel.unary_unary(
                '/sample_server.SampleServer/PullGradsAndSeeds',
                request_serializer=cezo__grpc_dot_sample__pb2.PullGradsAndSeedsRequest.SerializeToString,
                response_deserializer=cezo__grpc_dot_sample__pb2.PullGradsAndSeedsResponse.FromString,
                _registered_method=True)
        self.SubmitIteration = channel.unary_unary(
                '/sample_server.SampleServer/SubmitIteration',
                request_serializer=cezo__grpc_dot_sample__pb2.SubmitIterationRequest.SerializeToString,
                response_deserializer=cezo__grpc_dot_sample__pb2.EmptyRequest.FromString,
                _registered_method=True)


class SampleServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Connect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TryToJoinIteration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PullGradsAndSeeds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitIteration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SampleServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Connect': grpc.unary_unary_rpc_method_handler(
                    servicer.Connect,
                    request_deserializer=cezo__grpc_dot_sample__pb2.EmptyRequest.FromString,
                    response_serializer=cezo__grpc_dot_sample__pb2.ConnectResponse.SerializeToString,
            ),
            'TryToJoinIteration': grpc.unary_unary_rpc_method_handler(
                    servicer.TryToJoinIteration,
                    request_deserializer=cezo__grpc_dot_sample__pb2.TryToJoinIterationRequest.FromString,
                    response_serializer=cezo__grpc_dot_sample__pb2.TryToJoinIterationResponse.SerializeToString,
            ),
            'PullGradsAndSeeds': grpc.unary_unary_rpc_method_handler(
                    servicer.PullGradsAndSeeds,
                    request_deserializer=cezo__grpc_dot_sample__pb2.PullGradsAndSeedsRequest.FromString,
                    response_serializer=cezo__grpc_dot_sample__pb2.PullGradsAndSeedsResponse.SerializeToString,
            ),
            'SubmitIteration': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitIteration,
                    request_deserializer=cezo__grpc_dot_sample__pb2.SubmitIterationRequest.FromString,
                    response_serializer=cezo__grpc_dot_sample__pb2.EmptyRequest.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sample_server.SampleServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('sample_server.SampleServer', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class SampleServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Connect(request,
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
            '/sample_server.SampleServer/Connect',
            cezo__grpc_dot_sample__pb2.EmptyRequest.SerializeToString,
            cezo__grpc_dot_sample__pb2.ConnectResponse.FromString,
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
    def TryToJoinIteration(request,
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
            '/sample_server.SampleServer/TryToJoinIteration',
            cezo__grpc_dot_sample__pb2.TryToJoinIterationRequest.SerializeToString,
            cezo__grpc_dot_sample__pb2.TryToJoinIterationResponse.FromString,
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
    def PullGradsAndSeeds(request,
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
            '/sample_server.SampleServer/PullGradsAndSeeds',
            cezo__grpc_dot_sample__pb2.PullGradsAndSeedsRequest.SerializeToString,
            cezo__grpc_dot_sample__pb2.PullGradsAndSeedsResponse.FromString,
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
    def SubmitIteration(request,
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
            '/sample_server.SampleServer/SubmitIteration',
            cezo__grpc_dot_sample__pb2.SubmitIterationRequest.SerializeToString,
            cezo__grpc_dot_sample__pb2.EmptyRequest.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
