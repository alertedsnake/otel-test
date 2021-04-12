A test case for the issue described in https://github.com/open-telemetry/opentelemetry-python-contrib/pull/272

Setup:
  
* put your Datadog API key in environment variable `$DD_API_KEY`
* set environment variables:
  * `AWS_ACCESS_KEY_ID=X`
  * `AWS_SECRET_ACCESS_KEY=X`
* run `docker-compose up -d`
* setup a virtualenv with all the otel dependencies from main branches
* run `bin/createdb` to create the Dynamo table
* run `bin/dbserver` to run the server
* run (in another terminal) `bin/client dbserver` to make a request.

Client Output observed:

```
$ bin/client dbserver
Traceback (most recent call last):
  File "/home/michael/work/otel-test/bin/client", line 26, in <module>
    resp = stub.Get(proto.WidgetRequest(name = "one"))
  File "/home/michael/work/otel-test/.venv/lib64/python3.9/site-packages/grpc/_channel.py", line 923, in __call__
    return _end_unary_response_blocking(state, call, False, None)
  File "/home/michael/work/otel-test/.venv/lib64/python3.9/site-packages/grpc/_channel.py", line 826, in _end_unary_response_blocking
    raise _InactiveRpcError(state)
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNKNOWN
        details = "Exception calling application: Unable to describe table: An HTTP Client raised an unhandled exception: expected string or bytes-like object"
        debug_error_string = "{"created":"@1617815515.280641845","description":"Error received from peer ipv6:[::1]:50052","file":"src/core/lib/surface/call.cc","file_line":1067,"grpc_message":"Exception calling application: Unable to describe table: An HTTP Client raised an unhandled exception: expected string or bytes-like object","grpc_status":2}"
```

Server output observed:
```
$ bin/dbserver
DEBUG:ddtrace.sampler:initialized RateSampler, sample 100% of traces
DEBUG:ddtrace.sampler:initialized RateSampler, sample 100% of traces
DEBUG:ddtrace.tracer:Connecting to DogStatsd(udp://localhost:8125)
INFO:server:Listening on localhost:50052
INFO:pynamodb.settings:Override settings for pynamo not available /etc/pynamodb/global_default_settings.py
INFO:pynamodb.settings:Using Default settings value
ERROR:grpc._server:Exception calling application: Unable to describe table: An HTTP Client raised an unhandled exception: expected string or bytes-like object                                                        n
Traceback (most recent call last):
  File "/home/michael/work/otel-test/.venv/lib64/python3.9/site-packages/grpc/_server.py", line 435, in _call_behavior
    response_or_iterator = behavior(argument, context)
  File "/home/michael/xfer/opentelemetry-python-contrib/instrumentation/opentelemetry-instrumentation-grpc/src/opentelemetry/instrumentation/grpc/_server.py", line 297, in telemetry_interceptor
    raise error
  File "/home/michael/xfer/opentelemetry-python-contrib/instrumentation/opentelemetry-instrumentation-grpc/src/opentelemetry/instrumentation/grpc/_server.py", line 288, in telemetry_interceptor
    return behavior(request_or_iterator, context)
  File "/home/michael/work/otel-test/bin/dbserver", line 34, in Get
    widget = Widget.get(request.name)
  File "/home/michael/work/otel-test/.venv/lib/python3.9/site-packages/pynamodb/models.py", line 485, in get
    data = cls._get_connection().get_item(
  File "/home/michael/work/otel-test/.venv/lib/python3.9/site-packages/pynamodb/connection/table.py", line 171, in get_item
    return self.connection.get_item(
  File "/home/michael/work/otel-test/.venv/lib/python3.9/site-packages/pynamodb/connection/base.py", line 1125, in get_item
    operation_kwargs = self.get_operation_kwargs(
  File "/home/michael/work/otel-test/.venv/lib/python3.9/site-packages/pynamodb/connection/base.py", line 859, in get_operation_kwargs
    operation_kwargs.update(self.get_identifier_map(table_name, hash_key, range_key, key=key))
  File "/home/michael/work/otel-test/.venv/lib/python3.9/site-packages/pynamodb/connection/base.py", line 781, in get_identifier_map                                                                                  n
    tbl = self.get_meta_table(table_name)
  File "/home/michael/work/otel-test/.venv/lib/python3.9/site-packages/pynamodb/connection/base.py", line 550, in get_meta_table
    six.raise_from(TableError("Unable to describe table: {}".format(e), e), None)
  File "<string>", line 3, in raise_from
pynamodb.exceptions.TableError: Unable to describe table: An HTTP Client raised an unhandled exception: expected string or bytes-like object
DEBUG:ddtrace._worker:Starting AgentWriter thread
DEBUG:ddtrace.internal.writer:sent 549B in 0.00557s
DEBUG:ddtrace._worker:Stopping AgentWriter thread
DEBUG:ddtrace._worker:Waiting 5 seconds for AgentWriter to finish. Hit ctrl-c to quit.
DEBUG:ddtrace._worker:Shutting down AgentWriter thread
DEBUG:ddtrace._worker:Stopping AgentWriter thread
DEBUG:ddtrace._worker:Stopping AgentWriter thread
```

## Discovery

The best way to verify what's going on here is to hack the
`HTTPConnection.putheader()` method in  `urllib3.connection` such that it
prints out headers as they're being set.

You'll see this:
```
putheader: Host, ('localhost:8000',)
putheader: Accept-Encoding, ('identity',)
putheader: X-Amz-Target, (b'DynamoDB_20120810.DescribeTable',)
putheader: Content-Type, (b'application/x-amz-json-1.0',)
putheader: User-Agent, (b'Botocore/1.20.19 Python/3.9.2 Linux/5.11.11-200.fc33.x86_64',)
putheader: X-Amz-Date, (b'20210407T175114Z',)
putheader: Authorization, (b'AWS4-HMAC-SHA256 Credential=[redacted], SignedHeaders=content-type;host;x-amz-date;x-amz-target, Signature=[redacted]',)
putheader: x-datadog-trace-id, (b'4114137752167852186',)
putheader: x-datadog-parent-id, (b'16388060792200103103',)
putheader: x-datadog-sampling-priority, (b'1',)
putheader: x-datadog-origin, (None,)
```

As you can see with that last one, `None` is being provided.

