from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModuleData(_message.Message):
    __slots__ = ("id", "content", "usage", "module_id", "data_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    content: _struct_pb2.Struct
    usage: _struct_pb2.Struct
    module_id: str
    data_type: str
    def __init__(self, id: _Optional[str] = ..., content: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., usage: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., module_id: _Optional[str] = ..., data_type: _Optional[str] = ...) -> None: ...

class StoreRequest(_message.Message):
    __slots__ = ("mission_id", "items")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    items: _containers.RepeatedCompositeFieldContainer[ModuleData]
    def __init__(self, mission_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[ModuleData, _Mapping]]] = ...) -> None: ...

class StoreResponse(_message.Message):
    __slots__ = ("success", "message", "module_data_ids")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MODULE_DATA_IDS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    module_data_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., module_data_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class RetrieveRequest(_message.Message):
    __slots__ = ("mission_id", "data_type")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    data_type: str
    def __init__(self, mission_id: _Optional[str] = ..., data_type: _Optional[str] = ...) -> None: ...

class RetrieveResponse(_message.Message):
    __slots__ = ("success", "message", "items")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    items: _containers.RepeatedCompositeFieldContainer[ModuleData]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., items: _Optional[_Iterable[_Union[ModuleData, _Mapping]]] = ...) -> None: ...
