import grpc
import logging
import socket

from concurrent import futures
from opentelemetry.instrumentation.grpc     import server_interceptor
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.boto     import BotoInstrumentor

log = logging.getLogger(__name__)

__version__ = '0.1.0'


class GrpcServer:

    def __init__(self, name='otel-grpc-test', listen='localhost:50051'):
        self._name = name

        interceptors = []

        self._enable_otel()

        interceptors.append(server_interceptor(self.tracer))

        # here's the gRPC server
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers = 10),
            interceptors = interceptors)

        self.server.add_insecure_port(listen)
        log.info("Listening on %s", listen)

    def add_servicer(self, adder, obj):
        adder(obj, self.server)


    def _enable_otel(self):

        from opentelemetry                  import trace
        from opentelemetry.propagate        import set_global_textmap
        from opentelemetry.sdk.resources    import Resource
        from opentelemetry.sdk.trace        import TracerProvider
        from opentelemetry.exporter.datadog import DatadogSpanExporter, DatadogExportSpanProcessor
        from opentelemetry.exporter.datadog.propagator import DatadogFormat
        from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient

        r = Resource({
            'app.version':      __version__,
            'app.framework':    ':'.join((self._name, __version__)),
            'net.hostname':     socket.gethostname(),
            'service.name':     self._name,
            'service.version':  __version__,
        })
        trace.set_tracer_provider(TracerProvider(resource = r))
        self.tracer = trace.get_tracer_provider()

        self.exporter = DatadogSpanExporter(
            service   = self._name,
            agent_url = 'http://localhost:8126',
            version   = __version__,
            env       = 'dev',
        )
        self.tracer.add_span_processor(DatadogExportSpanProcessor(self.exporter))
        set_global_textmap(DatadogFormat())


        # setup client instrumentation
        GrpcInstrumentorClient().instrument(tracer = self.tracer)
        BotocoreInstrumentor().instrument(tracer_provider = self.tracer)
        BotoInstrumentor().instrument(tracer_provider = self.tracer)


    def run(self):
        self.server.start()
        try:
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.stop(0)
