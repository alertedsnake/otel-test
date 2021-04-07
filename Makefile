
VENV_LIB = $(shell python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
PROTOC = python -m grpc_tools.protoc -I . -I proto -I /usr/local/include -I $(VENV_LIB)

all: server_protos

server_protos:
	$(PROTOC) --python_out=. --grpc_python_out=. proto/widget/widget.proto
.PHONY: server_protos
