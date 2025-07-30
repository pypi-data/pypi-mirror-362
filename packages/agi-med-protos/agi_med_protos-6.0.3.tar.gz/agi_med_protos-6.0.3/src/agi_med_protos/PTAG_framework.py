# PTAG ~ "Pydantic Type Adapter GRPC"

import inspect
import types
from typing import Callable, Dict, get_type_hints, Tuple, TypeVar

import grpc
from pydantic import TypeAdapter

from .PTAG_pb2 import PTAGResponse, PTAGRequest
from .PTAG_pb2_grpc import PTAGServiceServicer, add_PTAGServiceServicer_to_server, PTAGServiceStub

T = TypeVar('T')


def analyze_method(method: Callable):
    """
    Analyze a method's type hints and return Pydantic adapters for the argument and return value.
    """
    sig = inspect.signature(method)
    type_hints = get_type_hints(method)
    params = [p for p in sig.parameters.values() if p.name != "self"]
    params_types = [type_hints[param.name] for param in params]
    args_type = Tuple[*params_types]
    result_type = type_hints["return"]
    args_adapter = TypeAdapter(args_type)
    result_adapter = TypeAdapter(result_type)
    method_metadata = {
        "method": method,
        "name": method.__name__,
        "args_adapter": args_adapter,
        "result_adapter": result_adapter,
    }
    return method_metadata


class WrappedPTAGService(PTAGServiceServicer):
    def __init__(self, service_object):
        self.obj = service_object
        self.methods: Dict[str, dict] = {}

        for name, method in inspect.getmembers(service_object, predicate=inspect.ismethod):
            self.methods[name] = analyze_method(method)

    def Invoke(self, request, context):
        method_name = request.FunctionName
        method_metadata = self.methods.get(method_name)

        if method_metadata is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Method {method_name} not found")
            return PTAGResponse()

        method = method_metadata["method"]
        args_adapter = method_metadata["args_adapter"]
        result_adapter = method_metadata["result_adapter"]

        # [args_bytes] -(args_adapter.validate)-> [args] -(method)-> [result] -(result_adapter.dump)-> [result_bytes]
        try:
            input_obj = args_adapter.validate_json(request.Payload)
            output_obj = method(*input_obj)
            payload = result_adapter.dump_json(output_obj)
            return PTAGResponse(FunctionName=method_name, Payload=payload)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return PTAGResponse()


def make_proxy(grpc_stub, method_metadata):
    mm = method_metadata

    def proxy(self, *args):
        args_bytes = mm["args_adapter"].dump_json(args)
        request = PTAGRequest(FunctionName=mm["name"], Payload=args_bytes)
        response = grpc_stub.Invoke(request)
        result_bytes = response.Payload
        result = mm["result_adapter"].validate_json(result_bytes)
        return result

    return proxy


class ClientProxy:
    def __init__(self, service_interface, grpc_stub):
        # [args] -(args_adapter.dump)-> [args_bytes] -(send)-> [result_bytes] -(return_adapter.validate)-> [result]
        for name, method in inspect.getmembers(service_interface, predicate=inspect.isfunction):
            method_metadata = analyze_method(method)
            proxy = make_proxy(grpc_stub, method_metadata)
            bound_method = types.MethodType(proxy, self)
            setattr(self, name, bound_method)


def ptag_attach(server, service_object):
    """
    Attach a service object implementing the interface to a gRPC server.
    """
    service = WrappedPTAGService(service_object)
    add_PTAGServiceServicer_to_server(service, server)


def ptag_client(service_interface: T, address: str) -> T:
    """
    Create a dynamic client for the given interface at the provided gRPC address.
    """
    channel = grpc.insecure_channel(address)
    stub = PTAGServiceStub(channel)
    return ClientProxy(service_interface, stub)
