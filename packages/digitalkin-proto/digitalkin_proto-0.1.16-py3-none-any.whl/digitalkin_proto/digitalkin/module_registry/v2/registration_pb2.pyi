from digitalkin_proto.digitalkin.module_registry.v2 import metadata_pb2 as _metadata_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterRequest(_message.Message):
    __slots__ = ("module_id", "module_type", "address", "port", "version", "metadata")
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    MODULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    module_id: str
    module_type: str
    address: str
    port: int
    version: str
    metadata: _metadata_pb2.Metadata
    def __init__(self, module_id: _Optional[str] = ..., module_type: _Optional[str] = ..., address: _Optional[str] = ..., port: _Optional[int] = ..., version: _Optional[str] = ..., metadata: _Optional[_Union[_metadata_pb2.Metadata, _Mapping]] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class DeregisterRequest(_message.Message):
    __slots__ = ("module_id",)
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    module_id: str
    def __init__(self, module_id: _Optional[str] = ...) -> None: ...

class DeregisterResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
